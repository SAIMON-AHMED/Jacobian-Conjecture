import streamlit as st
import sympy as sp
import random
import json

st.set_page_config(page_title="Jacobian Cryptosystem Tool", layout="wide")

st.title("Jacobian-Based Polynomial Cryptosystem")
st.markdown("""
This tool supports two modes:
1. **Generate triangular or affine maps** with Jacobian determinant 1  
2. **Manually define your own maps** and inspect their Jacobian matrices
""")

# Variables
col1, col2 = st.columns(2)

with col1:
    n_vars = st.slider("Number of variables (n)", 2, 6, 3, key="n_vars")

with col2:
    num_maps = st.slider("Number of maps (k)", 1, 5, 2, key="num_maps")

# Define symbolic variables like x1, x2, ..., xn
variables = sp.symbols(f'x1:{n_vars + 1}')

# Mode selection
mode = st.radio("Select Mode", ["Generate Maps", "Define Maps"])
uploaded = st.file_uploader("Load Map Set", type="json")
if uploaded:
    st.session_state.maps = json.load(uploaded)
    st.success("Map set loaded.")


if "maps" not in st.session_state:
    st.session_state.maps = {}

# --- Mode 1: Generator Mode ---
if mode == "Generate Maps":
    map_type = st.selectbox("Map Type", ["Upper Triangular", "Lower Triangular", "Affine"])

    def generate_upper_triangular():
        maps = []
        for _ in range(num_maps):
            components = []
            for i in range(n_vars):
                poly = variables[i]
                for j in range(i):  # upper triangular
                    coeff = random.randint(1, 5)
                    poly += coeff * variables[j]**random.randint(1, 2)
                components.append(sp.simplify(poly))
            maps.append(components)
        return maps

    def generate_lower_triangular():
        maps = []
        for _ in range(num_maps):
            components = []
            for i in range(n_vars):
                poly = variables[i]
                for j in range(i+1, n_vars):  # lower triangular
                    coeff = random.randint(1, 5)
                    poly += coeff * variables[j]**random.randint(1, 2)
                components.append(sp.simplify(poly))
            maps.append(components)
        return maps

    def generate_affine():
        maps = []
        for _ in range(num_maps):
            while True:
                # Random invertible matrix over Z_p (Jacobian condition)
                A = sp.eye(n_vars)
                for i in range(n_vars):
                    for j in range(n_vars):
                        if i != j:
                            A[i, j] = random.randint(0, 2)
                # Check if determinant == 1 over integers
                if A.det() == 1:
                    # Random translation vector
                    b = sp.Matrix([random.randint(0, 5) for _ in range(n_vars)])
                    components = list(A * sp.Matrix(variables) + b)
                    maps.append(components)
                    break  # valid map found

        return maps

    if st.button("Generate Maps"):
        if map_type == "Upper Triangular":
            st.session_state.maps = {
                f"f{i+1}": [str(expr) for expr in m]
                for i, m in enumerate(generate_upper_triangular())
            }
        elif map_type == "Lower Triangular":
            st.session_state.maps = {
                f"f{i+1}": [str(expr) for expr in m]
                for i, m in enumerate(generate_lower_triangular())
            }
        else:
            st.session_state.maps = {
                f"f{i+1}": [str(expr) for expr in m]
                for i, m in enumerate(generate_affine())
            }

# --- Mode 2: Manual Entry ---
elif mode == "Define Maps":
    for i in range(1, num_maps + 1):
        with st.expander(f"Define Map f_{i}", expanded=(i == 1)):
            components = []
            for j in range(n_vars):
                expr = st.text_input(f"f_{i}[{j+1}] = ", f"x{j+1}", key=f"f{i}_x{j+1}")
                components.append(expr)
            st.session_state.maps[f"f{i}"] = components

# --- Analysis Section ---
st.subheader("Jacobian Matrix & Determinant")
selected_map = st.selectbox("Select map for analysis", list(st.session_state.maps.keys()) if st.session_state.maps else [])
if selected_map:
    try:
        fx = [sp.sympify(e) for e in st.session_state.maps[selected_map]]
        J = sp.Matrix(fx).jacobian(variables)
        detJ = sp.simplify(J.det())
        st.markdown("**Jacobian Matrix:**")
        st.latex(sp.latex(J))
        st.markdown("**Determinant:**")
        st.latex(sp.latex(detJ))
        if detJ == 1:
            st.success("✅ Determinant is 1 — map is invertible.")
        else:
            st.warning("⚠️ Determinant is not 1.")
    except Exception as e:
        st.error(f"Error computing Jacobian: {e}")

# Save/load/export
map_json = json.dumps(st.session_state.maps, indent=2)
st.download_button("Download Map Set (JSON)", data=map_json, file_name="maps.json")

if st.button("Export to LaTeX"):
    latex_code = ""
    for name, exprs in st.session_state.maps.items():
        fx = sp.Matrix([sp.sympify(e) for e in exprs])
        latex_code += f"{name}(x) = {sp.latex(fx)} \\\\\n"

    st.download_button("Download LaTeX", data=latex_code, file_name="maps.tex", mime="text/plain")

st.markdown("### Current Maps:")
for name, exprs in st.session_state.maps.items():
    st.markdown(f"**{name}:** " + ", ".join(exprs))

if st.button("Reset All"):
    st.session_state.maps = {}
    st.rerun()

st.markdown("---")
st.markdown("This tool is designed to help you explore and understand Jacobian-based polynomial cryptosystems. You can generate maps, analyze their properties, and export your work for further use.")
# End of app.py
# Note: This code is a Streamlit app that allows users to generate and analyze Jacobian-based polynomial cryptosystems.
# It includes features for generating triangular and affine maps, computing Jacobians, and exporting results.

# Footer
st.markdown("Developed by Saimon Ahmed, [Linkedin](https://www.linkedin.com/in/saimon-ahmed/)")
st.markdown("For more information, visit [GitHub Repository](https://github.com/SAIMON-AHMED/Jacobian-Conjecture)")