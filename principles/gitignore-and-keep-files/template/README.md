# `.gitignore` + keep-files template

A starter `.gitignore` covering the patterns most projects need, plus an
example `empty-dir/` showing how `.gitkeep` preserves an otherwise-empty
directory in git.

## What's here

- `.gitignore` — annotated starter covering dependencies, build output, secrets, OS files, editor state, and logs. Each section is commented so a reader knows *why* a pattern exists.
- `empty-dir/.gitkeep` — empty placeholder so the directory survives `git add`. Replace with real content (and delete the `.gitkeep`) once the dir has files.
- This `README.md`.

## To adopt this template

1. Copy `.gitignore` into your repo root: `cp template/.gitignore <your-repo>/.gitignore`. Review every section; **delete patterns that don't apply** to your stack — a long ignore file you don't understand is worse than a short one you wrote.
2. Add language-specific ignores you don't see here. GitHub's official template repo (https://github.com/github/gitignore) has per-language starters; copy the relevant one and merge it in.
3. Anywhere your layout requires a directory to exist before files arrive (`data/raw/`, `logs/`, `migrations/`), drop a `.gitkeep` (or `.keep`, or a one-line `README.md`) inside.
4. Pick one keep-file convention — `.gitkeep`, `.keep`, or `README.md` — and stay consistent. Don't mix.

## What to rename, fill, delete

- **Rename**: nothing. `.gitignore` and `.gitkeep` are exact filenames; git matches them literally.
- **Fill**: add your stack's specific patterns to `.gitignore` (Python? Add `*.pyc`, `__pycache__/`. Rust? Add `Cargo.lock` if you're a library).
- **Delete**: any commented section that doesn't apply (no Python? remove `__pycache__/`; no Java? remove `*.class`). Less is more.
- **Delete**: `empty-dir/` if you don't need a placeholder example. The `.gitkeep` inside is illustrative, not load-bearing.

## A note on `.gitkeep` vs `.keep` vs `README.md`

`.gitkeep` is **not** a real git convention — git just tracks any non-empty
directory. Three sensible choices, in roughly increasing order of value:

1. `.gitkeep` — community default; zero bytes; signals "this dir intentionally exists".
2. `.keep` — Rails-flavored; same mechanic, shorter name.
3. `README.md` — does the same job *and* documents the directory. Pick this when you have anything to say.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this `README.md` to exist. Don't delete it before replacing.
