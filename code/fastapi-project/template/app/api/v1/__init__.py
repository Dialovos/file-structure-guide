"""v1 API router — composes resource routers under one prefix."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.routers import items, users

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(items.router)
