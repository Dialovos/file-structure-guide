"""Bundled audio plugin — minimal example."""

from __future__ import annotations

from core.plugin_api import Plugin


class AudioPlugin(Plugin):
    """Stub audio plugin demonstrating the contract.

    Replace `run` with the real audio pipeline (decode/encode/etc.).
    Use `setup`/`teardown` for resource acquisition.
    """

    def name(self) -> str:
        return "audio"

    def run(self) -> None:  # pragma: no cover - stub
        # Real implementation would decode/encode an audio stream.
        return None
