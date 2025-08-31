import tkinter as tk
import random
import tkinter.messagebox as messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

#genera n numeros aleatorios y cuenta cuantos caen en cada rango
def simular_muestra(n,p):
    secuencia = []
    num_Exitos, num_Fracasos = 0, 0
    for _ in range(n):
        r = random.random()
        if r <= p:
            secuencia.append("E")  # Éxito
            num_Exitos += 1
        else:
            secuencia.append("F")  # Fracaso
            num_Fracasos += 1
    return num_Exitos, num_Fracasos, secuencia

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

# Función para mostrar la secuencia de éxitos y fracasos
def mostrar_detalles(secuencia, frame_detalles):
    # Limitar a 100 elementos
    secuencia_a_mostrar = secuencia[:100]
    texto = ", ".join(secuencia_a_mostrar)
    
    for widget in frame_detalles.winfo_children():
        widget.destroy()
    
    text_widget = tk.Text(frame_detalles, height=5, width=80)
    text_widget.pack()
    text_widget.insert(tk.END, texto)
    text_widget.config(state=tk.DISABLED)

def generar_Bernoulli(entrada_n, deslizador_p, frame_grafica, frame_detalles):
    try:
        n = int(entrada_n.get())
        p = deslizador_p.get()

        num_Exitos, num_Fracasos, secuencia = simular_muestra(n, p)

        graficar_Bernulli(num_Exitos, num_Fracasos, frame_grafica)

        # Botón para ver detalles
        for widget in frame_detalles.winfo_children():
            widget.destroy()
        
        boton_detalles = tk.Button(frame_detalles, text="¿Desea ver detalles?", command=lambda: mostrar_detalles(secuencia, frame_detalles))
        boton_detalles.pack()

    except ValueError:
        messagebox.showerror("Error", "Ingresa un número válido")