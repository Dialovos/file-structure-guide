"""Plot helpers — used by notebooks; output goes to reports/figures/."""

from __future__ import annotations

from pathlib import Path


def save_figure(fig, name: str, figures_dir: Path = Path("reports/figures")) -> Path:
    """Save FIG to reports/figures/<name>.png and return the path.

    Stub: extend with date-prefixed naming if you want
    `2026-04-30-<name>.png` filenames.
    """
    figures_dir.mkdir(parents=True, exist_ok=True)
    out = figures_dir / f"{name}.png"
    # Real implementation: fig.savefig(out, dpi=200, bbox_inches="tight")
    return out
