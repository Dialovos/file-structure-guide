"""OrderRepository port.

Defined as a Protocol so any class with the right shape satisfies
it — that includes in-memory fakes for unit tests and the
SQLAlchemy adapter in infrastructure/persistence/.
"""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from myservice.domain.models.order import Order


class OrderRepository(Protocol):
    """Persistence port for the Order aggregate."""

    def save(self, order: Order) -> None:
        """Insert or update an order."""

    def get(self, order_id: UUID) -> Order:
        """Return an order by id; raise LookupError if absent."""
