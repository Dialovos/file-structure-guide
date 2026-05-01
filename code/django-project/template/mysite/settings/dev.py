"""Development settings — local-only overrides.

Imported via ``DJANGO_SETTINGS_MODULE=mysite.settings.dev``. Default
in ``manage.py``. Never used in production.
"""

from __future__ import annotations

from .base import *  # noqa: F401,F403

DEBUG = True

# Development convenience only — never use in production.
SECRET_KEY = "django-insecure-dev-key-replace-me"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE  # noqa: F405

INTERNAL_IPS = ["127.0.0.1"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
