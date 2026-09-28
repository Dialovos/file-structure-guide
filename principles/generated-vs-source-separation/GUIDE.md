# Generated vs. source separation

## TL;DR

Anything a build step *produces* — compiled JS in `dist/`, Rust binaries in `target/`, Java class files in `build/` or `target/`, Hugo's `public/`, downloaded dependencies in `node_modules/` or `.venv/` — lives in a dedicated directory, is gitignored, and is fully regeneratable from source. *Never* mix generated artefacts with source. The dividing line is "could a fresh clone reproduce this from `git pull && <build command>`?" Yes -> generated, gitignore it. No -> source, track it.

## Principles & why

The reason this matters comes down to two questions readers ask of any directory: "is this hand-written?" and "if I delete this, will it come back?" Mixing those answers in one directory destroys both signals. A reader can't tell at a glance which files are authoritative. A maintainer can't safely run `rm -rf dist/` because some hand-written file might be in there. Toolchains can't reliably exclude or rebuild because the input/output sets are tangled.

Separation also makes the build idempotent and portable. If `dist/` is *only* output, then `rm -rf dist/ && npm run build` always reproduces a clean state — no leftover stale artefacts, no manual cleanup. CI can cache `node_modules/` independently from `src/`. Docker builds can copy source and run the build, ignoring whatever the developer's local `dist/` happened to contain. The cleanliness of these workflows is downstream of the separation, not separable from it.

The third reason is review hygiene. When `dist/` is committed by mistake, every code change generates a giant diff in the bundled output. PRs become unreadable. Reviewers waste cycles asking "did you intend to change `dist/main.js` line 47829?" The fix is to never track the directory at all — `.gitignore` it from day one and let the build produce it locally.

## When to use

Always — for any project with a build step. The output directory name follows ecosystem convention; the *separation* itself is universal:

- **JavaScript / TypeScript** — `dist/`, `build/`, `out/`, `.next/`, `.nuxt/`, `lib/` (for libraries that ship pre-compiled). `node_modules/` for installed deps.
- **Rust** — `target/` (Cargo's default; holds debug, release, doc builds, all generated).
- **Java / Maven** — `target/`. **Gradle** — `build/`. **CMake / Make / C / C++** — typically `build/` or `out/`, sometimes `_build/`.
- **Python** — `build/`, `dist/`, `*.egg-info/`, `.venv/` for virtualenvs, `__pycache__/` for byte code (almost always gitignored).
- **Static site generators** — Hugo `public/`, Jekyll `_site/`, Eleventy `_site/`, Next.js export `out/`, MkDocs `site/`.
- **Docs builders** — Sphinx `_build/`, Doxygen `html/` or `latex/`, mdBook `book/`.

Whatever your stack: pick the convention, stick to it, gitignore it.

## When NOT to use

Genuinely rare. The only cases where this rule doesn't apply:

- **Static-only projects with no build step.** A pure-HTML/CSS site, a markdown wiki, a config-only repo. There's nothing being generated, so there's nothing to separate.
- **Libraries that intentionally ship pre-built code in-repo** for ecosystems without a runtime build step. Some legacy npm packages commit `lib/` because consumers expect to `require()` JS directly. Modern practice: build during `npm publish`, not commit. If you must commit pre-built output, isolate it to one well-marked directory and document it.
- **Vendored generated code** as input to *another* build (e.g. protobuf-generated stubs that downstream consumers can't regenerate). Track it, but in a directory clearly marked `generated/` with a README explaining the regen command. Treat it as source-of-record from the consumer's perspective even though it's generated upstream.

In all three cases, the rule still bends, doesn't break — generated stays in *its own directory*, just possibly tracked.

## Tree diagram

```
project/
├── src/                ← source (tracked)
│   └── main.ts
├── dist/               ← generated (gitignored)
│   └── main.js
├── node_modules/       ← generated (gitignored)
└── package.json
```

## Naming rules

1. **Use the ecosystem's default name.** Don't rename `target/` to `output/` for Rust; tooling and contributors expect the standard. Same for `dist/`, `build/`, `node_modules/`, `.venv/`.
2. **One output directory per build pipeline.** If your project has a frontend bundle and a docs site, you'll have *two* output directories (`dist/` and `docs/_site/`), each gitignored. Don't merge them into one `output/`.
3. **Mark intentionally tracked generated code.** If you have to commit generated files (rare; protobuf stubs, etc.), put them in `generated/` or `gen/` and add a README explaining the regen command. Don't pretend they're source.
4. **Underscore prefix for sort-order tricks** (`_build/`, `_site/`) is fine when the ecosystem already does it (Sphinx, Jekyll). Don't invent your own prefix; follow the convention you're already in.
5. **Caches go in dotfile dirs at the source root** (`.cache/`, `.next/`, `.pytest_cache/`) so they hide from default `ls` and clearly signal "tool state, regeneratable, ignore."
6. **Never name a source directory the same as an output directory.** If your build outputs to `build/`, don't have a `build/` directory of source files. The collision will produce one of the worst classes of confusing bug.

## Worked example

A Python project commits `build/`, `*.egg-info/`, and a compiled `docs/_build/` because someone ran `git add .` once.

1. Apply the litmus test to each directory: could `git clone && <build command>` recreate it? If yes it's generated.
2. Untrack without deleting: `git rm -r --cached build docs/_build` (repeat for each generated directory).
3. Add them to `.gitignore` at the repo root, anchored (`/build/`, `/docs/_build/`).
4. Point every tool at one output directory per kind (`dist/` for wheels, `docs/_build/` for docs) and document them in the README.
5. In CI, build from a clean checkout to prove the sources are complete.

Then `git status` after a full build is clean, which is the ongoing proof the separation holds.

## Anti-patterns

- **`dist/` committed to git.** Every PR has a 50,000-line diff in the bundled output; review becomes impossible. Gitignore it; let the build produce it locally and CI/registry produce it for releases.
- **Source inside `node_modules/`.** Hand-edits to a vendored dependency. Survives until someone runs `npm install --force` or deletes the directory to debug. Use a patch tool (`patch-package`, `pnpm patch`) instead, or fork the dep.
- **Mixed `src/` containing both authored and generated files** with no marker on which is which. Common with codegen tools that drop output next to source. Either move the generated files to `generated/` or use a clear suffix (`*.generated.ts`) plus a gitignore entry.
- **`build/` next to a source `Build/` (case-collision)** on case-insensitive filesystems. macOS and Windows treat them as the same directory; linux as separate. Avoid case differences as semantic carriers.
- **Tracked `__pycache__/` or `*.pyc`.** Python byte code is always regeneratable; tracking it makes git pulls noisy and merges painful.
- **Tracked `.next/` or `.cache/`** from a Next.js / build-tool project. These are local incremental-build state, not artefacts. CI doesn't need them; collaborators definitely don't.

## Scaling & failure modes

- **Checked-in generated files** are sometimes right: lockfiles, generated API clients, protobuf stubs that consumers need without a toolchain. Mark them (`# generated, do not edit` header, `linguist-generated` in `.gitattributes`) and add a CI check that regeneration produces no diff.
- **Multiple build targets** multiply output directories. Keep them under one parent (`build/<target>/`) so one ignore rule covers them.
- **Caches inside source trees** (`__pycache__/`, `.pytest_cache/`) are generated too; ignore by pattern, not by path.
- **Editors that index generated code** slow down; exclude output directories in editor and search config.

## Variants

- **Ecosystem-default-only.** Just use the conventional name (`target/`, `dist/`, `build/`, `node_modules/`) and gitignore. The simplest, recommended for most teams.
- **Custom-named for archival.** Ship "snapshot" builds to a named directory (`out-2026-04-snapshot/`, `dist-v2.1.0/`) for archival or A/B comparison. These are typically still gitignored but checked into a release artefact store.
- **Underscore-prefixed for sort order.** `_build/`, `_site/` to push generated dirs to the start of an alphabetical listing. Common in static-site generators and Sphinx.
- **Hidden / dotfile cache dirs.** `.next/`, `.cache/`, `.pytest_cache/`, `.mypy_cache/` for transient build state. Combines this rule with the hidden-files-policy: dotfile because it's plumbing, gitignored because it's regeneratable.
- **`generated/` for intentionally-tracked generated code.** Used when downstream consumers can't run the regen command themselves (protobuf, OpenAPI clients shipped to non-build environments). Distinct from `src/` so readers know the lifecycle.

## Adoption checklist

- [ ] After a full build and test run, `git status --porcelain` is empty.
- [ ] Each generated directory is named in `.gitignore` and appears in the README's build section.
- [ ] Any deliberately committed generated file is labeled and has a regeneration check in CI.
- [ ] A fresh clone builds with one documented command.

## Real-world projects using this

- **Maven** — `target/` is the canonical output directory across the entire Java/Maven ecosystem; explicitly gitignored in every Maven project's recommended `.gitignore`.
- **Cargo / Rust** — `target/` is Cargo's output dir; the official `.gitignore` template for Rust ships with `target/` as the first entry.
- **npm / Node** — `node_modules/` is the per-project dependency cache; universally gitignored. The npm CLI itself owns the contract.
- **Webpack / Vite / Rollup / esbuild** — all default to `dist/` for bundle output; gitignored by convention.
- **Hugo** — `public/` is the rendered static site; gitignored when the site is deployed via CI, tracked when deploying via GitHub Pages with a `gh-pages` branch.
- **Jekyll / Eleventy** — `_site/` is the rendered output; gitignored, with deploy pipelines pushing it to a hosting provider.
- **Sphinx** — `_build/` for HTML/PDF docs output; gitignored, with Read the Docs or CI doing the production builds.

## Migration & references

To clean up a repo that has tracked generated output:

```bash
# 1. Identify candidates: large diffs every commit, tool-produced names.
git log --pretty=format: --name-only | sort -u | grep -E '^(dist|build|target|out|_site|public|node_modules|__pycache__)/'

# 2. Add to .gitignore (an example block).
cat >> .gitignore <<'EOF'

# --- Build outputs (regeneratable) ---
dist/
build/
target/
out/
_site/
public/

# --- Dependency caches ---
node_modules/
.venv/
__pycache__/
EOF

# 3. Remove the tracked copies *without* deleting the local files.
git rm -r --cached dist/ build/ target/ node_modules/ 2>/dev/null || true

# 4. Commit the policy change as a single, well-labelled commit.
git add .gitignore
git commit -m "chore: gitignore build outputs and caches per generated-vs-source-separation"
```

After the migration:

- Verify the build still produces a working artefact: `<your build cmd>` then sanity-check `dist/` (or your equivalent) locally.
- Update CI to run the build before deploying (it should already, but confirm).
- For static sites that previously relied on a tracked `_site/` for GitHub Pages, switch to a build action (`actions/jekyll-build-pages`, `actions/configure-pages`, `peaceiris/actions-gh-pages`).

Further reading:

- *The Twelve-Factor App*, "V. Build, release, run" — the doctrinal source for separating build artefacts from source.
- *Maven Standard Directory Layout* — formal definition of `target/` as the build output.
- *Cargo Reference: target directory* — Rust's official spec for `target/`.
- `principles/gitignore-and-keep-files/` — sibling rule covering the gitignore mechanics in detail.
- `principles/hidden-files-policy/` — for cache directories that combine "generated" with "hidden" (`.next/`, `.cache/`).
