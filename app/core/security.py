import hashlib
import secrets


def _hash_with_salt(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        390000,
    ).hex()


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    derived = _hash_with_salt(password, salt)
    return f"{salt}${derived}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, digest = stored_hash.split("$", 1)
    except ValueError:
        return False
    candidate = _hash_with_salt(password, salt)
    return secrets.compare_digest(candidate, digest)
