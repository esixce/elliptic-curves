# Elliptic Curve Cryptography: From Theory to Bitcoin

Interactive Jupyter notebooks covering the mathematical foundations of elliptic curve cryptography and its applications in Bitcoin — from abstract algebra through ECDSA, Schnorr signatures, and onion routing.

## Course Modules

Work through these in order. Each notebook is self-contained (shared code is included as a preamble cell).

| # | File | What it covers |
|---|------|---------------|
| 0 | `00-intro.ipynb` | Motivation, the two problems ECC solves, roadmap |
| 1 | `01-algebraic-foundations.ipynb` | Groups, rings, fields, finite fields, projective space |
| 2 | `02-elliptic-curves.ipynb` | Weierstrass equation, secp256k1 parameters, curves over F_p |
| 3 | `03-point-operations.ipynb` | Point addition, doubling, scalar multiplication, compression |
| 4 | `04-key-exchange.ipynb` | ECDH, ElGamal encryption/decryption on curves |
| 5 | `05-ecdsa.ipynb` | Signing, verification, nonce catastrophe, DER encoding |
| 6 | `06-bitcoin-applications.ipynb` | Schnorr signatures (BIP 340), ECDH in Lightning onion routing |
| 7 | `07-exercises.ipynb` | Self-assessment, exercises, knowledge map, further reading |

## Appendix Notebooks

| File | What it covers |
|------|---------------|
| `A1-wright-trick.ipynb` | How Craig Wright faked a Satoshi signature in 2016 |
| `A2-nonsense-signature.ipynb` | The "nonsense signature" algebraic forgery trick |
| `A3-original-paper.ipynb` | Original research paper companion notebook |

## Teaching

See `SPEAKER-NOTES.md` for bullet-point talking points, live demo callouts, and timing estimates per module (~93 min total).

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

Then open `00-intro.ipynb` and work through the modules in order.
