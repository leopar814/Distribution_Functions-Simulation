import tkinter as tk
import tkinter.messagebox as messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from functions.bernoulli import generar_Bernoulli
from functions.binomial import generar_Binomial
from functions.exponential import generar_exponencial
from functions.multinomial import generar_multinomial

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

    tk.Label(nueva, text="Distribución Binomial", bg="#CAE6F1", fg="black", font=("Arial", 16)).pack(pady=20)

    frame_botones = tk.Frame(nueva, bg="#CAE6F1")
    frame_botones.pack(side="bottom", fill="x", pady=10, padx=10)

    btn_regresar = tk.Button(frame_botones, text="Regresar", font=("Arial", 12), bg="#DEB6B6", fg="black", width=12, command=nueva.destroy)
    btn_regresar.pack(side="left", anchor="w")
    
    btn_info = tk.Button(frame_botones, text="Info", font=("Arial", 12), bg="gray", fg="black", width=12, command=lambda: messagebox.showinfo("Info", "Aquí va la información de Bernoulli"))
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
    boton = tk.Button(nueva, text="Generar", bg="#B6DEBF", command = lambda: generar_Binomial(entrada_n, entrada_k, deslizador_p, frame_grafica, frame_detalles))
    boton.pack(pady=10)

def abrir_multinomial():
    nueva = tk.Toplevel(ventana)
    nueva.title("Distribución Multinomial")
    nueva.geometry("900x900")
    nueva.configure(bg="#CADECD")

    tk.Label(nueva, text="Distribución Multinomial", bg="#CADECD", fg="black", font=("Arial", 16)).pack(pady=20)

    frame_botones = tk.Frame(nueva, bg="#CADECD")
    frame_botones.pack(side="bottom", fill="x", pady=10, padx=10)
    tk.Button(frame_botones, text="Regresar", width=12, command=nueva.destroy).pack(side="left", anchor="w")
    tk.Button(frame_botones, text="Info", width=12, command=lambda: messagebox.showinfo("Info", "La multinomial modela n ensayos con k categorías con probabilidades que suman 1.")).pack(side="right", anchor="e")

    # Checkbutton Dado equilibrado
    dado_eq_var = tk.IntVar(value=0)
    def toggle_dado_eq():
        if dado_eq_var.get() == 1:
            for entry in entradas_probs:
                entry.delete(0, tk.END)
                entry.insert(0, "1/6")
        else:
            for entry in entradas_probs:
                entry.delete(0, tk.END)
    tk.Checkbutton(nueva, text="Dado equilibrado", variable=dado_eq_var,
                   command=toggle_dado_eq, bg="#CADECD").pack(pady=5)

    # Probabilidades cara por cara
    frame_probs = tk.Frame(nueva, bg="#CADECD")
    frame_probs.pack(pady=10)
    entradas_probs = []
    for i in range(6):
        subframe = tk.Frame(frame_probs, bg="#CADECD")
        subframe.pack(anchor="w")
        tk.Label(subframe, text=f"Cara {i+1}:", bg="#CADECD").pack(side="left")
        entry = tk.Entry(subframe, width=6)
        entry.pack(side="left", padx=5)
        entradas_probs.append(entry)

    # Tamaño muestra n
    tk.Label(nueva, text="Tamaño de la muestra (n):").pack(pady=(10,5))
    entrada_n = tk.Entry(nueva, width=10)
    entrada_n.insert(0, "50")
    entrada_n.pack(pady=2)

    # Número de repeticiones R
    tk.Label(nueva, text="Número de repeticiones (R):").pack(pady=(10,5))
    entrada_rep = tk.Entry(nueva, width=10)
    entrada_rep.insert(0, "1")
    entrada_rep.pack(pady=2)

    # Frames para resultados y gráfica
    container = tk.Frame(nueva, bg="#CADECD")
    container.pack(pady=10, fill="both", expand=True)

    frame_resultados = tk.Frame(container, bg="#CADECD")
    frame_resultados.pack(side="left", padx=20, fill="y")

    frame_grafica = tk.Frame(container, bg="#CADECD")
    frame_grafica.pack(side="right", padx=20, fill="both", expand=True)

    frame_detalles = tk.Frame(container, bg="#CADECD")
    frame_detalles.pack(side="bottom", pady=5, fill="x")

    tk.Button(nueva, text="Generar",command=lambda: generar_multinomial(entrada_n, entradas_probs, entrada_rep, frame_grafica, frame_resultados, frame_detalles)).pack(pady=10)

def abrir_exponencial():
    nueva = tk.Toplevel(ventana)
    nueva.title("Distribución Bernoulli")
    nueva.geometry("800x900")
    nueva.configure(bg="#CACDE6")

    tk.Label(nueva, text="Distribución Exponencial", bg="#E6D5CA", fg="black", font=("Arial", 16)).pack(pady=20)

    frame_botones = tk.Frame(nueva, bg="#CACDE6")
    frame_botones.pack(side="bottom", fill="x", pady=10, padx=10)

    btn_regresar = tk.Button(frame_botones, text="Regresar", font=("Arial", 12), bg="lightgray", fg="black", width=12, command=nueva.destroy)
    btn_regresar.pack(side="left", anchor="w")
    
    btn_info = tk.Button(frame_botones, text="Info", font=("Arial", 12), bg="lightgray", fg="black", width=12, command=lambda: messagebox.showinfo("Info", "Aquí va la información de Bernoulli"))
    btn_info.pack(side="right", anchor="e")

    tk.Label(nueva, text="Tamaño de la muestra(n):").pack(pady=(5))
    entrada_n = tk.Entry(nueva)
    entrada_n.pack()

    tk.Label(nueva, text="Valor de λ (lambda):").pack(pady=(5))
    entrada_lambda = tk.Entry(nueva)
    entrada_lambda.pack(pady=(5))

    frame_grafica = tk.Frame(nueva)
    frame_grafica.pack(pady=(10))

    # Frame para los detalles(secuencia)
    frame_detalles = tk.Frame(nueva)
    frame_detalles.pack(pady=5)

    tk.Button(nueva, text="Generar", command=lambda: generar_exponencial(entrada_n, entrada_lambda, frame_grafica, frame_detalles)).pack()





# Ventana principal
ventana = tk.Tk()
ventana.title("Simulación de distribuciones")
ventana.geometry("800x600")
ventana.configure(bg="#B9D0CD")


tk.Label(ventana, text="Elige una opción: ", bg="#B9D0CD", font=("Arial", 12)).pack(pady=20)

# Botones
tk.Button(ventana, text="Bernoulli", width=20, command=abrir_bernoulli).pack(pady=10)
tk.Button(ventana, text="Binomial", width=20, command=abrir_binomial).pack(pady=10)
tk.Button(ventana, text="Multinomial", width=20, command=abrir_multinomial).pack(pady=10)
tk.Button(ventana, text="Exponencial", width=20, command=abrir_exponencial).pack(pady=10)


ventana.mainloop()

