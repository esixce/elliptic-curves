# Criptografía de Curvas Elípticas: De la Teoría a Bitcoin

Cuadernos Jupyter interactivos que cubren los fundamentos matemáticos de la criptografía de curvas elípticas y sus aplicaciones en Bitcoin — desde álgebra abstracta hasta ECDSA, firmas Schnorr y enrutamiento cebolla.

## Módulos del Curso

Trabájalos en orden. Cada cuaderno importa el código compartido del paquete `ecc/`.

| # | Archivo | Qué cubre |
|---|---------|-----------|
| 0 | `00-intro.ipynb` | Motivación, los dos problemas que resuelve la ECC, hoja de ruta |
| 1 | `01-algebraic-foundations.ipynb` | Grupos, anillos, cuerpos, cuerpos finitos, espacio proyectivo |
| 2 | `02-elliptic-curves.ipynb` | Ecuación de Weierstrass, parámetros secp256k1, curvas sobre F_p |
| 3 | `03-point-operations.ipynb` | Suma de puntos, duplicación, multiplicación escalar, compresión |
| 4 | `04-key-exchange.ipynb` | ECDH, cifrado/descifrado ElGamal en curvas |
| 5 | `05-ecdsa.ipynb` | Firma, verificación, catástrofe del nonce, codificación DER |
| 6 | `06-bitcoin-applications.ipynb` | Firmas Schnorr (BIP 340), ECDH en enrutamiento cebolla Lightning |
| 7 | `07-exercises.ipynb` | Autoevaluación, ejercicios, mapa de conocimiento, lecturas adicionales |

## Cuadernos Apéndice

| Archivo | Qué cubre |
|---------|-----------|
| `A1-wright-trick.ipynb` | Cómo Craig Wright falsificó una firma de Satoshi en 2016 |
| `A2-nonsense-signature.ipynb` | El truco de falsificación algebraica "firma sin sentido" |
| `A3-original-paper.ipynb` | Cuaderno acompañante del artículo de investigación original |

## Enseñanza

Ver `SPEAKER-NOTES.md` para puntos de discusión, indicaciones de demos en vivo y estimaciones de tiempo por módulo (~93 min en total).

## Configuración

**Requisitos previos:** Python 3.11+

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install jupyterlab matplotlib numpy plotly
```

## Ejecutar

```bash
source .venv/bin/activate
jupyter lab
```

Luego abre `00-intro.ipynb` y avanza por los módulos en orden.
