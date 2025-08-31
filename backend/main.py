from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import random   

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



# def get_distribution(
#     type: str = "normal",
#     mean: float = 0,
#     std: float = 1,
#     n: int = 10
# ):
#     """Genera muestras de una distribución y las regresa como JSON"""
#     if type == "normal":
#         data = np.random.normal(mean, std, n).tolist()
#     elif type == "uniform":
#         data = np.random.uniform(-1, 1, n).tolist()
#     else:
#         data = []
#     return {"samples": data}
