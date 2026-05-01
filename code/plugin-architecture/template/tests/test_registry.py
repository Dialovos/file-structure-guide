"""Smoke tests for the registry.

These exercise the in-tree discovery path with the bundled audio /
video plugins. External entry-point plugins are integration-tested
elsewhere.
"""

from __future__ import annotations

from core import Plugin
from core.registry import discover, load


def test_discover_finds_bundled_plugins() -> None:
    names = {info.name for info in discover()}
    # At least the in-tree audio + video plugins must be visible.
    assert "audio" in names
    assert "video" in names


def test_load_returns_plugin_instance() -> None:
    plugin = load("audio")
    assert isinstance(plugin, Plugin)
    assert plugin.name() == "audio"


def test_load_unknown_plugin_raises() -> None:
    try:
        load("does-not-exist")
    except LookupError:
        return
    raise AssertionError("expected LookupError for unknown plugin")
