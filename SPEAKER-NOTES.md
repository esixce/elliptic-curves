# ECC Teaching — Speaker Notes

Bullet points only. Open the matching notebook, run cells live, talk from these notes.

---

## 00-intro.ipynb (~5 min)

**Open with the problem, not the math.**

- "Bitcoin is a public ledger. Everyone can read every transaction."
- Two problems to solve:
  - **Alias** — need a public identity derived from a secret (one-way function)
  - **Proof** — need to prove you control the alias without revealing the secret (digital signature)
- P = d x G is the one-way function. Easy forward, impossible backward.
- P2PKH: funds locked to hash of public key. You reveal P only when spending.
- Taproot (P2TR): locks to pubkey directly, uses Schnorr instead of ECDSA.

**Key phrase:** "Same two problems, every script type. Alias + Proof."

- Why ECC over RSA? Show the table: 256-bit ECC = 3072-bit RSA. 12x smaller.
- Koblitz & Miller (1985): "same discrete log trick, harder group"

**Transition:** "To build this, we need specific math. Let's see what rules this world obeys."

---

## 01-algebraic-foundations.ipynb (~20 min)

**This is the longest module. Don't rush axioms — they pay off in Module 5.**

- Start: "We need a one-way function. But the operation can't be just anything."
- The operation needs 5 properties. That's called an Abelian group.

**Run cells live for each axiom — use small numbers (mod 7):**

| Axiom | Say this | Cell |
|-------|---------|------|
| Closure | "5+5=10, but 10 isn't odd. Closure failed. That's why we use a finite field — mod p keeps us inside." | Cell 2-3 |
| Associativity | "Grouping doesn't matter. Boring but essential — ECDSA verification rearranges terms." | Cell 4-5 |
| Identity | "Adding zero changes nothing. On the curve, it's the point at infinity." | Cell 6-7 |
| Inverse | "Every element has an undo partner. That's how the verifier reverses the signer's work." | Cell 8-9 |
| Commutativity | "Order doesn't matter. Signer and verifier compute the same thing different ways." | Cell 10-11 |

- After all 5: show the ECDSA equation table (cell 12) — "see, every property is used"

**Historical context (cell 1 intro):**
- ElGamal: group properties were FREE (integers mod p, textbook since 1800s)
- ECC: same scheme, NEW group — now properties are a CHECKLIST
- "They didn't invent groups for ECC. They went shopping for a harder group."

**Fields section — go fast, just the intuition:**
- "The field is the ground the curve is drawn on"
- Curve equation needs +, -, x → that's a ring (cell 13)
- Slope formula needs division → that's a field (cell 13)
- Finite field F_p: mod p makes it finite and secure (cell 14-16)
- Run the F_11 inverse table (cell 14) — "every nonzero element has an inverse"

**Projective space — optional, can skip if short on time:**
- Only needed to explain point at infinity
- "What happens when you add a point to its own negative? Vertical line, no third intersection."
- Projective space: parallel lines meet at infinity. Problem solved.
- If time: show the plotly sphere (cells 21-23) — drag to rotate, good visual

**Transition:** "Now we know the rules. Let's see the actual curve."

---

## 02-elliptic-curves.ipynb (~8 min)

- Weierstrass equation: y^2 = x^3 + ax + b
- Bitcoin uses secp256k1: a=0, b=7, so y^2 = x^3 + 7
- Run cell 1: prints all the secp256k1 parameters (P, N, G coordinates)
- "P is the field prime (where coordinates live), N is the group order (where scalars live)"
- Over reals: smooth curve. Over F_p: scattered dots with vertical symmetry.
- Run cell 3: plots y^2 = x^3 + x + 1 over F_23 — "see the symmetry?"
- Point out: for every (x, y) there's (x, p-y)
- Non-singular: discriminant != 0, no cusps or self-intersections

**Key phrase:** "The curve is just a set of points. The magic is in what we do with them."

**Transition:** "We have points. Now let's add them."

---

## 03-point-operations.ipynb (~12 min)

**This is the hands-on module. Run every cell.**

- Run preamble cell first (cell 0) — loads secp256k1 params
- Cell 1: Point class, mod_inverse, point_add, point_double, point_negate
  - "Draw a line through two points, find the third, reflect. That's addition."
  - "Tangent line at one point: that's doubling."
- Cell 2: test point_add and point_double on secp256k1 G
  - Show: G + G = 2G, and that the result is on the curve

**Scalar multiplication (cell 3-4):**
- "Private key d, generator G, public key P = d x G"
- Double-and-add: O(log k) — "256 doublings and additions, not 2^256 additions"
- Run the demo: pick random private key, compute public key
- "This is the one-way function. We just did it."

**Compressed public keys (cell 5-6):**
- 65 bytes uncompressed (04 || x || y) vs 33 bytes compressed (02/03 || x)
- "y^2 = x^3+7 has two solutions for y. Even or odd. One bit is enough."
- Run: generate key, serialize compressed, parse back, verify match

**Transition:** "We can make keys. Before signatures, let's see where this idea came from."

---

## 04-key-exchange.ipynb (~8 min)

- ElGamal vs ECC side-by-side (cell 1)
  - "Same structure: private scalar, public point, shared secret"
  - ECDH: Alice has (a, A=aG), Bob has (b, B=bG), shared = a*B = b*A = abG
  - Run it: two parties, same shared secret

- ECC encryption on small curve (cell 2): y^2 = x^3 - x + 4 over F_457
  - Encrypt a message as a curve point
  - "This is literally ElGamal transplanted onto an elliptic curve"
  - Decrypt: C2 - d*C1 = Pm + k*Q - d*(k*G) = Pm (the k's cancel)

**Key phrase:** "ECC isn't a new idea. It's an old idea in a harder group."

**Transition:** "Now the main event: digital signatures."

---

## 05-ecdsa.ipynb (~15 min)

**The payoff. Everything converges here.**

- Run preamble cell first (cell 0)
- "The one-way function fires TWICE in every Bitcoin transaction"
  - Once for the alias: P = d x G (your public key)
  - Once per signature: R = k x G (fresh nonce point)

**Signing (cell 1):**
- Walk through the equation: s = k^{-1}(z + r*d) mod N
- z = hash of the message, r = x-coordinate of R, d = private key, k = nonce
- Run: sign a message, print (r, s)

**Verification (cell 2):**
- "The verifier doesn't know k or d. Only (r, s), z, and P."
- u1 = z/s, u2 = r/s, R' = u1*G + u2*P
- Check R'_x == r — "every group property is used in this rearrangement"
- Run: verify returns True

**Nonce catastrophe (cell 3):**
- "Reuse k and you leak d. This actually happened — PlayStation 3, 2010."
- Same k for two messages → two equations, two unknowns → solve for d
- Run the demo: two signatures with same k → private key extracted
- "This is why RFC 6979 exists — deterministic nonce from message + key"

**From math to bytes (cells 4-5):**
- DER encoding: variable length, ~72 bytes, ASN.1 format
- Low-S normalization: s > N/2 → replace with N-s (BIP 62, anti-malleability)
- Schnorr: fixed 64 bytes. No DER, no ambiguity.
- Show the transaction layout diagram
- Run cell 5: builds DER encoding from scratch, compares with Schnorr

**Key phrase:** "The math produces big integers. DER wraps them for the wire."

**Transition:** "ECDSA works. But Bitcoin moved on to something cleaner."

---

## 06-bitcoin-applications.ipynb (~10 min)

**Schnorr (cell 1-2):**
- "BIP 340. Simpler than ECDSA: s = k + e*d, verify: sG = R + eP"
- Fixed 64-byte signature (R_x || s), no DER encoding needed
- Key advantage: **linear** — signatures can be aggregated (MuSig2)
- Run: sign and verify with Schnorr
- "This is what Taproot uses. Every key-path spend is one Schnorr sig."

**ECDH in Lightning onion routing (cell 3-4):**
- Onion routing: sender wraps payment in layers, each hop peels one
- ECDH at each hop: shared secret from ephemeral key + hop's public key
- "Same ECDH from Module 4, but now each hop blinds the ephemeral key"
- Run: 3-hop onion route, show each hop derives the same shared secret

**Transition:** "That's the full picture. Let's test your understanding."

---

## 07-exercises.ipynb (~15 min or homework)

**Can assign as homework or do live if time permits.**

- 6 exercises, progressive difficulty:
  1. Finite field arithmetic (mod inverse)
  2. Points on a curve (find y given x)
  3. Point negation
  4. Double-and-add trace (count operations for a given k)
  5. ECDSA verify by hand (walk through u1, u2, R')
  6. Nonce recovery (extract private key from reused nonce)

- Knowledge map (cell 8): checklist of all concepts — good self-assessment
- Further study (cell 9): links to SEC 2, BIP 340, Silverman, Paar/Pelzl

**If running short:** assign exercises 1-4 as homework, do 5-6 live (they're the most impactful).

---

## Appendix Notebooks

Available if questions come up or for bonus material:

| Notebook | When to use |
|----------|------------|
| A1-wright-trick.ipynb | "How did Craig Wright fake a signature?" — good after Module 5 |
| A2-nonsense-signature.ipynb | "Can you make a valid signature without knowing the key?" — good after nonce section |
| A3-original-paper.ipynb | Reference: the original research paper as a notebook |

---

## Timing Summary

| Module | Notebook | Estimate |
|--------|----------|----------|
| Intro | 00-intro | 5 min |
| Algebraic Foundations | 01-algebraic-foundations | 20 min |
| Elliptic Curves | 02-elliptic-curves | 8 min |
| Point Operations | 03-point-operations | 12 min |
| Key Exchange | 04-key-exchange | 8 min |
| ECDSA | 05-ecdsa | 15 min |
| Bitcoin Applications | 06-bitcoin-applications | 10 min |
| Exercises | 07-exercises | 15 min |
| **Total** | | **~93 min** |

If you need to cut to 60 min: skip projective space in Module 1, go fast through Module 4, assign exercises as homework.
