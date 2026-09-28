## TL;DR

A **rust-workspace** is multiple crates sharing one repo, one `Cargo.lock`, and one `target/` directory. The workspace root holds a `Cargo.toml` with a `[workspace]` table; member crates live in subdirectories (this guide uses `crates/<name>/` namespacing). The two big wins: faster builds (shared `target/` means each dep is compiled once for the whole workspace) and simpler version management (a `[workspace.package]` table lets every member inherit `version`, `edition`, `license`, etc., so you bump one place). The third win, less obvious until you need it: workspace deps in a `[workspace.dependencies]` table mean you specify `serde = "1"` once and members write `serde = { workspace = true }`. This is how you stop deps from drifting across crates. Use a workspace when you'd otherwise have a `cli` + `lib` + `server` + `tests` repo all wanting to share a core. **Don't** use a workspace if your crates have genuinely independent release cycles — at that point the cost of cross-crate version coordination outweighs the build speedup, and a polyrepo is honest about it.

## Principles & why

A workspace is shaped by four principles, all of which save real time at scale.

1. **One `Cargo.lock` for the whole repo.** Every crate in the workspace resolves deps together, which means dep version conflicts (`crate-a` wants `serde = "1.0.150"`, `crate-b` wants `serde = "1.0.180"`) get resolved once at the workspace level instead of per-crate. The lockfile lives at the workspace root, not in member directories. **The lockfile is committed if any member is a binary; gitignored only if every member is a library.** Most workspaces have at least one binary, so committed is the default.
2. **Shared `target/` directory.** The first build of a workspace compiles each dep once, and every subsequent member crate that needs that dep links against the cached artifact. On a workspace with 20 crates and 200 deps, this is the difference between a 3-minute and a 30-minute CI build.
3. **Inherit metadata via `[workspace.package]`.** Crates declare `version.workspace = true`, `edition.workspace = true`, `license.workspace = true`. Bumping the workspace version cascades to every member. This is the single most useful workspace feature once you have ≥3 crates.
4. **Workspace deps via `[workspace.dependencies]`.** Declare common deps once at the workspace root with their version constraint and feature set; members opt in with `serde = { workspace = true }`. This stops the bug where `crate-a` enables `serde/derive` and `crate-b` doesn't — they now share one dep spec.

The downside: workspaces couple release cycles. If `crates/core/` breaks, `crates/cli/` and `crates/server/` can't release until it's fixed. Most projects accept that coupling because it matches reality (they're all built from one source tree). When the coupling stops matching reality — separate maintainers, separate users, separate cadences — split into a polyrepo.

## When to use

- **Multi-binary projects sharing a common library.** A CLI + a server + an admin tool all built from the same `core` crate.
- **Splitting a binary into thin frontend + thick library.** Even one binary often grows into "the library that's testable" + "the binary that's the entrypoint" + "the WASM bindings" + "the FFI bindings". Workspace from day one.
- **Projects with proc-macros.** Proc-macro crates must be in a separate crate (compiler limitation). If your library has derive macros, the natural layout is workspace with `mylib/` and `mylib-derive/`.
- **Multiple binaries with non-trivial config.** `src/bin/foo.rs` + `src/bin/bar.rs` works for small binaries, but if `bar` needs different deps or features than `foo`, separate crates are cleaner.
- **Reducing CI build time.** The shared `target/` win is real and gets bigger as the project grows.

## When NOT to use

- **Single-crate projects.** A workspace with one member is overhead with no benefit. Use `code/rust-binary/` or `code/rust-library/`.
- **Genuinely independent release cycles.** Two crates that want their own versions, their own changelog, their own release cadence — a polyrepo is honest about that. A workspace forces coordination.
- **Wildly different MSRVs across members.** Workspaces support per-crate `rust-version`, but if `crate-a` needs 1.80 and `crate-b` is targeting embedded with 1.60, you're fighting the tooling. Polyrepo.
- **Crates published by different organisations.** A workspace is a single publish unit in spirit. Cross-org publishing is friction.

## Tree diagram

```
myworkspace/
├── Cargo.toml              ← [workspace] members = ["crates/*"]
├── Cargo.lock
├── README.md
├── LICENSE
├── .gitignore
├── crates/
│   ├── core/
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   ├── cli/
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   └── server/
│       ├── Cargo.toml
│       └── src/main.rs
└── target/                  ← gitignored, shared by all crates
```

## Naming rules

- **Workspace root directory**: `kebab-case` (`my-workspace/`, `myproject/`). The root has no crate name; only members do.
- **Member crate directories**: `kebab-case` under `crates/` (`crates/core/`, `crates/cli/`, `crates/http-server/`).
- **Member crate names in `Cargo.toml`**: prefix with the workspace name to avoid crates.io collisions. `myworkspace-core`, `myworkspace-cli`. The `core` crate's directory is `crates/core/` but its package is `myworkspace-core`. This is the convention used by tokio (`tokio`, `tokio-util`, `tokio-stream`), serde (`serde`, `serde_json`, `serde_derive`), and clap (`clap`, `clap_derive`, `clap_builder`).
- **Internal-only crates (not published)**: still use the prefix (`myworkspace-internal-foo`). It documents intent and prevents accidental publishing.
- **Path deps between members**: `myworkspace-core = { path = "../core" }` in `crates/cli/Cargo.toml`. The path is relative to the member crate's `Cargo.toml`, not the workspace root.
- **`crates/` vs flat-members**: putting members under `crates/` (`crates/core/`, `crates/cli/`) is more scannable than peer directories (`core/`, `cli/`) once you have ≥3 crates. The flat layout is older Rust convention; `crates/` is the current preference.

## Worked example

Three crates live in separate repos and their dependency versions drift.

1. Create the root `Cargo.toml` with `[workspace] members = ["crates/*"]` and `resolver = "2"`.
2. Add shared metadata in `[workspace.package]` (`version`, `edition`, `license`) and common dependencies in `[workspace.dependencies]`.
3. In each member, inherit: `version.workspace = true` and `serde = { workspace = true }`.
4. Move crates into `crates/core`, `crates/cli`, `crates/server`; depend on siblings with `core = { path = "../core" }`.
5. Build once, share the cache: `cargo build --workspace`; test with `cargo test --workspace`.
6. Use `cargo hack` or `--exclude` in CI for feature combinations of a single crate.

A dependency bump is a one-line change and every crate compiles it once.

## Anti-patterns

- **Per-crate `Cargo.lock` files.** They will be silently ignored by Cargo (only the workspace root's lockfile counts), but they confuse readers and cause merge conflicts. Delete them; they don't belong.
- **Per-crate `target/` directories.** Same: Cargo writes everything to the workspace `target/`. If you see `crates/core/target/`, something has been run with `--manifest-path` from inside the member; clean it up.
- **Forgetting `resolver = "2"` in the workspace `Cargo.toml`.** Cargo 2024 edition crates default to resolver v2, but workspaces default to v1 unless you opt in. v2 is what you want; mismatched resolvers cause subtle dep resolution bugs.
- **Not using `[workspace.package]` inheritance.** Without it, every member duplicates `edition`, `license`, `authors`, `repository`. You'll forget to bump one. Inherit.
- **Not using `[workspace.dependencies]`.** Same drift problem. `crate-a/Cargo.toml` has `serde = "1.0.150"` and `crate-b/Cargo.toml` has `serde = "1.0.180"` — Cargo resolves to 1.0.180 for both, but the spec says different things. Pin once at the workspace level.
- **Mixing `[workspace]` and `[package]` at the root.** A workspace root *can* also be a crate (a "virtual+real" workspace), but it's confusing. Prefer a *virtual workspace*: the root `Cargo.toml` has only `[workspace]`, all crates live in `crates/`.
- **Nested workspaces.** Cargo doesn't support them well. If `crates/core/` is itself a workspace, you're in for surprises. One workspace per repo.

## Scaling & failure modes

- **Compile times** scale with crate count and dependency graph shape; a tall chain of crates serializes builds.
- **Publishing order** matters: publish leaf crates first and use path plus version dependencies.
- **Feature unification** across the workspace can enable features you didn't expect; resolver 2 reduces this for dev-dependencies and build-dependencies.
- **Too many crates** add ceremony without gain; split for compile time, API boundaries, or independent publishing.

## Variants

- **flat-members** — `core/`, `cli/`, `server/` as peers under the repo root. Older convention; some projects (rustls, actix) still use it. Functionally equivalent but less scannable at scale.
- **`crates/`-namespaced** (this guide) — members under `crates/`. Current preferred style; tokio, polars, bevy, wasmtime all use it.
- **mixed bins-only / lib-only members** — workspace where some members are libs and some are bins. The lockfile policy: committed because at least one binary exists.
- **virtual workspace** (this guide) — root `Cargo.toml` has only `[workspace]`, no `[package]`. Cleanest layout.
- **non-virtual workspace** — root is itself a crate, with `[package]` and `[workspace]` both at the root. Sometimes used when there's "the main crate" and a few helper crates. Slightly confusing; prefer virtual.
- **nested-workspaces** — rare and not well-supported. Avoid.

## Adoption checklist

- [ ] `cargo build --workspace && cargo test --workspace` pass from a clean clone.
- [ ] Shared versions and metadata use `[workspace.package]` and `[workspace.dependencies]`.
- [ ] `resolver = "2"` (or the edition default) is set.
- [ ] A single `Cargo.lock` is committed.
- [ ] The publish order and target crates are documented.

## Real-world projects using this

- **cargo itself** (rust-lang/cargo) — workspace with `cargo`, `cargo-test-support`, `cargo-platform`, etc. Reference for serious production use.
- **tokio** (tokio-rs/tokio) — workspace with `tokio`, `tokio-util`, `tokio-macros`, `tokio-stream`, `tokio-test`. Uses `crates/`-style under the hood but with flat top-level dirs for historical reasons.
- **wasmtime** (bytecodealliance/wasmtime) — large workspace with dozens of crates; reference for `[workspace.dependencies]` use.
- **bevy** (bevyengine/bevy) — game engine; workspace; clean `crates/` layout.
- **polars** (pola-rs/polars) — DataFrame library; workspace.
- **rustls** (rustls/rustls) — TLS implementation; flat-member style.
- **clap** (clap-rs/clap) — CLI parser; workspace with `clap`, `clap_derive`, `clap_builder`, `clap_complete`.

## Migration & references

- **From single crate to workspace**: create a new `Cargo.toml` at a new repo root with `[workspace] resolver = "2" members = ["crates/*"]`. Move the existing crate to `crates/<name>/`. Move `Cargo.lock` to the new root. Run `cargo build` to verify; the build should produce one `target/` at the new root. Update any CI paths.
- **From flat-members to `crates/`-namespaced**: `mkdir crates`, `git mv crate-a crates/`, `git mv crate-b crates/`, update `[workspace] members = ["crates/*"]`, update path deps if any (`{ path = "../crate-a" }` becomes `{ path = "../crate-a" }` still — paths are relative to the member, not the root, so most don't change). Run `cargo build`.
- **Adding `[workspace.package]` inheritance retrofit**: add `[workspace.package]` block at the root with shared metadata. In each member's `Cargo.toml`, replace `version = "0.1.0"` with `version.workspace = true`, `edition = "2021"` with `edition.workspace = true`, etc. One edit per member, then enjoy bumping the version in one place forever.
- **References**:
  - The Cargo Book — *Workspaces*, *Inheriting a Package's Properties*, *Inheriting from a Workspace*.
  - The Cargo Book — *The resolver* (resolver v2 vs v1).
  - cargo's own `Cargo.toml` (rust-lang/cargo) as a reference workspace.
  - Sibling guides: `code/rust-binary/`, `code/rust-library/`.
