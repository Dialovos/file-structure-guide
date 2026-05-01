"""Bundled video plugin — minimal example."""

from __future__ import annotations

from core.plugin_api import Plugin


class VideoPlugin(Plugin):
    """Stub video plugin demonstrating the contract.

    Replace `run` with the real video pipeline. The bundled audio
    plugin is the simpler twin to read first.
    """

    def name(self) -> str:
        return "video"

    def run(self) -> None:  # pragma: no cover - stub
        # Real implementation would transcode a video stream.
        return None
