"""Items router — endpoints for /api/v1/items."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.items import ItemRead

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemRead])
def list_items(db: Session = Depends(get_db)) -> list[ItemRead]:
    """Return a stub list of items. Replace with a real service call."""
    return [
        ItemRead(id=1, name="Widget", description="Sample item"),
    ]
