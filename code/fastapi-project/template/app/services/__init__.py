"""Business-logic layer.

Services are framework-agnostic: they take a SQLAlchemy session and
Pydantic schemas, return models or schemas, and contain no FastAPI
imports. This makes them reusable from CLI scripts, Celery tasks,
and tests.
"""
