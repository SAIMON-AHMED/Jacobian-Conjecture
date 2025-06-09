# benchmark_runner.py

import time
import numpy as np
from sympy import Matrix, symbols, simplify
import random
import pandas as pd
import matplotlib.pyplot as plt

def generate_affine_map(n, p):
  while True:
    A = np.random.randint(0, p, (n, n))
    A_sym = Matrix(A.tolist())
    try:
      if round(A_sym.det()) % p == 1:
        b = np.random.randint(0, p, n)
        return A, b
    except:
      continue

def encrypt_affine(A, b, x, p):
  return (Matrix(A.tolist()) * Matrix(x.tolist()) + Matrix(b.tolist())) % p

def decrypt_affine(A, b, fx, p):
  A_inv = Matrix(A.tolist()).inv_mod(p)
  return (A_inv * (fx - Matrix(b.tolist()))) % p

def generate_triangular_map(n, p, max_deg=3):
  vars = symbols(f'x1:{n+1}')
  components = []
  for i in range(n):
    expr = vars[i]
    for j in range(i):
      expr += random.randint(0, p - 1) * vars[j]
      if max_deg >= 2:
        expr += random.randint(0, p - 1) * vars[j]**2
      if max_deg >= 3:
        expr += random.randint(0, p - 1) * vars[j]**3
    components.append(simplify(expr))
  return components, vars

results = []
for n in range(2, 11):
  p = 26
  x = np.random.randint(0, p, n)

  start = time.time()
  A, b = generate_affine_map(n, p)
  affine_gen = time.time() - start

  start = time.time()
  fx = encrypt_affine(A, b, x, p)
  enc_time = time.time() - start

  start = time.time()
  x_back = decrypt_affine(A, b, fx, p)
  dec_time = time.time() - start

  affine_key_size = sum(len(str(Matrix(A.tolist())[i])) for i in range(n)) + len(str(b))

  start = time.time()
  tri_map, vars = generate_triangular_map(n, p)
  tri_gen = time.time() - start
  tri_key_size = sum(len(str(f)) for f in tri_map)

  results.append({
    "n": n,
    "Affine_Gen_Time_ms": affine_gen * 1000,
    "Affine_Enc_Time_ms": enc_time * 1000,
    "Affine_Dec_Time_ms": dec_time * 1000,
    "Affine_Key_Size": affine_key_size,
    "Triangular_Gen_Time_ms": tri_gen * 1000,
    "Triangular_Key_Size": tri_key_size
  })

df = pd.DataFrame(results)
df.to_csv("benchmark_results.csv", index=False)

# Save plot
plt.figure(figsize=(8, 5))
plt.plot(df["n"], df["Affine_Gen_Time_ms"], label="Affine Gen Time (ms)", marker='o')
plt.plot(df["n"], df["Triangular_Gen_Time_ms"], label="Triangular Gen Time (ms)", marker='o')
plt.xlabel("Number of Variables (n)")
plt.ylabel("Generation Time (ms)")
plt.title("Generation Time vs Number of Variables")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("benchmark_plot.png")
