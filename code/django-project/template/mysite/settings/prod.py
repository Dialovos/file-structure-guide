"""Production settings — environment-driven, secrets-free in source.

Imported via ``DJANGO_SETTINGS_MODULE=mysite.settings.prod``. Every
sensitive value is read from environment variables; do not commit
secrets here.
"""

from __future__ import annotations

import os

from .base import *  # noqa: F401,F403


def _required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


DEBUG = False

SECRET_KEY = _required("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

# Postgres connection via DATABASE_URL is the usual prod choice; here
# we keep the shape simple and let the operator wire psycopg / dj-database-url.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _required("POSTGRES_DB"),
        "USER": _required("POSTGRES_USER"),
        "PASSWORD": _required("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30  # 30 days; raise once you trust HTTPS everywhere
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
