"""Reusable FastAPI dependencies.

Anything injected via ``Depends(...)`` should live here. Keep the
file flat: one function per dependency, no classes unless required.
"""

from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Iterator[Session]:
    """Yield a SQLAlchemy session and ensure it's closed.

    Override this dependency in tests to bind to a transactional
    session that rolls back after each test.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
