# README placement

## TL;DR

Put a `README.md` in every directory a stranger might enter without a guide. The rule is "navigational point", not "every directory". A five-line README at a junction is more useful than a thousand-word one at the root.

## Principles & why

A repository is read more often than it's written, and most reads start by opening a directory in a browser or file tree. GitHub, GitLab, Gitea, and most file managers render `README.md` automatically — so a reader who lands at `src/billing/` either gets your one-paragraph orientation or they fend for themselves.

The cost of a missing README at a junction is real: a stranger has to grep, infer, or ask. The cost of a redundant README inside an obviously-named single-purpose dir is also real: it's another file to keep in sync, and stale README content is worse than none.

The principle splits the difference: READMEs go where reading them saves a question. Repo root, every category, every subtree whose purpose is non-obvious from name + content. Skip them in tiny self-evident leaves.

## When to use

Add a `README.md` whenever a directory is any of:

- The repo root (always).
- A top-level category (`src/`, `docs/`, `tests/`, `scripts/`).
- A subtree with multiple files whose collective purpose isn't obvious from the directory name (`src/billing/` — what does billing include?).
- A directory grouping conventions (`migrations/`, `fixtures/`, `examples/`) where contributors need to know naming or structure rules.
- A directory holding generated content where readers need to know not to edit it.
- Any subtree whose existence answers "why is this here?" — a deliberate non-default choice deserves the explanation in place.

The README at a junction should answer three questions: *what's here, how is it organised, where do I go next.* Five lines is plenty.

## When NOT to use

Skip the README when the directory's purpose is trivially clear:

- **Tiny tooling dirs** — `.github/`, `.vscode/`, `.devcontainer/`. Their convention is industry-standard; an extra README is noise.
- **Self-describing leaves** — `migrations/` containing `2026-04-30-add-users.sql`, `2026-04-30-drop-orders.sql`. The pattern speaks for itself.
- **Single-purpose containers** — `assets/icons/` containing nothing but `.svg` files; `fixtures/users/` containing nothing but `.json` files.
- **Auto-generated trees** — `node_modules/`, `target/`, `dist/`. Your `.gitignore` should exclude them; if they're tracked, the parent's README should explain why.
- **Tests mirroring src** — if the test layout is a one-to-one mirror of `src/` and the parent `tests/README.md` says so, individual test directories don't each need their own README.

The fail-safe heuristic: if you couldn't add anything beyond the directory name without padding, don't add the file.

## Tree diagram

```
project-root/
├── README.md           ← required
├── src/
│   ├── README.md       ← required (it's a navigational point)
│   ├── auth/
│   │   ├── README.md   ← optional (small, self-evident)
│   │   └── login.ts
│   └── billing/
│       └── README.md   ← required (multiple files, non-obvious purpose)
└── docs/
    └── README.md       ← required
```

## Naming rules

1. The file is always `README.md` — uppercase, exactly five characters before the extension. Most rendering tools pattern-match this exact spelling.
2. One README per directory, at its root. Never `README2.md` or `readme-extra.md`; if it's that long, split the directory.
3. The first heading is the directory's name or one-line purpose: `# Billing` or `# Billing — invoices, payments, refunds`.
4. Keep it ≤ ~30 lines unless the directory genuinely has that much to explain. Long-form docs belong in `docs/` and link from the README.
5. Cross-link siblings and parent: a junction README that doesn't tell you where to go next isn't doing its job.
6. Don't repeat the parent's README. Each level adds *its own* orientation, not a recap of the level above.

## Worked example

A repo has one long root README and none of `src/`, `docs/`, or `scripts/` explain themselves.

1. List the navigational points: directories a newcomer enters with a question. `find . -maxdepth 2 -type d -not -path './.git*'`.
2. Add a five-line `README.md` to each junction: what lives here, how it relates to its neighbors, one command to run or test it.
3. Trim the root README to summary, quick start, and a map of links to the sub-READMEs.
4. Link sibling READMEs to each other so there are no dead ends.
5. Check that every README opens with a one-sentence summary, which is what previews and search results display.

Result: a stranger can open any junction and know where they are in under 10 seconds.

## Anti-patterns

- **README missing at the repo root** — every package manager, code host, and search index treats this as the project's front door. Skipping it here is malpractice.
- **README at every leaf, including `migrations/2026-04-30-add-users-table/`** — overkill; the directory name is the explanation.
- **README that just lists `ls`** — the file tree is already visible; the README's job is to add *meaning*, not enumerate files.
- **Stale READMEs** — describes a structure that no longer exists. Worse than missing; readers act on wrong info.
- **README as the only docs** — a 2,000-line README hides itself. Move detail to `docs/` and keep README short.
- **Different `README.md` casings** — `Readme.md`, `readme.md`, `README.markdown`. Some renderers don't pick them up; pick exactly one (`README.md`) and stick to it.

## Scaling & failure modes

- **Every-directory READMEs** rot fastest. Skip small self-evident directories (`auth/` with two files).
- **Duplication** between the root README and sub-READMEs drifts; link instead of copying.
- **Generated docs** may replace a hand-written README at deep levels; state that in the parent README.
- **Monorepos** need a README per package plus a root README that maps packages to owners.

## Variants

- **Strict-everywhere** — every directory, even single-purpose leaves, gets a README. Common in regulated projects where "no undocumented directory" is an audit rule.
- **Navigational-points-only** (this repo's policy) — README at junctions, skip self-evident leaves. Best balance for active projects.
- **Index-only-at-roots** — only repo root and top-level category dirs (`src/`, `docs/`) get READMEs; everything below relies on naming. Fast to maintain, weak for newcomers.
- **MOC-style** — one large `INDEX.md` or `MOC.md` at the root replaces the per-dir READMEs. Works for note vaults; brittle for code.
- **Auto-generated READMEs** — tools like `doctoc`, `markdown-toc`, or custom scripts emit READMEs from front-matter. Keeps content fresh but requires the generator step in CI.

## Adoption checklist

- [ ] The root and each top-level directory have a README that starts with a one-line summary.
- [ ] Each README states how to run or test what is in that directory, if applicable.
- [ ] READMEs link to neighbors and to the root, so there are no dead ends.
- [ ] Setup commands in READMEs are run from a clean clone at least once a quarter.

## Real-world projects using this

- **Apache Foundation projects** — every module has a top-level README explaining its role inside the larger project.
- **kubernetes/kubernetes** — READMEs at every navigational point: `cmd/`, `pkg/`, each major subpackage, plus a root README that's a project-scale orientation.
- **Rust workspaces** — convention is one README per crate; `cargo` and crates.io both expose them.
- **The Go standard library docs** — every package has package-level documentation that serves the same role; the convention is rigorous.
- **Linux kernel** — many subsystem directories have READMEs (often `Documentation/`-linked); not universal but the convention is strong where it matters.
- **`facebook/react`** — root README plus a README in each major subdirectory (`packages/react/`, `packages/react-dom/`).

## Migration & references

To audit an existing repo for missing junction READMEs:

```bash
# List directories with > 1 child but no README
find . -type d -not -path './.git/*' | while read d; do
  count=$(find "$d" -maxdepth 1 -mindepth 1 | wc -l)
  if [[ $count -gt 1 && ! -f "$d/README.md" ]]; then
    echo "missing: $d"
  fi
done
```

To remove redundant leaf READMEs:

```bash
# Find READMEs that are < 5 lines and live next to obvious siblings
find . -name README.md | while read f; do
  lines=$(wc -l < "$f")
  [[ $lines -lt 5 ]] && echo "tiny: $f"
done
```

Then triage by hand — small isn't automatically bad; a five-line README at the right junction is exactly the goal.

Further reading:

- GitHub's "About READMEs" docs (https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) — the rendering rules this convention relies on.
- `principles/indexes-and-mocs/` — when a README is no longer enough and you need an index file.
- `principles/one-purpose-per-directory/` — pairs with this rule: clear purpose per dir means short READMEs.
- "Standard Readme" spec (https://github.com/RichardLitt/standard-readme) — useful section template for repo-root READMEs.
- The Diátaxis framework (https://diataxis.fr) — broader docs taxonomy when README alone is no longer enough.
