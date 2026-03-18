def mod_inverse(a: int, p: int) -> int:
    """a^-1 mod p via Fermat's little theorem: a^(p-2) mod p."""
    return pow(a, p - 2, p)


def mod_sqrt(a: int, p: int) -> int:
    """sqrt(a) mod p for p = 3 (mod 4): a^((p+1)/4) mod p."""
    return pow(a, (p + 1) // 4, p)


def is_quadratic_residue(n: int, p: int) -> bool:
    """True if n is a quadratic residue mod p (Euler's criterion)."""
    if n % p == 0:
        return True
    return pow(n, (p - 1) // 2, p) == 1
