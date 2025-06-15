# Jacobian-Based Public-Key Cryptosystem

This repository accompanies the research paper:  
“A Polynomial Public-Key Cryptosystem Based on Jacobian-Preserving Composition.”

## Features
- Generate triangular and affine maps with Jacobian determinant = 1
- Symbolically verify invertibility and algebraic security
- GUI for generating and inspecting maps
- Fully reproducible with test suite and examples

## Contents
- `/tests`: Determinant and inversion tests
- `/app`: Streamlit GUI app
- `/paper`: LaTeX version of the full research paper

## Getting Started

This repository contains a Python implementation of a public-key cryptosystem based on Jacobian-preserving polynomial composition. It includes triangular and affine map generators, encryption and decryption routines, and a benchmark script.

### Requirements

- Python 3.9+
- sympy
- numpy
- matplotlib
- pandas
- streamlit (optional, for GUI)

Install dependencies with:

```bash
pip install -r requirements.txt
