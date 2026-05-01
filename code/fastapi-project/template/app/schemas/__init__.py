"""Pydantic request/response schemas.

Schemas describe the wire shape; they are *not* SQLAlchemy models.
Keep them per-resource and use Create / Read / Update suffixes so
router signatures self-document.
"""
