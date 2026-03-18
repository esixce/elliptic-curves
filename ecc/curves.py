from typing import Optional

# secp256k1 parameters

SECP_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
SECP_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
SECP_GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
SECP_GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
A_COEFF = 0
B_COEFF = 7


class Point:
    """A point on secp256k1 (or the point at infinity)."""

    def __init__(self, x: Optional[int] = None, y: Optional[int] = None):
        self.x = x
        self.y = y

    def is_infinity(self) -> bool:
        return self.x is None or self.y is None

    def copy(self) -> "Point":
        return Point(self.x, self.y)

    def __eq__(self, other):
        if self.is_infinity() and other.is_infinity():
            return True
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        if self.is_infinity():
            return "O (point at infinity)"
        return f"({hex(self.x)[:16]}..., {hex(self.y)[:16]}...)"


G = Point(SECP_GX, SECP_GY)
INFINITY = Point()
