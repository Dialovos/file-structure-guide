# Depth vs breadth

## TL;DR

Prefer flat trees. Aim for at most three levels between the repo root and any leaf concept; four is the warning line; five or deeper is almost always wrong. Width is cheap to scan; depth compounds cognitive cost on every traversal.

## Principles & why

Every directory you cross is a context switch. The reader has to load the parent's purpose, find the relevant child, push that onto the stack, repeat. A six-level path means the reader holds six contexts before they look at the file.

Depth also fights tooling. Long paths break shell completion, exceed Windows MAX_PATH limits (260 chars on legacy APIs), wrap in editor breadcrumbs, and dominate `git diff` output. Width, by contrast, scrolls a screen — annoying once, painless thereafter.

The classic counter-argument is "but logical hierarchy". Real systems have hierarchy *somewhere*, but most organisations push it into the wrong axis: they nest by *type* (`components/forms/login/`) when they should peer by *purpose* (`auth/`, `billing/`). The peer arrangement is shallower because each peer is independently meaningful; the nested arrangement only makes sense top-down.

## When to use

Apply this rule whenever you decide where to put a new file or directory:

- New feature → does it deserve a peer at the existing level, or is it genuinely a child of one peer?
- Existing directory has > 30 children → split by content shape, not by inventing a parent.
- Path crosses four levels and the leaf is just a file → flatten one of the middle levels into the leaf name.
- Generated docs / build artifacts → keep them at known shallow paths (`dist/`, `build/`, `docs-out/`) so tooling stays portable.

This is the tiebreaker principle when two layouts are otherwise equal: pick the shallower one.

## When NOT to use

A handful of ecosystems mandate deep layouts and you cannot fight them without paying a tooling tax:

- **Maven / Gradle** — `src/main/java/com/example/foo/Bar.java` is fixed by the toolchain. Java's package-as-path mapping forces the depth.
- **Cookiecutter / Yeoman generators** — keep the generator's output as it ships; downstream tooling depends on it.
- **OS conventions** — `~/.config/<app>/<profile>/<file>` is set by XDG and apps that respect it.
- **Genuinely deep domains** — a JSON schema mirroring a deeply nested third-party API may need depth that matches the API; flattening would lose the mirror.

When you take the depth, do it deliberately and with a `README.md` at the deep root that explains why the depth exists.

## Tree diagram

```
shallow-good/
├── auth/
│   ├── login.ts
│   └── signup.ts
├── billing/
│   ├── invoices.ts
│   └── payments.ts
└── reports/
    └── monthly.ts

deep-bad/
└── src/
    └── main/
        └── app/
            └── modules/
                └── auth/
                    └── components/
                        └── forms/
                            └── login.ts   ← 8 levels
```

## Naming rules

1. The repo root counts as level 0; the first dir is level 1.
2. A "leaf concept" is a directory whose contents are all files, not further subdirectories.
3. Aim for leaf depth ≤ 3. Tolerate 4 with a written reason. Treat ≥ 5 as a defect to refactor.
4. Use `category/feature/file.ext` (3 levels) before `category/subcategory/feature/file.ext` (4 levels).
5. If a feature dir grows internal nesting (`feature/lib/`, `feature/util/`, `feature/types/`), it's usually time to split the feature into peers, not add depth.
6. Generated and vendored content lives at known shallow paths (`dist/`, `build/`, `target/`, `vendor/`, `node_modules/`).

## Worked example

A service has `src/main/app/modules/auth/components/forms/login.ts`: eight levels to reach one file.

1. Count depth from the repo root to each leaf: `find . -type f -not -path './.git/*' | awk -F/ '{print NF-1}' | sort -n | uniq -c`.
2. Collapse ceremonial levels first. `src/main/app/` adds nothing, so the code lives at `src/`.
3. Replace the `modules/` layer with the module names themselves: `src/auth/`.
4. Flatten `components/forms/` to `src/auth/login-form.ts`. Filenames now carry what the folder names used to.
5. Re-run the count. The target is a histogram whose tail stops at depth 3 or 4.

Result: `src/auth/login-form.ts` (three levels). The import path shrank from 9 segments to 3, and `auth/` now lists 6 files instead of hiding 6 folders.

## Anti-patterns

- **`src/main/app/modules/...`** ladder — four wrappers before any code. Common in Java-shaped projects copied into JS or Python where they aren't required.
- **One-child chains** — `docs/api/v1/` where `v1/` contains exactly one subdir, which contains exactly one subdir. Collapse them.
- **Type-nesting** — `components/buttons/primary/large/`. Replace with peers (`components/primary-large-button.tsx`) or flatten via composition.
- **Mirror-the-URL** — copying a URL hierarchy directly into a filesystem when the URL was already too deep.
- **"Just one more level"** — adding a parent for one item with the expectation more will arrive. They rarely arrive in the same shape; you've sunk the cost early.

## Scaling & failure modes

- **Wide isn't free either.** A directory with 80 children is as hard to scan as a deep tree. Past about 15 siblings, group by purpose (see `one-purpose-per-directory`) or add an `INDEX.md`.
- **Framework-imposed depth** (Maven's `src/main/java/com/example/app/`) is outside your control. Count from the first level you own.
- **Monorepos** legitimately add one or two levels (`apps/`, `packages/`). Treat the workspace prefix as free and apply the budget inside each package.
- **Deep trees regrow** through copy-paste of an existing deep template. Review new directories in pull requests.

## Variants

- **Strict 3-level** (this repo's default) — every leaf concept reachable in three levels. Forces hard splitting decisions early.
- **Pragmatic 4-level** — three for almost everything, four allowed when a domain genuinely justifies it, with a `README.md` explaining why.
- **Width threshold split** — flat until any directory exceeds N peers (often 30), then split by content shape. Common in monorepos where one feature dominates.
- **Hexagonal / clean-architecture** — deliberately deeper (`domain/usecase/port/adapter/`); accept the depth as the cost of explicit dependency direction.
- **Single-file-per-concept** — extreme flatness; one `auth.ts` instead of `auth/*.ts`. Works until it doesn't; the file becomes the directory and the rule re-applies inside the file.

## Adoption checklist

- [ ] The depth histogram has no leaf deeper than 4 (excluding vendored or generated trees).
- [ ] No directory holds a single child that is itself only a directory.
- [ ] No directory holds more than about 15 entries without an index.
- [ ] Exceptions (framework-mandated depth) are named in the README.

## Real-world projects using this

- **Linux kernel** — `drivers/`, `arch/`, `fs/`, `mm/`, `net/` are deliberately peers at the top level; the project has resisted reorganising them into a deeper hierarchy for thirty years.
- **Go standard library** — `net/`, `os/`, `io/`, `fmt/` are peers; subpackages are added only when there's a genuine sub-domain.
- **dotnet/runtime** — `src/coreclr/`, `src/libraries/` are flat-ish peers with feature dirs as children.
- **Rust workspaces** — `crates/<name>/src/` is the canonical three-level depth; nested workspaces are rare and considered a smell.
- **Kubernetes** — `pkg/`, `cmd/`, `staging/` peers at the top; even with the project's massive scope, leaf depth stays small.
- **`sqlite3` source tree** — famously flat; almost everything is in `src/` as peers.

## Migration & references

To shallow a deep tree, do it one collapse per commit so reviewers can follow:

```bash
# Collapse src/main/app → src/
git mv src/main/app/* src/
rmdir src/main/app src/main
git commit -m "flatten: drop src/main/app wrapper"
```

For renames that change import paths, follow with a code-side commit so the build is green at every step:

```bash
# After moving, fix imports
git grep -l "src/main/app" -- '*.ts' | xargs sed -i 's|src/main/app|src|g'
git commit -m "refactor: update imports after flatten"
```

Further reading:

- "The seven plus or minus two" working-memory bound (G. A. Miller, 1956) — informs the breadth-not-depth heuristic.
- `principles/one-purpose-per-directory/` — pairs with this rule to decide *what* to flatten into peers.
- `principles/naming-by-purpose-not-type/` — sibling principle: peers named by purpose stay shallower than children named by type.
- The Pragmatic Programmer (Hunt & Thomas), §"Orthogonality" — independence at the file/dir level.
- Go project layout conventions (https://github.com/golang-standards/project-layout) — opinionated but the depth limit is consistent with this rule.
