# Python flat-layout — template

A `cp -r`-able starter for a Python application or small project where
the package directory sits at the repo root, next to `pyproject.toml`.
Use this for apps you don't ship to PyPI; for libraries you publish,
prefer the [src-layout](../../python-src-layout/).

## What to rename

Replace every occurrence of `mypackage` with your real package name
(`snake_case`, mandated by PEP 8 because the directory name *is* the
import path). Specifically:

- The directory `mypackage/` → `<your_pkg>/`.
- `pyproject.toml` — `[project] name`, `[project.scripts]`, and
  `[tool.hatch.build.targets.wheel] packages`.
- Imports inside `mypackage/` and inside `tests/test_core.py`.

## What to fill

- **`pyproject.toml`** — `description`, `authors`, `dependencies`,
  classifiers. Bump the version with releases; keep it in sync with
  `__version__` in `mypackage/__init__.py`.
- **`LICENSE`** — replace `{{YEAR}}` and `{{NAME}}`, or pick another
  license and update `[project] license` accordingly.
- **`mypackage/core.py`** — replace `greet()` with real logic.
- **`tests/test_core.py`** — write tests for that real logic.

## What to delete

- This `README.md` (template usage notes) once you have your own.
- The `greet()` stub and its tests when you have real code.

## First run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
mypackage Ada     # exercises the CLI entry point
```

You can also run tests without installing — flat-layout puts the
package on `sys.path` automatically when pytest is invoked from the
repo root. Installing is still recommended so the `mypackage` console
script works.

## When to upgrade to src-layout

- You start publishing to PyPI.
- You add a CI step that builds and installs the wheel.
- You add tox or nox for multi-version testing.

See `../../python-src-layout/GUIDE.md` for the migration steps.

## Pair this with

- `../GUIDE.md` — the full reasoning behind flat-layout.
- `../../python-src-layout/` — when you outgrow flat-layout.
- `../../django-project/` — Django-flavored flat-layout for full sites.
- `../../fastapi-project/` — FastAPI-flavored layered layout for APIs.
