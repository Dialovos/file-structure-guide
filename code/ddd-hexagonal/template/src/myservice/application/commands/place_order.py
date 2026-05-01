"""PlaceOrder use case.

A thin orchestrator: build the aggregate using domain methods, save
via the repository port. No transport, no DB code; substitute a fake
repository in unit tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from myservice.domain.events.order_placed import OrderPlaced
from myservice.domain.models.order import Order, OrderLine
from myservice.domain.ports.order_repository import OrderRepository


@dataclass(frozen=True)
class PlaceOrderCommand:
    customer_id: UUID
    lines: tuple[tuple[str, int, Decimal], ...]


@dataclass
class PlaceOrder:
    """Use case: place an order for a customer."""

    repository: OrderRepository

    def execute(self, command: PlaceOrderCommand) -> OrderPlaced:
        if not command.lines:
            raise ValueError("an order must have at least one line")
        order = Order(customer_id=command.customer_id)
        for sku, quantity, unit_price in command.lines:
            order.add_line(sku, quantity, unit_price)
        self.repository.save(order)
        return OrderPlaced.now(
            order_id=order.id,
            customer_id=command.customer_id,
            total=order.total(),
        )
