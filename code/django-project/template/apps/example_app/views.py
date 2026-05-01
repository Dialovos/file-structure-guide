"""Views for example_app."""

from __future__ import annotations

from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    """Minimal placeholder view. Replace with real templates and logic."""
    return HttpResponse("example_app is wired up. Replace this view.")
