## TL;DR

A **uv workspace** keeps several related Python packages in one repository with **one lockfile and one virtual environment**. The root `pyproject.toml` declares `[tool.uv.workspace] members = ["packages/*"]`; each member under `packages/<name>/` is a normal package with its own `pyproject.toml`; members depend on each other with `{ workspace = true }` sources, so an edit to a library is visible to its consumers immediately, without publishing or version bumps. `uv lock` resolves everything together, so every member is guaranteed a mutually compatible set of dependencies, and `uv sync --all-packages` builds the whole environment. Use it for a service plus its shared libraries, or a set of libraries released from one repository. If you have a single package, use `python-src-layout`; if the projects should not share dependencies at all, use separate repositories.

## Principles & why

1. **One resolution, one truth.** A single `uv.lock` for all members means the same version of a dependency everywhere, and conflicts surface at lock time instead of at deploy time.
2. **Members are real packages.** Each has its own name, version, dependencies, and build configuration, so any member can be built (`uv build --package <name>`) and published on its own.
3. **Local dependencies are declared, not path-hacked.** `[tool.uv.sources] acme-core = { workspace = true }` records that a dependency comes from the workspace; no `sys.path` tricks, no relative editable installs.
4. **The root is a coordinator.** In a *virtual* workspace the root has no package of its own; it carries the workspace declaration, shared tool configuration, and development dependency groups.
5. **Separate what ships from what supports.** Deployable applications, libraries, and tooling each get a member, so their dependency sets stay honest and small.

## When to use

- **A service and the libraries it shares** with a worker, a CLI, or another service.
- **A family of libraries** released from one repository with coordinated changes.
- **An internal platform** where several teams' packages must agree on dependency versions.
- **Migrating from a tangle of editable installs** (`pip install -e ../other`) or multiple lockfiles that drift.

## When NOT to use

- **A single package.** The workspace machinery adds nothing over `python-src-layout`.
- **Components that need conflicting dependency versions.** A workspace has one resolution; if two members need incompatible versions, they belong in separate workspaces or repositories.
- **Projects owned by unrelated teams** with separate release cadences; use separate repositories (see `monorepo-vs-polyrepo`).
- **Research notebooks** that share no library code; use `jupyter-research` or `cookiecutter-data-science`.

## Tree diagram

```
acme/
├── pyproject.toml              ← virtual root: [tool.uv.workspace], dev groups, tool config
├── uv.lock                     ← one lockfile for every member
├── README.md
├── .python-version
├── packages/
│   ├── acme-core/
│   │   ├── pyproject.toml
│   │   ├── src/acme_core/
│   │   │   └── __init__.py
│   │   └── tests/
│   ├── acme-cli/
│   │   ├── pyproject.toml      ← depends on acme-core via workspace source
│   │   ├── src/acme_cli/
│   │   └── tests/
│   └── acme-api/
│       ├── pyproject.toml
│       ├── src/acme_api/
│       └── tests/
└── scripts/
```

## Naming rules

- **Distribution names** in each member's `pyproject.toml` are kebab-case with a shared prefix (`acme-core`, `acme-cli`), which avoids collisions on PyPI.
- **Import packages** under `src/` are `snake_case` (`acme_core`), the documented Python exception (see `naming-conventions`).
- **Member directories** match the distribution name, so `packages/acme-core/` is the source of `acme-core`.
- **Root** has no `[project]` table when it is a virtual workspace; if it has one, name it for the whole product.
- **Dependency groups** use conventional names (`dev`, `test`, `docs`) and live in the root `[dependency-groups]` table.

## Worked example

Three sibling repos (`core`, `cli`, `api`) install each other with `pip install -e ../core`, and versions drift.

1. Create the new repository and move the packages in as `packages/acme-core`, `packages/acme-cli`, `packages/acme-api`, each keeping its `src/` layout.
2. Write the root `pyproject.toml`:
```
[tool.uv.workspace]
members = ["packages/*"]

[dependency-groups]
dev = ["pytest", "ruff"]
```
3. In `packages/acme-cli/pyproject.toml`, declare the dependency and its source:
```
dependencies = ["acme-core"]

[tool.uv.sources]
acme-core = { workspace = true }
```
4. Resolve and install everything: `uv lock && uv sync --all-packages`.
5. Run one member's tests: `uv run --package acme-cli pytest packages/acme-cli`, or all with `uv run pytest`.
6. Build one member: `uv build --package acme-core`, and check the wheel contents.
7. In CI, cache uv's cache directory keyed by `uv.lock`.

A change to `acme-core` is immediately visible in `acme-cli`'s tests, with one lockfile guaranteeing compatible dependencies.

## Anti-patterns

- **Committing several lockfiles** (one per member) to a workspace. There is one `uv.lock` at the root.
- **Path dependencies instead of workspace sources.** `acme-core @ file:../acme-core` works locally and breaks when packages are built or published.
- **One giant member** containing everything. The point is separate packages with separate dependency sets.
- **Conflicting requirements papered over with `override-dependencies`.** If members truly need different versions, split the workspace.
- **Putting application-specific dev dependencies in the root** for all members. Keep test and lint tools in root groups, but runtime dependencies in the member that needs them.
- **Skipping the wheel check.** Editable workspace installs hide missing package data; build and inspect each publishable member.

## Scaling & failure modes

- **Many members** slow `uv sync` if you always install all of them; use `uv sync --package <name>` to install only what you need in CI jobs.
- **Different Python versions** per member are not supported by a single resolution; set a common `requires-python` at the intersection.
- **Release coordination**: independent versions per member are fine, but a change to `acme-core` requires bumping consumers' constraints if published; automate with a release tool and per-package tags (`acme-core/v1.2.0`).
- **Docker builds**: copy `pyproject.toml` files and `uv.lock` first, run `uv sync --frozen --no-install-workspace`, then copy sources, so dependency layers cache.
- **Ownership**: add `CODEOWNERS` per `packages/<name>/` once teams differ.

## Variants

- **Virtual workspace root** (this guide): the root has no package, only configuration.
- **Root package plus members**: the root is itself the main application, and `packages/*` are its libraries.
- **Multiple workspaces in one repo**: rare; only if resolution groups must stay separate.
- **Poetry or PDM monorepo**: similar layout using path dependencies; uv's workspace makes local dependencies first-class.
- **Polyglot monorepo**: Python members inside an Nx, Bazel, or Pants repository with their own task runner.

## Adoption checklist

- [ ] There is exactly one `uv.lock`, at the repository root, committed.
- [ ] Every member depends on siblings through `{ workspace = true }` sources.
- [ ] `uv sync --all-packages && uv run pytest` passes from a clean clone.
- [ ] Each publishable member builds a correct wheel (`uv build --package <name>`, inspect with `unzip -l`).
- [ ] The root has shared tool configuration (ruff, pytest) and dev groups.
- [ ] CI installs only what each job needs and caches uv's cache.

## Real-world projects using this

- **uv's documentation** ("Working on projects" and "Workspaces") describes the workspace model, `tool.uv.workspace`, and `workspace = true` sources; it credits Cargo workspaces as the inspiration.
- **Cargo workspaces** (see `rust-workspace`) are the model uv borrowed: one lockfile, shared target, member crates.
- **Astral's own tools** and many open-source Python projects use `uv` for development; browse their repositories for workspace examples.
- **PEP 735** (dependency groups) standardizes the `[dependency-groups]` table used for dev dependencies.

## Migration & references

- **From `pip install -e` chains or requirements files:** move packages into `packages/`, add the workspace table, convert cross-package installs to workspace sources, generate the lock, and delete the old requirement files.
- **From Poetry path dependencies:** convert each `path = "../core"` entry to a workspace source, and replace `poetry.lock` with `uv.lock` (`uv lock`).
- **From a single package that grew:** split by dependency set and release cadence into members, keeping import names stable.
- **References:**
  - `code/python-src-layout/` for each member's internal layout.
  - `code/python-flat-layout/` for unpublished applications.
  - `principles/monorepo-vs-polyrepo/` for the decision to share a repository.
  - `code/rust-workspace/` for the analogous Cargo model.
