# Stable-vs-volatile-separation template

Two stub directories side by side: one stable, one volatile. The point is the
split, not the contents.

## What's here

- `stable-src/` — placeholder for source code, hand-written configs, raw inputs. Tracked in git, backed up, reviewed.
- `volatile-cache/` — placeholder for caches, build artifacts, processed data, logs. Tracked in this template only via `.gitkeep` so the dir survives `cp -r`; in a real project you'd gitignore the contents.

## To adopt this template

1. Copy the two stubs as your starting skeleton: `cp -r template/stable-src/ src/` and `cp -r template/volatile-cache/ .cache/`.
2. Replace `stable-src/` with the real source layout your project needs (`src/`, `config/`, `data/raw/`, etc.).
3. Replace `volatile-cache/` with the real volatile dirs (`.cache/`, `logs/`, `dist/`, `data/processed/`).
4. Add the volatile dirs to `.gitignore`. Example:

   ```
   .cache/
   logs/
   dist/
   data/processed/
   ```

5. Delete the `.gitkeep` files in the volatile dirs once real (untracked) content lives there.

## On `.gitkeep` in volatile dirs

This template includes `volatile-cache/.gitkeep` *only* so the directory is
committed as a placeholder for the template. In a real project you would not
do this — the entire `.cache/` (or equivalent) directory should be gitignored,
including the directory itself. The volatile contents create themselves at
runtime; you don't need the directory pre-existing.

If your tooling does require an empty volatile dir to exist before it runs,
prefer creating it from a `Makefile` or build script (`mkdir -p .cache`) over
pinning it via `.gitkeep`.

## Acceptance test

After adopting, ask: *"If I `rm -rf` every volatile directory, does my project still build from a clean clone?"* If yes, the split is working. If no, something stable was hiding in a volatile dir; pull it out.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this `template/README.md` to exist. Don't delete it before replacing.
