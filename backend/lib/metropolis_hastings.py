import sympy as sp
import random
import math
import numpy as np

def generateTargetFunction(function_str):
    """Convierte el string de la función target a una expresión utilizable"""
    x = sp.Symbol('x')
    try:
        func = sp.sympify(function_str)
        vars = sorted(func.free_symbols, key=lambda v: v.name)
        f = sp.lambdify(vars, func, modules=["math", "numpy"])
        return f
    except Exception as e:
        raise ValueError(f"Error al interpretar la función: {e}")

def mH_Step(targetFunction, x_actual, sigma=1.0):
    """
    Un paso del algoritmo Metropolis-Hastings
    Retorna: (nuevo_estado, aceptado)
    """
    # 1. Proponer candidato desde distribución normal (propuesta simétrica)
    y = random.gauss(x_actual, sigma)
    
    try: 
        # 2. Evaluar densidades (no normalizadas)
        π_x = targetFunction(x_actual)
        π_y = targetFunction(y)

        # Validación de valores (permitir valores pequeños pero finitos)
        if not math.isfinite(π_x) or not math.isfinite(π_y) or π_x < 0 or π_y < 0:
            return x_actual, False
        
        # Si π_x es 0, no podemos aceptar (división por cero)
        if π_x == 0:
            return x_actual, False
        
        # 3. Ratio de aceptación (Metropolis-Hastings con propuesta simétrica)
        # α = min(1, π(y)/π(x))
        ratio = π_y / π_x
        alpha = min(1.0, ratio)

        # 4. Decisión de aceptación
        u = random.random()
        if u <= alpha:
            return y, True
        else:
            return x_actual, False
            
    except (ValueError, OverflowError, ZeroDivisionError) as e:
        # En caso de error numérico, rechazar
        return x_actual, False

def compute_autocorrelation(samples, max_lag=50):
    """Calcula la autocorrelación de las muestras"""
    samples = np.array(samples)
    mean = np.mean(samples)
    var = np.var(samples)
    
    if var == 0:
        return [1.0] * min(max_lag, len(samples))
    
    n = len(samples)
    max_lag = min(max_lag, n - 1)
    autocorr = []
    
    for lag in range(max_lag):
        if lag == 0:
            autocorr.append(1.0)
        else:
            c = np.mean((samples[:-lag] - mean) * (samples[lag:] - mean))
            autocorr.append(c / var)
    
    return autocorr

def effective_sample_size(samples, max_lag=50):
    """Estima el tamaño efectivo de muestra usando autocorrelación"""
    autocorr = compute_autocorrelation(samples, max_lag)
    n = len(samples)
    
    # ESS = n / (1 + 2*sum(autocorr))
    # Sumar hasta que la autocorrelación sea pequeña
    sum_autocorr = 0
    for i in range(1, len(autocorr)):
        if autocorr[i] < 0.05:  # Umbral de corte
            break
        sum_autocorr += autocorr[i]
    
    ess = n / (1 + 2 * sum_autocorr)
    return max(1, ess)

def mH_Run(targetFunctionRaw, InicialState, iterations=10000, sigma=1.0, burnin=1000):
    """
    Ejecuta el algoritmo Metropolis-Hastings
    
    Parámetros:
        targetFunctionRaw: string con la función objetivo (debe ser > 0)
        InicialState: valor inicial de la cadena
        iterations: número total de iteraciones
        sigma: desviación estándar de la propuesta
        burnin: iteraciones a descartar al inicio
    
    Retorna:
        dict con muestras, estadísticas y diagnósticos
    """
    
    targetFunction = generateTargetFunction(targetFunctionRaw)
    currentState = InicialState
    samples = []
    rawSamples = []
    acceptedCount = 0

    for i in range(iterations):
        currentState, accepted = mH_Step(targetFunction, currentState, sigma)

        if accepted:
            acceptedCount += 1

        rawSamples.append(currentState)

        # Guardar muestras después del burn-in
        if i >= burnin:
            samples.append(currentState)

    accepted_ratio = acceptedCount / iterations
    
    # Calcular estadísticas
    samples_array = np.array(samples)
    autocorr = compute_autocorrelation(samples, max_lag=min(100, len(samples)))
    ess = effective_sample_size(samples)
    
    # Diagnostico de convergencia (Geweke)
    # Comparar primera y última parte de la cadena
    first_10_pct = samples[:len(samples)//10]
    last_50_pct = samples[len(samples)//2:]
    
    geweke_z = None
    if len(first_10_pct) > 1 and len(last_50_pct) > 1:
        mean_diff = np.mean(first_10_pct) - np.mean(last_50_pct)
        se_diff = np.sqrt(np.var(first_10_pct)/len(first_10_pct) + 
                          np.var(last_50_pct)/len(last_50_pct))
        if se_diff > 0:
            geweke_z = mean_diff / se_diff

    return {
        "samples": samples,
        "raw_samples": rawSamples,
        "accepted_ratio": accepted_ratio,
        "initial_x": InicialState,
        "burnin": burnin,
        "total_iterations": iterations,
        "sigma": sigma,
        "statistics": {
            "mean": float(np.mean(samples_array)),
            "std": float(np.std(samples_array)),
            "min": float(np.min(samples_array)),
            "max": float(np.max(samples_array)),
            "median": float(np.median(samples_array)),
            "q25": float(np.percentile(samples_array, 25)),
            "q75": float(np.percentile(samples_array, 75))
        },
        "diagnostics": {
            "autocorrelation": autocorr[:50],  # Primeros 50 lags
            "ess": float(ess),
            "ess_ratio": float(ess / len(samples)),
            "geweke_z": float(geweke_z) if geweke_z is not None else None
        }
    }


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 60)
    print("METROPOLIS-HASTINGS - Simulación de Distribución Normal")
    print("=" * 60)
    
    # Ejemplo 1: Normal estándar
    result = mH_Run(
        targetFunctionRaw="exp(-x**2/2)",  # Normal(0,1) sin normalizar
        InicialState=0.0,
        iterations=10000,
        sigma=2.5,  # Desviación de la propuesta
        burnin=1000
    )
    
    print(f"\n{'Estado inicial:':<25} {result['initial_x']}")
    print(f"{'Iteraciones totales:':<25} {result['total_iterations']}")
    print(f"{'Burn-in:':<25} {result['burnin']}")
    print(f"{'Muestras útiles:':<25} {len(result['samples'])}")
    print(f"{'Tasa de aceptación:':<25} {result['accepted_ratio']:.2%}")
    print(f"{'Sigma (propuesta):':<25} {result['sigma']}")
    
    print(f"\n{'='*60}")
    print("ESTADÍSTICAS DE LAS MUESTRAS")
    print(f"{'='*60}")
    stats = result['statistics']
    print(f"{'Media:':<25} {stats['mean']:>10.4f}")
    print(f"{'Desviación estándar:':<25} {stats['std']:>10.4f}")
    print(f"{'Mediana:':<25} {stats['median']:>10.4f}")
    print(f"{'Q1 (25%):':<25} {stats['q25']:>10.4f}")
    print(f"{'Q3 (75%):':<25} {stats['q75']:>10.4f}")
    print(f"{'Mínimo:':<25} {stats['min']:>10.4f}")
    print(f"{'Máximo:':<25} {stats['max']:>10.4f}")
    
    print(f"\n{'='*60}")
    print("DIAGNÓSTICOS DE CONVERGENCIA")
    print(f"{'='*60}")
    diag = result['diagnostics']
    print(f"{'Tamaño efectivo (ESS):':<25} {diag['ess']:>10.1f}")
    print(f"{'Ratio ESS/n:':<25} {diag['ess_ratio']:>10.2%}")
    if diag['geweke_z'] is not None:
        print(f"{'Geweke Z-score:':<25} {diag['geweke_z']:>10.3f}")
        if abs(diag['geweke_z']) < 2:
            print(f"{'   (Convergencia):':<25} {'✓ BUENA' if abs(diag['geweke_z']) < 1 else '✓ ACEPTABLE':>10}")
        else:
            print(f"{'   (Convergencia):':<25} {'⚠ DUDOSA':>10}")
    
    print(f"\n{'='*60}")
    print("RECOMENDACIONES")
    print(f"{'='*60}")
    
    if result['accepted_ratio'] < 0.15:
        print("⚠️  Tasa de aceptación BAJA (<15%)")
        print("    → Reduce 'sigma' para hacer propuestas más conservadoras")
        print(f"    → Prueba con sigma ≈ {result['sigma'] * 0.5:.2f}")
    elif result['accepted_ratio'] > 0.50:
        print("⚠️  Tasa de aceptación ALTA (>50%)")
        print("    → Aumenta 'sigma' para explorar mejor el espacio")
        print(f"    → Prueba con sigma ≈ {result['sigma'] * 1.5:.2f}")
    else:
        print("✓ Tasa de aceptación ÓPTIMA (15%-50%)")
    
    if diag['ess_ratio'] < 0.1:
        print("\n⚠️  ESS ratio bajo (<10%)")
        print("    → Alta autocorrelación en las muestras")
        print("    → Considera aumentar el número de iteraciones")
    elif diag['ess_ratio'] > 0.5:
        print("\n✓ ESS ratio bueno (>50%)")
        print("    → Baja autocorrelación, muestras muy independientes")
    
    print(f"\n{'='*60}")
    print("AUTOCORRELACIÓN (primeros 10 lags)")
    print(f"{'='*60}")
    for i, ac in enumerate(result['diagnostics']['autocorrelation'][:10]):
        bar = "█" * int(ac * 20)
        print(f"Lag {i:2d}: {ac:6.3f} {bar}")
    
    print(f"\n{'='*60}")
    print("MUESTRA (primeras 10 observaciones)")
    print(f"{'='*60}")
    for i, v in enumerate(result['samples'][:10], 1):
        print(f"{i:3d}: {v:10.6f}")
    
    print(f"\n{'='*60}")
    print("Para una Normal(0,1), esperamos:")
    print("  Media ≈ 0, Desv. Est. ≈ 1")
    print(f"{'='*60}\n")
