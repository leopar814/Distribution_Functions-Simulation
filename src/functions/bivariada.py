import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Estilos
FONT_TITULO = ("Helvetica", 16, "bold")
FONT_LABEL = ("Helvetica", 12)
FONT_BOTON = ("Helvetica", 12)

COLOR_FONDO = "#E6F0FA"
COLOR_FRAME = "#CFE2F3"
COLOR_BOTON = "#5DADE2"
COLOR_BOTON_HOVER = "#3498DB"
COLOR_TEXTO = "#1B2631"

def on_enter(e):
    e.widget['bg'] = COLOR_BOTON_HOVER

def on_leave(e):
    e.widget['bg'] = COLOR_BOTON

# Función auxiliar: normal bivariada
def pdf_bivariada(x, y, mu, cov_matrix):
    det = np.linalg.det(cov_matrix)
    inv = np.linalg.inv(cov_matrix)
    norm_const = 1 / (2 * np.pi * np.sqrt(det))
    diff = np.stack([x - mu[0], y - mu[1]], axis=-1)
    return norm_const * np.exp(-0.5 * np.einsum('...i,ij,...j', diff, inv, diff))

# Función: Normal Bivariada comparativa
def generar_normal_bivariada_3d(entrada_n, entrada_mx, entrada_my,
                                entrada_varx, entrada_vary, entrada_rho,
                                frame_grafica, frame_detalles):
    try:
        n = int(entrada_n.get())
        mx = float(entrada_mx.get())
        my = float(entrada_my.get())
        varx = float(entrada_varx.get())
        vary = float(entrada_vary.get())
        rho = float(entrada_rho.get())

        if n <= 0 or varx <= 0 or vary <= 0 or not (-1 <= rho <= 1):
            raise ValueError("Parámetros inválidos")

        # Matriz de covarianza
        cov = rho * np.sqrt(varx * vary)
        cov_matrix = [[varx, cov],
                      [cov, vary]]

        # Generar muestra
        datos = np.random.multivariate_normal([mx, my], cov_matrix, n)
        x, y = datos[:,0], datos[:,1]

        # Preparar figura
        for w in frame_grafica.winfo_children():
            w.destroy()
        fig = plt.Figure(figsize=(12,5))

        ax1 = fig.add_subplot(1,2,1, projection='3d')
        X, Y = np.meshgrid(np.linspace(min(x), max(x), 60),
                           np.linspace(min(y), max(y), 60))
        Z = pdf_bivariada(X, Y, [mx,my], cov_matrix)
        ax1.plot_surface(X, Y, Z, cmap="viridis", alpha=0.9)
        ax1.set_title("PDF Teórica")
        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        ax1.set_zlabel("Densidad")
        ax1.view_init(30, -60)

        ax2 = fig.add_subplot(1,2,2)
        ax2.scatter(x, y, alpha=0.5, s=15, color="skyblue", edgecolor="k")
        ax2.set_title("Muestras simuladas")
        ax2.set_xlabel("X")
        ax2.set_ylabel("Y")
        ax2.set_aspect("equal", "box")

        # Mostrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Mostrar resultados
        for widget in frame_detalles.winfo_children():
            widget.destroy()
        tk.Label(frame_detalles, text=f"Media simulada X: {np.mean(x):.4f}", font=FONT_LABEL).pack(pady=2)
        tk.Label(frame_detalles, text=f"Media simulada Y: {np.mean(y):.4f}", font=FONT_LABEL).pack(pady=2)
        tk.Label(frame_detalles, text=f"Varianza simulada X: {np.var(x):.4f}", font=FONT_LABEL).pack(pady=2)
        tk.Label(frame_detalles, text=f"Varianza simulada Y: {np.var(y):.4f}", font=FONT_LABEL).pack(pady=2)
        tk.Label(frame_detalles, text=f"Correlación simulada: {np.corrcoef(x,y)[0,1]:.4f}", font=FONT_LABEL).pack(pady=2)

    except ValueError:
        messagebox.showerror("Error", "Ingresa valores válidos (n>0, varianzas>0, -1≤ρ≤1)")

# Ventana: Normal Bivariada
def abrir_normal_bivariada_3d():
    nueva = tk.Toplevel(ventana)
    nueva.title("Distribución Normal Bivariada")
    nueva.geometry("1100x700")
    nueva.configure(bg=COLOR_FONDO)

    tk.Label(nueva, text="Distribución Normal Bivariada", bg=COLOR_FONDO,
             fg=COLOR_TEXTO, font=FONT_TITULO).pack(pady=20)

    frame_params = tk.LabelFrame(nueva, text=" Parámetros ",
                                 bg=COLOR_FRAME, fg=COLOR_TEXTO,
                                 font=FONT_LABEL, padx=15, pady=15)
    frame_params.pack(pady=10, padx=20, fill="x")

    etiquetas = ["Media X (μx):", "Media Y (μy):", 
                 "Varianza X:", "Varianza Y:", "Correlación (ρ):", "Tamaño muestra (n):"]
    entradas = []
    for i, texto in enumerate(etiquetas):
        tk.Label(frame_params, text=texto, bg=COLOR_FRAME, fg=COLOR_TEXTO, font=FONT_LABEL).grid(row=i, column=0, sticky="w", pady=5)
        entrada = tk.Entry(frame_params, font=FONT_LABEL, justify="center", width=10)
        entrada.grid(row=i, column=1, padx=10, pady=5)
        entradas.append(entrada)

    # Valores por defecto
    entradas[0].insert(0, "0")
    entradas[1].insert(0, "0")
    entradas[2].insert(0, "1")
    entradas[3].insert(0, "1")
    entradas[4].insert(0, "0")
    entradas[5].insert(0, "500")

    # Frames de gráfico y detalles
    frame_resultados = tk.Frame(nueva, bg=COLOR_FONDO)
    frame_resultados.pack(padx=20, pady=15, fill="both", expand=True)

    frame_grafica = tk.LabelFrame(frame_resultados, text=" Gráficas ",
                                  bg=COLOR_FRAME, fg=COLOR_TEXTO, font=FONT_LABEL)
    frame_grafica.pack(fill="both", expand=True, padx=10, side="left")

    frame_detalles = tk.LabelFrame(frame_resultados, text=" Resultados ",
                                   bg=COLOR_FRAME, fg=COLOR_TEXTO, font=FONT_LABEL)
    frame_detalles.pack(fill="both", expand=True, padx=10, side="right")

    boton = tk.Button(nueva, text="Generar", font=FONT_BOTON,
                      bg=COLOR_BOTON, fg="white",
                      command=lambda: generar_normal_bivariada_3d(
                          entradas[5], entradas[0], entradas[1],
                          entradas[2], entradas[3], entradas[4],
                          frame_grafica, frame_detalles))
    boton.pack(pady=15)
    boton.bind("<Enter>", on_enter)
    boton.bind("<Leave>", on_leave)

# Ventana principal
ventana = tk.Tk()
ventana.title("Simulación de distribuciones")
ventana.geometry("800x600")
ventana.configure(bg=COLOR_FONDO)

tk.Label(ventana, text="Elige una distribución:", font=FONT_TITULO,
         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=20)

frame_menu = tk.Frame(ventana, bg=COLOR_FONDO)
frame_menu.pack(pady=20)

# Botón Normal Bivariada
btn = tk.Button(frame_menu, text="Normal Bivariada", font=FONT_BOTON,
                bg=COLOR_BOTON, fg="white", width=35,
                command=abrir_normal_bivariada_3d)
btn.pack(pady=8)
btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)

ventana.mainloop()
