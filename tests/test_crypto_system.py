import unittest
import numpy as np
from sympy import Matrix, mod_inverse, symbols, simplify
import random

# ======= Helper Functions (same as your code base) =======

def generate_affine_map(n, p):
  while True:
    A = np.random.randint(0, p, (n, n))
    A_sym = Matrix(A.tolist())
    try:
      if round(A_sym.det()) % p == 1:
        b = np.random.randint(0, p, n)
        return A, b
    except ValueError:
      continue

def test_affine_inversion_logic(A_np, b_np, p, trials=5):
  A = Matrix(A_np.tolist())
  b = Matrix(b_np.tolist())
  A_inv = A.inv_mod(p)
  n = A.rows
  for _ in range(trials):
    x = Matrix(np.random.randint(0, p, n).tolist())
    fx = (A * x + b) % p
    x_back = (A_inv * (fx - b)) % p
    assert list(x_back) == list(x)

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

# ========== Unit Test Class ==========

class TestJacobianCryptoSystem(unittest.TestCase):

  def test_affine_generation_and_inversion(self):
    p, n = 26, 3
    A, b = generate_affine_map(n, p)
    self.assertEqual(round(Matrix(A.tolist()).det()) % p, 1)
    test_affine_inversion_logic(A, b, p)

  def test_triangular_map_jacobian_is_one(self):
    p, n = 26, 4
    tri_map, vars = generate_triangular_map(n, p)

    J = Matrix(tri_map).jacobian(vars)
    det_J = J.det()

    # Use random substitution to numerically evaluate the symbolic det
    substitutions = {var: random.randint(0, p - 1) for var in vars}
    det_val = det_J.subs(substitutions) % p

    self.assertEqual(int(det_val), 1)

# ========== Run Tests ==========

if __name__ == '__main__':
  unittest.main()

