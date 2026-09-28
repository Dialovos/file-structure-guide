# Stable vs volatile separation

## TL;DR

Don't mix what changes daily with what changes yearly. Stable content (source code, hand-written configs, raw inputs) and volatile content (logs, caches, build outputs, processed data) belong in separate directories — they have different backup needs, different gitignore needs, different review needs, and different blast radii when something goes wrong. The classic mistake is `data/` containing both an immutable dump and last night's regenerable artifacts.

## Principles & why

Stable and volatile content fail in different ways. Lose your `src/` and you've lost work; lose your `.cache/` and you've lost nothing — it'll regenerate on the next run. The filesystem doesn't know the difference unless you tell it, and the cheapest way to tell it is by directory.

Once stable and volatile are separated, every downstream policy becomes mechanical. Backup tools include the stable trees and skip the volatile ones. `.gitignore` lists the volatile dirs (and only those). CI cleans the volatile dirs between runs but never touches the stable ones. Code review focuses on stable changes; volatile diffs are noise. Mixing them couples every policy decision to per-file judgement, which scales poorly and breaks under deadline.

The principle generalises beyond filesystems: it's the same reason databases distinguish persistent storage from caches, and the same reason XDG splits config / data / cache / state into four dirs. The shape varies by ecosystem, but the underlying observation is universal: *change frequency is a structural property*; treat it as one.

## When to use

Apply this whenever a tree mixes content with very different lifetimes:

- Any project that produces build artifacts (`dist/`, `build/`, `target/`) — segregate them and gitignore.
- Any project that generates derived data (`data/raw/` vs `data/processed/`) — `raw/` is checked in (or DVC-tracked); `processed/` is regenerable.
- Any project with logs, caches, or scratch space — name them clearly (`logs/`, `.cache/`, `tmp/`) and gitignore as a class.
- Any project where humans hand-edit some files but tools generate others — keep them in different directories so a `git diff` doesn't drown in tool noise.

The earlier the separation is established, the cheaper. Adding it after a year of mixed content costs more than enforcing it on day one.

## When NOT to use

A few cases don't benefit:

- **Genuinely homogeneous trees** — a `papers/` directory of read-only PDFs has no volatile content; no separation needed.
- **Monorepo top level** — applying this rule at the *top* of a monorepo can lead to orphaned `dist/` dirs scattered everywhere; usually better to keep volatile dirs *inside* each package.
- **Single-file projects** — a one-file script with no build step doesn't need a `.cache/` ceremony.
- **Trees the tooling owns** — `node_modules/`, `vendor/`, `target/` are volatile by ecosystem rule; you don't need a separate convention, only a `.gitignore` line.

For homogeneous and tool-owned trees, the rule reduces to "make sure they're gitignored if they're regenerable", which most ecosystems do for you.

## Tree diagram

```
project/
├── src/                ← stable (rarely renamed)
├── config/             ← semi-stable
├── data/
│   ├── raw/            ← stable inputs
│   └── processed/      ← regenerable, gitignored
├── logs/               ← volatile, gitignored
└── .cache/             ← ephemeral, gitignored
```

## Naming rules

1. Stable dirs use bare nouns describing intent: `src/`, `config/`, `docs/`, `data/raw/`.
2. Volatile dirs are either dotfile-prefixed (`.cache/`, `.tmp/`) or unambiguously named (`logs/`, `dist/`, `build/`, `target/`, `data/processed/`).
3. Never mix the two under a single name. `output/` containing both committed reports and regenerable artifacts is a smell — split into `reports/` (stable) and `output/` (volatile).
4. The `data/` split is canonical: `data/raw/` (committed or DVC-tracked, never edited) and `data/processed/` (regenerable, gitignored). Add `data/interim/` if your pipeline has a meaningful midpoint.
5. Cache dirs go under a single project-local `.cache/` or under `~/.cache/<project>/` (XDG), not scattered.
6. Logs go to `logs/` (file logs) or stdout/stderr (12-factor); not interleaved with source.

## Worked example

`data/` holds an immutable vendor dump next to last night's regenerated features, and nobody dares clean it.

1. Classify each entry by change rate and recoverability: irreplaceable input, hand-written config, regenerable output, ephemeral cache.
2. Split `data/` into `data/raw/` (never modified, backed up) and `data/processed/` (gitignored, disposable).
3. Move logs to `logs/` and caches to `.cache/`; ignore both.
4. Make the pipeline write only to `processed/`. Add a test that the raw directory hashes identically before and after a run.
5. Back up `raw/` and `config/`; skip the rest. Cleaning becomes `rm -rf data/processed logs .cache`.

The blast radius of a mistake is now the size of the volatile directories.

## Anti-patterns

- **`output/` for both kinds** — mixes regenerable artifacts with hand-curated reports. Two `output/`s would be redundant; the fix is renaming: `reports/` (stable) and `output/` (volatile).
- **`data/` flat** — every CSV in one directory regardless of whether it was committed input or regenerated output. Reviewers can't tell which files matter.
- **`tmp/` checked in** — the dotfiles are usually right; if `tmp/` is in git, either rename to `samples/` (it's stable now) or gitignore it.
- **`.gitkeep` in volatile dirs** — keeps the directory in git but suggests its contents matter. Either the dir is volatile (gitignore the contents, no `.gitkeep`) or stable (don't need `.gitkeep`).
- **Logs in `src/logs/`** — logs are runtime output; they don't share a lifecycle with source. Move them to `logs/` and gitignore.
- **Cache co-located with source** — `src/.cache/` makes greps hit cached files. Hoist the cache to repo root.

## Scaling & failure modes

- **Boundaries blur** when a stable input is derived from another stable input. Keep the derivation script beside the output and record its inputs.
- **Backup policy** should follow the split: nightly for volatile working data if it's expensive to regenerate, versioned for stable data.
- **Read-only raw data** is easiest to enforce with file permissions or an object store with versioning.
- **Volatile directories grow unbounded**; add a retention rule (delete after N days) or a size alert.

## Variants

- **Binary** (stable vs volatile) — simplest split. Two top-level groups; everything is one or the other.
- **Tertiary** (stable / semi-stable / volatile) — adds `config/` as semi-stable: human-edited but rarely. Useful when configs are versioned but reviewed differently from code.
- **XDG-flavored** (config / data / cache / state) — four-way split as defined by XDG Base Directory. Strongest variant for OS-installed apps; less common for project repos.
- **Cookiecutter Data Science** — `data/raw/`, `data/interim/`, `data/processed/`, `data/external/` — pipeline-shaped variant for ML/DS projects.
- **Build-artifact split** (Maven/Gradle, Cargo, npm) — ecosystem-mandated `target/`, `dist/`, `build/`. The ecosystem chose for you; lean into it rather than re-inventing.

## Adoption checklist

- [ ] Raw inputs live apart from anything a script writes.
- [ ] Volatile directories are gitignored and safe to delete.
- [ ] The backup job lists exactly the stable directories.
- [ ] A check confirms scripts never modify raw inputs.

## Real-world projects using this

- **XDG Base Directory Specification** — codifies the four-way split (`$XDG_CONFIG_HOME`, `$XDG_DATA_HOME`, `$XDG_CACHE_HOME`, `$XDG_STATE_HOME`). Used by virtually every modern Linux app.
- **Cookiecutter Data Science** template (`drivendata/cookiecutter-data-science`) — `data/raw/` vs `data/processed/` is the canonical ML/DS application.
- **Apache Maven** — `src/` (stable) vs `target/` (volatile) is non-negotiable in Maven projects.
- **Cargo (Rust)** — `src/` stable, `target/` volatile and `.gitignore`d by `cargo new`.
- **Hugo / Jekyll / Eleventy** — `content/` and `layouts/` (stable) vs `public/` and `_site/` (volatile generated output).
- **dbt** — `models/` (stable SQL source) vs `target/` (volatile compiled SQL and run artifacts).

## Migration & references

When migrating a mixed `output/` directory:

```bash
# 1. Inventory: which files are committed and which are gitignored?
git ls-files output/   # tracked (probably the stable ones)
git status --ignored output/   # ignored (the volatile ones)

# 2. Move the stable subset to a clearly-named dir
mkdir reports
git mv output/quarterly-summary.pdf reports/
git mv output/q1-readout.md reports/
git commit -m "split: extract stable reports from output/"

# 3. Tighten .gitignore so output/ is fully volatile
echo "output/" >> .gitignore
git rm -r --cached output/
git commit -m "chore: gitignore volatile output/"
```

For the data-science variant:

```bash
# Add data/raw/.gitkeep so the input dir is committed even when empty
mkdir -p data/raw data/processed
touch data/raw/.gitkeep
echo "data/processed/" >> .gitignore
```

Further reading:

- XDG Base Directory Specification (https://specifications.freedesktop.org/basedir-spec/) — the authoritative four-way split.
- Cookiecutter Data Science (https://drivendata.github.io/cookiecutter-data-science/) — `data/raw/` vs `data/processed/` rationale.
- *The Twelve-Factor App* (12factor.net), §VI ("Processes") and §XI ("Logs") — informs why logs don't go in `src/`.
- `principles/gitignore-and-keep-files/` — the per-line policy companion to this dir-level rule.
- `principles/one-purpose-per-directory/` — sibling rule; stable and volatile are *different purposes* by definition.
