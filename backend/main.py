from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import random   
from collections import Counter

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
