# Naming conventions

## TL;DR

Use `kebab-case` for every directory and most files. The dash is the only universally safe word separator across shells, URLs, package registries, and search-engines. Deviate only where an ecosystem mandates otherwise (Python `snake_case`, Java dotted lowercase, .NET `PascalCase`), and document the deviation in that subtree's `CONTRIBUTING.md`.

## Principles & why

A name is an interface. It crosses your shell, your editor, your VCS, your URL bar, your CI logs, and (for OSS work) every search index that ever crawls you. The fewer characters you allow yourself, the more places the name remains identical.

Spaces force quoting. Mixed case fights case-insensitive filesystems (macOS, Windows). Underscores look like spaces in some fonts and break double-click word selection. Camelcase loses its word boundaries the moment it hits a URL slug or a search hit.

Kebab-case (`lowercase-words-with-dashes`) is the lowest common denominator that survives every one of those boundaries unchanged. Picking it as a default and treating ecosystem rules as the *only* exception keeps a polyglot repo legible.

## When to use

Always — for any directory you create in this repo, for any free-form note or document filename, and for any URL slug derived from a filename. If you are creating a new top-level area, a feature folder, a docs subdirectory, a sample-projects folder, or a dataset folder, kebab-case is the default.

Use it for branch names too (`feat/customer-onboarding`), for issue and PR slug-style references, and for any name that may eventually become part of a URL.

If you find yourself reaching for a space, an apostrophe, or a capital letter in a directory name, that's the trigger to stop and re-derive the name in kebab-case.

## When NOT to use

Do not fight the ecosystem when a tool inspects the directory name itself:

- **Python packages** — `snake_case` is required by PEP 8 because the directory name *is* the import path. `customer_onboarding/__init__.py` is correct; `customer-onboarding/` cannot be `import`ed.
- **Java / Kotlin** — packages are lowercase dotted (`com.example.foo`); the directory tree mirrors that with all-lowercase, no separators (`com/example/foo`).
- **.NET / C#** — convention is `PascalCase` for project, namespace, and folder names (`Acme.Billing/Invoices/`).
- **Go** — short, lowercase, no separators (`internal/auth`, not `internal/auth-service`).

When you take an exception, write it down once in the affected subtree's `CONTRIBUTING.md` so the next contributor doesn't "fix" it back to kebab-case.

## Tree diagram

```
good/
├── customer-onboarding/
├── api-clients/
└── 2026-04-meeting-notes/

bad/
├── Customer Onboarding/   ← spaces, mixed case
├── api_clients/           ← underscores outside ecosystem rule
└── final_FINAL.txt        ← inconsistency in one tree
```

## Naming rules

1. Lowercase ASCII letters, digits, and hyphens only. No spaces, no underscores, no Unicode, no punctuation.
2. Start with a letter unless it's a date prefix (`2026-04-meeting-notes/` is fine).
3. Use a single hyphen between words; never double-hyphens or trailing hyphens.
4. Keep names ≤ 40 characters. If you can't, the directory is doing too much — split it.
5. Singular vs plural is by *content shape*: a directory holding many of one kind is plural (`invoices/`), a directory holding one logical thing is singular (`auth/`).
6. Date-prefixed directories use ISO `YYYY-MM-DD` or `YYYY-MM` first, then a kebab-case slug (`2026-04-meeting-notes/`).

## Anti-patterns

- **`Customer Onboarding/`** — spaces and capitals. Forces every shell command to quote it; breaks tab completion in the worst way (silent partial match).
- **`final_v2_FINAL_real.txt`** — encoding revisions in the name instead of using git. See `versioning-in-paths/`.
- **Mixed conventions in one tree** — `auth/`, `Billing/`, `customer_support/` side by side. Pick one and migrate the others; consistency beats local correctness.
- **Abbreviations nobody else uses** — `cust-onb/` instead of `customer-onboarding/`. The four characters you save cost every future reader a lookup.
- **Trailing date when a date prefix would sort better** — `meeting-notes-2026-04/` does not sort chronologically; `2026-04-meeting-notes/` does.

## Variants

- **Strict kebab** — no exceptions, ever. Forces ecosystem-deviating subtrees out of the main repo. Clean but rarely realistic.
- **Snake-only-where-mandated** (this repo's policy) — kebab everywhere, document each ecosystem exception in `CONTRIBUTING.md` of the affected subtree.
- **Lower-with-hyphens-or-underscores** — allow either, but pick one per repo and stick to it. Common in older Python/Ruby monorepos.
- **Type-suffix variant** — `customer-onboarding.feature/`, `customer-onboarding.docs/`. Adds machine-grepability at the cost of human readability; use only with tooling that depends on the suffix.

## Real-world projects using this

- **Linux kernel** — `drivers/`, `arch/`, `fs/` and most subdirectories are short kebab/lowercase; the discipline scales to tens of thousands of dirs.
- **npm** — package names enforce kebab-case (lowercase + hyphens) at the registry level.
- **Cargo / crates.io** — crate names accept kebab and snake; convention overwhelmingly favors kebab (`serde-json` exists alongside `serde_json` for the import path).
- **Kubernetes** — every resource name is kebab-case (`my-deployment`, `kube-system`); the convention is enforced by API validation.
- **Apache Foundation projects** — module dirs are lowercase, hyphenated (`apache-tomcat-embed-core`).
- **Homebrew** — formula filenames and tap repos are kebab-case (`homebrew-core`, `node-build`).

## Migration & references

To migrate a tree off mixed conventions, do it in one commit per directory rename so `git log --follow` keeps history readable:

```bash
git mv "Customer Onboarding" customer-onboarding
git mv api_clients api-clients
git commit -m "rename: kebab-case directories"
```

For files that other tools reference (CI configs, docs links, code imports), grep for the old name first:

```bash
git grep -l "Customer Onboarding"
```

Further reading:

- POSIX portable filename character set (IEEE Std 1003.1, §3.282) — defines the safe character set this rule mirrors.
- `principles/iso-date-formats/` — pairs with this rule for date-prefixed directories.
- `principles/capitalization-policy/` — when capitals *are* mandatory (`README.md`, `LICENSE`).
- npm, Cargo, and Go style guides — all converge on the same lowercase-with-separator default.
