"""Models for example_app.

Replace these stubs with real domain models. Run
``python manage.py makemigrations`` after every model change.
"""

from __future__ import annotations

from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
