# Elliptic Curve Cryptography: From Theory to Bitcoin

Interactive Jupyter notebooks covering the mathematical foundations of elliptic curve cryptography and its applications in Bitcoin — from abstract algebra through ECDSA, Schnorr signatures, and onion routing.

## Notebooks

| # | File | What it covers |
|---|------|---------------|
| 0 | `00-ecc-teachable-scheme.ipynb` | Full course — groups, rings, finite fields, elliptic curves, point operations, ECDSA, Schnorr, exercises |
| 1 | `01-ecc-wright-trick.ipynb` | How Craig Wright faked a Satoshi signature in 2016 |
| 2 | `02-ecc-nonsense-signature.ipynb` | The "nonsense signature" algebraic forgery trick |
| 3 | `03-ecc-original-paper.ipynb` | Original research paper companion notebook |
| 4 | `04-ecc-projective-sphere.ipynb` | Interactive 3D projective sphere visualization |

Start with `00-ecc-teachable-scheme.ipynb` and work through it sequentially.

## Setup

**Prerequisites:** Python 3.11+

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install jupyterlab matplotlib numpy plotly
```

## Run

```bash
source .venv/bin/activate
jupyter lab
```

Then open any notebook from the JupyterLab file browser.

## Source

Based on the research paper *Elliptic Curve Cryptography* (695.744 Reverse Engineering & Vulnerability Analysis). The original essay and companion notebook are in the `esixce/ecdsa-lab` repository.
