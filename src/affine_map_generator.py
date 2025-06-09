import numpy as np
from sympy import Matrix, mod_inverse

# === Take input from user ===
p = int(input("Enter modulus p (e.g., 26): "))
n = int(input("Enter number of variables n (e.g., 3): "))

# === Generate invertible matrix A over Z_p ===
def generate_affine_map(n, p):
    while True:
        A = np.random.randint(0, p, (n, n))
        det = round(np.linalg.det(A)) % p
        try:
            mod_inverse(det, p)  # check if det is invertible mod p
            if det == 1:
                break
        except ValueError:
            continue
    b = np.random.randint(0, p, n)
    return A, b

# === Generate map ===
A, b = generate_affine_map(n, p)

# === Display output ===
print("\nAffine Map: f(x) = A·x + b")
print("A =")
print(A)
print("b =", b)
print(f"det(A) mod {p} = {round(np.linalg.det(A)) % p}")
