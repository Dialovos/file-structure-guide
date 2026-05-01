"""Order aggregate — pure domain.

No imports from infrastructure or interfaces. Behaviour lives on the
entity (`mark_paid`, `total`); use cases orchestrate but do not
compute.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Iterable
from uuid import UUID, uuid4


@dataclass
class OrderLine:
    sku: str
    quantity: int
    unit_price: Decimal


@dataclass
class Order:
    """Aggregate root for an order."""

    id: UUID = field(default_factory=uuid4)
    customer_id: UUID | None = None
    lines: list[OrderLine] = field(default_factory=list)
    status: str = "pending"

    def add_line(self, sku: str, quantity: int, unit_price: Decimal) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        self.lines.append(OrderLine(sku=sku, quantity=quantity, unit_price=unit_price))

    def total(self) -> Decimal:
        return sum((line.quantity * line.unit_price for line in self.lines), Decimal("0"))

    def mark_paid(self) -> None:
        if self.status not in {"pending", "awaiting_payment"}:
            raise ValueError(f"cannot mark paid from status {self.status!r}")
        self.status = "paid"

    @classmethod
    def from_lines(cls, customer_id: UUID, lines: Iterable[OrderLine]) -> "Order":
        order = cls(customer_id=customer_id)
        order.lines = list(lines)
        return order
