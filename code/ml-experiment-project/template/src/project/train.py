"""Fake training loop that demonstrates the run-directory pattern."""
import argparse
import json
import platform
import random
import subprocess
import sys
from datetime import date
from pathlib import Path

from project.config import load


def git_info() -> dict:
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], text=True, stderr=subprocess.DEVNULL).strip())
    except (OSError, subprocess.CalledProcessError):
        commit, dirty = "unknown", None
    return {"commit": commit, "dirty": dirty}


def run(config: dict, seed: int, name: str, runs_dir: Path = Path("runs")) -> Path:
    run_dir = runs_dir / f"{date.today().isoformat()}-{name}-s{seed}"
    run_dir.mkdir(parents=True, exist_ok=False)  # runs are immutable: never reuse an ID
    (run_dir / "config.resolved.json").write_text(json.dumps(config, indent=2))
    meta = {"seed": seed, "python": platform.python_version(), **git_info()}
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2))

    random.seed(seed)
    loss = 1.0
    with open(run_dir / "metrics.jsonl", "w") as f:
        for step in range(config["optim"]["steps"]):
            loss *= 1 - config["optim"]["learning_rate"] * random.random()
            f.write(json.dumps({"step": step, "train/loss": loss}) + "\n")
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    config = load(args.config)
    print(run(config, args.seed, Path(args.config).stem))


if __name__ == "__main__":
    sys.exit(main())
