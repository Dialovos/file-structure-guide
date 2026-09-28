# Test colocation vs. separation

## TL;DR

Two viable patterns: **separated** (a `tests/` directory mirroring `src/`, the Python and Java/Maven norm) or **co-located** (test files sit next to source as `*.test.ts`, `*_test.go`, `__tests__/foo.ts`, the JS, Go, and Rust norm). Both work; neither is universally better. Pick one based on your language's idioms and your project's size, then apply it consistently across the repo. The single biggest mistake is mixing the two — a `tests/` directory *plus* scattered `*.spec.ts` files in `src/` doubles the cognitive load with no benefit.

## Principles & why

The choice is really about which adjacency you want to optimise: tests next to *source* (co-located) or tests next to *other tests* (separated). Co-location makes "what does this module test, exactly?" a one-glance answer — open the directory, the source and its test sit together. Separation makes "what's the test surface look like overall?" easy — open `tests/`, see the entire test estate in one place. Both are real questions; different teams ask one more often than the other.

Language conventions encode an implicit answer. Go's standard `testing` package finds files named `*_test.go` *in the same package directory* — co-location is the path of least resistance. Rust unit tests live inside the source file (`#[cfg(test)] mod tests`); integration tests live in a sibling `tests/` directory. Python's `pytest` traditionally discovers `tests/test_*.py`, with the test module mirroring the source layout. JavaScript's ecosystem is split (Jest can find `__tests__/` *or* `*.test.js` next to source; both are popular). When the language has a strong default, fight it only with a strong reason.

The "consistency over cleverness" rule matters because tests are read in two modes — *during* feature work (you want the test next to the code you're changing) and *during* triage (you want to scan the whole test surface fast). A consistent layout means muscle memory works in both modes. A mixed layout means every grep, every IDE jump, every coverage tool has to handle both shapes.

## When to use

**Use the separated `tests/` pattern when:**

- The language convention is separated (Python with pytest, Java/Maven `src/test/java`, Scala/sbt).
- You have a large codebase where the volume of test scaffolding (fixtures, helpers, integration setup) would clutter `src/`.
- You want strict separation between "shippable artefact" and "test-only code" — easier to build a wheel/jar that excludes `tests/` wholesale.
- Your test suite has a different deployment / packaging story than your source.

**Use the co-located pattern when:**

- The language convention is co-located (Go's `*_test.go`, Rust unit tests, JavaScript with `*.test.ts` or `__tests__/`).
- Modules are small and self-contained; "the test for this file" is always exactly one file.
- You want the test to move with the source under refactors — when you rename or move `auth.ts`, `auth.test.ts` follows automatically.
- New contributors should see immediately that a module *has* tests, without going hunting.

## When NOT to use

**Don't use separated when:**

- The language explicitly puts tests next to source (Go's `testing` looks in the package directory; fighting this means contorted build configs).
- Your test files outnumber your source files but are tiny — a parallel `tests/` tree with one-line test files becomes more navigation than content.
- You're in a polyglot repo where another co-located convention is already in force; consistency wins.

**Don't use co-located when:**

- The test files genuinely *are* a separate concern with their own scaffolding (large integration suites, end-to-end tests, performance benchmarks). Those go in their own top-level dir regardless of unit-test policy.
- Your build/packaging tooling can't reliably exclude `*.test.*` from a release artefact and you ship unit tests by accident.
- The language's convention pushes the other way and you'd be paying recurring tooling cost to swim against it.

## Tree diagram

```
separated (Python-style)/
├── src/
│   └── myapp/
│       ├── auth.py
│       └── billing.py
└── tests/
    ├── test_auth.py
    └── test_billing.py

co-located (JS/Go-style)/
└── src/
    ├── auth.ts
    ├── auth.test.ts
    ├── billing.ts
    └── billing.test.ts
```

## Naming rules

1. **Separated layout.** Mirror the source tree. If source lives at `src/myapp/auth.py`, the test lives at `tests/test_auth.py` (pytest) or `tests/myapp/test_auth.py` for deeper packages. Don't flatten — readers should jump from a source path to the matching test path mechanically.
2. **Co-located layout.** Use the language-convention suffix exactly: `*.test.ts` / `*.spec.ts` (Jest, Vitest), `*_test.go` (Go), `*.test.tsx` (React conventions). Don't invent a new suffix; tooling defaults won't pick it up.
3. **`__tests__/` directories** (a JS-ecosystem co-located variant) sit *next to* the source they cover, one per package or per src directory, not at repo root. They're co-located, just grouped.
4. **Integration / e2e tests** are a separate concern from unit tests. They typically go in a top-level `tests/`, `e2e/`, `integration/`, or `acceptance/` directory regardless of whether unit tests are co-located. Document this split in the README.
5. **Test fixtures / helpers** go alongside the tests they support: `tests/fixtures/`, `tests/helpers/`, or in co-located projects, `__fixtures__/`, `test-utils.ts`. Don't scatter them into `src/`.
6. **Pick one and document it.** Write the choice into `CONTRIBUTING.md` (or the project README) so newcomers know the convention before they add a test in the wrong shape.

## Worked example

A TypeScript service has `src/` with `*.test.ts` files mixed in, plus a legacy `tests/` directory with 30 more.

1. Choose by ecosystem idiom: for TS, co-located `foo.ts` and `foo.test.ts`.
2. Move each file in `tests/` next to its subject with `git mv`, renaming to `<subject>.test.ts`.
3. Update the test runner glob (`vitest` or `jest` `include`) to `src/**/*.test.ts` and confirm the count of discovered tests matches before and after.
4. Exclude test files from the build: `"exclude": ["src/**/*.test.ts"]` in the build tsconfig.
5. Keep cross-module integration tests in a top-level `tests/integration/` and say so in the README.

One rule remains: unit tests sit beside code, integration tests sit at the top.

## Anti-patterns

- **Mixed layout.** Some files have a sibling `*.test.ts`; others have a parallel `tests/` entry. Every grep needs both queries; every refactor risks orphaning the wrong copy. Pick one, migrate the rest.
- **`tests/` mirror that has drifted.** `src/auth/login.py` exists, but `tests/test_login.py` covers a deleted module from two refactors ago. The mirror only works if it's maintained — make moves atomic.
- **Tests in random locations.** A `test_quick.py` at the repo root, a `tmp_test.go` in `cmd/`. Either commit them to the conventional location or delete them.
- **One enormous `tests/test_everything.py`.** The mirror layout becomes useless when every test is in one file. One test module per source module (or per logical unit).
- **Fighting the language convention.** Forcing Go tests into a top-level `tests/` directory means losing access to package-private symbols and bending `go test`. Forcing Python tests next to source means most CI templates and `pyproject.toml` setups don't find them.
- **`src/test/`** *inside* the source tree as a co-located substitute. This is a Maven-ism that confuses Python or JS readers. If you want co-located, name it `__tests__/` or use `*.test.*` suffixes.

## Scaling & failure modes

- **Published packages** must not ship tests unless intended; verify with `npm pack --dry-run` or `unzip -l` of the wheel.
- **Large integration or end-to-end suites** need fixtures and data that don't belong beside source, so a top-level `tests/` is normal even in co-located repos.
- **Renames** of source files must carry their tests; co-location makes this automatic, separation needs a mirror-structure check.
- **Mixed conventions** across languages in a monorepo are fine if each package is consistent.

## Variants

- **Strict-separated.** All tests live in `tests/`; nothing test-related in `src/`. Cleanest packaging story.
- **Strict-co-located.** All tests sit next to source with the conventional suffix. Cleanest "where's the test for X?" story.
- **Hybrid: unit co-located, integration separated.** Unit tests live next to source (`*.test.ts`); integration tests, e2e tests, and benchmarks live in a top-level `tests/integration/`, `tests/e2e/`, `bench/`. Common in Rust (unit inline, integration in `tests/`) and many JS projects.
- **`__tests__/` grouping.** Co-located but each source directory has a `__tests__/` subfolder rather than peer `*.test.js` files. Reduces visual noise in directory listings; loses the "test sits literally next to source" payoff. A reasonable middle ground.
- **Doc-test variant.** Languages with doctest support (Rust, Python) put small tests *inside* docstrings or doc comments. Doesn't replace a unit-test policy; complements it.

## Adoption checklist

- [ ] The test runner discovers the same number of tests before and after any move.
- [ ] Build and package steps exclude test files.
- [ ] Unit vs integration test locations are documented.
- [ ] Each package uses a single convention.

## Real-world projects using this

- **Django** (Python) — separated layout: `tests/` at the project root mirroring the package tree. The Django docs explicitly recommend this for new projects.
- **Express.js** (JavaScript) — co-located `*.test.js` files inside `test/` subfolders per module historically; modern Node libraries skew toward `*.test.ts` next to source.
- **Go standard library** (`golang/go`) — co-located `*_test.go` is the language's own convention; the entire stdlib is the canonical example.
- **Rust standard library** (`rust-lang/rust`) — `#[cfg(test)] mod tests` *inside* source files for unit tests; a sibling `tests/` directory for integration tests. The hybrid variant in its native form.
- **pytest** (Python) — its own tutorials and the bundled `pytest` codebase use the separated `tests/` mirror layout, which has become the de facto Python convention.
- **React / Jest ecosystem** — the `__tests__/` directory pattern was popularised by Facebook's Jest defaults; many React projects still use it. Newer projects often prefer `*.test.tsx` next to source for the tighter co-location.

## Migration & references

To switch a repo from one layout to the other, do it in one big atomic commit (or a few large coherent commits) rather than module-by-module — partial migrations leave the repo in the worst-of-both state.

```bash
# Co-located -> separated (TS/JS):
#   For each src/foo/bar.ts with a sibling bar.test.ts,
#   move the test to tests/foo/bar.test.ts.
mkdir -p tests
git ls-files 'src/**/*.test.ts' | while read f; do
  rel="${f#src/}"
  dest="tests/${rel}"
  mkdir -p "$(dirname "$dest")"
  git mv "$f" "$dest"
done
git commit -m "refactor: migrate tests to tests/ mirror layout"

# Separated -> co-located (Python-style is rare to migrate; Go projects
# never go this direction). Sketch:
git ls-files 'tests/**/test_*.py' | while read f; do
  rel="${f#tests/}"
  base="$(basename "$rel" | sed 's/^test_//')"
  dir="$(dirname "$rel")"
  dest="src/${dir}/test_${base}"
  git mv "$f" "$dest"
done
```

After a migration, update:

- The test runner config (`pyproject.toml [tool.pytest.ini_options] testpaths`, Jest `testMatch`, etc.).
- CI configs that hard-code `tests/` paths.
- `CONTRIBUTING.md` to reflect the new convention.
- Any IDE settings checked into the repo (`.vscode/settings.json` test runners, etc.).

Further reading:

- *pytest documentation*, "Good Integration Practices" — canonical case for the separated layout.
- *Go documentation*, "Add a test" — canonical case for co-location.
- *The Rust Book*, ch. 11.3 "Test Organization" — explains the unit/integration split that grounds the hybrid variant.
- `principles/one-purpose-per-directory/` — sibling rule. A `tests/` directory has one purpose; co-located test files share their parent directory's purpose.
- `principles/naming-by-purpose-not-type/` — informs whether to call something `tests/` or organise tests by feature.
