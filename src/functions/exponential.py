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
    fig, ax = plt.subplots(figsize=(4,4))
    ax.hist(muestras, bins=15, density=True, color="skyblue", edgecolor="black")
    ax.set_ylabel("Densidad")
    ax.set_xlabel("x")
    ax.set_title("Histograma de Resultados")

    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    plt.close(fig)

def generar_exponencial(entrada_n, entrada_lambda, frame_grafica):
    try:
        n = int(entrada_n.get())
        lambda_ = float(entrada_lambda.get())

        if lambda_ <= 0:
            messagebox.showerror("Error", "λ debe mayor que 0")
            return
        
        muestras = simular_exponencial(n, lambda_)
        graficar_exponencial(muestras, frame_grafica)

    except ValueError:
        messagebox.showerror("Error", "Ingresa valores válidos")