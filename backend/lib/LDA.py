import spacy
import random
import math
import os
import numpy as np
from collections import defaultdict
from pathlib import Path

def generateUsableFiles(file_path: str):
    """
    Genera archivos de corpus lematizado y vocabulario.
    Cada capítulo será un documento.
    Además, guarda cada capítulo en data/documentos/capitulo_X.txt
    """
    nlp = spacy.load("es_core_news_md")

    # Leer libro completo
    with open(file_path, "r", encoding="utf-8") as f:
        texto = f.read()

    # Detectar capítulos por líneas que contienen solo un número
    lineas = texto.split("\n")
    capitulos = []
    cap_actual = []
    
    import re
    for linea in lineas:
        if re.fullmatch(r"\d+", linea.strip()):
            if cap_actual:
                capitulos.append("\n".join(cap_actual).strip())
                cap_actual = []
            cap_actual.append(linea)
        else:
            cap_actual.append(linea)

    if cap_actual:
        capitulos.append("\n".join(cap_actual).strip())

    # Crear carpetas necesarias
    Path("data").mkdir(exist_ok=True)
    Path("data/documentos").mkdir(exist_ok=True)

    documentos_lematizados = []
    vocab_set = set()

    # Procesar cada capítulo
    for i, cap in enumerate(capitulos, start=1):

        # Guardar capítulo crudo en archivo independiente (opcional pero útil)
        raw_path = f"data/documentos/capitulo_{i}.txt"
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(cap)

        # Procesamiento lingüístico
        doc = nlp(cap)
        palabras = [
            token.lemma_.lower()
            for token in doc
            if token.is_alpha and not token.is_stop
        ]

        if palabras:
            documentos_lematizados.append(palabras)
            vocab_set.update(palabras)

    # Crear vocabulario global
    vocab_list = sorted(vocab_set)
    vocab = {w: i for i, w in enumerate(vocab_list)}
    inv_vocab = {i: w for w, i in vocab.items()}

    # Guardar diccionario
    with open("data/diccionario.txt", "w", encoding="utf-8") as f:
        for idx, palabra in inv_vocab.items():
            f.write(f"{idx}\t{palabra}\n")

    # Guardar documentos convertidos a índices
    with open("data/documentos.txt", "w", encoding="utf-8") as f:
        for palabras in documentos_lematizados:
            indices = [str(vocab[w]) for w in palabras]
            f.write(" ".join(indices) + "\n")

    # Lista final de documentos en índices
    documents_idx = [
        [vocab[w] for w in doc if w in vocab]
        for doc in documentos_lematizados
    ]
    documents_idx = [doc for doc in documents_idx if len(doc) > 0]

    print("✔ Corpus generado correctamente")
    print(f"  - {len(documents_idx)} capítulos procesados")
    print(f"  - {len(vocab)} palabras únicas en el vocabulario")
    print("  Archivos generados en la carpeta /data")

    return documents_idx, vocab, inv_vocab


def load_corpus_and_vocab(docs_path="data/documentos.txt", vocab_path="data/diccionario.txt"):
    """Carga corpus lematizado y diccionario."""
    vocab = {}
    inv_vocab = {}

    with open(vocab_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                idx, word = parts
                idx = int(idx)
                vocab[word] = idx
                inv_vocab[idx] = word

    documents = []
    with open(docs_path, "r", encoding="utf-8") as f:
        for line in f:
            indices = [int(i) for i in line.split()]
            if indices:
                documents.append(indices)

    return documents, vocab, inv_vocab


def initialize_topics(documents, K, V):
    """
    Inicializa tópicos aleatoriamente.
    CORRECCIÓN: usa V (tamaño del vocabulario) en lugar de len(documents[0])
    """
    ndk = defaultdict(lambda: np.zeros(K, dtype=int))
    nkw = defaultdict(lambda: np.zeros(V, dtype=int))
    nk = np.zeros(K, dtype=int)

    z_dn = []
    for d, doc in enumerate(documents):
        current_topics = []
        for w in doc:
            if w < 0 or w >= V:
                continue
            topic = random.randrange(K)
            current_topics.append(topic)

            ndk[d][topic] += 1
            nkw[topic][w] += 1
            nk[topic] += 1

        z_dn.append(current_topics)

    return z_dn, ndk, nkw, nk


def sample_topic(d, w, ndk, nkw, nk, K, alpha, beta, V):
    """
    Muestrea un nuevo tópico usando Gibbs Sampling.
    MEJORA: usa numpy para eficiencia y normalización más robusta.
    """
    probs = np.zeros(K)

    for k in range(K):
        probs[k] = ((ndk[d][k] + alpha) * 
                    (nkw[k][w] + beta) / 
                    (nk[k] + V * beta))

    # Normalizar
    probs /= probs.sum()
    
    # Muestrear
    return np.random.choice(K, p=probs)


def compute_perplexity(documents, ndk, nkw, nk, alpha, beta, V):
    """
    Calcula perplejidad para evaluar convergencia del modelo.
    NUEVA FUNCIÓN: permite monitorear la calidad del ajuste.
    """
    K = len(nk)
    log_likelihood = 0
    total_words = 0
    
    for d, doc in enumerate(documents):
        for w in doc:
            prob_w = 0
            for k in range(K):
                theta_dk = (ndk[d][k] + alpha) / (sum(ndk[d]) + K * alpha)
                phi_kw = (nkw[k][w] + beta) / (nk[k] + V * beta)
                prob_w += theta_dk * phi_kw
            
            log_likelihood += math.log(prob_w + 1e-10)
            total_words += 1
    
    perplexity = math.exp(-log_likelihood / total_words)
    return perplexity


def LDA(documents, V, K=5, iterations=500, alpha=0.1, beta=0.01, compute_perp=True):
    """
    Ejecuta LDA con Gibbs Sampling.
    MEJORAS: 
    - Cálculo correcto de V
    - Monitoreo de perplejidad
    - Mejor tracking de progreso
    """
    print(f"Iniciando LDA: K={K}, V={V}, docs={len(documents)}")
    # for d_i, doc in enumerate(documents):
    #     for w in doc:
    #         if w < 0 or w >= V:
    #             print("❌ ERROR: palabra fuera de rango")
    #             print("Documento:", d_i, "Palabra:", w, "Vocab size:", V)
    #             raise Exception("Índice fuera del rango del vocabulario")
    

    z_dn, ndk, nkw, nk = initialize_topics(documents, K, V)

    perplexities = []

    for it in range(iterations):
        for d, doc in enumerate(documents):
            for i, w in enumerate(doc):
                old_topic = z_dn[d][i]

                # Remover conteos
                ndk[d][old_topic] -= 1
                nkw[old_topic][w] -= 1
                nk[old_topic] -= 1

                # Muestrear nuevo tópico
                new_topic = sample_topic(d, w, ndk, nkw, nk, K, alpha, beta, V)

                # Actualizar conteos
                ndk[d][new_topic] += 1
                nkw[new_topic][w] += 1
                nk[new_topic] += 1

                z_dn[d][i] = new_topic

        if (it + 1) % 50 == 0:
            if compute_perp:
                perp = compute_perplexity(documents, ndk, nkw, nk, alpha, beta, V)
                perplexities.append(perp)
                print(f"Iteración {it+1}/{iterations} - Perplejidad: {perp:.2f}")
            else:
                print(f"Iteración {it+1}/{iterations}")

    return z_dn, ndk, nkw, nk, perplexities


def compute_theta(ndk, alpha, K):
    """Matriz documento-tópico."""
    theta = []
    for d in sorted(ndk.keys()):
        row = ndk[d]
        total = sum(row)
        theta.append([(c + alpha) / (total + K * alpha) for c in row])
    return np.array(theta)


def compute_phi(nkw, beta, V, K):
    """Matriz tópico-palabra."""
    phi = []
    for k in range(K):
        row = nkw[k]
        total = sum(row)
        phi.append([(c + beta) / (total + V * beta) for c in row])
    return np.array(phi)


def print_topics(phi, inv_vocab, top_n=10):
    """Muestra las palabras más representativas de cada tópico."""
    K = len(phi)
    for k in range(K):
        print(f"\n{'='*50}")
        print(f"TÓPICO {k}:")
        print('='*50)
        dist = phi[k]
        top_words = sorted(range(len(dist)), key=lambda i: dist[i], reverse=True)[:top_n]
        for rank, idx in enumerate(top_words, 1):
            print(f"  {rank:2d}. {inv_vocab[idx]:20s} ({dist[idx]:.4f})")


def get_document_topics(theta, top_n=3):
    """
    NUEVA FUNCIÓN: Muestra los tópicos dominantes por documento.
    """
    doc_topics = []
    for d, dist in enumerate(theta):
        top_topics = sorted(range(len(dist)), key=lambda k: dist[k], reverse=True)[:top_n]
        doc_topics.append([(k, dist[k]) for k in top_topics])
    return doc_topics


def save_results(theta, phi, inv_vocab, output_dir="output"):
    """
    Guarda resultados en archivos incluyendo distribuciones completas.
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    # Guardar matriz theta (documentos-tópicos)
    np.savetxt(f"{output_dir}/theta_matriz.txt", theta, fmt='%.6f')
    
    # Guardar matriz phi (tópicos-palabras)
    np.savetxt(f"{output_dir}/phi_matriz.txt", phi, fmt='%.6f')
    
    # Guardar distribuciones de tópicos por documento
    with open(f"{output_dir}/distribucion_topicos_documentos.txt", "w", encoding="utf-8") as f:
        f.write("DISTRIBUCIÓN DE TÓPICOS EN CADA DOCUMENTO\n")
        f.write("="*70 + "\n\n")
        for d, dist in enumerate(theta):
            f.write(f"Documento {d}:\n")
            for k, prob in enumerate(dist):
                f.write(f"  Tópico {k}: {prob:.4f} ({prob*100:.2f}%)\n")
            f.write("\n")
    
    # Guardar palabras principales por tópico
    with open(f"{output_dir}/palabras_por_topico.txt", "w", encoding="utf-8") as f:
        f.write("DISTRIBUCIÓN DE PALABRAS EN CADA TÓPICO\n")
        f.write("="*70 + "\n\n")
        for k in range(len(phi)):
            f.write(f"TÓPICO {k}:\n")
            dist = phi[k]
            top_words = sorted(range(len(dist)), key=lambda i: dist[i], reverse=True)[:30]
            for idx in top_words:
                f.write(f"  {inv_vocab[idx]:25s} {dist[idx]:.6f} ({dist[idx]*100:.3f}%)\n")
            f.write("\n" + "-"*70 + "\n\n")
    
    print(f"\n✓ Resultados guardados en '{output_dir}/'")


def mostrar_distribucion_topico(phi, inv_vocab, topico, top_n=20):
    """
    Muestra la distribución de palabras en un tópico específico.
    """
    if topico < 0 or topico >= len(phi):
        print(f"Error: Tópico {topico} no existe. Debe estar entre 0 y {len(phi)-1}")
        return
    
    print(f"\n{'='*70}")
    print(f"DISTRIBUCIÓN DE PALABRAS EN TÓPICO {topico}")
    print('='*70)
    
    dist = phi[topico]
    top_words = sorted(range(len(dist)), key=lambda i: dist[i], reverse=True)[:top_n]
    
    print(f"\n{'Rank':<6} {'Palabra':<25} {'Probabilidad':<15} {'Porcentaje'}")
    print("-"*70)
    
    for rank, idx in enumerate(top_words, 1):
        prob = dist[idx]
        print(f"{rank:<6} {inv_vocab[idx]:<25} {prob:.6f}        {prob*100:.3f}%")
    
    print()


def mostrar_distribucion_documento(theta, doc_id, K):
    """
    Muestra la distribución de tópicos en un documento específico.
    """
    if doc_id < 0 or doc_id >= len(theta):
        print(f"Error: Documento {doc_id} no existe. Debe estar entre 0 y {len(theta)-1}")
        return
    
    print(f"\n{'='*70}")
    print(f"DISTRIBUCIÓN DE TÓPICOS EN DOCUMENTO {doc_id}")
    print('='*70)
    
    dist = theta[doc_id]
    
    print(f"\n{'Tópico':<10} {'Probabilidad':<15} {'Porcentaje':<15} {'Barra'}")
    print("-"*70)
    
    for k in range(K):
        prob = dist[k]
        bar_length = int(prob * 50)
        bar = '█' * bar_length
        print(f"{k:<10} {prob:.6f}        {prob*100:.2f}%          {bar}")
    
    # Mostrar tópico dominante
    dominant = np.argmax(dist)
    print(f"\nTópico dominante: {dominant} ({dist[dominant]*100:.2f}%)")
    print()


def mostrar_todas_distribuciones_topicos(phi, inv_vocab, top_n=15):
    """
    Muestra la distribución de palabras en TODOS los tópicos.
    """
    K = len(phi)
    print(f"\n{'='*70}")
    print(f"DISTRIBUCIÓN DE PALABRAS EN TODOS LOS TÓPICOS")
    print('='*70)
    
    for k in range(K):
        print(f"\n{'-'*70}")
        print(f"TÓPICO {k}:")
        print('-'*70)
        
        dist = phi[k]
        top_words = sorted(range(len(dist)), key=lambda i: dist[i], reverse=True)[:top_n]
        
        for rank, idx in enumerate(top_words, 1):
            prob = dist[idx]
            print(f"  {rank:2d}. {inv_vocab[idx]:25s} {prob:.6f} ({prob*100:.3f}%)")
    
    print()


def mostrar_todas_distribuciones_documentos(theta, K, max_docs=None):
    """
    Muestra la distribución de tópicos en TODOS los documentos.
    """
    print(f"\n{'='*70}")
    print(f"DISTRIBUCIÓN DE TÓPICOS EN TODOS LOS DOCUMENTOS")
    print('='*70)
    
    num_docs = len(theta) if max_docs is None else min(max_docs, len(theta))
    
    for d in range(num_docs):
        print(f"\n{'-'*70}")
        print(f"Documento {d}:")
        print('-'*70)
        
        dist = theta[d]
        
        for k in range(K):
            prob = dist[k]
            bar_length = int(prob * 40)
            bar = '█' * bar_length
            print(f"  Tópico {k}: {prob:.4f} ({prob*100:.2f}%)  {bar}")
        
        dominant = np.argmax(dist)
        print(f"  → Dominante: Tópico {dominant}")
    
    if max_docs and max_docs < len(theta):
        print(f"\n(Mostrando {max_docs} de {len(theta)} documentos)")
    
    print()


def generar_matrices(theta, phi, output_dir="output"):
    """
    Genera y guarda las matrices principales del algoritmo LDA.
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    print(f"\n{'='*70}")
    print("GENERANDO MATRICES DEL ALGORITMO LDA")
    print('='*70)
    
    # Matriz Theta (Documentos × Tópicos)
    theta_path = f"{output_dir}/matriz_theta_documentos_topicos.txt"
    np.savetxt(theta_path, theta, fmt='%.6f', 
               header=f"Matriz THETA (Documentos × Tópicos)\nDimensiones: {theta.shape[0]} documentos × {theta.shape[1]} tópicos")
    print(f"\n✓ Matriz THETA guardada: {theta_path}")
    print(f"  Dimensiones: {theta.shape[0]} documentos × {theta.shape[1]} tópicos")
    print(f"  Cada fila representa un documento")
    print(f"  Cada columna representa la probabilidad de un tópico")
    
    # Matriz Phi (Tópicos × Palabras)
    phi_path = f"{output_dir}/matriz_phi_topicos_palabras.txt"
    np.savetxt(phi_path, phi, fmt='%.6f',
               header=f"Matriz PHI (Tópicos × Palabras)\nDimensiones: {phi.shape[0]} tópicos × {phi.shape[1]} palabras")
    print(f"\n✓ Matriz PHI guardada: {phi_path}")
    print(f"  Dimensiones: {phi.shape[0]} tópicos × {phi.shape[1]} palabras")
    print(f"  Cada fila representa un tópico")
    print(f"  Cada columna representa la probabilidad de una palabra")
    
    print(f"\n✓ Matrices generadas exitosamente en '{output_dir}/'")
    print()


def menu_interactivo(theta, phi, inv_vocab, K, num_docs):
    """
    Menú interactivo para explorar los resultados del LDA.
    """
    while True:
        print("\n" + "="*70)
        print("MENÚ DE ANÁLISIS LDA")
        print("="*70)
        print(f"Corpus: {num_docs} documentos | {len(inv_vocab)} palabras | {K} tópicos")
        print()
        print("1. Ver distribución de palabras en un tópico específico")
        print("2. Ver distribución de tópicos en un documento específico")
        print("3. Ver distribución de palabras en TODOS los tópicos")
        print("4. Ver distribución de tópicos en TODOS los documentos")
        print("5. Generar matrices THETA y PHI")
        print("6. Ver resumen de tópicos principales")
        print("7. Estadísticas del corpus")
        print("0. Salir")
        print()
        
        try:
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == "1":
                topico = int(input(f"Ingresa el número de tópico (0-{K-1}): "))
                top_n = int(input("¿Cuántas palabras mostrar? (default 20): ") or "20")
                mostrar_distribucion_topico(phi, inv_vocab, topico, top_n)
            
            elif opcion == "2":
                doc_id = int(input(f"Ingresa el número de documento (0-{num_docs-1}): "))
                mostrar_distribucion_documento(theta, doc_id, K)
            
            elif opcion == "3":
                top_n = int(input("¿Cuántas palabras por tópico? (default 15): ") or "15")
                mostrar_todas_distribuciones_topicos(phi, inv_vocab, top_n)
            
            elif opcion == "4":
                max_docs = input(f"¿Cuántos documentos mostrar? (Enter para todos los {num_docs}): ").strip()
                max_docs = int(max_docs) if max_docs else None
                mostrar_todas_distribuciones_documentos(theta, K, max_docs)
            
            elif opcion == "5":
                output_dir = input("Directorio de salida (default 'output'): ").strip() or "output"
                generar_matrices(theta, phi, output_dir)
            
            elif opcion == "6":
                print_topics(phi, inv_vocab, top_n=15)
            
            elif opcion == "7":
                mostrar_estadisticas_corpus(theta, phi, K, num_docs)
            
            elif opcion == "0":
                print("\n¡Hasta luego!")
                break
            
            else:
                print("\n⚠ Opción no válida. Intenta de nuevo.")
        
        except ValueError:
            print("\n⚠ Error: Debes ingresar un número válido.")
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n⚠ Error: {e}")


def mostrar_estadisticas_corpus(theta, phi, K, num_docs):
    """
    Muestra estadísticas generales del corpus y los resultados.
    """
    print(f"\n{'='*70}")
    print("ESTADÍSTICAS DEL CORPUS")
    print('='*70)
    
    print(f"\nNúmero de documentos: {num_docs}")
    print(f"Número de tópicos: {K}")
    print(f"Tamaño del vocabulario: {phi.shape[1]}")
    
    # Distribución de documentos por tópico dominante
    print(f"\n{'Distribución de documentos por tópico dominante:'}")
    print("-"*50)
    dominant_topics = np.argmax(theta, axis=1)
    for k in range(K):
        count = np.sum(dominant_topics == k)
        pct = (count / num_docs) * 100
        bar = '█' * int(pct / 2)
        print(f"  Tópico {k}: {count:4d} docs ({pct:5.2f}%)  {bar}")
    
    # Entropía promedio de documentos
    print(f"\n{'Diversidad de tópicos en documentos:'}")
    print("-"*50)
    entropies = []
    for dist in theta:
        entropy = -np.sum(dist * np.log(dist + 1e-10))
        entropies.append(entropy)
    avg_entropy = np.mean(entropies)
    print(f"  Entropía promedio: {avg_entropy:.4f}")
    print(f"  (Mayor entropía = documentos más diversos en tópicos)")
    
    print()


if __name__ == "__main__":
    print("="*70)
    print("ANÁLISIS DE TÓPICOS CON LDA (Latent Dirichlet Allocation)")
    print("="*70)
    
    # Cargar datos
    print("\nCargando corpus...")
    documents, vocab, inv_vocab = load_corpus_and_vocab()
    V = len(vocab)
    num_docs = len(documents)
    
    print(f"✓ Corpus cargado: {num_docs} documentos, {V} palabras únicas")
    
    # Parámetros
    K = 5
    iterations = 100
    alpha = 50 / K
    beta = 0.01
    
    print(f"\nParámetros del modelo:")
    print(f"  Número de tópicos (K): {K}")
    print(f"  Iteraciones: {iterations}")
    print(f"  Alpha: {alpha:.4f}")
    print(f"  Beta: {beta}")
    
    # Ejecutar LDA
    print("\nEjecutando algoritmo LDA...")
    z_dn, ndk, nkw, nk, perplexities = LDA(
        documents, 
        K=K, 
        iterations=iterations, 
        alpha=alpha, 
        beta=beta
    )
    
    # Computar matrices finales
    print("\nCalculando matrices finales...")
    theta = compute_theta(ndk, alpha, K)
    phi = compute_phi(nkw, beta, V, K)
    
    # Guardar resultados automáticamente
    print("\nGuardando resultados...")
    save_results(theta, phi, inv_vocab)
    
    # Mostrar resumen inicial
    print("\n" + "="*70)
    print("RESUMEN DE TÓPICOS PRINCIPALES")
    print("="*70)
    print_topics(phi, inv_vocab, top_n=10)
    
    # Iniciar menú interactivo
    menu_interactivo(theta, phi, inv_vocab, K, num_docs)