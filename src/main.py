import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter.ttk import Combobox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# ========================
#  Estilos globales
# ========================
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

# ========================
#  Funciones Auxiliares
# ========================
def _graficar_barras(valores, etiquetas, frame, titulo="Gráfico"):
    """Dibuja un gráfico de barras en el frame especificado."""
    for w in frame.winfo_children():
        w.destroy()
    fig, ax = plt.subplots(figsize=(4,3))
    ax.bar(etiquetas, valores, color='skyblue')
    ax.set_title(titulo)
    ax.set_ylabel("Frecuencia")
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def _simular_una_multinomial(n, probs):
    """Genera un vector multinomial."""
    conteos = np.random.multinomial(n, probs)
    return conteos, probs

def _parse_probabilidad_texto(texto):
    try:
        return float(eval(texto))
    except:
        return 0.0

# ========================
#  Funciones de distribución
# ========================
def generar_Bernoulli(entrada_n, deslizador_p, frame_grafica, frame_detalles):
    try:
        n = int(entrada_n.get())
        p = deslizador_p.get()
    except ValueError:
        messagebox.showerror("Error", "Introduce valores numéricos válidos")
        return
    datos = np.random.binomial(1, p, n)
    frec = [np.sum(datos==0), np.sum(datos==1)]
    _graficar_barras(frec, ["0","1"], frame_grafica, "Distribución Bernoulli")
    for w in frame_detalles.winfo_children():
        w.destroy()
    tk.Label(frame_detalles, text=f"Frecuencia de 0: {frec[0]}\nFrecuencia de 1: {frec[1]}").pack(anchor="w")

def generar_Binomial(entrada_n, entrada_k, deslizador_p, frame_grafica, frame_detalles):
    try:
        n = int(entrada_n.get())
        k = int(entrada_k.get())
        p = deslizador_p.get()
    except ValueError:
        messagebox.showerror("Error", "Introduce valores numéricos válidos")
        return
    datos = np.random.binomial(k, p, n)
    conteos = [np.sum(datos==i) for i in range(k+1)]
    _graficar_barras(conteos, [str(i) for i in range(k+1)], frame_grafica, "Distribución Binomial")
    for w in frame_detalles.winfo_children():
        w.destroy()
    tk.Label(frame_detalles, text=f"Conteos: {conteos}").pack(anchor="w")

# ========================
#  Ventanas de distribución
# ========================
def abrir_bernoulli():
    nueva = tk.Toplevel(ventana)
    nueva.title("Distribución Bernoulli")
    nueva.geometry("900x700")
    nueva.configure(bg=COLOR_FONDO)

    tk.Label(nueva, text="Distribución Bernoulli", bg=COLOR_FONDO,
             fg=COLOR_TEXTO, font=FONT_TITULO).pack(pady=20)

    frame_params = tk.LabelFrame(nueva, text=" Parámetros ", bg=COLOR_FRAME,
                                 fg=COLOR_TEXTO, font=FONT_LABEL, padx=15, pady=15)
    frame_params.pack(pady=10, padx=20, fill="x")

    tk.Label(frame_params, text="Probabilidad de Éxito (p):", bg=COLOR_FRAME,
             fg=COLOR_TEXTO, font=FONT_LABEL).grid(row=0, column=0, sticky="w", pady=5)
    deslizador_p = tk.Scale(frame_params, from_=0, to=1, resolution=0.01,
                            orient="horizontal", length=300, bg=COLOR_FRAME,
                            highlightthickness=0, troughcolor="white")
    deslizador_p.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_params, text="Tamaño de la muestra (n):", bg=COLOR_FRAME,
             fg=COLOR_TEXTO, font=FONT_LABEL).grid(row=1, column=0, sticky="w", pady=5)
    entrada_n = tk.Entry(frame_params, font=FONT_LABEL, justify="center", width=10)
    entrada_n.grid(row=1, column=1, padx=10, pady=5)

    frame_resultados = tk.Frame(nueva, bg=COLOR_FONDO)
    frame_resultados.pack(padx=20, pady=15, fill="both", expand=True)

    frame_grafica = tk.LabelFrame(frame_resultados, text=" Gráfica ",
                                  bg=COLOR_FRAME, fg=COLOR_TEXTO, font=FONT_LABEL)
    frame_grafica.pack(side="left", fill="both", expand=True, padx=10)

    frame_detalles = tk.LabelFrame(frame_resultados, text=" Resultados ",
                                   bg=COLOR_FRAME, fg=COLOR_TEXTO, font=FONT_LABEL)
    frame_detalles.pack(side="right", fill="both", expand=True, padx=10)

    boton = tk.Button(nueva, text="Generar", font=FONT_BOTON,
                      bg=COLOR_BOTON, fg="white", width=15,
                      command=lambda: generar_Bernoulli(entrada_n, deslizador_p,
                                                        frame_grafica, frame_detalles))
    boton.pack(pady=15)
    boton.bind("<Enter>", on_enter)
    boton.bind("<Leave>", on_leave)

    frame_botones = tk.Frame(nueva, bg=COLOR_FRAME)
    frame_botones.pack(side="bottom", fill="x", pady=10, padx=10)

    btn_regresar = tk.Button(frame_botones, text="Regresar", font=FONT_BOTON,
                             bg=COLOR_BOTON, fg="white", width=12,
                             command=nueva.destroy)
    btn_regresar.pack(side="left", anchor="w", padx=5)
    btn_regresar.bind("<Enter>", on_enter)
    btn_regresar.bind("<Leave>", on_leave)
    
    btn_info = tk.Button(frame_botones, text="Info", font=FONT_BOTON,
                         bg=COLOR_BOTON, fg="white", width=12,
                         command=lambda: messagebox.showinfo("Info", "Distribución Bernoulli"))
    btn_info.pack(side="right", anchor="e", padx=5)
    btn_info.bind("<Enter>", on_enter)
    btn_info.bind("<Leave>", on_leave)

# ---------- Abrir Binomial ----------
def abrir_binomial():
    nueva = tk.Toplevel(ventana)
    nueva.title("Distribución Binomial")
    nueva.geometry("900x700")
    nueva.configure(bg=COLOR_FONDO)

    tk.Label(nueva, text="Distribución Binomial", bg=COLOR_FONDO,
             fg=COLOR_TEXTO, font=FONT_TITULO).pack(pady=20)

    tk.Label(nueva, text="Probabilidad de Éxito (p):", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=5)
    deslizador_p = tk.Scale(nueva, from_=0, to=1, resolution=0.01, orient="horizontal", length=300)
    deslizador_p.pack(pady=5)

    tk.Label(nueva, text="Número de Repeticiones (k):", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=5)
    entrada_k = tk.Entry(nueva)
    entrada_k.pack(pady=5)

    tk.Label(nueva, text="Tamaño de la muestra (n):", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=5)
    entrada_n = tk.Entry(nueva)
    entrada_n.pack(pady=5)

    frame_grafica = tk.Frame(nueva)
    frame_grafica.pack(pady=10)
    frame_detalles = tk.Frame(nueva)
    frame_detalles.pack(pady=5)

    tk.Button(nueva, text="Generar", command=lambda: generar_Binomial(entrada_n, entrada_k, deslizador_p, frame_grafica, frame_detalles)).pack(pady=10)
# ========================
# Distribución Multinomial
# ========================
# ========================
# Distribución Multinomial
# ========================
def abrir_multinomial():
    nueva = tk.Toplevel(ventana)
    nueva.title("Distribución Multinomial")
    nueva.geometry("1000x700")
    nueva.configure(bg=COLOR_FONDO)

    tk.Label(nueva, text="Distribución Multinomial",
             bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FONT_TITULO).pack(pady=10)

    frame_principal = tk.Frame(nueva, bg=COLOR_FONDO)
    frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

    # ------------------ Frame parámetros con scroll ------------------
    frame_params_container = tk.LabelFrame(frame_principal, text=" Parámetros ",
                                           bg=COLOR_FRAME, fg=COLOR_TEXTO,
                                           font=FONT_LABEL, padx=0, pady=0)
    frame_params_container.pack(side="left", fill="y", padx=5, pady=5)

    canvas_params = tk.Canvas(frame_params_container, bg=COLOR_FRAME, highlightthickness=0, width=250)
    scrollbar_params = tk.Scrollbar(frame_params_container, orient="vertical", command=canvas_params.yview)
    scrollable_params = tk.Frame(canvas_params, bg=COLOR_FRAME)

    scrollable_params.bind(
        "<Configure>",
        lambda e: canvas_params.configure(scrollregion=canvas_params.bbox("all"))
    )

    canvas_params.create_window((0,0), window=scrollable_params, anchor="nw")
    canvas_params.configure(yscrollcommand=scrollbar_params.set)

    canvas_params.pack(side="left", fill="both", expand=True)
    scrollbar_params.pack(side="right", fill="y")

    # ------------------ Widgets de parámetros ------------------
    tk.Label(scrollable_params, text="Número de resultados posibles (k):", bg=COLOR_FRAME, fg=COLOR_TEXTO).pack(anchor="w")
    entrada_k = tk.Entry(scrollable_params, width=5, font=FONT_LABEL, justify="center")
    entrada_k.insert(0, "6")
    entrada_k.pack(pady=5)

    frame_probs = tk.Frame(scrollable_params, bg=COLOR_FRAME)
    frame_probs.pack(pady=5)
    entradas_probs = []

    def generar_campos():
        for w in frame_probs.winfo_children():
            w.destroy()
        entradas_probs.clear()
        try:
            k = int(entrada_k.get())
        except ValueError:
            messagebox.showerror("Error", "Introduce un número válido")
            return
        for i in range(k):
            subframe = tk.Frame(frame_probs, bg=COLOR_FRAME)
            subframe.pack(anchor="w", pady=2)
            tk.Label(subframe, text=f"Resultado {i+1}:", bg=COLOR_FRAME, fg=COLOR_TEXTO).pack(side="left")
            entry = tk.Entry(subframe, width=6, font=FONT_LABEL, justify="center")
            entry.pack(side="left", padx=5)
            entradas_probs.append(entry)

    tk.Button(scrollable_params, text="Generar campos", font=FONT_BOTON,
              bg=COLOR_BOTON, fg="white", width=15,
              command=generar_campos).pack(pady=5)

    evento_eq_var = tk.IntVar(value=0)
    def toggle_evento_eq():
        if evento_eq_var.get() == 1:
            k = len(entradas_probs)
            for e in entradas_probs:
                e.delete(0, tk.END)
                e.insert(0, f"1/{k}")
        else:
            for e in entradas_probs:
                e.delete(0, tk.END)
    tk.Checkbutton(scrollable_params, text="Evento equilibrado", variable=evento_eq_var,
                   command=toggle_evento_eq, bg=COLOR_FRAME, fg=COLOR_TEXTO).pack(pady=5)

    tk.Label(scrollable_params, text="Tamaño de la muestra (n):", bg=COLOR_FRAME, fg=COLOR_TEXTO).pack(anchor="w", pady=2)
    entrada_n = tk.Entry(scrollable_params, width=10, font=FONT_LABEL, justify="center")
    entrada_n.insert(0, "20")
    entrada_n.pack(pady=2)

    tk.Label(scrollable_params, text="Número de repeticiones (R):", bg=COLOR_FRAME, fg=COLOR_TEXTO).pack(anchor="w", pady=2)
    entrada_rep = tk.Entry(scrollable_params, width=10, font=FONT_LABEL, justify="center")
    entrada_rep.insert(0, "6")  # default para que veas 6 vectores
    entrada_rep.pack(pady=2)

    # ------------------ Frame gráfica ------------------
    frame_grafica = tk.LabelFrame(frame_principal, text=" Gráfica ",
                                  bg=COLOR_FRAME, fg=COLOR_TEXTO, font=FONT_LABEL)
    frame_grafica.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    # ------------------ Frame resultados con scroll ------------------
    frame_resultados_container = tk.LabelFrame(nueva, text=" Vectores de frecuencia ",
                                               bg=COLOR_FRAME, fg=COLOR_TEXTO, font=FONT_LABEL)
    frame_resultados_container.pack(fill="both", expand=True, padx=10, pady=5)

    canvas_resultados = tk.Canvas(frame_resultados_container, bg=COLOR_FRAME, highlightthickness=0)
    scrollbar_resultados = tk.Scrollbar(frame_resultados_container, orient="vertical", command=canvas_resultados.yview)
    scrollable_resultados = tk.Frame(canvas_resultados, bg=COLOR_FRAME)

    scrollable_resultados.bind(
        "<Configure>",
        lambda e: canvas_resultados.configure(scrollregion=canvas_resultados.bbox("all"))
    )

    canvas_resultados.create_window((0,0), window=scrollable_resultados, anchor="nw")
    canvas_resultados.configure(yscrollcommand=scrollbar_resultados.set)

    canvas_resultados.pack(side="left", fill="both", expand=True)
    scrollbar_resultados.pack(side="right", fill="y")

    # ------------------ Lista de vectores generados ------------------
    lista_vectores = []

    # ------------------ Función generar ------------------
    def generar_multinomial_fn():
        nonlocal lista_vectores
        for w in frame_grafica.winfo_children():
            w.destroy()
        for w in scrollable_resultados.winfo_children():
            w.destroy()
        lista_vectores.clear()

        if not entradas_probs:
            messagebox.showerror("Error", "Primero genera los campos de probabilidades")
            return

        try:
            n = int(entrada_n.get())
            R = int(entrada_rep.get())
            probs = [_parse_probabilidad_texto(e.get()) for e in entradas_probs]
        except ValueError:
            messagebox.showerror("Error", "Introduce valores numéricos válidos")
            return

        if abs(sum(probs)-1.0) > 1e-6:
            messagebox.showerror("Error", "Las probabilidades deben sumar 1")
            return

        # ---------------- Generar todos los vectores ----------------
        for r in range(R):
            conteos, _ = _simular_una_multinomial(n, probs)
            lista_vectores.append(conteos.tolist())

        # ---------------- Mostrar todos los vectores ----------------
        tk.Label(scrollable_resultados, text="Vectores generados:").pack(anchor="w")
        for idx, vec in enumerate(lista_vectores):
            texto_vec = ", ".join(str(v) for v in vec)
            tk.Label(scrollable_resultados, text=f"{idx+1}: [{texto_vec}]").pack(anchor="w")

        # ---------------- Combobox para graficar vector seleccionado ----------------
        combobox = Combobox(scrollable_resultados, values=[i+1 for i in range(len(lista_vectores))], state="readonly")
        combobox.current(0)
        combobox.pack(pady=2)

        def graficar_seleccionado():
            idx = int(combobox.get())-1
            for w in frame_grafica.winfo_children():
                w.destroy()
            _graficar_barras(lista_vectores[idx], [f"{i+1}" for i in range(len(probs))],
                             frame_grafica, f"Vector {idx+1}")

        tk.Button(scrollable_resultados, text="Graficar vector seleccionado", command=graficar_seleccionado,
                  bg=COLOR_BOTON, fg="white", font=FONT_BOTON).pack(pady=5)

    # ------------------ Botón Generar visible siempre ------------------
    boton_generar = tk.Button(nueva, text="Generar", font=FONT_BOTON,
                              bg=COLOR_BOTON, fg="white", width=15,
                              command=generar_multinomial_fn)
    boton_generar.pack(pady=10)
    boton_generar.bind("<Enter>", on_enter)
    boton_generar.bind("<Leave>", on_leave)

# ========================
# Distribución Exponencial
# ========================
def generar_exponencial(entrada_n, entrada_lambda, frame_grafica):
    try:
        n = int(entrada_n.get())
        lam = float(entrada_lambda.get())
    except ValueError:
        messagebox.showerror("Error", "Introduce valores numéricos válidos")
        return
    datos = np.random.exponential(1/lam, n)
    _graficar_barras(np.histogram(datos, bins=10)[0], range(1,11), frame_grafica, "Distribución Exponencial")

def abrir_exponencial():
    nueva = tk.Toplevel(ventana)
    nueva.title("Distribución Exponencial")
    nueva.geometry("900x700")
    nueva.configure(bg=COLOR_FONDO)

    tk.Label(nueva, text="Distribución Exponencial", bg=COLOR_FONDO,
             fg=COLOR_TEXTO, font=FONT_TITULO).pack(pady=20)

    tk.Label(nueva, text="Tamaño de la muestra(n):", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=5)
    entrada_n = tk.Entry(nueva)
    entrada_n.pack(pady=5)

    tk.Label(nueva, text="Valor de λ (lambda):", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=5)
    entrada_lambda = tk.Entry(nueva)
    entrada_lambda.pack(pady=5)

    frame_grafica = tk.Frame(nueva)
    frame_grafica.pack(pady=10)

    tk.Button(nueva, text="Generar", command=lambda: generar_exponencial(entrada_n, entrada_lambda, frame_grafica),
              bg=COLOR_BOTON, fg="white", font=FONT_BOTON).pack(pady=10)

# ========================
# Distribución Normal
# ========================
def abrir_normal():
    nueva = tk.Toplevel(ventana)
    nueva.title("Distribución Normal")
    nueva.geometry("900x700")
    nueva.configure(bg=COLOR_FONDO)

    tk.Label(nueva, text="Distribución Normal", bg=COLOR_FONDO,
             fg=COLOR_TEXTO, font=FONT_TITULO).pack(pady=20)

    frame_params = tk.LabelFrame(nueva, text=" Parámetros ",
                                 bg=COLOR_FRAME, fg=COLOR_TEXTO,
                                 font=FONT_LABEL, padx=15, pady=15)
    frame_params.pack(pady=10, padx=20, fill="x")

    tk.Label(frame_params, text="Media (μ):", bg=COLOR_FRAME, fg=COLOR_TEXTO, font=FONT_LABEL).grid(row=0, column=0, sticky="w", pady=5)
    entrada_mu = tk.Entry(frame_params, font=FONT_LABEL, justify="center", width=10)
    entrada_mu.insert(0, "0")
    entrada_mu.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_params, text="Desviación estándar (σ):", bg=COLOR_FRAME, fg=COLOR_TEXTO, font=FONT_LABEL).grid(row=1, column=0, sticky="w", pady=5)
    entrada_sigma = tk.Entry(frame_params, font=FONT_LABEL, justify="center", width=10)
    entrada_sigma.insert(0, "1")
    entrada_sigma.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame_params, text="Tamaño de la muestra (n):", bg=COLOR_FRAME, fg=COLOR_TEXTO, font=FONT_LABEL).grid(row=2, column=0, sticky="w", pady=5)
    entrada_n = tk.Entry(frame_params, font=FONT_LABEL, justify="center", width=10)
    entrada_n.insert(0, "100")
    entrada_n.grid(row=2, column=1, padx=10, pady=5)

    frame_resultados = tk.Frame(nueva, bg=COLOR_FONDO)
    frame_resultados.pack(padx=20, pady=15, fill="both", expand=True)

    frame_grafica = tk.LabelFrame(frame_resultados, text=" Gráfica ",
                                  bg=COLOR_FRAME, fg=COLOR_TEXTO, font=FONT_LABEL)
    frame_grafica.pack(fill="both", expand=True, padx=10, side="left")

    frame_detalles = tk.LabelFrame(frame_resultados, text=" Resultados ",
                                   bg=COLOR_FRAME, fg=COLOR_TEXTO, font=FONT_LABEL)
    frame_detalles.pack(fill="both", expand=True, padx=10, side="right")

    def generar_normal_fn():
        try:
            n = int(entrada_n.get())
            mu = float(entrada_mu.get())
            sigma = float(entrada_sigma.get())
            if n <= 0 or sigma <= 0:
                raise ValueError

            datos = np.random.normal(mu, sigma, n)

            fig, ax = plt.subplots(figsize=(5,4))
            ax.hist(datos, bins=20, density=True, color="skyblue", alpha=0.7, edgecolor="black")

            x = np.linspace(min(datos), max(datos), 200)
            f_x = (1/(sigma * np.sqrt(2*np.pi))) * np.exp(-((x - mu)**2)/(2*sigma**2))
            ax.plot(x, f_x, "r", linewidth=2, label="Densidad teórica")

            ax.set_title("Distribución Normal")
            ax.set_xlabel("Valor")
            ax.set_ylabel("Densidad")
            ax.legend()

            for w in frame_grafica.winfo_children():
                w.destroy()
            canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            plt.close(fig)

            for w in frame_detalles.winfo_children():
                w.destroy()
            tk.Label(frame_detalles, text=f"Media simulada: {np.mean(datos):.4f}", font=FONT_LABEL).pack(pady=5)
            tk.Label(frame_detalles, text=f"Desviación simulada: {np.std(datos):.4f}", font=FONT_LABEL).pack(pady=5)

        except ValueError:
            messagebox.showerror("Error", "Introduce valores válidos para n, μ y σ")

    tk.Button(nueva, text="Generar", font=FONT_BOTON, bg=COLOR_BOTON, fg="white",
              command=generar_normal_fn).pack(pady=15)


# ========================
# Ventana Principal
# ========================
ventana = tk.Tk()
ventana.title("Simulación de distribuciones")
ventana.geometry("800x600")
ventana.configure(bg=COLOR_FONDO)

tk.Label(ventana, text="Elige una distribución:", font=FONT_TITULO,
         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=20)

frame_menu = tk.Frame(ventana, bg=COLOR_FONDO)
frame_menu.pack(pady=20)

for texto, comando in [
    ("Bernoulli", abrir_bernoulli),
    ("Binomial", abrir_binomial),
    ("Multinomial (simulación de un dado)", abrir_multinomial),
    ("Exponencial", abrir_exponencial),
    ("Normal", abrir_normal)
]:
    btn = tk.Button(frame_menu, text=texto, font=FONT_BOTON,
                    bg=COLOR_BOTON, fg="white", width=30, command=comando)
    btn.pack(pady=8)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

ventana.mainloop()
