## TL;DR

The **src-layout** puts your importable package one directory below the repo root, in `src/<package>/`. The repo root holds `pyproject.toml`, README, license, tests/, and tooling — never an importable package. The guarantee this buys you is invariant: tests, examples, and CI cannot accidentally import from your working tree. They can only import from the *installed* distribution. That single property is why this layout is the current PyPA recommendation for any library destined for PyPI. Hatch, Flit, and Poetry all support it natively. The cost is one extra directory level and a small habit change (`pip install -e .` is now mandatory before testing). The payoff is that your test runs catch packaging bugs the same day you introduce them, instead of two releases later when a downstream user reports `ImportError`. If you publish wheels, this is the default. If you don't publish, the simpler [flat-layout](../python-flat-layout/) is fine.

## Principles & why

The src-layout is one principle wearing two faces.

1. **Source is not the install.** The repo root is *not* importable as your package. To import the package, you must build/install it. This forces a clean separation between "files I'm editing" and "the artifact users get." Without this separation, a typo in a `setup.py`/`pyproject.toml` (forgetting a subpackage, missing `package_data`, wrong wheel target) goes undetected because `python -c "import mypackage"` from the repo root happens to work — until a user installs the wheel and discovers the missing module.
2. **Tests run against the installed package, not the working tree.** Combined with `pip install -e .` (editable install), tests still see your live edits, but through the *installed* import path. That means tests catch missing-file bugs that would otherwise ship.

The structural cost: one extra directory (`src/`). The structural payoff: a class of bugs is now impossible.

This layout also enforces **no top-level scripts pretending to be the package**. With src-layout, you cannot write `import mypackage` from a `dev_script.py` at the repo root unless `mypackage` is installed. That's a feature, not a bug — it pushes one-off scripts into `scripts/` or `tools/` where they belong.

The PyPA Packaging User Guide adopted src-layout as the recommended default in 2021. Hynek Schlawack's writeups (the *Python application layouts* series) document why. Pytest, attrs, and the jaraco family of libraries all use it. If you're publishing to PyPI in 2026, this is the table-stakes layout.

## When to use

- **Libraries you publish to PyPI.** The whole point. Buys you packaging-correctness on every test run.
- **Multi-developer projects** where import-path mistakes are expensive. The layout makes them impossible.
- **Anything tested with tox or nox.** Both tools install your package into ephemeral envs and run tests against the install — exactly what src-layout assumes.
- **Projects with C extensions or build steps** where "build artifacts must be present to import" needs to be enforced. Src-layout makes the dependency explicit.
- **OSS projects accepting outside contributions.** First-time contributors don't accidentally break packaging because they can't even run tests without `pip install -e .` first.

## When NOT to use

- **Single-file scripts and one-shot CLIs.** A script in `tools/` or `bin/` doesn't need a package, let alone a layout. See `cli-tool/`.
- **Apps you don't ship as a wheel** (FastAPI services, Django sites, internal tools). The flat layout is simpler and the packaging benefit doesn't apply. See `python-flat-layout/`.
- **Notebook-driven research projects.** Jupyter workflows expect to `import mypackage` from the repo root with `sys.path` tricks; src-layout fights that. Use `jupyter-research/` or `cookiecutter-data-science/`.
- **Tutorials and learning projects** where the extra directory is pedagogical noise. Use the flat layout, learn the concepts, then graduate to src-layout when you publish.
- **Tiny utilities (≤200 LOC, one module)** where `pyproject.toml` + `mymod.py` is honest about the size. Don't manufacture a package directory you don't need.

## Tree diagram

```
mypackage/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── .editorconfig
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── core.py
│       └── cli.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_core.py
└── docs/
```

## Naming rules

- **Repo directory**: `kebab-case` is fine (`my-package/`); the directory name is decoupled from the import name.
- **Package directory under `src/`**: `snake_case`, mandated by PEP 8 and required because the directory name *is* the Python import path. `mypackage/` or `my_package/`, never `my-package/`. This is the documented exception in `principles/naming-conventions/`.
- **Module filenames**: `snake_case.py`. `core.py`, `cli.py`, `http_client.py`. Never `CoreLogic.py` or `core-logic.py`.
- **`__init__.py`** is mandatory in every package directory (including `tests/` if you want tests to be importable as a package, which conftest discovery prefers).
- **Distribution name** in `pyproject.toml` (`name = "mypackage"`) typically matches the import name. Hyphens are allowed in distribution names but discouraged unless there's a reason — they map to underscores at install time and that aliasing trips people up.
- **Tests live in `tests/`**, never in `src/`. `tests/` is not a package on PyPI; the wheel only ships `src/mypackage/`.

## Worked example

A library's tests pass locally but the released wheel is missing `mypackage/data/schema.json`.

1. Move the package to `src/mypackage/` and delete any `sys.path` hacks.
2. Declare package data in the build config (`[tool.hatch.build.targets.wheel] packages = ["src/mypackage"]`, plus include patterns for data files).
3. Install in editable mode: `pip install -e .[dev]`, then run `pytest`. Tests now import from the installed package.
4. Build and inspect the wheel: `python -m build && unzip -l dist/*.whl` and check that `schema.json` is listed.
5. In CI, test the built wheel in a fresh venv (`pip install dist/*.whl && pytest`) using tox or nox.

The missing-file bug is caught in the pull request that introduced it.

## Anti-patterns

- **Adding `src/` to `sys.path` to import without installing.** Defeats the entire point of src-layout. If you find yourself doing this, you wanted flat-layout.
- **Putting `__init__.py` directly under `src/`.** `src/` is not a package; it's a build-system convention. Only `src/mypackage/__init__.py` is correct.
- **Multiple top-level packages under `src/` with no namespace plan.** `src/foo/` and `src/bar/` produces two separate distributions awkwardly bundled. Either use a namespace package (PEP 420) deliberately or split the repo.
- **Forgetting `pip install -e .` after cloning.** Tests fail with `ModuleNotFoundError`; new contributor concludes the project is broken. Document this in README's "Development setup".
- **Mirroring `src/mypackage/` in `tests/mypackage/`.** Tests import *from* the package; they aren't *part of* the package. `tests/test_core.py` is enough.
- **Using `setup.py` in 2026.** PEP 517/518 made `pyproject.toml` the source of truth. `setup.py` is fine if it exists for legacy reasons, but new src-layout projects should not start with one.

## Scaling & failure modes

- **Editable-install caveats**: some tools don't see editable packages; test the wheel too.
- **Multiple packages** in one repo need a namespace plan or separate distributions.
- **Type stubs and data files** need explicit inclusion in the build config; audit the wheel content on each release.
- **Contributor friction**: the mandatory install step trips newcomers; put it at the top of `CONTRIBUTING.md`.

## Variants

- **src-layout-hatch-managed** (this guide) — current PyPA preference; Hatch handles version, build, env management.
- **src-layout-poetry-managed** — Poetry's `tool.poetry` table replaces `[project]`. Functionally equivalent layout. Choose Poetry if you want lockfiles and want a single tool for deps + build.
- **src-layout-flit-managed** — Flit is minimal, opinionated, pure-Python only. Smallest `pyproject.toml`. No good if you have C extensions.
- **src-layout-setuptools-managed** — the classic. Still works, still maintained, more verbose `pyproject.toml`. Use if you have legacy `setup.py` you can't migrate.
- **src-layout-with-co-located-tests** — `src/mypackage/tests/` instead of top-level `tests/`. Rare; ships tests inside the wheel. Justified only if downstream users call your tests as a runnable suite (almost never).
- **src-layout-namespace-packages** — `src/mycompany/billing/` and `src/mycompany/auth/` shipped as separate distributions sharing the `mycompany` namespace. Advanced; see PEP 420 and PyPA namespace-package guide.

## Adoption checklist

- [ ] `pip install -e .[dev] && pytest` passes on a clean venv.
- [ ] The built wheel's file list was inspected for data files and type marker (`py.typed`).
- [ ] CI installs the wheel (not the source tree) for at least one test job.
- [ ] `src/` contains only the package directory.
- [ ] Version is defined in exactly one place.

## Real-world projects using this

- **pytest** — uses src-layout; the canonical reference.
- **attrs** — Hynek Schlawack's library, src-layout, hatch-managed.
- **structlog**, **environ-config**, **service-identity** — same family, all src-layout.
- **The jaraco family** (jaraco.functools, jaraco.path, ~30 small libraries) — src-layout across the board.
- **Packaging.python.org's "src layout vs flat layout" tutorial** — the official explainer for why this layout exists.
- **PEP 517/518/621** documents establish `pyproject.toml` as the modern build configuration; src-layout is the layout that pairs with them.

## Migration & references

- **From flat-layout**: create `src/`, move `mypackage/` into it as `src/mypackage/`, update `pyproject.toml` `[tool.hatch.build.targets.wheel] packages = ["src/mypackage"]` (or the equivalent for your build backend), run `pip install -e .` in your venv, run tests. If tests pass without `sys.path` tricks, you're done. If they fail with `ModuleNotFoundError`, you had a hidden import dependency on the working tree — fix the import.
- **From `setup.py`-only legacy**: minimum viable migration is to add a `pyproject.toml` with `[build-system]` and `[project]` tables, then move source into `src/`. Keep `setup.py` as a one-line shim (`from setuptools import setup; setup()`) only while downstream tooling needs it; otherwise delete it.
- **From `src/__init__.py`-bug layout**: if you ever wrote `src/__init__.py`, delete it. `src/` is not a package. The package is one level deeper.
- **References**:
  - PyPA Packaging User Guide — *src layout vs flat layout*.
  - Hynek Schlawack — *Python application layouts: A reference*.
  - PEP 517, PEP 518, PEP 621 — modern packaging foundations.
  - Sibling guides: `code/python-flat-layout/` (the simpler alternative), `code/cli-tool/` (when you need a single-binary CLI), `code/cookiecutter-data-science/` (for research-flavored layouts).
  - Naming exception: `principles/naming-conventions/` documents `snake_case` for Python package directories.
