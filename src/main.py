import tkinter as tk
import tkinter.messagebox as messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from functions.bernoulli import generar_Bernoulli
from functions.binomial import generar_Binomial

def abrir_bernoulli():
    nueva = tk.Toplevel(ventana)
    nueva.title("Distribución Bernoulli")
    nueva.geometry("800x800")
    nueva.configure(bg="lightblue")

    tk.Label(nueva, text="Distribución Bernoulli", bg="lightblue", fg="black", font=("Arial", 16)).pack(pady=20)

    frame_botones = tk.Frame(nueva, bg="lightblue")
    frame_botones.pack(side="bottom", fill="x", pady=10, padx=10)

    btn_regresar = tk.Button(frame_botones, text="Regresar", font=("Arial", 12), bg="lightgray", fg="black", width=12, command=nueva.destroy)
    btn_regresar.pack(side="left", anchor="w")
    
    btn_info = tk.Button(frame_botones, text="Info", font=("Arial", 12), bg="lightgray", fg="black", width=12, command=lambda: messagebox.showinfo("Info", "Aquí va la información de Bernoulli"))
    btn_info.pack(side="right", anchor="e")

    # Etiqueta para el deslizador
    etiqueta_p = tk.Label(nueva, text="Probabilidad de Éxito:")
    etiqueta_p.pack(pady=5)

    deslizador_p = tk.Scale(nueva, from_=0, to=1, resolution=0.01, orient="horizontal", length=300)
    deslizador_p.pack(pady=5)

    # Etiqueta para la muestra
    etiqueta_n = tk.Label(nueva, text="Tamaño de la muestra (n):")
    etiqueta_n.pack(pady=5)

    # Cuadro de texto para ingresar el tamaño de la muestra
    entrada_n = tk.Entry(nueva)
    entrada_n.pack(pady=5)

    # Frame para la gráfica
    frame_grafica = tk.Frame(nueva)
    frame_grafica.pack(pady=10)

    # Frame para los detalles(secuencia)
    frame_detalles = tk.Frame(nueva)
    frame_detalles.pack(pady=5)

    # Botón para ejecutar
    boton = tk.Button(nueva, text="Generar", command = lambda: generar_Bernoulli(entrada_n, deslizador_p, frame_grafica, frame_detalles))
    boton.pack(pady=10)


def abrir_binomial():
    nueva = tk.Toplevel(ventana)
    nueva.title("Distribución Bernoulli")
    nueva.geometry("800x900")
    nueva.configure(bg="#CAE6F1")

    tk.Label(nueva, text="Distribución Binomial", bg="#F1E9CA", fg="black", font=("Arial", 16)).pack(pady=20)

    frame_botones = tk.Frame(nueva, bg="lightblue")
    frame_botones.pack(side="bottom", fill="x", pady=10, padx=10)

    btn_regresar = tk.Button(frame_botones, text="Regresar", font=("Arial", 12), bg="lightgray", fg="black", width=12, command=nueva.destroy)
    btn_regresar.pack(side="left", anchor="w")
    
    btn_info = tk.Button(frame_botones, text="Info", font=("Arial", 12), bg="lightgray", fg="black", width=12, command=lambda: messagebox.showinfo("Info", "Aquí va la información de Bernoulli"))
    btn_info.pack(side="right", anchor="e")

    # Etiqueta para el deslizador
    etiqueta_p = tk.Label(nueva, text="Probabilidad de Éxito:")
    etiqueta_p.pack(pady=5)

    deslizador_p = tk.Scale(nueva, from_=0, to=1, resolution=0.01, orient="horizontal", length=300)
    deslizador_p.pack(pady=5)

    etiqueta_k = tk.Label(nueva, text="Número de Repeticiones(k):")
    etiqueta_k.pack(pady=5)

    # Cuadro de texto para ingresar el tamaño de la muestra
    entrada_k = tk.Entry(nueva)
    entrada_k.pack(pady=5)

    etiqueta_n = tk.Label(nueva, text="Tamaño de la muestra(n):")
    etiqueta_n.pack(pady=5)

    # Cuadro de texto para ingresar el tamaño de la muestra
    entrada_n = tk.Entry(nueva)
    entrada_n.pack(pady=5)

    # Frame para la gráfica
    frame_grafica = tk.Frame(nueva)
    frame_grafica.pack(pady=10)

    # Frame para los detalles(secuencia)
    frame_detalles = tk.Frame(nueva)
    frame_detalles.pack(pady=5)

    # Botón para ejecutar
    boton = tk.Button(nueva, text="Generar", command = lambda: generar_Binomial(entrada_n, entrada_k, deslizador_p, frame_grafica, frame_detalles))
    boton.pack(pady=10)


# Ventana principal
ventana = tk.Tk()
ventana.title("Simulación de distribuciones")
ventana.geometry("800x600")
ventana.configure(bg="#CDCDCD")


tk.Label(ventana, text="Elige una distribución:", font=("Arial", 14)).pack(pady=20)

# Botones
tk.Button(ventana, text="Bernoulli", width=20, command=abrir_bernoulli).pack(pady=5)
tk.Button(ventana, text="Binomial", width=20, command=abrir_binomial).pack(pady=5)


ventana.mainloop()

