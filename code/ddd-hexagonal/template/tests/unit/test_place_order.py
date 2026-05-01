"""Unit test for the PlaceOrder use case.

No DB, no HTTP — a fake repository that satisfies the OrderRepository
port is enough. This is the payoff of hexagonal: domain + application
unit tests are pure-Python and millisecond-fast.
"""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID, uuid4

from myservice.application.commands.place_order import PlaceOrder, PlaceOrderCommand
from myservice.domain.models.order import Order
from myservice.domain.ports.order_repository import OrderRepository


class FakeOrderRepository(OrderRepository):
    """In-memory fake satisfying the OrderRepository port."""

    def __init__(self) -> None:
        self._store: dict[UUID, Order] = {}

    def save(self, order: Order) -> None:
        self._store[order.id] = order

    def get(self, order_id: UUID) -> Order:
        try:
            return self._store[order_id]
        except KeyError as exc:
            raise LookupError(str(order_id)) from exc


def test_place_order_persists_and_emits_event() -> None:
    repo = FakeOrderRepository()
    use_case = PlaceOrder(repository=repo)
    command = PlaceOrderCommand(
        customer_id=uuid4(),
        lines=(("SKU-1", 2, Decimal("9.99")),),
    )

    event = use_case.execute(command)

    assert event.customer_id == command.customer_id
    assert event.total == Decimal("19.98")
    saved = repo.get(event.order_id)
    assert saved.total() == Decimal("19.98")
