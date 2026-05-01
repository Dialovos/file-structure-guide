# Rust library crate — template

A `cp -r`-able starter for a Rust library destined for crates.io.
Wired with `thiserror` for the public error type, `criterion` for
benchmarks, dual MIT/Apache-2.0 licensing, and a CI matrix that
checks fmt, clippy, tests, docs, and a pinned MSRV build.

## What to rename

The crate name in `Cargo.toml` is `mylib`. Replace it everywhere:

- `Cargo.toml` — `[package] name`, `[lib] name`.
- `src/lib.rs` — the `# mylib` doc comment.
- `src/error.rs` — the `MylibError` enum.
- `src/core.rs`, `tests/public_api.rs`, `benches/core_bench.rs`,
  `examples/basic_usage.rs` — every `mylib::` import.
- This `README.md` — replace with the project-facing version.

If your crate name needs to be `kebab-case` (`my-lib`, the crates.io
convention), keep in mind the import path will be the underscore form
(`use my_lib::...`).

## What to fill

- `Cargo.toml` — `description`, `repository`, `documentation`,
  `homepage`, `keywords`, `categories`, `authors`. These all show on
  the crates.io page.
- `LICENSE-MIT` and `LICENSE-APACHE` — replace `{{YEAR}}` and
  `{{NAME}}`. If you don't want dual-licensing, delete one and update
  `[package] license` in `Cargo.toml`.
- `src/core.rs` — replace `greet`/`greet_checked` with the real API.
- `src/error.rs` — extend the `MylibError` enum with your variants.
- `tests/public_api.rs` — exercise the real public surface.

## What to delete

- This template `README.md`.
- The `greet` stub once you have real logic.
- `benches/core_bench.rs` if you don't run benchmarks (and remove
  `[[bench]]` from `Cargo.toml`).
- `.github/workflows/ci.yml` if you use a different CI.

## First run

```bash
cargo build --all-features
cargo test --all-features
cargo doc --no-deps --open
cargo bench                     # criterion runs benches/
cargo run --example basic_usage
```

Once `cargo test` and `cargo doc` succeed, the crate is ready to
publish: `cargo publish --dry-run` to validate, then `cargo publish`.

## Lockfile policy

`Cargo.lock` is gitignored for this crate because libraries do not
ship lockfiles to consumers. Binaries do — see `code/rust-binary/`
for that case.

## Pair this with

- `../GUIDE.md` — full reasoning behind this layout.
- `../../rust-binary/` — for single-binary CLIs.
- `../../rust-workspace/` — for multi-crate projects.
