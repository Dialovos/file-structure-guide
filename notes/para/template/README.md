# PARA template

A bare PARA vault skeleton: the four canonical buckets, a starter `INDEX.md` explaining the scheme, and `.gitkeep` placeholders so empty directories survive `git add`.

## What's here

- `1-projects/.gitkeep` — placeholder; replace with one folder per active project (e.g. `1-projects/q2-redesign/`).
- `2-areas/.gitkeep` — placeholder; replace with one folder per ongoing standard (e.g. `2-areas/health/`).
- `3-resources/.gitkeep` — placeholder; replace with topical reference folders (e.g. `3-resources/design-references/`).
- `4-archive/.gitkeep` — placeholder; sub-organise by year (`4-archive/2024/`) or by source bucket once anything retires.
- `INDEX.md` — example top-of-vault note explaining the four buckets, decision rules, and weekly review.
- `README.md` — this file. Keep it during template adoption; remove it once your real vault has taken shape.

## To adopt this template

1. Copy `template/` into your vault root (or directly into a fresh directory if you're starting from scratch):
   ```bash
   cp -r template/ ~/vault/
   cd ~/vault
   ```
2. Delete the four `.gitkeep` files; add your first real project, area, and resource folders.
3. Edit `INDEX.md` to match how you describe your own work — the example wording is starter text, not gospel.
4. Optional: initialise as a git repo (`git init`), an Obsidian vault, or a Notion workspace.

## What to rename or remove

- The four bucket names (`1-projects/`, `2-areas/`, `3-resources/`, `4-archive/`) are the load-bearing convention; keep them as-is unless adopting the [`PARA-without-numbers`](../GUIDE.md) variant.
- `INDEX.md` is optional — drop it if you'd rather rely on your tool's sidebar.
- `README.md` (this file) can be deleted as soon as the template is in use; the verifier needs it only while it lives in this repo.

## Verifier

`docs/superpowers/scripts/verify-guideline.sh notes/para` checks that this README, `GUIDE.md`, `tree.md`, and the `template/` directory all exist with the required sections.
