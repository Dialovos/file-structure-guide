"""Starter tests for the users router.

Uses FastAPI's TestClient to drive the app in-process. Replace the
stub assertions once you have real endpoints and services.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz_ok() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_read_user_stub() -> None:
    response = client.get("/api/v1/users/1")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["email"] == "ada@example.com"


def test_read_user_not_found() -> None:
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404
