# Rust binary crate — template

A `cp -r`-able starter for a Rust binary crate using the
**main-with-lib** variant: `src/main.rs` is a thin entrypoint, `src/lib.rs`
holds the logic, integration tests live in `tests/`, and `examples/`
links against the library half. `clap` is wired up for argument parsing.

## What to rename

The package name in `Cargo.toml` is `mybin` (snake_case to satisfy Rust
crate-naming rules cleanly; the *repo directory* can be `kebab-case`).
Replace it everywhere:

- `Cargo.toml` — `[package] name`, `[[bin]] name`, `[lib] name`.
- `src/main.rs` — `mybin::run()` call.
- `src/lib.rs` — `//! mybin` doc comment.
- `tests/integration_test.rs` — `use mybin::greet;`.
- `examples/basic.rs` — `mybin::greet(...)`.
- This `README.md` — replace the project-facing copy.

If your import path needs hyphens (`my-bin`), keep in mind Rust will
normalise them to underscores inside `use` statements (`use my_bin::...`).

## What to fill

- `Cargo.toml` — `description`, `repository`, `keywords`, `categories`.
- `LICENSE` — the placeholder MIT text needs your year and name.
- `src/cli.rs` — replace the `name`/`verbose` flags with your real CLI.
- `src/lib.rs` — replace `greet` and `run` with the real program.
- `tests/integration_test.rs` — write tests that hit the public API.

## What to delete

- This template `README.md` once you've internalised it (overwrite it
  with the user-facing README).
- The `greet`/`Cli::name` stub once you have real logic.
- `.github/workflows/ci.yml` if you don't use GitHub Actions.

## First run

```bash
cargo build
cargo test
cargo run -- alice              # prints "hello, alice"
cargo run --example basic       # exercises the library half
```

If `cargo test` reports passing tests for both the unit test in
`lib.rs` and the integration tests in `tests/`, the layout is wired
correctly.

## Adding a second binary

Drop a file in `src/bin/`:

```
src/bin/admin.rs
```

Cargo auto-discovers it. `cargo run --bin admin`. No `Cargo.toml`
changes needed.

## Pair this with

- `../GUIDE.md` — full reasoning behind this layout.
- `../../rust-library/` — for crates published to crates.io.
- `../../rust-workspace/` — when you grow into multiple crates.
