"""Load a trained model and produce predictions.

Stub: replace with real inference. Mirrors train_model.py — both live
in src/project/models/ so notebooks can import either.
"""

from __future__ import annotations

from pathlib import Path


def predict(model_dir: Path = Path("models")) -> None:
    """Load model from MODEL_DIR and run predictions."""
    # Real implementation: load model artifact, load test data, predict.
    print(f"[predict_model] stub — would load model from {model_dir}")


if __name__ == "__main__":
    predict()
