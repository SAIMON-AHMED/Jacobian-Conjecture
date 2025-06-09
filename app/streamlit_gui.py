# === Streamlit GUI: Affine & Triangular Map Generator ===

import streamlit as st
import numpy as np
from sympy import symbols, Matrix, simplify

st.title("Affine and Triangular Map Generator (Det = 1)")

# User inputs
n = st.number_input("Number of variables (n)", min_value=2, value=3)
p = st.number_input("Modulus (p)", min_value=2, value=26)
map_type = st.selectbox("Map Type", ["Affine", "Upper Triangular"])

vars = symbols(f"x1:{n+1}")  # creates x1, x2, ..., xn

if st.button("Generate Map"):
    if map_type == "Affine":
        # Generate random A with det = 1 mod p
        while True:
            A = np.random.randint(0, p, size=(n, n))
            if round(np.linalg.det(A)) % p == 1:
                break
        b = np.random.randint(0, p, size=n)
        
        st.subheader("Affine Map:")
        st.write("f(x) = A·x + b")
        st.write("Matrix A:")
        st.code(A)
        st.write("Vector b:")
        st.code(b)
        st.write(f"det(A) mod {p} = {round(np.linalg.det(A)) % p}")

    else:
        functions = []
        for i in range(n):
            expr = vars[i]
            for j in range(i):
                coeff = np.random.randint(0, p)
                expr += coeff * vars[j]
                if j < i - 1:
                    expr += np.random.randint(0, p) * vars[j] * vars[i-1]
                expr += np.random.randint(0, p) * vars[j]**2
            functions.append(simplify(expr))

        J = Matrix(functions).jacobian(vars)
        det = J.det() % p

        st.subheader("Upper Triangular Map:")
        for i, f in enumerate(functions):
            st.latex(f"f_{{{i+1}}}(x) = {f}")
        st.write(f"Jacobian determinant mod {p} = {det}")
