# normal.py
import tkinter as tk
import random, math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import messagebox

def box_muller(n, mu=0, sigma=1):
    """Genera n valores normales usando Box-Muller"""
    datos = []
    for _ in range(n // 2 + 1):
        u1, u2 = random.random(), random.random()
        z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
        datos.append(mu + sigma * z1)
        if len(datos) < n:
            datos.append(mu + sigma * z2)
    return datos

def generar_normal(entrada_n, entrada_mu, entrada_sigma, frame_grafica, frame_detalles):
    try:
        n = int(entrada_n.get())
        mu = float(entrada_mu.get())
        sigma = float(entrada_sigma.get())
        if n <= 0 or sigma <= 0:
            raise ValueError("Parámetros inválidos")

        # Generar muestra
        muestra = box_muller(n, mu, sigma)

        # Graficar histograma + curva teórica
        fig, ax = plt.subplots(figsize=(5,4))
        ax.hist(muestra, bins=20, density=True, color="skyblue", alpha=0.7, edgecolor="black")
        x = np.linspace(min(muestra), max(muestra), 200)
        f_x = (1/(sigma * np.sqrt(2*np.pi))) * np.exp(-((x-mu)**2)/(2*sigma**2))
        ax.plot(x, f_x, "r", linewidth=2, label="Densidad teórica")
        ax.set_title("Distribución Normal")
        ax.set_xlabel("Valor")
        ax.set_ylabel("Densidad")
        ax.legend()

        for widget in frame_grafica.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

        # Mostrar detalles
        for widget in frame_detalles.winfo_children():
            widget.destroy()
        tk.Label(frame_detalles, text=f"Media simulada: {np.mean(muestra):.4f}", font=("Helvetica",12)).pack(pady=5)
        tk.Label(frame_detalles, text=f"Desviación simulada: {np.std(muestra):.4f}", font=("Helvetica",12)).pack(pady=5)

    except ValueError:
        messagebox.showerror("Error", "Ingresa valores válidos para n, μ y σ")
