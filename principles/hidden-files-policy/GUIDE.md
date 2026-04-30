# Hidden files policy

## TL;DR

A leading dot on a file or directory name is a Unix convention that hides the entry from default directory listings (`ls`, `Finder`, most file managers). Use it for things the user almost never edits by hand: tool configuration (`.editorconfig`, `.prettierrc`), CI infrastructure (`.github/`), runtime caches, lockfiles in some ecosystems, and environment files. *Don't* hide anything a contributor needs to discover to understand the project — `README.md`, `pyproject.toml`, `package.json`, `Cargo.toml` are visible because they're load-bearing knowledge. The leading dot is a "this is plumbing, not surface" marker; reserve it for plumbing.

## Principles & why

The dotfile convention dates back to early Unix — `ls` originally had no `-a` flag and dotfiles were a way to keep `.` and `..` out of listings, then generalised into "hide things the user shouldn't usually see." Modern shells, `git`, IDE file trees and OS file browsers all still honour it. That long-standing semantic is the lever you're pulling: when a contributor opens the project root, they see the *meaningful* files first, and the tool plumbing fades into the background unless they go looking.

The signal only works if it's used consistently. If you hide `Makefile` (developers edit it constantly), they'll think the project has no build entry point. If you leave `.npmrc` visible at the root, every `ls` output gains a line of noise that contributes nothing to understanding the codebase. Calibrate by asking: "When a new contributor `cd`s into this project, do they need to *know* this file exists to do useful work?" Yes -> visible. No, the tool reads it automatically -> hidden.

There's also a tooling-contract dimension. `.gitignore`, `.editorconfig`, `.github/`, `.env` are recognised by tools precisely *because* they're dotfiles in conventional locations. Renaming `.gitignore` to `gitignore.txt` would break Git. So part of the rule is descriptive (these names are dotfiles by external mandate), and part is prescriptive (pick the right side of the line for files where you have a choice).

## When to use

Hide an entry with a leading dot when at least one of the following is true:

- The file is **tool configuration** the developer rarely edits manually: `.editorconfig`, `.prettierrc`, `.eslintrc.json`, `.stylelintrc`, `.babelrc`, `.npmrc`, `.nvmrc`, `.tool-versions`, `.python-version`.
- The file is **CI / VCS infrastructure**: `.github/`, `.gitlab/`, `.circleci/`, `.gitignore`, `.gitattributes`, `.gitmodules`, `.git/`.
- The file holds **environment variables or secrets**: `.env`, `.env.local`, `.env.production`. The committed *template* (`.env.example`) is hidden but tracked, by convention.
- The directory is a **tool cache or state**: `.cache/`, `.next/`, `.nuxt/`, `.terraform/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.venv/`, `.idea/`, `.vscode/`. Most of these are also gitignored.
- The file is **conventionally a dotfile** in its ecosystem and the convention is doing useful work (tool discovery, `XDG_CONFIG_HOME` semantics, etc.).

## When NOT to use

Keep visible — *no leading dot* — anything a contributor must learn to understand or change the project:

- `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md` and the rest of the canonical UPPERCASE meta set.
- Build manifests with project-shaping content: `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `Gemfile`, `composer.json`, `pom.xml`. These declare dependencies, scripts, metadata — non-negotiable knowledge.
- Build entry points the developer edits: `Makefile`, `Dockerfile`, `Containerfile`, `docker-compose.yml`, `Justfile`.
- Anything inside `src/`, `tests/`, `docs/`, `scripts/`, etc. — the actual project material.
- Lockfiles, *unless* the ecosystem explicitly hides them (most don't): `package-lock.json`, `yarn.lock`, `Cargo.lock`, `poetry.lock`, `Pipfile.lock` are all visible. They're machine-managed but contributors *do* notice and review them in PRs.

The litmus test: would a contributor ever open the file to read or edit it for project reasons? Visible. Does only the tool read it? Hidden is fine.

## Tree diagram

```
project/
├── .editorconfig       ← hidden: tool config, rarely edited
├── .gitignore          ← hidden: tool config
├── .github/            ← hidden: CI config
├── .env.example        ← hidden but committed (a discoverable template)
├── .env                ← hidden, gitignored, secrets
├── README.md           ← visible
├── pyproject.toml      ← visible: meaningful config
└── src/
    └── main.py
```

## Naming rules

1. **Tool configs created by the tool maintainer** keep whatever name the tool defines — almost always a dotfile (`.editorconfig`, `.prettierrc`, `.gitignore`). You don't have a choice; using a non-dotted name breaks discovery.
2. **Project metadata files** (`pyproject.toml`, `package.json`, `Makefile`) follow ecosystem convention — almost always *not* hidden — and you don't have a choice either.
3. **Files where you do have a choice** — internal scripts, generated indexes, project-specific configs — should follow the contributor-discovery test. If a new hire needs to know the file exists, leave it visible.
4. **Hidden but committed** is a real and useful pattern: `.env.example`, `.github/workflows/*.yml`, `.editorconfig`. The dot signals "tool plumbing"; tracking signals "this is part of the project, not local-only state."
5. **Hidden and gitignored** is the other common pattern: `.env`, `.venv/`, `.idea/`, `.vscode/settings.json` (in some teams). The dot signals "plumbing"; gitignore signals "local-only."
6. **Don't invent a non-standard dotfile** to make a file feel "private." If the file is project-relevant, leave it visible; if it's purely local state, gitignore the whole pattern.

## Anti-patterns

- **Hiding the `Makefile`** as `.makefile` — Make won't find it by default and contributors won't either. Make is a developer-edited build file; visible.
- **Visible cache directories** at the root — `node_modules/` is the famous and grandfathered exception (npm chose visibility), but `cache/`, `tmp/`, `pytest-cache/` (no dot) at the root pollute every `ls`. Either hide them with the dot or move them under a single `_cache/` umbrella.
- **`README.md` hidden as `.readme.md`** — defeats every README-rendering tool on the planet. README is canonical UPPERCASE *and* visible; both signals are required.
- **Custom `.notes/` for project documentation** — if these are docs contributors should read, they go in `docs/`. Hiding them buries useful material.
- **`.config/` at the project root holding things the user must edit** — XDG-style `.config/` is for *user-level* config in `$HOME`. At a project root, use `config/` (visible) or named tool dotfiles.
- **Inconsistent dotting** — `eslintrc.json` next to `.prettierrc` looks like a mistake. Match the ecosystem default for each tool; don't invent one.

## Variants

- **Strict (this repo's choice)** — only files the user almost never edits get a leading dot; everything else is visible. Easiest to teach, easiest to enforce.
- **Pragmatic** — developer-edited tool configs stay visible (`Makefile` not `.makefile`, `Justfile` not `.justfile`) even when other tool configs are dotfiles. This is essentially the strict variant with the developer-edit test as the hard rule.
- **All-visible** — some teams (especially in scientific/educational codebases) prefer no hidden files at all so newcomers can see everything. Costs you the noise tradeoff but can be appropriate for didactic projects.
- **All-XDG** — point every tool at `$XDG_CONFIG_HOME` (typically `~/.config/`) instead of project-local dotfiles. Cleans up the project root but moves config out-of-tree where it's harder to version with the project. Sensible for personal dotfiles repos, rarely sensible for application projects.
- **Underscore-prefixed alternative** — some Windows-leaning projects use `_config/`, `_build/` to sort first/last alphabetically and avoid Unix-only conventions. Loses the broad cross-tool dotfile semantics; only worth it if Windows-first is a hard constraint.

## Real-world projects using this

- **XDG Base Directory Specification** — codifies the dotfile convention in `$HOME` (`.config/`, `.cache/`, `.local/share/`). Defines what "user-level config goes in dotted directories" means industry-wide.
- **Git** — the `.git/` directory, `.gitignore`, `.gitattributes`, `.gitmodules`, `.gitkeep` (community convention). All hidden because Git owns the plumbing; users edit through commands or named config files.
- **Node.js / npm** — `.npmrc`, `.nvmrc`, `.node-version` are dotfiles; `package.json` and `package-lock.json` are visible. Clean illustration of the developer-edit test.
- **Rust / Cargo** — `.cargo/config.toml` (per-project tool config) hidden, `Cargo.toml` and `Cargo.lock` visible. Same split.
- **Python / pyenv / pipenv** — `.python-version`, `.tool-versions`, `.venv/` hidden; `pyproject.toml`, `Pipfile` visible.
- **Every modern OSS project on GitHub** — the `.github/` directory holds workflows, issue templates, funding metadata. Universally hidden, universally tracked.

## Migration & references

To audit an existing repo:

```bash
# 1. List all top-level entries, hidden and visible, side by side.
ls -A1 | sort

# 2. For each *hidden* entry, ask: "would a new contributor ever
#    need to edit this by hand for project reasons?" If yes, consider
#    making it visible (or moving its content into a visible file).
#
# 3. For each *visible* entry, ask: "is this just tool plumbing the
#    user almost never edits?" If yes, consider hiding it — but only
#    if the tool actually supports the dotfile name.

# 4. Find files that should be gitignored but are tracked, or vice versa.
git ls-files | grep -E '^\.' | sort   # tracked dotfiles
git status --ignored | head           # ignored entries summary
```

Common migration cases:

```bash
# Promote a buried doc-as-dotfile back to visibility:
git mv .notes/architecture.md docs/architecture.md
git commit -m "chore: surface architecture doc per hidden-files-policy"

# Demote a noisy visible config to dotfile (only if the tool supports it):
git mv prettier.config.js .prettierrc.json
git commit -m "chore: rename to canonical .prettierrc.json"
```

Further reading:

- *XDG Base Directory Specification* (freedesktop.org) — the canonical reference for dotfile placement at user level; the same rationale scales down to project level.
- POSIX spec on file naming (POSIX.1-2017, §3.281) — explains why a leading `.` is a portable convention rather than a filesystem feature.
- `principles/gitignore-and-keep-files/` — sibling rule covering the other axis: tracked vs. ignored. Hidden ≠ ignored; the two attributes are independent.
- `principles/capitalization-policy/` — sibling rule for case. Together they cover the two visual signals on a filename.
