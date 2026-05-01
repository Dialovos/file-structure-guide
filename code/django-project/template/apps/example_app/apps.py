"""AppConfig for example_app.

The ``name`` attribute uses the full dotted path (``apps.example_app``).
Renaming the app means updating this string and ``INSTALLED_APPS``.
"""

from __future__ import annotations

from django.apps import AppConfig


class ExampleAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.example_app"
    verbose_name = "Example App"
