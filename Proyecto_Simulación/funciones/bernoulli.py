import tkinter as tk
import random
import tkinter.messagebox as messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

#genera n numeros aleatorios y cuenta cuantos caen en cada rango
def simular_muestra(n,p):
    num_Exitos, num_Fracasos = 0, 0
    for _ in range(n):
        r = random.random()
        if r <= p:
            num_Exitos += 1
        else:
            num_Fracasos += 1
    return num_Exitos, num_Fracasos

def graficar_Bernulli(num_Exitos, num_Fracasos, frame):
    fig, ax = plt.subplots(figsize=(4,3))
    barras = ax.bar(["CARAS", "CRUCES"], [num_Exitos, num_Fracasos], color=["skyblue", "red"])
    ax.set_ylabel("Frecuencia")
    ax.set_title("Histograma de Resultados")

    for barra in barras: #etiquetas encima de las barras
        altura = barra.get_height() #obtiene la altura
        ax.text(barra.get_x() + barra.get_width()/2, altura+0.1, str(altura), ha='center', va='bottom', fontsize=10)

    for widget in frame.winfo_children(): #Limpia el frame
        widget.destroy()
    
    #insertar la gráfica
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    plt.close(fig) #liberar memoria

def generar_Bernoulli(entrada_n, deslizador_p, frame_grafica):
    try:
        n = int(entrada_n.get())
        p = deslizador_p.get()

        num_Exitos, num_Fracasos = simular_muestra(n, p)

        graficar_Bernulli(num_Exitos, num_Fracasos, frame_grafica)

    except ValueError:
        messagebox.showerror("Error", "Ingresa un número válido")