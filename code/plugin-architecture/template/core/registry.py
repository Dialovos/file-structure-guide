"""Plugin discovery and loading.

Two discovery paths are supported:

1. Entry points (``importlib.metadata.entry_points`` for the group
   ``myhost.plugins``). This is how plugins shipped as separate
   distributions register themselves.
2. In-tree fallback that scans ``plugins/<name>/plugin.toml`` siblings
   of the host. This is the development-mode path and the default for
   bundled plugins.

Both paths produce the same ``PluginInfo`` shape so the host code
never has to know the difference.
"""

from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Iterable

if sys.version_info >= (3, 11):
    import tomllib  # type: ignore[import-not-found]
else:  # pragma: no cover - py3.10 fallback
    import tomli as tomllib  # type: ignore[import-not-found]

from core.plugin_api import Plugin

ENTRY_POINT_GROUP = "myhost.plugins"
PLUGINS_DIR = Path(__file__).resolve().parent.parent / "plugins"


@dataclass(frozen=True)
class PluginInfo:
    """Metadata about a discoverable plugin (without importing it)."""

    name: str
    version: str
    entry_point: str  # "module:Class"
    capabilities: tuple[str, ...] = ()


def discover() -> list[PluginInfo]:
    """Return every plugin found via entry points and the in-tree scan.

    Entry points win on name collisions; the in-tree scan is the
    fallback for development. Discovery is cheap: no plugin code is
    executed here.
    """
    seen: dict[str, PluginInfo] = {}
    for info in _discover_entry_points():
        seen[info.name] = info
    for info in _discover_in_tree():
        seen.setdefault(info.name, info)
    return sorted(seen.values(), key=lambda p: p.name)


def load(name: str) -> Plugin:
    """Import the plugin module, instantiate its class, and return it.

    Failures are isolated: one bad plugin raises here but does not
    affect any other plugin returned by ``discover()``.
    """
    for info in discover():
        if info.name == name:
            module_path, _, class_name = info.entry_point.partition(":")
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            instance = cls()
            if not isinstance(instance, Plugin):
                raise TypeError(
                    f"plugin {name!r} does not implement core.Plugin"
                )
            return instance
    raise LookupError(f"no plugin registered as {name!r}")


def _discover_entry_points() -> Iterable[PluginInfo]:
    eps = metadata.entry_points()
    if hasattr(eps, "select"):
        group = eps.select(group=ENTRY_POINT_GROUP)
    else:  # pragma: no cover - py<3.10 shape
        group = eps.get(ENTRY_POINT_GROUP, [])
    for ep in group:
        yield PluginInfo(
            name=ep.name,
            version=getattr(ep.dist, "version", "0.0.0") if ep.dist else "0.0.0",
            entry_point=ep.value,
        )


def _discover_in_tree() -> Iterable[PluginInfo]:
    if not PLUGINS_DIR.is_dir():
        return
    for child in PLUGINS_DIR.iterdir():
        manifest = child / "plugin.toml"
        if not manifest.is_file():
            continue
        with manifest.open("rb") as fh:
            data = tomllib.load(fh)
        plugin = data.get("plugin", {})
        name = plugin.get("name")
        entry_point = plugin.get("entry_point")
        if not name or not entry_point:
            continue
        yield PluginInfo(
            name=name,
            version=plugin.get("version", "0.0.0"),
            entry_point=entry_point,
            capabilities=tuple(plugin.get("capabilities", ())),
        )
