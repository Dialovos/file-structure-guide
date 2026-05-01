"""Plugin contract.

This module defines the abstract base class that every plugin must
subclass. Bump API_VERSION on any backwards-incompatible change; the
registry rejects plugins targeting a different major version at load
time.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

API_VERSION = "1.0"


class Plugin(ABC):
    """Abstract base for all plugins loaded by the host.

    Subclasses must implement `name` and `run`. Override `setup` and
    `teardown` if you need lifecycle hooks; the defaults are no-ops so
    simple plugins stay short.
    """

    @abstractmethod
    def name(self) -> str:
        """Return a unique, human-readable name for this plugin."""

    @abstractmethod
    def run(self) -> None:
        """Execute the plugin's main behaviour."""

    def setup(self) -> None:
        """Called once after the plugin is loaded. Default: no-op."""

    def teardown(self) -> None:
        """Called once before the plugin is unloaded. Default: no-op."""
