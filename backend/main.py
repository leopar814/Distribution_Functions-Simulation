from fastapi import FastAPI, Query, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import numpy as np
import sympy as sp
import random   
import math
from collections import Counter
from typing import List
import spacy
from pathlib import Path
import json
import shutil

# Importar funciones de LDA
from lda_lib.LDA import (
    generateUsableFiles,
    load_corpus_and_vocab, 
    LDA, 
    compute_theta,
    compute_phi,
    compute_perplexity
)

app = FastAPI()

# Permitir que el frontend en otro puerto pueda conectarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales para mantener el estado del LDA
lda_state = {
    "trained": False,
    "documents": None,
    "vocab": None,
    "inv_vocab": None,
    "theta": None,
    "phi": None,
    "K": None,
    "V": None,
    "num_docs": None,
    "metadata": None
}

# --------------------
# Simulación Bernoulli 
# --------------------
@app.get("/bernoulli")
def generar_bernoulli(repeticiones: int, proba_exito: float):
    num_exitos, num_fracasos = 0, 0
    secuencia = []

    for _ in range(repeticiones):
        r = random.random()
        if r <= proba_exito:
            secuencia.append("E")
            num_exitos += 1
        else:
            secuencia.append("F")
            num_fracasos += 1

    return {
        "repeticiones": repeticiones,
        "proba_exito": proba_exito,
        "exitos": num_exitos,
        "fracasos": num_fracasos,
        "secuencia": secuencia
    }

# --------------------
# Simulación Binomial
# --------------------
@app.get("/binomial")
def simular_binomial(muestra : int, ensayos : int, proba_exito : float):
    secuencia = []
    for _ in range(muestra):  
        resultado = generar_bernoulli(ensayos, proba_exito)
        num_Exitos = resultado["exitos"]
        secuencia.append(num_Exitos)
    conteo = Counter(secuencia)

    frecuencias = [{"x" : i, "y" : conteo.get(i, 0)} for i in range(ensayos + 1)]
    return {
        "frecuencias": frecuencias,
        "secuencia" : secuencia
    }

# --------------------
# Simulación Exponencial
# --------------------
@app.get("/exponential")
def simular_exponencial(n : int, lambda_ : float):
    
    muestras = []
    for _ in range(n):
        u = random.random()
        x = -math.log(1 - u) / lambda_
        muestras.append(x)

    conteo, bordes = np.histogram(muestras, bins="auto", density=True)
    centers = (bordes[:-1] + bordes[1:]) / 2
    frecuencias = [
        {"x": float(c), "y": float(d)}
        for c, d in zip(centers, conteo)
    ]

    max_x = max(muestras)
    theo_x = np.linspace(0, max_x, 100)
    theo_y = lambda_ * np.exp(-lambda_ * theo_x)
    teorica = [{"x": float(x), "y": float(y)} for x, y in zip(theo_x, theo_y)]

    return {
        "muestras": muestras,
        "frecuencias": frecuencias,
        "teorica": teorica,
        "lambda": lambda_
    }

# --------------------
# Simulación Multinomial
# --------------------
def simular_multinomial(n: int, probs: List[float]):
    k = len(probs)
    conteos = [0] * k
    secuencia = []
    acumuladas = []
    total = 0.0
    for p in probs:
        total += p
        acumuladas.append(total)
    for _ in range(n):
        r = random.random()
        for i, c in enumerate(acumuladas):
            if r <= c:
                conteos[i] += 1
                secuencia.append(f"C{i+1}")
                break
    return conteos, secuencia

@app.get("/multinomial")
def generar_multinomial(
    n: int,
    rep: int = 1,
    probs: List[float] = Query(..., description="Lista de probabilidades que suman 1")
):
     
    if n <= 0 or rep <= 0:
        raise HTTPException(status_code=400, detail="n y repeticiones deben ser positivos")
    if any(p < 0 for p in probs):
        raise HTTPException(status_code=400, detail="Las probabilidades no pueden ser negativas")
    if abs(sum(probs) - 1.0) > 1e-6:
        raise HTTPException(status_code=400, detail="Las probabilidades deben sumar 1")

    vectores = []
    ultima_secuencia = []
    for _ in range(rep):
        conteos, secuencia = simular_multinomial(n, probs)
        vectores.append(conteos)
        ultima_secuencia = secuencia

    categorias = [f"C{i+1}" for i in range(len(probs))]

    return {
        "n": n,
        "rep": rep,
        "categorias": categorias,
        "vectores": vectores,
        "conteos": vectores[0],
        "secuencia": ultima_secuencia[:100]
    }

# --------------------
# Simulación Gibss
# --------------------
    
x, y, t = sp.symbols('x y t')

def X(f, xmin, xmax, y_val):
    fy = sp.integrate(f, (x, xmin, xmax))
    fxy = (f / fy).subs(y, y_val)
    Fxy = sp.integrate(fxy.subs(x, t), (t, xmin, x))
    u = random.random()
    sol = sp.solve(Fxy - u, x)
    sol_real = [s for s in sol if s.is_real and xmin <= s <= xmax]
    return float(sol_real[0]) if sol_real else None

def Y(f, ymin, ymax, x_val):
    fx = sp.integrate(f, (y, ymin, ymax))
    fyx = (f / fx).subs(x, x_val)
    Fyx = sp.integrate(fyx.subs(y, t), (t, ymin, y))
    v = random.random()
    sol = sp.solve(Fyx - v, y)
    sol_real = [s for s in sol if s.is_real and ymin <= s <= ymax]
    return float(sol_real[0]) if sol_real else None

@app.get("/gibss")
def generar_gibbs(
    funcion: str, 
    xmin: float, 
    xmax: float, 
    ymin: float, 
    ymax: float, 
    n: int = 100, 
    xinicio: Optional[float] = None,
    yinicio: Optional[float] = None
):
    f = sp.sympify(funcion)

    muestras = []

    if xinicio is not None and yinicio is not None:
        xn, yn = xinicio, yinicio
    else:
        xn = random.uniform(0, 10)
        yn = random.uniform(0, 10)
    
    muestras.append((xn, yn))

    for _ in range(n - 1):
        xn = X(f, xmin, xmax, yn)
        yn = Y(f, ymin, ymax, xn)
        muestras.append((xn, yn))

    return {
        "muestras": [{"x": float(px), "y": float(py)} for px, py in muestras],
        "inicio": {"x": float(muestras[0][0]), "y": float(muestras[0][1])},
        "fin": {"x": float(muestras[-1][0]), "y": float(muestras[-1][1])}
    }

# --------------------
# Simulación Normal
# --------------------
@app.get("/normal")
def generar_normal(
    repeticiones: int,
    mu: float = 0.0,
    sigma: float = 1.0,
    bins: int = 20
):
    if repeticiones <= 0 or sigma <= 0:
        raise HTTPException(status_code=400, detail="repeticiones y sigma deben ser positivos")

    datos = []
    pares = (repeticiones + 1) // 2
    for _ in range(pares):
        u1, u2 = random.random() or 1e-10, random.random()
        r = math.sqrt(-2 * math.log(u1))
        z1 = r * math.cos(2 * math.pi * u2)
        z2 = r * math.sin(2 * math.pi * u2)
        datos.append(mu + sigma * z1)
        if len(datos) < repeticiones:
            datos.append(mu + sigma * z2)

    muestra = datos

    counts, edges = np.histogram(muestra, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    frecuencias = [{"x": float(c), "y": float(d)} for c, d in zip(centers, counts)]

    xs = np.linspace(min(muestra), max(muestra), 200)
    pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-((xs - mu)**2) / (2 * sigma**2))
    teorica = [{"x": float(x), "y": float(y)} for x, y in zip(xs, pdf)]

    return {
        "repeticiones": repeticiones,
        "frecuencias": frecuencias,
        "teorica": teorica,
        "muestra": muestra[:100]
    }

# --------------------
# Simulación Bivariada
# --------------------
def pdf_bivariada_grid(mx: float, my: float, cov_matrix: np.ndarray, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    X, Y = np.meshgrid(xs, ys)
    pos = np.dstack((X, Y))
    inv = np.linalg.inv(cov_matrix)
    det = np.linalg.det(cov_matrix)
    norm_const = 1.0 / (2 * np.pi * np.sqrt(det))
    diff = pos - np.array([mx, my])
    Z = np.empty(X.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            v = diff[i, j]
            Z[i, j] = norm_const * np.exp(-0.5 * (v @ inv @ v))
    return Z

def simular_multivariada(n: int, mx: float, my: float, varx: float, vary: float, rho: float):
    cov = rho * np.sqrt(varx * vary)
    cov_matrix = np.array([[varx, cov], [cov, vary]])
    datos = np.random.multivariate_normal([mx, my], cov_matrix, size=n)
    return datos, cov_matrix

@app.get("/normal_bivariada")
def generar_normal_bivariada(
    n: int,
    mx: float = 0.0,
    my: float = 0.0,
    varx: float = 1.0,
    vary: float = 1.0,
    rho: float = 0.0,
    grid: int = 60
) -> Dict[str, Any]:
    
    if n <= 0 or varx <= 0 or vary <= 0:
        raise HTTPException(status_code=400, detail="n, varx y vary deben ser positivos")
    if not (-1.0 <= rho <= 1.0):
        raise HTTPException(status_code=400, detail="rho debe estar en [-1, 1]")

    datos, cov_matrix = simular_multivariada(n, mx, my, varx, vary, rho)
    xs = datos[:, 0].tolist()
    ys = datos[:, 1].tolist()

    xmin, xmax = float(np.min(datos[:,0])), float(np.max(datos[:,0]))
    ymin, ymax = float(np.min(datos[:,1])), float(np.max(datos[:,1]))
    pad_x = (xmax - xmin) * 0.1 if xmax > xmin else 1.0
    pad_y = (ymax - ymin) * 0.1 if ymax > ymin else 1.0
    xs_grid = np.linspace(xmin - pad_x, xmax + pad_x, grid)
    ys_grid = np.linspace(ymin - pad_y, ymax + pad_y, grid)
    Z = pdf_bivariada_grid(mx, my, cov_matrix, xs_grid, ys_grid)

    mean_x = float(np.mean(xs))
    mean_y = float(np.mean(ys))
    var_x = float(np.var(xs, ddof=0))
    var_y = float(np.var(ys, ddof=0))
    corr = float(np.corrcoef(xs, ys)[0,1])

    muestras = [[float(px), float(py)] for px, py in zip(xs, ys)]

    return {
        "n": n,
        "mx": mx,
        "my": my,
        "varx": varx,
        "vary": vary,
        "rho": rho,
        "muestras": muestras,
        "inicio": {"x": float(muestras[0][0]), "y": float(muestras[0][1])},
        "fin":    {"x": float(muestras[-1][0]), "y": float(muestras[-1][1])},
        "grid": {
            "x": xs_grid.tolist(),
            "y": ys_grid.tolist(),
            "z": Z.tolist()
        },
        "stats": {
            "mean_x": mean_x,
            "mean_y": mean_y,
            "var_x": var_x,
            "var_y": var_y,
            "corr": corr
        }
    }

# ============================================================
# ENDPOINTS DE LDA
# ============================================================

@app.post("/lda/upload")
async def upload_corpus(file: UploadFile = File(...)):
    """
    Recibe un archivo .txt con el corpus y lo procesa para LDA.
    """
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos .txt")
    
    try:
        Path("data").mkdir(exist_ok=True)
        temp_path = "temp_corpus.txt"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        documents, vocab, inv_vocab = generateUsableFiles(temp_path)

        lda_state["documents"] = documents
        lda_state["vocab"] = vocab
        lda_state["inv_vocab"] = inv_vocab
        lda_state["V"] = len(vocab)
        lda_state["num_docs"] = len(documents)
        lda_state["trained"] = False
                
        return {
            "success": True,
            "message": "Corpus procesado exitosamente",
            "num_docs": len(documents),
            "vocab_size": len(vocab),
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar archivo: {str(e)}")

@app.get("/lda/train")
def train_lda(
    K: int = Query(5, description="Número de tópicos"),
    iterations: int = Query(300, description="Número de iteraciones"),
    alpha: Optional[float] = Query(None, description="Parámetro alpha (default: 50/K)"),
    beta: float = Query(0.01, description="Parámetro beta")
):
    """
    Entrena el modelo LDA con el corpus previamente cargado.
    """
    if lda_state["documents"] is None:
        raise HTTPException(status_code=400, detail="Primero debes cargar un corpus usando /lda/upload")
    
    try:
        documents = lda_state["documents"]
        vocab = lda_state["vocab"]
        inv_vocab = lda_state["inv_vocab"]
        V = lda_state["V"]
        num_docs = lda_state["num_docs"]
        
        if alpha is None:
            alpha = 50 / K
        
        z_dn, ndk, nkw, nk, perplexities = LDA(
            documents, V=V, K=K, iterations=iterations,
            alpha=alpha, beta=beta, compute_perp=True
        )
        
        theta = compute_theta(ndk, alpha, K)
        phi = compute_phi(nkw, beta, V, K)
        
        metadata = {
            "K": K, "iterations": iterations, "alpha": alpha, "beta": beta,
            "num_docs": num_docs, "vocab_size": V,
            "final_perplexity": float(perplexities[-1]) if perplexities else None
        }
        
        lda_state["trained"] = True
        lda_state["theta"] = theta
        lda_state["phi"] = phi
        lda_state["K"] = K
        lda_state["metadata"] = metadata
        
        return {
            "success": True,
            "message": "Modelo LDA entrenado exitosamente",
            "num_docs": num_docs, "vocab_size": V, "K": K,
            "iterations": iterations, "alpha": alpha, "beta": beta,
            "final_perplexity": float(perplexities[-1]) if perplexities else None,
            "perplexity_history": [
                {"iteration": (i+1)*50, "perplexity": float(p)} 
                for i, p in enumerate(perplexities)
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al entrenar LDA: {str(e)}")

@app.get("/lda/info")
def get_lda_info():
    """Retorna información general del modelo LDA entrenado."""
    if not lda_state["trained"]:
        raise HTTPException(status_code=400, detail="Modelo no entrenado. Primero carga un corpus y entrena el modelo.")
    
    theta = lda_state["theta"]
    K = lda_state["K"]
    num_docs = lda_state["num_docs"]
    
    dominant_topics = np.argmax(theta, axis=1)
    topic_distribution = []
    for k in range(K):
        count = int(np.sum(dominant_topics == k))
        pct = (count / num_docs) * 100
        topic_distribution.append({"topic": k, "count": count, "percentage": round(pct, 2)})
    
    entropies = []
    for dist in theta:
        entropy = float(-np.sum(dist * np.log(dist + 1e-10)))
        entropies.append(entropy)
    avg_entropy = float(np.mean(entropies))
    
    return {
        "trained": True, "num_docs": num_docs, "vocab_size": lda_state["V"], "K": K,
        "topic_distribution": topic_distribution, "avg_entropy": round(avg_entropy, 4),
        "metadata": lda_state["metadata"]
    }



@app.get("/lda/topics")
def get_all_topics(top_n: int = Query(15, description="Número de palabras por tópico")):
    """Retorna las palabras más representativas de todos los tópicos."""
    if not lda_state["trained"]:
        raise HTTPException(status_code=400, detail="Modelo no entrenado.")
    
    phi = lda_state["phi"]
    inv_vocab = lda_state["inv_vocab"]
    K = lda_state["K"]
    
    topics = []
    for k in range(K):
        dist = phi[k]
        top_words_idx = sorted(range(len(dist)), key=lambda i: dist[i], reverse=True)[:top_n]
        words = [{
            "word": inv_vocab[idx],
            "probability": round(float(dist[idx]), 6),
            "percentage": round(float(dist[idx]) * 100, 3)
        } for idx in top_words_idx]
        topics.append({"topic_id": k, "words": words})
    
    return {"K": K, "top_n": top_n, "topics": topics}



@app.get("/lda/topic/{topic_id}")
def get_topic_details(
    topic_id: int, 
    top_n: int = Query(20, description="Número de palabras a mostrar")
):
    """
    Retorna detalles de un tópico específico.
    """
    if not lda_state["trained"]:
        raise HTTPException(status_code=400, detail="Modelo no cargado.")
    
    K = lda_state["K"]
    if topic_id < 0 or topic_id >= K:
        raise HTTPException(status_code=400, detail=f"topic_id debe estar entre 0 y {K-1}")
    
    phi = lda_state["phi"]
    inv_vocab = lda_state["inv_vocab"]
    
    dist = phi[topic_id]
    top_words_idx = sorted(range(len(dist)), key=lambda i: dist[i], reverse=True)[:top_n]
    
    words = []
    for rank, idx in enumerate(top_words_idx, 1):
        words.append({
            "rank": rank,
            "word": inv_vocab[idx],
            "probability": round(float(dist[idx]), 6),
            "percentage": round(float(dist[idx]) * 100, 3)
        })
    
    # Para gráfico de barras
    chart_data = [
        {"word": w["word"], "probability": w["probability"]} 
        for w in words[:15]  # Top 15 para gráfico
    ]
    
    return {
        "topic_id": topic_id,
        "top_n": top_n,
        "words": words,
        "chart_data": chart_data
    }


@app.get("/lda/document/{doc_id}")
def get_document_details(doc_id: int):
    """
    Retorna la distribución de tópicos en un documento específico.
    """
    if not lda_state["trained"]:
        raise HTTPException(status_code=400, detail="Modelo no cargado.")
    
    num_docs = lda_state["num_docs"]
    if doc_id < 0 or doc_id >= num_docs:
        raise HTTPException(status_code=400, detail=f"doc_id debe estar entre 0 y {num_docs-1}")
    
    theta = lda_state["theta"]
    K = lda_state["K"]
    
    dist = theta[doc_id]
    
    topics = []
    for k in range(K):
        prob = float(dist[k])
        topics.append({
            "topic_id": k,
            "probability": round(prob, 6),
            "percentage": round(prob * 100, 2)
        })
    
    # Tópico dominante
    dominant_topic = int(np.argmax(dist))
    dominant_prob = float(dist[dominant_topic])
    
    # Para gráfico
    chart_data = [
        {"topic": f"Tópico {t['topic_id']}", "probability": t["probability"]}
        for t in topics
    ]
    
    return {
        "doc_id": doc_id,
        "K": K,
        "topics": topics,
        "dominant_topic": dominant_topic,
        "dominant_probability": round(dominant_prob, 4),
        "chart_data": chart_data
    }


@app.get("/lda/documents/summary")
def get_documents_summary(limit: int = Query(50, description="Número máximo de documentos a retornar")):
    """
    Retorna un resumen de la distribución de tópicos en todos los documentos.
    """
    if not lda_state["trained"]:
        raise HTTPException(status_code=400, detail="Modelo no cargado.")
    
    theta = lda_state["theta"]
    K = lda_state["K"]
    num_docs = lda_state["num_docs"]
    
    # Limitar la cantidad de documentos
    max_docs = min(limit, num_docs)
    
    documents = []
    for d in range(max_docs):
        dist = theta[d]
        dominant = int(np.argmax(dist))
        
        # Top 3 tópicos
        top_topics_idx = sorted(range(K), key=lambda k: dist[k], reverse=True)[:3]
        top_topics = [
            {
                "topic_id": k,
                "probability": round(float(dist[k]), 4),
                "percentage": round(float(dist[k]) * 100, 2)
            }
            for k in top_topics_idx
        ]
        
        documents.append({
            "doc_id": d,
            "dominant_topic": dominant,
            "dominant_probability": round(float(dist[dominant]), 4),
            "top_topics": top_topics
        })
    
    return {
        "num_docs": num_docs,
        "showing": max_docs,
        "K": K,
        "documents": documents
    }


@app.get("/lda/matrices/theta")
def get_theta_matrix(limit: int = Query(100, description="Número máximo de filas")):
    """
    Retorna la matriz THETA (Documentos × Tópicos).
    """
    if not lda_state["trained"]:
        raise HTTPException(status_code=400, detail="Modelo no cargado.")
    
    theta = lda_state["theta"]
    num_docs = min(limit, len(theta))
    
    matrix = []
    for d in range(num_docs):
        matrix.append({
            "doc_id": d,
            "distribution": [round(float(p), 6) for p in theta[d]]
        })
    
    return {
        "matrix_name": "THETA",
        "description": "Distribución de tópicos por documento",
        "dimensions": {
            "documents": lda_state["num_docs"],
            "topics": lda_state["K"],
            "showing": num_docs
        },
        "matrix": matrix
    }


@app.get("/lda/matrices/phi")
def get_phi_matrix(limit_words: int = Query(50, description="Número máximo de palabras por tópico")):
    """
    Retorna la matriz PHI (Tópicos × Palabras) con las palabras más probables.
    """
    if not lda_state["trained"]:
        raise HTTPException(status_code=400, detail="Modelo no cargado.")
    
    phi = lda_state["phi"]
    inv_vocab = lda_state["inv_vocab"]
    K = lda_state["K"]
    
    matrix = []
    for k in range(K):
        dist = phi[k]
        top_words_idx = sorted(range(len(dist)), key=lambda i: dist[i], reverse=True)[:limit_words]
        
        words_dist = []
        for idx in top_words_idx:
            words_dist.append({
                "word": inv_vocab[idx],
                "word_id": idx,
                "probability": round(float(dist[idx]), 6)
            })
        
        matrix.append({
            "topic_id": k,
            "top_words": words_dist
        })
    
    return {
        "matrix_name": "PHI",
        "description": "Distribución de palabras por tópico",
        "dimensions": {
            "topics": K,
            "vocab_size": lda_state["V"],
            "showing_words": limit_words
        },
        "matrix": matrix
    }


@app.get("/lda/visualize/topic_comparison")
def visualize_topic_comparison():
    """
    Retorna datos para comparar todos los tópicos visualmente.
    """
    if not lda_state["trained"]:
        raise HTTPException(status_code=400, detail="Modelo no cargado.")
    
    phi = lda_state["phi"]
    inv_vocab = lda_state["inv_vocab"]
    K = lda_state["K"]
    
    # Obtener top 10 palabras por cada tópico
    topics_comparison = []
    for k in range(K):
        dist = phi[k]
        top_10_idx = sorted(range(len(dist)), key=lambda i: dist[i], reverse=True)[:10]
        
        words = [inv_vocab[idx] for idx in top_10_idx]
        probs = [float(dist[idx]) for idx in top_10_idx]
        
        topics_comparison.append({
            "topic_id": k,
            "label": f"Tópico {k}",
            "top_words": words,
            "probabilities": probs
        })
    
    return {
        "K": K,
        "topics": topics_comparison
    }


@app.get("/lda/visualize/document_distribution")
def visualize_document_distribution():
    """
    Retorna datos para visualizar la distribución de documentos por tópico dominante.
    """
    if not lda_state["trained"]:
        raise HTTPException(status_code=400, detail="Modelo no cargado.")
    
    theta = lda_state["theta"]
    K = lda_state["K"]
    num_docs = lda_state["num_docs"]
    
    dominant_topics = np.argmax(theta, axis=1)
    
    distribution = []
    for k in range(K):
        count = int(np.sum(dominant_topics == k))
        distribution.append({
            "topic": f"Tópico {k}",
            "topic_id": k,
            "count": count,
            "percentage": round((count / num_docs) * 100, 2)
        })
    
    return {
        "K": K,
        "num_docs": num_docs,
        "distribution": distribution
    }


# @app.post("/lda/load")
# def load_lda_model(output_dir: str = Query("output", description="Directorio con los archivos del modelo")):
#     """
#     Carga un modelo LDA previamente entrenado desde archivos.
#     """
#     success, message = load_lda_results(output_dir)
    
#     if success:
#         return {
#             "success": True,
#             "message": message,
#             "num_docs": lda_state["num_docs"],
#             "vocab_size": lda_state["V"],
#             "K": lda_state["K"],
#             "metadata": lda_state["metadata"]
#         }
#     else:
#         raise HTTPException(status_code=404, detail=message)
