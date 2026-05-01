"""URL configuration for mysite."""

from __future__ import annotations

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("example/", include("apps.example_app.urls")),
]
