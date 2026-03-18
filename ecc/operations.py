from .algebra import mod_inverse, mod_sqrt
from .curves import SECP_P, SECP_N, Point


def point_add(p1: Point, p2: Point) -> Point:
    """Add two points on secp256k1."""
    if p1.is_infinity():
        return p2.copy()
    if p2.is_infinity():
        return p1.copy()

    if p1.x == p2.x:
        if (p1.y + p2.y) % SECP_P == 0:
            return Point()
        return point_double(p1)

    lam = ((p2.y - p1.y) * mod_inverse(p2.x - p1.x, SECP_P)) % SECP_P
    x3 = (lam * lam - p1.x - p2.x) % SECP_P
    y3 = (lam * (p1.x - x3) - p1.y) % SECP_P
    return Point(x3, y3)


def point_double(p: Point) -> Point:
    """Double a point on secp256k1 (tangent line method)."""
    if p.is_infinity() or p.y == 0:
        return Point()

    lam = (3 * p.x * p.x * mod_inverse(2 * p.y, SECP_P)) % SECP_P
    x3 = (lam * lam - 2 * p.x) % SECP_P
    y3 = (lam * (p.x - x3) - p.y) % SECP_P
    return Point(x3, y3)


def point_negate(p: Point) -> Point:
    """Negate: -P = (x, -y mod P)."""
    if p.is_infinity():
        return Point()
    return Point(p.x, (SECP_P - p.y) % SECP_P)


def scalar_mult(k: int, p: Point) -> Point:
    """Compute k * P using double-and-add. O(log k) operations."""
    if k == 0 or p.is_infinity():
        return Point()
    k = k % SECP_N
    if k == 0:
        return Point()

    result = Point()
    addend = p.copy()

    while k > 0:
        if k & 1:
            result = point_add(result, addend)
        addend = point_double(addend)
        k >>= 1

    return result


def serialize_compressed(p: Point) -> bytes:
    """Point -> 33-byte compressed public key."""
    prefix = 0x03 if (p.y & 1) else 0x02
    return bytes([prefix]) + p.x.to_bytes(32, "big")


def parse_compressed(data: bytes) -> Point:
    """33-byte compressed public key -> Point."""
    x = int.from_bytes(data[1:], "big")
    y2 = (pow(x, 3, SECP_P) + 7) % SECP_P
    y = mod_sqrt(y2, SECP_P)
    if (y & 1) != (data[0] == 0x03):
        y = SECP_P - y
    return Point(x, y)
