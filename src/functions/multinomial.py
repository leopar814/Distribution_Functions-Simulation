import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# =========================
# Funciones auxiliares
# =========================
def _parse_probabilidad_texto(texto):
    """Convierte '1/6' o '0.16' a float"""
    texto = texto.strip()
    if "/" in texto:
        num, den = texto.split("/")
        return float(num) / float(den)
    else:
        return float(texto)

def _simular_una_multinomial(n, probs):
    """Simula un experimento multinomial"""
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

def _graficar_barras(valores, etiquetas, frame, titulo):
    """Genera un gráfico de barras dentro de un frame de Tkinter"""
    fig, ax = plt.subplots(figsize=(4, 3))
    barras = ax.bar(etiquetas, valores)
    ax.set_ylabel("Frecuencia")
    ax.set_title(titulo)
    for barra in barras:
        altura = barra.get_height()
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            altura + 0.1,
            str(round(altura, 2)),
            ha="center",
            va="bottom",
            fontsize=10
        )
    for widget in frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    plt.close(fig)

def _mostrar_detalles(secuencia, frame_detalles):
    """Muestra los primeros 100 elementos de la secuencia"""
    for widget in frame_detalles.winfo_children():
        widget.destroy()
    texto = ", ".join(secuencia[:100])
    text_widget = tk.Text(frame_detalles, height=5, width=50)
    text_widget.pack()
    text_widget.insert(tk.END, texto)
    text_widget.config(state=tk.DISABLED)

# =========================
# Función principal multinomial
# =========================
def generar_multinomial(
    entrada_n, entradas_probs, entrada_rep,
    frame_resultados, frame_grafica, frame_detalles
):
    """Función principal que se llama desde la ventana Tkinter"""
    try:
        n = int(entrada_n.get())
        if n <= 0:
            messagebox.showerror("Error", "La muestra (n) debe ser positiva.")
            return

        R = int(entrada_rep.get())
        if R <= 0:
            messagebox.showerror("Error", "Número de repeticiones debe ser positivo.")
            return

        probs = []
        for e in entradas_probs:
            val = e.get().strip()
            if val == "":
                messagebox.showerror("Error", "Todas las probabilidades deben llenarse.")
                return
            probs.append(_parse_probabilidad_texto(val))

        if any(p < 0 for p in probs):
            messagebox.showerror("Error", "No puede haber probabilidades negativas.")
            return
        if abs(sum(probs) - 1.0) > 1e-6:
            messagebox.showerror("Error", "Las probabilidades deben sumar 1")
            return

        # -----------------------------
        # Generar todos los vectores
        # -----------------------------
        lista_vectores = []
        ultima_secuencia = []

        for _ in range(R):
            conteos, sec = _simular_una_multinomial(n, probs)
            lista_vectores.append(conteos)
            ultima_secuencia = sec

        etiquetas = [f"{i+1}" for i in range(len(probs))]

        # Limpiar resultados previos
        for w in frame_resultados.winfo_children():
            w.destroy()

        # Mostrar todos los vectores generados
        tk.Label(frame_resultados, text="Vectores generados:").pack(anchor="w")
        for idx, vec in enumerate(lista_vectores):
            tk.Label(frame_resultados, text=f"{idx+1}: {vec}").pack(anchor="w")

        # Combobox para elegir cuál graficar
        combo = Combobox(frame_resultados, values=[str(i+1) for i in range(len(lista_vectores))], state="readonly")
        combo.current(0)
        combo.pack(pady=2)

        def graficar_seleccionado():
            idx = int(combo.get()) - 1
            for w in frame_grafica.winfo_children():
                w.destroy()
            _graficar_barras(lista_vectores[idx], etiquetas, frame_grafica, f"Vector {idx+1}")

        tk.Button(frame_resultados, text="Graficar vector seleccionado",
                  command=graficar_seleccionado).pack(pady=5)

        # Botón para ver detalles
        if frame_detalles:
            for w in frame_detalles.winfo_children():
                w.destroy()
            tk.Button(
                frame_detalles,
                text="Ver detalles (100 primeros)",
                command=lambda: _mostrar_detalles(ultima_secuencia, frame_detalles)
            ).pack()

    except ValueError:
        messagebox.showerror("Error", "Ingresa valores numéricos válidos")
