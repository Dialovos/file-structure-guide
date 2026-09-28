## TL;DR

The **rust-library** layout is for crates published to crates.io: `src/lib.rs` is the public entrypoint, modules in `src/`, integration tests in `tests/` (which exercise the crate as an external consumer would), criterion benchmarks in `benches/`, runnable demos in `examples/`. Three things differ meaningfully from the binary layout: (1) **`Cargo.lock` is gitignored** because downstream consumers resolve their own deps, (2) **dual MIT/Apache-2.0 licensing** is the strong convention in the Rust ecosystem (`LICENSE-MIT` + `LICENSE-APACHE` files at the root), and (3) the `Cargo.toml` carries publishing metadata: `description`, `repository`, `documentation`, `keywords`, `categories`, `readme`, `license`. The `[lib]` table is implicit (you don't need to write one if the file is at `src/lib.rs`). `thiserror` for error types and `criterion` for benchmarks are the de-facto defaults; this template wires both in. The single biggest mistake is committing `Cargo.lock` for a library — it produces noisy merge conflicts and deceives users into thinking your stated MSRV is anything other than what your deps actually require.

## Principles & why

A Rust library is shaped by four principles:

1. **`src/lib.rs` is the public API.** Only items reachable through `pub` chains starting at `lib.rs` exist for downstream users. Everything else is private. The crate's job is to make `pub` surface tiny and intentional. The Rust API Guidelines (rust-lang.github.io/api-guidelines) is the canonical checklist.
2. **`Cargo.lock` is gitignored for libraries.** The reasoning: a library declares dep ranges (`serde = "1"`); consumers resolve those ranges in their own lockfile. Committing your lockfile only pins *your test* environment — it doesn't (and can't) affect consumers. Worse, every dep update churns it and produces merge conflicts. Rust's official guidance: commit lockfiles for binaries, ignore them for libraries.
3. **Integration tests in `tests/` test the crate as a consumer would.** Each `.rs` file under `tests/` is compiled as its own crate and can only see the crate's `pub` items. This is a feature: it's the most realistic test of your public API. Unit tests of private items go in `#[cfg(test)] mod tests` inside the file they test.
4. **Dual MIT/Apache-2.0 licensing is the Rust ecosystem default.** The compiler itself, std, and most of the ecosystem dual-license under MIT OR Apache-2.0. Why both: MIT alone lacks an explicit patent grant; Apache-2.0 has one but is incompatible with GPL-2-only. Offering both lets consumers pick. Rust's API guidelines (C-PERMISSIVE) recommend this combo.

A fifth, softer principle: **`thiserror` for library error types, `anyhow` for application errors.** `thiserror` produces named error enums with `#[derive(Error)]`; consumers can match on variants. `anyhow` produces opaque `anyhow::Error` blobs; great for binaries, wrong for libraries because it strips type information from your public surface.

## When to use

- **Crates you publish to crates.io.** The whole reason this layout exists.
- **Internal libraries** consumed by other crates within your organisation (private cargo registry, git deps).
- **Reusable algorithms, data structures, protocol implementations.** Anything where the API is the product.
- **WASM-targeted libraries** (with `wasm-bindgen`). The layout is unchanged; you add a `[lib] crate-type = ["cdylib", "rlib"]` table.
- **FFI libraries** for use from C/Python/Node — same layout, you add `crate-type = ["cdylib"]`.

## When NOT to use

- **Single-binary CLI tools.** Use `code/rust-binary/`. The lockfile policy is the opposite, license conventions differ, and you don't need `benches/` or `examples/` ceremony for one binary.
- **Multi-crate projects.** If you have a public lib + an internal lib + a CLI, use `code/rust-workspace/` so they share a `target/` and a single `Cargo.lock`.
- **Throwaway code / demos.** A library implies a public API contract. Don't manufacture one if you're prototyping.
- **Crates that are mostly procedural macros.** Proc-macro crates have a different shape (`crate-type = ["proc-macro"]`, no `examples/` because proc-macros can't be called from `examples/`). Use a workspace with a tiny proc-macro sub-crate alongside a normal lib.

## Tree diagram

```
mylib/
├── Cargo.toml
├── README.md
├── LICENSE-MIT
├── LICENSE-APACHE
├── .gitignore
├── src/
│   ├── lib.rs
│   ├── core.rs
│   └── error.rs
├── tests/
│   └── public_api.rs
├── benches/
│   └── core_bench.rs
└── examples/
    └── basic_usage.rs
```

## Naming rules

- **Crate name in `Cargo.toml`**: `kebab-case` is the crates.io convention (`my-lib`, `serde-json`, `tokio-util`). Underscores work but are less common.
- **Library import path**: Cargo normalises hyphens to underscores. `my-lib` becomes `use my_lib::...`. Plan accordingly; if the import name matters more than the crates.io name, pick a name that's already an identifier.
- **Module filenames**: `snake_case.rs`. `core.rs`, `error.rs`, `http_client.rs`. Same as `code/rust-binary/`.
- **Public type names**: `CamelCase` for types/traits/enums (`MylibError`, `Config`), `snake_case` for functions/methods (`fn parse(...)`). Enforced by `cargo clippy`.
- **Error type naming**: end with `Error` (`MylibError`, `ParseError`). The Rust API Guidelines (C-GOOD-ERR) calls this out.
- **Test file naming**: `tests/<feature>.rs`. Each top-level `.rs` is a separate test crate. `tests/public_api.rs` is a common name for "smoke test of the documented surface".
- **Bench naming**: must match `[[bench]] name = "..."` in `Cargo.toml`. Convention: `<thing>_bench.rs` (criterion uses this).

## Worked example

A crate is about to be published for the first time.

1. Fill `Cargo.toml` metadata: `description`, `license = "MIT OR Apache-2.0"`, `repository`, `readme`, `keywords`, `categories`, `rust-version`.
2. Add both license files (`LICENSE-MIT`, `LICENSE-APACHE`) and gitignore `Cargo.lock`.
3. Expose the public API from `lib.rs` with `pub use`, and keep everything else private; add `#![deny(missing_docs)]`.
4. Put doc tests in item docs and integration tests in `tests/` (they only see the public API).
5. Run `cargo publish --dry-run` and `cargo package --list` to check what will ship.
6. Check semver with `cargo semver-checks` before every release.

Docs on docs.rs compile from the doc comments, and accidental API breakage is caught before release.

## Anti-patterns

- **Committing `Cargo.lock`.** The single most common mistake. Adds it to `.gitignore` and remove from index: `git rm --cached Cargo.lock`. Confusion source: `cargo new --lib` *does not* generate a `.gitignore` rule for `Cargo.lock`, but it's the convention nonetheless.
- **Single MIT license without thinking.** Fine for personal projects; inconsistent with the ecosystem if you want broad adoption. Default to dual MIT/Apache-2.0 unless you have a reason.
- **Using `anyhow::Error` in public function signatures.** Hides type information from consumers. Use `thiserror`-derived enums for the public surface; `anyhow` is for internal plumbing or binaries.
- **Putting unit tests in `tests/`.** That's for integration tests. Unit tests go inline in `#[cfg(test)] mod tests` blocks.
- **Skipping `#![deny(missing_docs)]`.** Library code without doc comments rots fast. Either add the lint or commit to writing the docs by hand.
- **Reaching into private modules from `tests/`.** Tests under `tests/` only see `pub` items; if you need to reach private internals, that's a unit test. The fact that the language enforces this is a feature.
- **Wide `pub use` re-exports of internals.** Each item re-exported from `lib.rs` becomes part of your stable API. Be deliberate. Typed errors, traits, and one or two top-level types — not the entire module tree.
- **Forgetting `[package.metadata.docs.rs]` for non-default features.** If your crate has feature flags, docs.rs builds with default features only unless you opt in. Add `all-features = true` or pick the right set.

## Scaling & failure modes

- **Public API drift**: every `pub` item is a promise; prefer `pub(crate)` and re-export deliberately.
- **Feature flags** multiply test combinations; test with `--all-features` and `--no-default-features` in CI.
- **MSRV** (minimum supported Rust version) should be declared and tested.
- **Breaking changes** in 0.x versions still require care; document them in the changelog.

## Variants

- **crates-io-published, dual-licensed** (this guide) — the strong default. MIT OR Apache-2.0, lockfile gitignored, full `Cargo.toml` metadata, `examples/` and `benches/` populated.
- **internal-only-lib** — single license (whatever your org uses), no `[package] description/keywords/categories` ceremony, possibly committed lockfile if the lib is consumed only by binaries in the same repo. Often becomes a workspace member.
- **no_std-friendly** — adds `#![no_std]` at the top of `lib.rs`, gates `std`-using code behind a `#[cfg(feature = "std")]`, declares `default-features = false` on deps. Layout unchanged; CI must build with `--no-default-features` for embedded targets.
- **proc-macro-only** — `crate-type = ["proc-macro"]`, paired with a sibling `*-macros` crate in a workspace. No `examples/`, limited `tests/`.
- **FFI / cdylib** — `crate-type = ["cdylib", "rlib"]` for a library that produces both a shared library (for non-Rust consumers) and a Rust-importable rlib.

## Adoption checklist

- [ ] `cargo publish --dry-run` succeeds and `cargo package --list` shows the expected files.
- [ ] `Cargo.lock` is ignored, both license files exist.
- [ ] `#![deny(missing_docs)]` is on and doc tests pass.
- [ ] CI tests default, all, and no default features.
- [ ] `cargo semver-checks` runs before release.

## Real-world projects using this

- **serde** (serde-rs/serde) — the canonical Rust library. Workspace, dual-licensed, `serde` and `serde_derive` as separate crates.
- **tokio** (tokio-rs/tokio) — async runtime; workspace; rich `examples/`, `benches/`, feature flags.
- **reqwest** — HTTP client; reference for FFI-aware libs (uses `cdylib` patterns where useful).
- **anyhow** and **thiserror** (dtolnay/anyhow, dtolnay/thiserror) — the error-handling pair this guide recommends. Tiny crates with exemplary `Cargo.toml`s.
- **clap** (clap-rs/clap) — argument parser. Workspace; published as a library with derive macros.
- **rand** (rust-random/rand) — randomness; workspace with a clean modular structure.
- The Rust API Guidelines (rust-lang.github.io/api-guidelines) and *The Rust Performance Book* are the closest things to "official" companion docs.

## Migration & references

- **From a binary to a library**: extract logic into a new crate. Often easiest as a workspace migration: create `Cargo.toml` with `[workspace]`, move the binary into `crates/cli/`, the library into `crates/<libname>/`, and switch the binary's deps to a path dep on the library.
- **From single MIT to dual MIT/Apache-2.0**: add `LICENSE-APACHE`, update `[package] license = "MIT OR Apache-2.0"`, update `README.md`'s license section. No code change; the prior MIT grant remains valid for prior versions.
- **From `anyhow` in public API to `thiserror`**: define a `pub enum MylibError` with `#[derive(thiserror::Error)]`. Map every public function's `anyhow::Result<T>` to `Result<T, MylibError>`. This is a breaking change; bump major version.
- **From committed `Cargo.lock` to gitignored**: `git rm --cached Cargo.lock`, add `Cargo.lock` to `.gitignore`, commit. Note in the changelog so contributors regenerate locally.
- **References**:
  - The Cargo Book — *Cargo.toml vs Cargo.lock* (the lockfile rule).
  - Rust API Guidelines — `https://rust-lang.github.io/api-guidelines/`.
  - The Rust Book — *Chapter 14: More about Cargo and Crates.io*.
  - `thiserror` and `anyhow` READMEs — the canonical case for typed-vs-opaque errors.
  - Sibling guides: `code/rust-binary/`, `code/rust-workspace/`.
