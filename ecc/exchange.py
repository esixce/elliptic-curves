import hashlib
import hmac as hmac_lib

from .curves import SECP_N
from .operations import scalar_mult, serialize_compressed
from .curves import Point


def ecdh_shared_secret(my_private: int, their_public: Point) -> bytes:
    """ECDH: shared secret = SHA256(compress(my_private * their_public))."""
    shared_point = scalar_mult(my_private, their_public)
    compressed = serialize_compressed(shared_point)
    return hashlib.sha256(compressed).digest()


def generate_key(shared_secret: bytes, key_type: str) -> bytes:
    """Derive a specific key from shared secret (BOLT #4 key derivation)."""
    return hmac_lib.new(key_type.encode(), shared_secret, hashlib.sha256).digest()


def blind_ephemeral(ephemeral_pub: Point, shared_secret: bytes) -> Point:
    """Blind ephemeral key so next hop can't link it to previous hop."""
    pub_bytes = serialize_compressed(ephemeral_pub)
    blind_bytes = hashlib.sha256(pub_bytes + shared_secret).digest()
    blind_factor = int.from_bytes(blind_bytes, "big") % SECP_N
    return scalar_mult(blind_factor, ephemeral_pub)
