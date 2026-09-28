"""Load base config, merge an experiment file, apply overrides."""
import tomllib
from pathlib import Path


def merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = merge(out[key], value)
        else:
            out[key] = value
    return out


def load(experiment: str | Path, base: str | Path = "configs/base.toml") -> dict:
    with open(base, "rb") as f:
        cfg = tomllib.load(f)
    with open(experiment, "rb") as f:
        return merge(cfg, tomllib.load(f))
