"""URLs for example_app.

Mounted by mysite/urls.py at ``/example/``. Add new routes here as
the app grows.
"""

from __future__ import annotations

from django.urls import path

from . import views

app_name = "example_app"

urlpatterns = [
    path("", views.index, name="index"),
]
