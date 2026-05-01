"""SQLAlchemy adapter implementing OrderRepository.

This is the *only* place SQLAlchemy lives. The mapping translates
between rows and the domain Order aggregate; the domain class itself
has no SQLAlchemy imports.
"""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import Column, ForeignKey, Numeric, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy.types import Uuid

from myservice.domain.models.order import Order, OrderLine
from myservice.domain.ports.order_repository import OrderRepository


class _Base(DeclarativeBase):
    pass


class _OrderRow(_Base):
    __tablename__ = "orders"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    customer_id: Mapped[UUID] = mapped_column(Uuid)
    status: Mapped[str] = mapped_column(String, default="pending")
    lines = relationship("_OrderLineRow", cascade="all, delete-orphan")


class _OrderLineRow(_Base):
    __tablename__ = "order_lines"
    order_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("orders.id"), primary_key=True)
    sku: Mapped[str] = mapped_column(String, primary_key=True)
    quantity: Mapped[int] = mapped_column()
    unit_price = Column(Numeric(scale=4))


class SqlAlchemyOrderRepository(OrderRepository):
    """Implements OrderRepository on top of a SQLAlchemy Session."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, order: Order) -> None:
        row = _OrderRow(id=order.id, customer_id=order.customer_id, status=order.status)
        row.lines = [
            _OrderLineRow(
                order_id=order.id,
                sku=line.sku,
                quantity=line.quantity,
                unit_price=line.unit_price,
            )
            for line in order.lines
        ]
        self._session.merge(row)
        self._session.commit()

    def get(self, order_id: UUID) -> Order:
        row = self._session.get(_OrderRow, order_id)
        if row is None:
            raise LookupError(f"order {order_id} not found")
        order = Order(id=row.id, customer_id=row.customer_id, status=row.status)
        order.lines = [
            OrderLine(sku=line.sku, quantity=line.quantity, unit_price=Decimal(str(line.unit_price)))
            for line in row.lines
        ]
        return order


def make_engine(url: str):
    """Convenience helper for the composition root."""
    return create_engine(url, future=True)
