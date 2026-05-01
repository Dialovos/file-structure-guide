"""FastAPI adapter — composition root for the HTTP transport.

This module knows about the framework, the database, and the
application layer; it is the only place that imports across all
three. Keep it thin: build wiring, mount routers, return the app.
"""

from __future__ import annotations

from fastapi import FastAPI
from sqlalchemy.orm import Session, sessionmaker

from myservice.application.commands.place_order import PlaceOrder
from myservice.infrastructure.persistence.sqlalchemy_order_repo import (
    SqlAlchemyOrderRepository,
    make_engine,
)


def build_app(database_url: str = "sqlite:///./local.db") -> FastAPI:
    engine = make_engine(database_url)
    SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine)

    app = FastAPI(title="myservice")

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/orders")
    def create_order(payload: dict) -> dict:  # pragma: no cover - stub
        # The interfaces/api/ layer would parse a Pydantic model here
        # and call PlaceOrder. This stub illustrates the wiring shape.
        with SessionLocal() as session:
            repo = SqlAlchemyOrderRepository(session)
            use_case = PlaceOrder(repository=repo)
            # event = use_case.execute(...)
        return {"received": True}

    return app
