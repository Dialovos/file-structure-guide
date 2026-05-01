# Plugin architecture — template

A `cp -r`-able starter for an extensible host with a small, stable
plugin contract. The host (`core/`) defines the abstract `Plugin`
class and a registry that discovers plugins via two paths:
`importlib.metadata.entry_points` for plugins shipped as separate
distributions, and an in-tree scan of `plugins/<name>/plugin.toml`
for development and bundled defaults.

## What to rename

- `myhost` → your host name in `pyproject.toml`, the entry-points
  group (`[project.entry-points."myhost.plugins"]`), the
  `ENTRY_POINT_GROUP` constant in `core/registry.py`, and any
  references in plugin manifests.
- `audio` and `video` are placeholder bundled plugins; replace with
  your real first plugins or remove them.
- The `Plugin` class name in `core/plugin_api.py` can stay generic
  or become `<HostName>Plugin` if `Plugin` collides in your domain.

## What to fill

- **`core/plugin_api.py`** — add the methods plugins must implement.
  Bump `API_VERSION` when you change a signature.
- **`core/registry.py`** — extend with caching, sandboxing, or
  capability-based filtering as needs grow. The current shape is
  the minimum.
- **`plugins/<name>/plugin.toml`** — add fields for any host-specific
  metadata (license, homepage, supported file types).
- **`tests/test_registry.py`** — add tests that exercise your real
  plugin behaviour, not just discovery.

## What to delete

- This `README.md` once you have a real one.
- The bundled `audio` / `video` plugins once your real plugins land.

## First run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

Inspect what's discovered:

```bash
python -c "from core.registry import discover; \
           print([p.name for p in discover()])"
```

## Layout cheat-sheet

| You're looking for…             | Path                                  |
|---------------------------------|---------------------------------------|
| Plugin contract (ABC)           | `core/plugin_api.py`                  |
| Discovery + loading             | `core/registry.py`                    |
| Bundled plugin example          | `plugins/audio/audio_plugin.py`       |
| Plugin manifest format          | `plugins/audio/plugin.toml`           |
| External plugin registration    | `pyproject.toml` (entry-points group) |
| Tests                           | `tests/test_registry.py`              |

## Pair this with

- `../GUIDE.md` — full reasoning behind the layout.
- `../python-src-layout/` — when the host itself becomes a
  publishable distribution.
- `../cli-tool/` — for plugin-driven CLIs.
- `../../principles/depth-vs-breadth/` — why one folder per plugin
  beats one giant `plugins.py`.
