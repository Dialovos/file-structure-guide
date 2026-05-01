## TL;DR

The **rust-binary** layout is for crates that compile to one (or a few) executables: CLI tools, services, daemons. The shape is the default `cargo new --bin mybin` shape — `Cargo.toml`, `src/main.rs`, optional `tests/`, `examples/`, and `benches/`. The single most important architectural choice is whether to keep all code in `src/main.rs` (fine for ≤200 LOC scripts) or split into `src/main.rs` (a thin entrypoint, ~10 lines) plus `src/lib.rs` (where the actual logic lives, fully testable). This guide picks the **main-with-lib** variant because it scales cleanly: `lib.rs` exposes a `pub fn run() -> Result<...>` that `main.rs` calls; integration tests in `tests/` link against the library half; examples in `examples/` exercise the library half. If you later need multiple binaries (e.g. `mybin` and `mybin-admin`), drop them in `src/bin/foo.rs` and `src/bin/bar.rs` — Cargo auto-discovers each as a separate binary target. **`Cargo.lock` is committed for binaries** (it pins exact dep versions for reproducible builds), unlike libraries where it is gitignored.

## Principles & why

The rust-binary layout encodes three principles, each load-bearing.

1. **Thin `main.rs`, thick `lib.rs`.** The entrypoint should do nothing but parse arguments and call `lib::run()`. Why: anything inside a binary crate is unreachable to integration tests, examples, and benchmarks — they can only link against the *library* half. Keeping logic in `lib.rs` means `tests/integration_test.rs` can `use mybin::run;` and exercise it directly, which is impossible if the same code lives in `main.rs`. This is the cargo book's recommended pattern and is how ripgrep, fd, and bat are all structured.
2. **`Cargo.lock` is committed for binaries.** Cargo treats binaries and libraries differently here. For a binary, you ship a *specific build* — pinning exact deps via a committed lockfile gives you reproducible builds, deterministic CI, and bisectable history. For a library, the lockfile is gitignored because downstream consumers will resolve their own. Mixing this up is one of the most common Rust packaging mistakes.
3. **`src/bin/*.rs` is the official multi-binary mechanism.** Don't invent your own. Cargo auto-discovers every `*.rs` in `src/bin/` as a separate binary target named after the file. This means adding a second binary (`mybin-admin`, `mybin-debug`) requires zero `Cargo.toml` changes — just drop the file in.

The result: a layout where `cargo build` produces the binary, `cargo test` exercises both unit tests (in `lib.rs`) and integration tests (in `tests/`), `cargo run --example basic` runs the example, and `cargo install --path .` installs the tool locally — all without any custom configuration.

## When to use

- **CLI tools.** ripgrep, fd, bat, eza, hyperfine all use this layout. `clap` for arg parsing, `lib.rs` for the work, `main.rs` as the entrypoint.
- **Services and daemons.** Anything that compiles to one binary you ship as a Docker image or a systemd unit.
- **Anything you `cargo install`.** The binary half is what gets installed; the lib half is incidental.
- **Anything testable end-to-end via integration tests.** With the main-with-lib variant, `tests/` can drive the entire program.
- **Projects that might grow a second binary** (admin tool, debug tool, migration runner). Adding `src/bin/admin.rs` later is zero ceremony.

## When NOT to use

- **Libraries published to crates.io.** Use `code/rust-library/` — the layout is similar but the build product, license conventions, and lockfile policy differ.
- **Multi-crate projects.** If you have a CLI, a server, and a shared core that all want to live together, use `code/rust-workspace/`. A workspace gives you a shared `target/`, a single `Cargo.lock`, and per-crate `Cargo.toml`s.
- **One-shot scripts.** A 50-line tool you'll run once doesn't need `lib.rs`, `tests/`, and CI. Use a single `src/main.rs` or even a `cargo-script`/`rust-script` shebang file.
- **Mixed-language projects** (Rust + Python via PyO3, Rust + Node via napi-rs). Those have their own layouts driven by the bindings tool.

## Tree diagram

```
mybin/
├── Cargo.toml
├── Cargo.lock
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   ├── main.rs
│   ├── cli.rs              ← CLI args parsing (clap)
│   └── lib.rs              ← optional, exposes guts as a library too
├── tests/
│   └── integration_test.rs
└── examples/
    └── basic.rs
```

## Naming rules

- **Repo / crate directory**: `kebab-case` is conventional for the *repo* directory (`my-bin/`, `ripgrep/`), but the **package name in `Cargo.toml`** must be a valid Rust identifier-ish: lowercase, `_` or `-` allowed, but the convention for binary crates published to crates.io is `kebab-case` for the *package name* and `snake_case` for *library targets*. crates.io treats `foo-bar` and `foo_bar` as the same crate to prevent typo-squatting.
- **Library target name**: when `lib.rs` exists, the library is reachable as `use my_bin::run;` — Rust normalises hyphens in package names to underscores in import paths. Plan your name with this in mind: `mybin` is unambiguous; `my-bin` becomes `my_bin` at import time.
- **Module filenames** in `src/`: `snake_case.rs`. `cli.rs`, `http_client.rs`, `config_loader.rs`. Never `CamelCase.rs`.
- **`src/bin/<name>.rs`**: the filename (minus `.rs`) becomes the binary name on disk. `src/bin/admin.rs` produces a binary called `admin`. `snake_case` or `kebab-case` both work in filenames, but the resulting binary name is taken verbatim.
- **Integration test files**: `tests/<descriptive_name>.rs`. Each top-level `.rs` in `tests/` is compiled as its own crate, so name them by feature (`tests/cli_smoke.rs`, `tests/config_parsing.rs`).
- **Example files**: `examples/<descriptive_name>.rs`. Run with `cargo run --example basic`.

## Anti-patterns

- **Putting all logic in `main.rs` then trying to write integration tests.** Integration tests cannot reach binary-only code. Symptom: you write `tests/integration_test.rs` and discover none of your functions are visible. Fix: extract logic into `lib.rs`.
- **Not committing `Cargo.lock` for a binary crate.** You will hit the day where `cargo build` reproduces a different binary than yesterday's because a transitive dep released a patch. Always commit `Cargo.lock` for binaries.
- **Committing `Cargo.lock` for a *library*.** Confusingly, the opposite rule. For libs, downstream picks deps; your lockfile is irrelevant and just causes merge conflicts. Use `code/rust-library/` for that case.
- **Hand-rolled `[[bin]]` tables in `Cargo.toml` for files in `src/bin/`.** Cargo auto-discovers them. Adding `[[bin]] name = "admin" path = "src/bin/admin.rs"` is redundant unless you need to override the auto-discovered name.
- **Mixing `src/main.rs` + `src/bin/*.rs` without thinking.** This works (you get `mybin` from `src/main.rs` and `admin` from `src/bin/admin.rs`), but it confuses readers. Prefer either: one binary in `src/main.rs`, OR all binaries in `src/bin/`. Don't split.
- **Using `tests/` for unit tests.** Unit tests go in `#[cfg(test)] mod tests` *inside* the file they test. `tests/` is for integration tests that exercise the public API.
- **Forgetting `examples/` exists.** It's free CI: every example must compile when you run `cargo build --examples`. Use it to keep your README's code samples honest.

## Variants

- **main-only** — single `src/main.rs`, no `lib.rs`. Fine for ≤200 LOC. Cannot have integration tests against internal logic. Switch to main-with-lib the day you write the second non-trivial function.
- **main-with-lib** (this guide) — `src/main.rs` is a thin wrapper, `src/lib.rs` holds the logic. Default for any non-trivial CLI.
- **multi-binary** — drop `src/bin/foo.rs`, `src/bin/bar.rs`, and Cargo produces two binaries. Combine with `lib.rs` so each binary is also a thin wrapper around shared library code.
- **binary + workspace member** — for very large projects, the binary becomes one crate inside a workspace; see `code/rust-workspace/`.
- **binary with build.rs** — adds a `build.rs` for codegen, vendored C deps, or version-stamping. The layout is unchanged; `build.rs` sits next to `Cargo.toml`.

## Real-world projects using this

- **ripgrep** (BurntSushi/ripgrep) — the canonical Rust CLI. Workspace + main-with-lib + `src/bin/`. A reference for production-grade structure.
- **fd** (sharkdp/fd) — fast `find` replacement; clean main-with-lib layout.
- **bat** (sharkdp/bat) — `cat` with syntax highlighting; same shape.
- **hyperfine** (sharkdp/hyperfine) — command-line benchmarking tool.
- **eza** (eza-community/eza) — modern `ls`; main-with-lib + clap-derive, instructive Cargo.toml.
- **just** (casey/just) — command runner; small, readable, exemplary.
- The Rust Book chapter 12 (*Building a command line program*) walks through this exact layout and is the primary documentation source.

## Migration & references

- **From main-only to main-with-lib**: create `src/lib.rs`, move everything except `fn main()` into it, expose a `pub fn run() -> Result<(), Box<dyn std::error::Error>>`, and reduce `main.rs` to `fn main() { if let Err(e) = mybin::run() { eprintln!("{e}"); std::process::exit(1); } }`. Run `cargo test`; integration tests now have a target to import.
- **From single-binary to multi-binary**: rename `src/main.rs` → `src/bin/<name>.rs` (or keep `src/main.rs` as the primary and add new binaries under `src/bin/`). No `Cargo.toml` changes needed. `cargo build --bin <name>` to build a specific one.
- **From binary to workspace**: when a second crate is needed, create `Cargo.toml` at a new repo root with `[workspace] members = ["mybin"]`, move the existing `mybin/` under the workspace, and add new crates as siblings. See `code/rust-workspace/`.
- **References**:
  - The Rust Book — *Chapter 12: An I/O Project: Building a Command Line Program*.
  - The Cargo Book — *Project Layout* (cargo auto-discovery rules).
  - The Cargo Book — *Cargo.toml vs Cargo.lock* (the lockfile policy).
  - clap docs — *Derive tutorial* for the CLI parsing pattern this guide assumes.
  - Sibling guides: `code/rust-library/` (publishable lib), `code/rust-workspace/` (multi-crate).
