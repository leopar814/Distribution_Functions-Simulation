from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import sympy as sp
import random   
import math
from collections import Counter
from typing import List

app = FastAPI()

# Permitir que el frontend en otro puerto pueda conectarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Simulación Bernoulli 
# --------------------
@app.get("/bernoulli")
def generar_bernoulli(repeticiones: int, proba_exito: float):
    num_exitos, num_fracasos = 0, 0
    secuencia = []

    for _ in range(repeticiones):
        r = random.random()
        if r <= proba_exito:
            secuencia.append("E")
            num_exitos += 1
        else:
            secuencia.append("F")
            num_fracasos += 1

    return {
        "repeticiones": repeticiones,
        "proba_exito": proba_exito,
        "exitos": num_exitos,
        "fracasos": num_fracasos,
        "secuencia": secuencia  # limitar a 100 elementos para frontend
    }

# --------------------
# Simulación Binomial
# --------------------
@app.get("/binomial")
def simular_binomial(repeticiones : int, muestra : int, proba_exito : float):
    secuencia = []  # Lista con el número de éxitos de cada repetición
    for _ in range(repeticiones):  
        resultado = generar_bernoulli(muestra, proba_exito)  # Reutilizamos Bernoulli k veces
        num_Exitos = resultado["exitos"]
        secuencia.append(num_Exitos)  # Guardamos los éxitos de esta repetición
    conteo = Counter(secuencia)

    frecuencias = [{"x" : i, "y" : conteo.get(i, 0)} for i in range(muestra + 1)]
    return {
        "frecuencias": frecuencias,
        "secuencia" : secuencia
    }

# --------------------
# Simulación Exponencial
# --------------------
@app.get("/exponential")
def simular_exponencial(n : int, lambda_ : float):
    
    muestras = []
    for _ in range(n):
        u = random.random()
        x = -math.log(1 - u) / lambda_
        muestras.append(x)

    conteo, bordes = np.histogram(muestras, bins="auto", density=True)
    centers = (bordes[:-1] + bordes[1:]) / 2
    frecuencias = [
        {"x": float(c), "y": float(d)}
        for c, d in zip(centers, conteo)
    ]

    
    max_x = max(muestras)
    theo_x = np.linspace(0, max_x, 100)
    theo_y = lambda_ * np.exp(-lambda_ * theo_x)
    teorica = [{"x": float(x), "y": float(y)} for x, y in zip(theo_x, theo_y)]

    return {
        "muestras": muestras[:100],   # Para detalle
        "frecuencias": frecuencias,   # Histograma simulado
        "teorica": teorica,           # Curva teórica
        "lambda": lambda_
    }

# --------------------
# Simulación Multinomial
# --------------------
def simular_multinomial(n: int, probs: List[float]):
    k = len(probs)
    conteos = [0] * k
    secuencia = []
    acumuladas = []
    total = 0.0
    for p in probs:
        total += p
        acumuladas.append(total)
    for _ in range(n):
        r = random.random()
        for i, c in enumerate(acumuladas):
            if r <= c:
                conteos[i] += 1
                secuencia.append(f"C{i+1}")
                break
    return conteos, secuencia

@app.get("/multinomial")
def generar_multinomial(
    n: int,
    rep: int = 1,
    probs: List[float] = Query(..., description="Lista de probabilidades que suman 1")
):
     
    if n <= 0 or rep <= 0:
        raise HTTPException(status_code=400, detail="n y repeticiones deben ser positivos")
    if any(p < 0 for p in probs):
        raise HTTPException(status_code=400, detail="Las probabilidades no pueden ser negativas")
    if abs(sum(probs) - 1.0) > 1e-6:
        raise HTTPException(status_code=400, detail="Las probabilidades deben sumar 1")

    vectores = []
    ultima_secuencia = []
    for _ in range(rep):
        conteos, secuencia = simular_multinomial(n, probs)
        vectores.append(conteos)
        ultima_secuencia = secuencia

    categorias = [f"C{i+1}" for i in range(len(probs))]

    return {
        "n": n,
        "rep": rep,
        "categorias": categorias,
        "vectores": vectores,
        "conteos": vectores[0],  # por defecto el primero
        "secuencia": ultima_secuencia[:100]
    }

    
# --------------------
# Simulación Gebbs
# --------------------
    
x, y, t = sp.symbols('x y t')

def X(f, xmin, xmax, y_val):
    fy = sp.integrate(f, (x, xmin, xmax))
    fxy = (f / fy).subs(y, y_val)
    Fxy = sp.integrate(fxy.subs(x, t), (t, xmin, x))
    u = random.random()
    sol = sp.solve(Fxy - u, x)
    sol_real = [s for s in sol if s.is_real and xmin <= s <= xmax]
    return float(sol_real[0]) if sol_real else None

def Y(f, ymin, ymax, x_val):
    fx = sp.integrate(f, (y, ymin, ymax))
    fyx = (f / fx).subs(x, x_val)
    Fyx = sp.integrate(fyx.subs(y, t), (t, ymin, y))
    v = random.random()
    sol = sp.solve(Fyx - v, y)
    sol_real = [s for s in sol if s.is_real and ymin <= s <= ymax]
    return float(sol_real[0]) if sol_real else None

@app.get("/gebbs")
def generar_gibbs(funcion: str, xmin: float, xmax: float, ymin: float, ymax: float, n: int = 100):
    f = sp.sympify(funcion)

    muestras = []
    xn = random.uniform(xmin, xmax)
    yn = random.uniform(ymin, ymax)
    muestras.append((xn, yn))

    for _ in range(n - 1):
        xn = X(f, xmin, xmax, yn)
        yn = Y(f, ymin, ymax, xn)
        muestras.append((xn, yn))

    return {
        "muestras": [{"x": float(px), "y": float(py)} for px, py in muestras],
        "inicio": {"x": float(muestras[0][0]), "y": float(muestras[0][1])},
        "fin": {"x": float(muestras[-1][0]), "y": float(muestras[-1][1])}
    }

# --------------------
# Simulación Normal
# --------------------
@app.get("/normal")
def generar_normal(
    repeticiones: int,
    mu: float = 0.0,
    sigma: float = 1.0,
    bins: int = 20
):
    if repeticiones <= 0 or sigma <= 0:
        raise HTTPException(status_code=400, detail="repeticiones y sigma deben ser positivos")

    # Box–Muller
    datos = []
    pares = (repeticiones + 1) // 2
    for _ in range(pares):
        u1, u2 = random.random() or 1e-10, random.random()
        r = math.sqrt(-2 * math.log(u1))
        z1 = r * math.cos(2 * math.pi * u2)
        z2 = r * math.sin(2 * math.pi * u2)
        datos.append(mu + sigma * z1)
        if len(datos) < repeticiones:
            datos.append(mu + sigma * z2)

    muestra = datos

    # Histograma (densidad)
    counts, edges = np.histogram(muestra, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    frecuencias = [{"x": float(c), "y": float(d)} for c, d in zip(centers, counts)]

    # Curva teórica más suave
    xs = np.linspace(min(muestra), max(muestra), 200)
    pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-((xs - mu)**2) / (2 * sigma**2))
    teorica = [{"x": float(x), "y": float(y)} for x, y in zip(xs, pdf)]

    return {
        "repeticiones": repeticiones,
        "frecuencias": frecuencias,
        "teorica": teorica,
        "muestra": muestra[:100]
    }
