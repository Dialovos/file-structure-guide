"""OrderPlaced — domain event.

Past tense. Emitted by the domain when an order has been placed; the
application layer publishes it through an outbound port.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class OrderPlaced:
    order_id: UUID
    customer_id: UUID
    total: Decimal
    occurred_at: datetime

    @classmethod
    def now(cls, *, order_id: UUID, customer_id: UUID, total: Decimal) -> "OrderPlaced":
        return cls(
            order_id=order_id,
            customer_id=customer_id,
            total=total,
            occurred_at=datetime.now(timezone.utc),
        )
