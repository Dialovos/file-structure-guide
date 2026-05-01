# Rust workspace — template

A `cp -r`-able starter for a Rust workspace using the
**virtual + `crates/`-namespaced** variant. Two members are wired in:
`crates/core/` (the shared library) and `crates/cli/` (a thin clap-based
binary that calls into core). Add `crates/server/`, `crates/wasm/`,
etc. as siblings.

## Layout at a glance

```
.
├── Cargo.toml              # [workspace] only — virtual workspace
├── Cargo.lock              # committed (workspace has a binary)
└── crates/
    ├── core/               # myworkspace-core (lib)
    └── cli/                # myworkspace-cli (bin: `myworkspace`)
```

## What to rename

`myworkspace` is the workspace name; member crates are
`myworkspace-core` and `myworkspace-cli`. Replace everywhere:

- Root `Cargo.toml` — `[workspace.package] repository`/`homepage`,
  `[workspace.dependencies] myworkspace-core` path key.
- `crates/core/Cargo.toml` — `[package] name`, `[lib] name`.
- `crates/cli/Cargo.toml` — `[package] name`, `[[bin]] name`.
- `crates/cli/src/main.rs` — `use myworkspace_core::greet;`.
- This `README.md`.

Convention: prefix every member's package name with the workspace name
(`myworkspace-foo`) to avoid crates.io collisions. The directory
itself can be the short form (`crates/foo/`).

## What to fill

- `Cargo.toml` — `[workspace.package]` metadata (you fill these once
  and every member inherits via `version.workspace = true`).
- `[workspace.dependencies]` — declare common deps once; members opt
  in via `dep = { workspace = true }`. This stops version drift.
- Each member's `[package] description`.
- `LICENSE` — replace `{{YEAR}}` and `{{NAME}}`.

## What to delete

- This template `README.md`.
- The `greet` stub once you have real logic.
- `.github/workflows/ci.yml` if you don't use GitHub Actions.

## First run

```bash
cargo build --workspace
cargo test --workspace
cargo run -p myworkspace-cli -- alice
# → "hello, alice"
```

## Adding a new member

```bash
mkdir -p crates/server/src
# write crates/server/Cargo.toml (inherit metadata via workspace)
# write crates/server/src/main.rs
# no edits to root Cargo.toml needed — `members = ["crates/*"]` glob
# auto-includes it.
cargo build -p myworkspace-server
```

## Lockfile policy

`Cargo.lock` is committed because the workspace contains a binary
(`myworkspace-cli`). For a workspace where every member is a library,
gitignore the lockfile instead — same rule as `code/rust-library/`.

## Pair this with

- `../GUIDE.md` — full reasoning.
- `../../rust-binary/` — single-crate binary alternative.
- `../../rust-library/` — single-crate library alternative.
