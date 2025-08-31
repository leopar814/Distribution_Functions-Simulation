import tkinter as tk
import tkinter.messagebox as messagebox

from collections import Counter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from functions.bernoulli import simular_muestra, mostrar_detalles

def simular_binomial(n, k, p):
    resultados = []  # Lista con el número de éxitos de cada repetición
    for _ in range(n):  
        num_Exitos, _, _ = simular_muestra(k, p)  # Reutilizamos Bernoulli k veces
        resultados.append(num_Exitos)  # Guardamos los éxitos de esta repetición
    return resultados

def graficar_binomial(resultados, k, frame):
    conteo = Counter(resultados) #cuenta cuántas veces salió cada número de éxito

    #ordenamos los posibles resultados (0...k)
    valores = list(range(k+1))
    frecuencias = [conteo.get(v,0) for v in valores]

    fig, ax = plt.subplots(figsize=(5,4))
    barras = ax.bar(valores, frecuencias, color="skyblue")
    ax.set_xlabel("Númeor de éxitos")
    ax.set_ylabel("Frecuencia")
    ax.set_title("Histograma de Resultados")

    for barra in barras:
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2, altura+0.1, str(altura),ha='center', va='bottom', fontsize=9)

    for widget in frame.winfo_children():
        widget.destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    plt.close(fig)


def generar_Binomial(entrada_n, entrada_k, deslizador_p, frame_grafica, frame_detalles):
    try:
        n = int(entrada_n.get())
        k = int(entrada_k.get())
        p = deslizador_p.get()

        resultados = simular_binomial(n, k, p)

        graficar_binomial(resultados, k, frame_grafica)

        for widget in frame_detalles.winfo_children():
            widget.destroy()
        boton_detalles = tk.Button(frame_detalles, text="¿Desea ver detalles?", command=lambda: mostrar_detalles(list(map(str, resultados)), frame_detalles))
        boton_detalles.pack()

    except ValueError:
        messagebox.showerror("Error", "Ingresa valores válidos")
