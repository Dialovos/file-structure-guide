"""FastAPI application entry point.

Run with::

    uvicorn app.main:app --reload

Keep this file thin: build the FastAPI instance, include the
versioned API router, register lifespan events. Push everything
else into ``app/core/``, ``app/api/``, or ``app/services/``.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.api.v1 import api_router as v1_router
from app.core.config import settings


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )
    application.include_router(v1_router, prefix="/api/v1")
    return application


app = create_app()


@app.get("/healthz", tags=["health"])
def healthz() -> dict[str, str]:
    """Liveness probe. Replace with real readiness logic if needed."""
    return {"status": "ok"}
