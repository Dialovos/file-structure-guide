# Python src-layout — template

A `cp -r`-able starter for a PyPI-publishable Python library using the
modern `src/` layout, hatch as the build backend, and pytest for tests.
This template is configured to be one or two edits away from running.

## What to rename

Replace every occurrence of `mypackage` with your real package name
(`snake_case`, mandated by PEP 8 because the directory name *is* the
import path). Specifically:

- The directory `src/mypackage/` → `src/<your_pkg>/`.
- `pyproject.toml` — `[project] name`, `[project.scripts]`, and
  `[tool.hatch.build.targets.wheel] packages`.
- Imports inside `src/mypackage/` (use your editor's rename-symbol).
- Imports in `tests/test_core.py`.
- The `mypackage` mentions in `README.md`.

## What to fill

- **`pyproject.toml`** — `description`, `authors`, `keywords`,
  `classifiers`, `dependencies`, `[project.urls]`. Bump the version
  when you cut a release; keep it in sync with `__version__` in
  `src/<pkg>/__init__.py`.
- **`LICENSE`** — replace `{{YEAR}}` and `{{NAME}}` (or pick a
  different license entirely; remember to update `[project] license`
  in `pyproject.toml`).
- **`README.md`** — the project-facing one (this file is template
  notes; the project README is at the same path level after you
  rename).
- **`src/<pkg>/core.py`** — replace the `greet()` stub with the real
  public API.
- **`tests/test_core.py`** — write tests for your real API.

## What to delete

- This `README.md` (template usage notes) once you've internalised it.
- The `greet()` stub and its tests once you have real code.
- `docs/.gitkeep` once `docs/` has real documentation.
- `.github/workflows/ci.yml` if you don't use GitHub Actions (or
  port it to your CI of choice).

## First run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

If `pytest` reports 3 passing tests, the layout is wired correctly
and you can start replacing stubs with real code.

## Pair this with

- `../GUIDE.md` — the full reasoning behind src-layout.
- `../../python-flat-layout/` — the simpler alternative for apps you
  don't publish.
- `../../cli-tool/` — for single-binary CLIs that don't justify a
  full library layout.
