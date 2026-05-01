"""RabbitMQ publisher adapter — stub.

Replace `publish` with a real `pika`/`aio_pika` call. The application
layer depends on an outbound port (`EventPublisher`); this is the
adapter implementing it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class RabbitPublisher:
    """Stub publisher; swap for a real pika/aio_pika integration."""

    exchange: str

    def publish(self, routing_key: str, payload: dict[str, Any]) -> None:  # pragma: no cover - stub
        # Real implementation would connect, declare the exchange, and publish.
        return None
