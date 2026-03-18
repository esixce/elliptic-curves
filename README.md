# Elliptic Curve Cryptography: From Theory to Bitcoin

# Criptografía de Curvas Elípticas: De la Teoría a Bitcoin

Interactive Jupyter notebooks covering elliptic curve cryptography and its applications in Bitcoin — from abstract algebra through ECDSA, Schnorr signatures, and onion routing.

Cuadernos Jupyter interactivos que cubren la criptografía de curvas elípticas y sus aplicaciones en Bitcoin — desde álgebra abstracta hasta ECDSA, firmas Schnorr y enrutamiento cebolla.

## Choose your language / Elige tu idioma

| Language | Directory | README |
|----------|-----------|--------|
| English  | [`en/`](./en/) | [en/README.md](./en/README.md) |
| Español  | [`es/`](./es/) | [es/README.md](./es/README.md) |

## Setup / Configuración

**Prerequisites / Requisitos:** Python 3.11+

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install jupyterlab matplotlib numpy plotly
```

## Run / Ejecutar

```bash
source .venv/bin/activate
cd en/  # or: cd es/
jupyter lab
```

Open `00-intro.ipynb` and work through the modules in order.

Abre `00-intro.ipynb` y avanza por los módulos en orden.

## Structure / Estructura

```
elliptic-curves/
  ecc/          Shared Python package (code lives once)
  en/           English notebooks + docs
  es/           Spanish notebooks + docs (cuadernos en español)
  README.md     This file
```

All notebooks import from `ecc/` — fix a bug once, both languages get it.

Todos los cuadernos importan de `ecc/` — corrige un bug una vez y ambos idiomas lo reciben.
