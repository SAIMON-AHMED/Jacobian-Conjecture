from sympy import symbols, Matrix, simplify, mod
import random

# === Take input from user ===
p = int(input("Enter modulus p (e.g., 26): "))
n = int(input("Enter number of variables n (e.g., 6): "))
max_deg = 3  # You can make this user-defined too

# === Define symbolic variables: x1, x2, ..., xn ===
vars = symbols(f'x1:{n+1}')  # Creates tuple: (x1, x2, ..., xn)

# === Generate high-degree triangular map ===
tri_map = []

for i in range(n):
    expr = vars[i]  # Start with f_i(x) = x_i

    for j in range(i):
        expr += random.randint(0, p - 1) * vars[j]
        if max_deg >= 2:
            expr += random.randint(0, p - 1) * vars[j]**2
        if max_deg >= 3:
            expr += random.randint(0, p - 1) * vars[j]**3
        if max_deg >= 2 and j < i - 1:
            for k in range(j + 1, i):
                expr += random.randint(0, p - 1) * vars[j] * vars[k]

    tri_map.append(simplify(expr % p))  # Reduce mod p

# === Display the triangular map ===
print("\nGenerated Triangular Map:")
for i, fi in enumerate(tri_map):
    print(f"f{i+1}(x) = {fi}")

# === Compute and display Jacobian determinant mod p ===
J = Matrix(tri_map).jacobian(vars)
det_J = mod(J.det(), p)
print(f"\nJacobian determinant mod {p} = {det_J}")
