"""Host package — defines the plugin contract and the registry.

The host should never import a specific plugin. Use registry.discover()
and registry.load() to obtain Plugin instances.
"""

from core.plugin_api import API_VERSION, Plugin

__all__ = ["API_VERSION", "Plugin"]
