"""Train a model from features and persist it to models/.

Stub: replace with real training. The flow is always
load -> fit -> evaluate -> persist.
"""

from __future__ import annotations

from pathlib import Path


def train_model(model_dir: Path = Path("models")) -> None:
    """Train and save a model under MODEL_DIR."""
    model_dir.mkdir(parents=True, exist_ok=True)
    # Real implementation: load features, fit estimator, save artifact.
    print(f"[train_model] stub — would persist a model under {model_dir}")


if __name__ == "__main__":
    train_model()
