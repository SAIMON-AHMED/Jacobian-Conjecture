import numpy as np
from sympy import Matrix, mod_inverse

# === Affine Inversion Test over Z_p ===
def test_inversion_affine(A_np, b_np, p, trials=10):
    A = Matrix(A_np.tolist())
    b = Matrix(b_np.tolist())

    det = round(A.det()) % p
    try:
        _ = mod_inverse(det, p)
    except ValueError:
        print("Matrix is not invertible modulo", p)
        return

    A_inv = A.inv_mod(p)
    n = A.rows

    for _ in range(trials):
        x = Matrix(np.random.randint(0, p, n).tolist())
        fx = (A * x + b) % p
        x_back = (A_inv * (fx - b)) % p
        assert list(x_back) == list(x), f"FAIL: x = {x}, x_back = {x_back}"
    print("Affine inversion test passed.")

# === Example Usage ===
p = 26
A = np.array([[1, 2, 3], [0, 1, 4], [0, 0, 1]])  # Must have det = 1 mod p
b = np.array([5, 6, 7])

print("Testing A =\n", A)
print("Testing b =", b)
test_inversion_affine(A, b, p)
