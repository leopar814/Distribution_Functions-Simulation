import tkinter as tk
from tkinter import messagebox
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def _parse_probabilidad_texto(texto):
    """Convierte 1/6 o 0.16 a float"""
    texto = texto.strip()
    if "/" in texto:
        num, den = texto.split("/")
        return float(num) / float(den)
    else:
        return float(texto)


def _simular_una_multinomial(n, probs):
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
    fig, ax = plt.subplots(figsize=(4, 3))
    barras = ax.bar(etiquetas, valores)
    ax.set_ylabel("Frecuencia")
    ax.set_title(titulo)

    # Números sobre las barras (si quieres quitar, comenta este bloque)
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
    for widget in frame_detalles.winfo_children():
        widget.destroy()
    texto = ", ".join(secuencia[:100])
    text_widget = tk.Text(frame_detalles, height=5, width=50)
    text_widget.pack()
    text_widget.insert(tk.END, texto)
    text_widget.config(state=tk.DISABLED)


def generar_multinomial(
    entrada_n, entradas_probs, entrada_rep,
    frame_grafica, frame_resultados, frame_detalles
):
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

        lista_conteos = []
        ultima_secuencia = []
        for _ in range(R):
            conteos, sec = _simular_una_multinomial(n, probs)
            lista_conteos.append(conteos)
            ultima_secuencia = sec

        etiquetas = [f"{i+1}" for i in range(len(probs))]

        # Limpiar resultados previos
        for w in frame_resultados.winfo_children():
            w.destroy()

        if R == 1:
            for i, c in enumerate(lista_conteos[0]):
                tk.Label(frame_resultados, text=f"{c}").pack(anchor="w")
            _graficar_barras(lista_conteos[0], etiquetas, frame_grafica, "Multinomial")
        else:
            proms = [sum(lista_conteos[r][i] for r in range(R)) / R for i in range(len(probs))]
            tk.Label(frame_resultados, text=f"Promedio en {R} repeticiones:").pack(anchor="w")
            for v in proms:
                tk.Label(frame_resultados, text=f"{round(v, 2)}").pack(anchor="w")
            tk.Label(frame_resultados, text="Última repetición:").pack(anchor="w", pady=(8, 0))
            for c in lista_conteos[-1]:
                tk.Label(frame_resultados, text=f"{c}").pack(anchor="w")
            _graficar_barras(proms, etiquetas, frame_grafica, f"Promedio de {R} repeticiones")

        # Mostrar detalles
        for w in frame_detalles.winfo_children():
            w.destroy()
        tk.Button(
            frame_detalles,
            text="Ver detalles (100 primeros)",
            command=lambda: _mostrar_detalles(ultima_secuencia, frame_detalles)
        ).pack()

    except ValueError:
        messagebox.showerror("Error", "Ingresa valores numéricos válidos")