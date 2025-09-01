import tkinter as tk
import random
import tkinter.messagebox as messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math

def simular_exponencial(n, lambda_):
    muestras = []
    for _ in range(n):
        u = random.random()
        x = -math.log(1 - u) / lambda_
        muestras.append(x)
    return muestras

def graficar_exponencial(muestras, frame):
    fig, ax = plt.subplots(figsize=(6,4))
    ax.hist(muestras, bins='auto', density=True, color="skyblue", edgecolor="black")
    ax.set_ylabel("Densidad")
    ax.set_xlabel("x")
    ax.set_title("Histograma de Resultados")

    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    plt.close(fig)

def mostrar_detalles_exponencial(muestras, frame_detalles):
    # Limitar a 50 elementos
    muestras_a_mostrar = [f"{x:.2f}" for x in muestras[:50]]
    texto = ", ".join(muestras_a_mostrar)

    for widget in frame_detalles.winfo_children():
        widget.destroy()

    text_widget = tk.Text(frame_detalles, height=5, width=80)
    text_widget.pack()
    text_widget.insert(tk.END, texto)
    text_widget.config(state=tk.DISABLED)

def generar_exponencial(entrada_n, entrada_lambda, frame_grafica, frame_detalles):
    try:
        n = int(entrada_n.get())
        lambda_ = float(entrada_lambda.get())

        if lambda_ <= 0:
            messagebox.showerror("Error", "λ debe mayor que 0")
            return
        
        muestras = simular_exponencial(n, lambda_)
        graficar_exponencial(muestras, frame_grafica)

        for widget in frame_detalles.winfo_children():
            widget.destroy()

        boton_detalles = tk.Button(frame_detalles, text="¿Desea ver detalles?", command=lambda: mostrar_detalles_exponencial(muestras, frame_detalles))
        boton_detalles.pack()


    except ValueError:
        messagebox.showerror("Error", "Ingresa valores válidos")