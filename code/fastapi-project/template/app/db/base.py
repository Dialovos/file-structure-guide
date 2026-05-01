"""SQLAlchemy declarative base.

All ORM models inherit from ``Base``. Importing
``app.models`` once is enough to register every model with
``Base.metadata``, which is what Alembic introspects.
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Project-wide declarative base."""
