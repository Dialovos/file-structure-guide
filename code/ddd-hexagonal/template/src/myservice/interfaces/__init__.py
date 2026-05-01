"""Interfaces — entry points (HTTP, CLI, worker).

Each transport lives in its own subpackage and constructs its own
composition root. Adding a new transport never touches domain or
application.
"""
