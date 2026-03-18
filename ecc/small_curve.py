"""Small elliptic curve (y^2 = x^3 - x + 4 over F_457) for ECC demos."""

P_SMALL = 457
A_SMALL = -1
B_SMALL = 4
K_ENC = 30


class SmallPoint:
    """A point on a small demo curve (or infinity)."""

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def is_infinity(self):
        return self.x is None

    def copy(self):
        return SmallPoint(self.x, self.y)

    def __eq__(self, other):
        if self.is_infinity() and other.is_infinity():
            return True
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        if self.is_infinity():
            return "O"
        return f"({self.x}, {self.y})"


def small_add(p1, p2):
    """Point addition on the small demo curve."""
    if p1.is_infinity():
        return p2.copy()
    if p2.is_infinity():
        return p1.copy()
    if p1.x == p2.x:
        if (p1.y + p2.y) % P_SMALL == 0:
            return SmallPoint()
        lam = (
            (3 * p1.x * p1.x + A_SMALL)
            * pow(2 * p1.y, P_SMALL - 2, P_SMALL)
        ) % P_SMALL
    else:
        lam = (
            (p2.y - p1.y) * pow(p2.x - p1.x, P_SMALL - 2, P_SMALL)
        ) % P_SMALL
    x3 = (lam * lam - p1.x - p2.x) % P_SMALL
    y3 = (lam * (p1.x - x3) - p1.y) % P_SMALL
    return SmallPoint(x3, y3)


def small_mult(k, p):
    """Scalar multiplication on the small demo curve."""
    if k == 0 or p.is_infinity():
        return SmallPoint()
    result = SmallPoint()
    addend = p.copy()
    while k > 0:
        if k & 1:
            result = small_add(result, addend)
        addend = small_add(addend, addend)
        k >>= 1
    return result


def small_negate(p):
    """Negate a point on the small demo curve."""
    if p.is_infinity():
        return SmallPoint()
    return SmallPoint(p.x, (P_SMALL - p.y) % P_SMALL)


def small_sqrt(a, p):
    """Square root mod p using Tonelli-Shanks (works for any odd prime)."""
    if a % p == 0:
        return 0
    if pow(a, (p - 1) // 2, p) != 1:
        return None
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i = 1
        tmp = (t * t) % p
        while tmp != 1:
            tmp = (tmp * tmp) % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, (b * b) % p, (t * b * b) % p, (r * b) % p
    return r


G_SMALL = SmallPoint(4, 8)


def encode_char_to_point(m_val):
    """Koblitz encoding: find point with x near K_ENC*m on the small curve."""
    for j in range(K_ENC):
        x = K_ENC * m_val + j
        rhs = (x**3 + A_SMALL * x + B_SMALL) % P_SMALL
        y = small_sqrt(rhs, P_SMALL)
        if y is not None:
            return SmallPoint(x, y)
    return None


def decode_point_to_char(pt):
    """Reverse Koblitz encoding: point -> character value."""
    return pt.x // K_ENC
