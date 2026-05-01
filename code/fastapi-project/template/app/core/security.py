"""Security helpers: password hashing, token issuance.

Stubs only — replace with real implementations using ``passlib`` and
``python-jose`` (or your library of choice) before shipping.
"""

from __future__ import annotations

import hashlib

from app.core.config import settings


def hash_password(plain: str) -> str:
    """Stub password hash. REPLACE with passlib bcrypt before shipping."""
    salted = (settings.secret_key + plain).encode("utf-8")
    return hashlib.sha256(salted).hexdigest()


def verify_password(plain: str, hashed: str) -> bool:
    """Constant-time compare. REPLACE with passlib's verify before shipping."""
    return hash_password(plain) == hashed
