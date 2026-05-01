"""SQLAlchemy engine and session factory.

The engine is bound to ``settings.database_url``. ``SessionLocal`` is
the per-request session factory used by ``app.api.deps.get_db``.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
)
