"""SQLAlchemy ORM models.

Each entity gets its own module — ``app/models/user.py``,
``app/models/item.py``. Re-export the classes here so Alembic and
``app.db.base`` can discover them via a single import.
"""

from __future__ import annotations

from app.models.item import Item
from app.models.user import User

__all__ = ["User", "Item"]
