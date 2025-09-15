import sympy as sp
import random

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk



x, y, t = sp.symbols('x y t')

def X (f, xmin, xmax, y_val):
    fy = sp.integrate(f, (x, xmin, xmax))
    fxy = (f / fy).subs(y, y_val) #f(x|y)
    Fxy = sp.integrate(fxy.subs(x, t), (t, xmin, x))
    u = random.random()
    sol = sp.solve(Fxy - u, x)
    sol_real = [s for s in sol if s.is_real and xmin <= s <= xmax]
    return float(sol_real[0]) if sol_real else None


def Y (f, ymin, ymax,x_val):
    fx = sp.integrate(f, (y, ymin, ymax))
    fyx = (f / fx).subs(x, x_val) #f(y|x)
    Fyx = sp.integrate(fyx.subs(y, t), (t, ymin, y))
    v = random.random()
    sol = sp.solve(Fyx - v, y)
    sol_real = [s for s in sol if s.is_real and ymin <= s <= ymax]
    return float(sol_real[0]) if sol_real else None


def graficar_Gibbs(muestras, frame):
    """
    Grafica los puntos generados por Gibbs en un scatter plot dentro de un frame de Tkinter.
    """
    # Separar valores X e Y
    xs = [p[0] for p in muestras]
    ys = [p[1] for p in muestras]

    # Crear figura
    fig, ax = plt.subplots(figsize=(4,3))
    ax.scatter(xs, ys, color="red", edgecolors="black", alpha=0.5)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Muestreo por Gibbs")

    # Etiquetar primer y último punto
    if muestras:
        ax.annotate("Inicio", (xs[0], ys[0]), textcoords="offset points", xytext=(5,5), fontsize=8)
        ax.annotate("Fin", (xs[-1], ys[-1]), textcoords="offset points", xytext=(5,5), fontsize=8)

    # Limpiar frame anterior
    for widget in frame.winfo_children():
        widget.destroy()

    # Insertar la gráfica en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    plt.close(fig)  # liberar memoria

def mostrar_puntos(muestras, frame_detalles):
    # Limpiar frame
    for widget in frame_detalles.winfo_children():
        widget.destroy()

    # Crear canvas y scrollbar
    canvas = tk.Canvas(frame_detalles)
    scrollbar = tk.Scrollbar(frame_detalles, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Insertar cada punto en scrollable_frame
    for i, (x_val, y_val) in enumerate(muestras, start=1):
        texto = f"Punto {i}: X={x_val:.4f}, Y={y_val:.4f}"
        label = tk.Label(scrollable_frame, text=texto, anchor="w", justify="left", font=("Arial", 9))
        label.pack(fill="x", padx=5, pady=1)


def generar_gebbs(inFuncion, inXmin, inXmax, inYmin, inYmax, inN, frame_grafica, frame_detalles): 
    funcion_texto = inFuncion.get()
    xmin = float(inXmin.get())
    xmax = float(inXmax.get())
    ymin = float(inYmin.get())
    ymax = float(inYmax.get())
    N = int(inN.get())

    f = sp.sympify(funcion_texto)

    muestras = []

    #Punto inicial
    xn = random.uniform(0, 10)
    yn = random.uniform(0, 10)
    
    muestras.append((xn, yn))

    for _ in range(N-1):
        xn = X(f, xmin, xmax, yn)
        yn = Y(f, ymin, ymax, xn)
        muestras.append((xn, yn))

    graficar_Gibbs(muestras, frame_grafica) 
    mostrar_puntos(muestras, frame_detalles)



    


