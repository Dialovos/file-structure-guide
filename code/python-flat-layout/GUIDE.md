## TL;DR

The **flat layout** puts the importable package directly at the repo root: `mypackage/__init__.py` next to `pyproject.toml`. No `src/` indirection, no extra level. The repo *is* the import path. This is the simpler of the two canonical Python layouts and the right default for **applications you don't publish to PyPI** — Django sites, FastAPI services, internal tools, single-file CLIs that grew. The cost: `python -c "import mypackage"` from the repo root works without installing, which sounds nice but hides packaging bugs (missing files in the wheel, wrong includes). For apps you ship as a wheel, that hidden bug is real and worth avoiding — switch to [src-layout](../python-src-layout/). For everything else, flat is fine and friendlier. The PyPA tutorial calls flat-layout "appropriate for some non-package projects, applications, scripts, and similar"; that's where it lives.

## Principles & why

The flat layout commits to one trade.

1. **Source root = import root.** `mypackage/` at the repo root means `python -c "import mypackage"` works the second you `cd` into the repo. No editable install required for one-off scripts. Lower friction for newcomers, lower friction for `python script.py` tooling.
2. **No protection against packaging-config drift.** Because the import works without installing, your tests, examples, and CI never exercise the wheel. If `pyproject.toml` is missing a subpackage, your tests still pass — they read from the working tree, not the install. This is fine when you don't ship a wheel; harmful when you do.

That second point is the entire reason src-layout exists. If you ship to PyPI, the flat layout's friendliness becomes a footgun. If you don't ship, the friendliness is just friendliness.

The flat layout is also **friendlier to scripts and tooling** that import the package by sitting next to it. A `dev_helpers.py` at the repo root can `import mypackage` and start working. With src-layout, that same script needs the package installed first.

For Django, the layout meshes with `manage.py` conventions: `manage.py` at the root, the project package next to it. For FastAPI, the layout meshes with `uvicorn app.main:app` from the repo root.

The current PyPA stance: flat-layout is appropriate for non-libraries; src-layout is the default for libraries. This guide sticks to that line.

## When to use

- **Apps you don't publish.** Django sites, FastAPI services, Flask apps, scripts. The wheel-correctness benefit of src-layout doesn't apply, so claim the simplicity dividend.
- **Single-file CLI tools that grew into a package.** Going from `mytool.py` to `mytool/{__init__,core,cli}.py` is a one-step refactor in flat-layout.
- **Internal tools at companies** that get installed via `pip install -e .` from a checkout, never from a registry. Packaging-correctness still matters for editable installs but the bar is lower.
- **Tutorial code, demo repos, conference-talk code** — readers can `git clone` and `python -m mypackage` immediately, no install dance.
- **Notebook-driven research** when you've grown past a single notebook but still want `import mypackage` to work from a sibling `.ipynb`.

## When NOT to use

- **Anything published to PyPI.** Flat-layout hides packaging bugs that bite downstream users on `pip install`. Use src-layout.
- **Multi-developer libraries** where the team would benefit from the structural guarantee that tests run against the install.
- **Projects using tox or nox** that test against multiple Python versions in ephemeral envs. Tox installs the package; flat-layout's "import works without install" advantage evaporates and you're left with src-layout's discipline missing.
- **Libraries with namespace packages** or non-trivial `package_data`. Both are exactly the cases src-layout protects you against.
- **Anything where `dev_script.py` at the repo root accidentally importing your package would be a bug.** Flat-layout enables that import; src-layout blocks it.

## Tree diagram

```
mypackage/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── mypackage/
│   ├── __init__.py
│   ├── core.py
│   └── cli.py
└── tests/
    └── test_core.py
```

## Naming rules

- **Package directory**: `snake_case` per PEP 8 — `mypackage/` or `my_package/`, never `my-package/`. Same exception as src-layout, same reason: directory name is the import path. Documented in `principles/naming-conventions/`.
- **Repo / outer directory** can be anything — kebab-case (`my-package/`) is fine; the outer name is decoupled from the import name.
- **Module filenames**: `snake_case.py`. `cli.py`, `http_client.py`, never `cli-main.py`.
- **`__init__.py`** is required to make `mypackage/` an importable package.
- **`tests/` is not a package** by default; tests are discovered by pytest collection. Add `tests/__init__.py` only if you have strong reasons (e.g. shared test helpers imported across files).
- **Distribution name** in `pyproject.toml` (`name = "mypackage"`) typically matches the import name. Keep them aligned to avoid surprises when users `pip install` a different name from what they `import`.

## Anti-patterns

- **Two top-level packages at the repo root.** `mypackage/` and `myhelper/` next to each other usually means you wanted a single package with a sub-package, or two repos. Decide.
- **Tests as a top-level package without `__init__.py`** but with `tests/__init__.py` in some subdirs and not others. Pytest can cope; humans can't. Pick one convention.
- **Mixing the package directory with unrelated repo content.** Keep `mypackage/` clean — no `notes.txt`, no scratch files. Use `scripts/` or `tools/` for ad-hoc helpers.
- **Letting `dev_script.py` at the repo root grow into a parallel "package."** Either move it inside `mypackage/` or put it in `scripts/`. Top-level Python files at the repo root are siren songs.
- **Publishing flat-layout to PyPI without checking the wheel.** Build the wheel, install it into a fresh venv, run the test suite against the install. If anything breaks, you needed src-layout.
- **`from mypackage import *`** inside `__init__.py` to re-export everything. It works in flat-layout (and src-layout), it's still a bad idea — be explicit about your public API.

## Variants

- **flat-with-tests-dir** (this guide) — the default; `tests/` next to the package.
- **flat-with-co-located-tests** — `mypackage/tests/test_core.py`. Useful when the package is meant to be importable *with* its tests, e.g. for downstream re-use of test fixtures. Rare.
- **flat-without-tests-dir** — single-file or two-file CLIs where a `tests/` directory is overkill. Add tests inline (`test_*.py` next to source files) or as you grow.
- **flat-monorepo** — multiple flat packages next to each other in one repo (`mypackage/`, `mytool/`, `myservice/`). Workable for internal tools; PyPI publishing of multiple packages from one repo is a separate problem (see Hatch / setuptools workspace docs).
- **Django flat-layout** — Django's `startproject` template is a flat layout with `manage.py` at the root. See `code/django-project/` for the larger app-per-feature variant.

## Real-world projects using this

- **Flask** (early versions) — flat-layout, package at the repo root. Migrated closer to src-layout in modern releases.
- **Werkzeug** (older) — flat-layout for years before adopting src.
- **Many Django apps and FastAPI services** in the wild — flat-layout is the default the framework docs assume.
- **Internal tools at companies** — overwhelmingly flat-layout because they're never published. Pick any company's open-source `awesome-tools` repo and you'll usually find this layout.
- **The cookiecutter `pypackage-minimal` template** (and its descendants) — flat-layout starter for small Python projects that don't yet justify src.
- **Most "my first Python project" tutorials** — flat-layout, because it's simpler to teach.

## Migration & references

- **From single-file `script.py`**: create `mypackage/`, move logic into `mypackage/core.py`, add `mypackage/__init__.py` (can re-export `from .core import *` or be explicit), add `pyproject.toml` with `name = "mypackage"`. Add `tests/test_core.py`. The migration is mechanical and reversible.
- **From flat to src** (when you decide to publish): create `src/`, `git mv mypackage/ src/mypackage/`, update `pyproject.toml` build-target to point at `src/mypackage`, run `pip install -e .` and re-run tests. Fix any `ModuleNotFoundError`s — they reveal hidden working-tree imports you should own.
- **From "scripts at the root" sprawl**: gather scripts into `scripts/` or `tools/`, leave only the package and `pyproject.toml` next to each other. The repo becomes navigable.
- **References**:
  - PyPA Packaging User Guide — *src layout vs flat layout*.
  - Hynek Schlawack — *Python application layouts: A reference*.
  - Sibling guides: `code/python-src-layout/` (when to upgrade), `code/django-project/` (Django-flavored flat-layout), `code/fastapi-project/` (FastAPI-flavored layered layout), `code/cli-tool/` (when one file is enough).
  - Naming exception: `principles/naming-conventions/`, "Python packages" section.
