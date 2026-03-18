import hashlib
import secrets

from .algebra import mod_sqrt
from .curves import SECP_P, SECP_N, G, Point
from .operations import point_add, scalar_mult


def tagged_hash(tag: str, data: bytes) -> bytes:
    """BIP340 tagged hash: SHA256(SHA256(tag) || SHA256(tag) || data)."""
    tag_hash = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(tag_hash + tag_hash + data).digest()


# ---------------------------------------------------------------------------
# ECDSA
# ---------------------------------------------------------------------------

def ecdsa_sign(message: bytes, private_key: int) -> tuple:
    """Generate ECDSA signature (r, s)."""
    z = int.from_bytes(hashlib.sha256(message).digest(), "big")

    while True:
        k = secrets.randbelow(SECP_N - 1) + 1
        R = scalar_mult(k, G)
        r = R.x % SECP_N
        if r == 0:
            continue

        k_inv = pow(k, SECP_N - 2, SECP_N)
        s = (k_inv * (z + r * private_key)) % SECP_N
        if s == 0:
            continue

        return (r, s)


def ecdsa_verify(message: bytes, signature: tuple, public_key: Point) -> bool:
    """Verify ECDSA signature."""
    r, s = signature
    z = int.from_bytes(hashlib.sha256(message).digest(), "big")

    s_inv = pow(s, SECP_N - 2, SECP_N)
    u1 = (z * s_inv) % SECP_N
    u2 = (r * s_inv) % SECP_N

    R_prime = point_add(scalar_mult(u1, G), scalar_mult(u2, public_key))
    return R_prime.x % SECP_N == r


# ---------------------------------------------------------------------------
# Schnorr (BIP 340)
# ---------------------------------------------------------------------------

def schnorr_sign(message: bytes, private_key: int) -> bytes:
    """Simplified BIP340 Schnorr signature -> 64-byte bytes."""
    P = scalar_mult(private_key, G)
    d = private_key if P.y % 2 == 0 else SECP_N - private_key

    aux = secrets.token_bytes(32)
    t = int.from_bytes(aux, "big") ^ d
    k_bytes = tagged_hash(
        "BIP0340/nonce",
        t.to_bytes(32, "big") + P.x.to_bytes(32, "big") + message,
    )
    k = int.from_bytes(k_bytes, "big") % SECP_N
    if k == 0:
        raise ValueError("k is zero")

    R = scalar_mult(k, G)
    if R.y % 2 != 0:
        k = SECP_N - k
        R = scalar_mult(k, G)

    e_bytes = tagged_hash(
        "BIP0340/challenge",
        R.x.to_bytes(32, "big") + P.x.to_bytes(32, "big") + message,
    )
    e = int.from_bytes(e_bytes, "big") % SECP_N

    s = (k + e * d) % SECP_N
    return R.x.to_bytes(32, "big") + s.to_bytes(32, "big")


def schnorr_verify(message: bytes, signature: bytes, pubkey_x: int) -> bool:
    """Simplified BIP340 Schnorr verification."""
    R_x = int.from_bytes(signature[:32], "big")
    s = int.from_bytes(signature[32:], "big")

    y2 = (pow(pubkey_x, 3, SECP_P) + 7) % SECP_P
    y = mod_sqrt(y2, SECP_P)
    if y % 2 != 0:
        y = SECP_P - y
    P = Point(pubkey_x, y)

    e_bytes = tagged_hash(
        "BIP0340/challenge",
        R_x.to_bytes(32, "big") + pubkey_x.to_bytes(32, "big") + message,
    )
    e = int.from_bytes(e_bytes, "big") % SECP_N

    lhs = scalar_mult(s, G)

    R_y2 = (pow(R_x, 3, SECP_P) + 7) % SECP_P
    R_y = mod_sqrt(R_y2, SECP_P)
    if R_y % 2 != 0:
        R_y = SECP_P - R_y
    R = Point(R_x, R_y)

    rhs = point_add(R, scalar_mult(e, P))
    return lhs == rhs


# ---------------------------------------------------------------------------
# DER encoding
# ---------------------------------------------------------------------------

def der_encode_integer(value: int) -> bytes:
    """Encode a positive integer in DER format (0x02 || length || bytes)."""
    b = value.to_bytes((value.bit_length() + 7) // 8, "big")
    if b[0] & 0x80:
        b = b"\x00" + b
    return bytes([0x02, len(b)]) + b


def der_encode_signature(r: int, s: int) -> bytes:
    """DER-encode an ECDSA signature: 0x30 || total_len || r_der || s_der."""
    r_der = der_encode_integer(r)
    s_der = der_encode_integer(s)
    body = r_der + s_der
    return bytes([0x30, len(body)]) + body


def low_s_normalize(s: int, N: int) -> int:
    """BIP 62: if s > N/2, replace with N - s."""
    if s > N // 2:
        return N - s
    return s
