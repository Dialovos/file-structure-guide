"""Ports — interfaces the domain needs the outside world to provide.

Ports live with the domain because the domain *defines its needs*.
Adapters in infrastructure/ implement them. The application layer
consumes ports; the composition root injects adapters.
"""
