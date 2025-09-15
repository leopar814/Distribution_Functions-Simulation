from fastapi import FastAPI, Query
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
        "secuencia": secuencia[:100]  # limitar a 100 elementos para frontend
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

    conteo, bordes = np.histogram(muestras, bins="auto", density=False)
    frecuencias = [{"x": float(bordes[i]), "y": int(conteo[i])} for i in range(len(conteo))]
    
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
    lista_conteos = []
    ultima_secuencia = []
    for _ in range(rep):
        conteos, secuencia = simular_multinomial(n, probs)
        lista_conteos.append(conteos)
        ultima_secuencia = secuencia

    if rep == 1:
        return {
            "conteos": lista_conteos[0],
            "secuencia": ultima_secuencia[:100],
            "categorias": [f"C{i+1}" for i in range(len(probs))]
        }
    else:
        proms = [sum(lista_conteos[r][i] for r in range(rep)) / rep for i in range(len(probs))]
        return {
            "conteos": proms,
            "secuencia": ultima_secuencia[:100],
            "categorias": [f"C{i+1}" for i in range(len(probs))]
        }
    
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

