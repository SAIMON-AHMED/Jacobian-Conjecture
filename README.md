# Jacobian-Based Public-Key Cryptosystem

This repository supports the research paper:

**"A Polynomial Public-Key Cryptosystem Based on Jacobian-Preserving Composition"**  
By Saimon Ahmed  
[Read the paper (PDF)](https://github.com/SAIMON-AHMED/Jacobian-Conjecture/blob/main/paper/jacobian_crypto.pdf)

---

## Overview

This project implements a novel public-key encryption scheme based on **compositions of invertible polynomial maps** with Jacobian determinant equal to 1. Inspired by the Jacobian Conjecture and designed for post-quantum resilience, the scheme uses structured triangular and affine maps to build algebraically secure trapdoor functions.

---

## Features

- Generate upper and lower triangular maps with symbolic Jacobian = 1
- Construct affine maps with modular invertibility
- Compose maps for public key; invert using private sequence
- Symbolically verify Jacobians and inversion correctness
- Benchmark runtime over varying numbers of variables
- Streamlit GUI for interactive exploration

---

## Directory Structure

```bash
Jacobian-Conjecture/
├── app/           # Streamlit GUI for map generation & inspection
├── benchmark/     # Runtime tests and benchmark plots
├── paper/         # LaTeX version of the full research paper
├── src/           # Core implementation (map generators, Jacobians, etc.)
├── tests/         # Unit tests for determinant, invertibility, etc.
├── LICENSE        # MIT License
├── requirements.txt
└── README.md
```
## Getting Started

Install the required packages:

```bash
pip install -r requirements.txt
```
To run the app:
```bash
streamlit run app/app.py
```
## License

This project is licensed under the terms of the MIT License.



