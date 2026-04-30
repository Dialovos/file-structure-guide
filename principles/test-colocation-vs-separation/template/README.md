# Test colocation vs. separation template

This template ships **both** layouts side by side so you can compare
them, then pick one for your project. Don't ship both — the whole point
of the policy is to apply *one* convention consistently.

## What's here

```
template/
├── README.md
├── separated-example/
│   ├── src/
│   │   └── main.py            ← source
│   └── tests/
│       └── test_main.py       ← test in a parallel tests/ tree
└── colocated-example/
    ├── main.ts                ← source
    └── main.test.ts           ← test next to source
```

Two trivial example modules, each with one test file, demonstrating the
two patterns in their native language idioms (Python = separated,
TypeScript = co-located).

## Layout 1: separated (Python-style)

`separated-example/` shows the pattern most natural in Python and
Java/Maven:

- Source lives under `src/` (here, just `src/main.py`).
- Tests live under `tests/`, with the directory structure mirroring
  `src/` and filenames prefixed `test_` (here, `tests/test_main.py`).

Pytest discovers files matching `test_*.py` automatically; the runner
does not need configuration to find this layout. In a larger project,
`src/myapp/auth.py` would be tested by `tests/myapp/test_auth.py`.

Strengths: clean packaging boundary (`tests/` is excluded from the
shipped wheel), good for large projects with lots of test scaffolding.

## Layout 2: co-located (JS / Go-style)

`colocated-example/` shows the pattern most natural in JavaScript,
TypeScript, Go, and Rust unit testing:

- Source: `main.ts`
- Test: `main.test.ts` — same base name, `.test` infix, same directory.

Vitest, Jest, and Go's `testing` package discover the `*.test.*` /
`*_test.go` suffix automatically. In a larger project,
`src/auth/login.ts` is tested by `src/auth/login.test.ts`.

Strengths: tests follow source under refactor (move/rename), the
"where's the test for X?" question has a one-glance answer, smaller
projects feel cleaner with no parallel `tests/` tree.

## To adopt this template

1. Pick one layout based on your language's convention and your team's
   preference. Don't copy both into your project.
2. Copy the relevant subfolder's *structure* — not the example files —
   into your project. Adjust paths to match your actual package name
   (e.g. `src/myapp/...` instead of just `src/main.py`).
3. Configure your test runner if needed:
   - **pytest** (separated): set `testpaths = ["tests"]` in
     `pyproject.toml [tool.pytest.ini_options]`.
   - **Vitest / Jest** (co-located): the default `*.test.ts` /
     `*.spec.ts` matchers are sufficient.
   - **Go**: nothing to configure; `go test ./...` finds `*_test.go`.
4. Document the choice in `CONTRIBUTING.md` so contributors don't drift
   into the other pattern.

## A note on hybrid layouts

Rust uses a hybrid: unit tests are inline (`#[cfg(test)] mod tests`)
*inside* the source file, and integration tests live in a separate
top-level `tests/` directory. Many JS projects do something similar —
unit tests co-located, end-to-end tests in `e2e/` or `tests/e2e/`. The
hybrid is fine; it just requires a slightly longer rule in
`CONTRIBUTING.md`. The forbidden case is *unintentional* hybrid: some
modules co-located, others separated, with no documented rule.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this
`template/README.md` to exist. Don't delete it before replacing.
