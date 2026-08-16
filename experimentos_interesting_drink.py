# Experimentos - Interesting Drink (Codeforces 706B)
# Para subir a Google Colab o GitHub.
# Contiene: implementacion del algoritmo, casos de prueba, benchmark de tiempo y grafico.

import random, time, bisect, math
import matplotlib.pyplot as plt

# ---------- Algoritmo ----------
def solve(prices, budgets):
    xs = sorted(prices)
    return [bisect.bisect_right(xs, m) for m in budgets]

# ---------- 1. Casos de prueba ----------
cases = [
    ("Tipico (enunciado)", [3,10,8,6,11], [1,10,3,11], [0,4,1,5]),
    ("Borde: n=1, m < precio", [50], [1], [0]),
    ("Borde: n=1, m == precio", [50], [50], [1]),
    ("Borde: m mayor a todos los precios", [3,10,8,6,11], [10**9], [5]),
    ("Borde: m menor a todos los precios", [3,10,8,6,11], [1], [0]),
    ("Precios repetidos", [5,5,5,2,9], [5], [4]),
    ("m coincide con precios repetidos", [4,4,4,4], [4], [4]),
]

print("=== Casos de prueba ===")
for name, prices, budgets, expected in cases:
    got = solve(prices, budgets)
    ok = "OK" if got == expected else "FALLA"
    print(f"{name:45s} esperado={expected} obtenido={got}  -> {ok}")

# ---------- 2. Benchmark de tiempo ----------
random.seed(42)
sizes = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
results = []
for n in sizes:
    q = n
    prices = [random.randint(1, 100000) for _ in range(n)]
    budgets = [random.randint(1, 10**9) for _ in range(q)]
    best = None
    for _ in range(5):
        t0 = time.perf_counter()
        solve(prices, budgets)
        t1 = time.perf_counter()
        dt = t1 - t0
        if best is None or dt < best:
            best = dt
    results.append((n, q, best))

print("\n=== Tiempos medidos ===")
for n, q, t in results:
    print(n, q, f"{t*1000:.3f} ms")

# ---------- 3. Grafico ----------
ns = [r[0] for r in results]
ts_ms = [r[2]*1000 for r in results]
theo = [(n+q)*math.log2(n) for n,q,t in results]
scale = ts_ms[-1] / theo[-1]
theo_scaled = [v*scale for v in theo]

fig, axes = plt.subplots(1, 2, figsize=(12,5))
ax = axes[0]
ax.plot(ns, ts_ms, 'o-', label='Tiempo medido')
ax.plot(ns, theo_scaled, '--', label='Theta((n+q) log n) escalada')
ax.set_xlabel('n = q'); ax.set_ylabel('Tiempo (ms)')
ax.set_title('Tiempo vs tamano de entrada'); ax.legend(); ax.grid(alpha=0.3)

ax = axes[1]
ax.plot(ns, ts_ms, 'o-', label='Tiempo medido')
ax.plot(ns, theo_scaled, '--', label='Theta((n+q) log n) escalada')
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('n = q (log)'); ax.set_ylabel('Tiempo (ms, log)')
ax.set_title('Escala log-log'); ax.legend(); ax.grid(alpha=0.3, which='both')

plt.tight_layout()
plt.savefig('grafico_tiempo_vs_n.png', dpi=150)
print("\nGrafico guardado como grafico_tiempo_vs_n.png")
