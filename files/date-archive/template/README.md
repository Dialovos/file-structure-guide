# Date archive template

An empty-tree skeleton for a `YYYY/YYYY-MM/` archive. Three sample buckets are provided so you can drop content in immediately and see the pattern; replace them with your own years and months as the archive grows.

## What's here

- `2026/2026-04/` — the current year's current month (placeholder; bump as time passes).
- `2026/2026-05/` — next month, pre-created so it's there when you need it.
- `2025/2025-12/` — last year's most-recent month, useful for testing roll-over.

Each directory has a `.gitkeep` so the empty shape survives `git add`.

## To adopt this template

1. Copy the `template/` tree into the root of your archive: `cp -r template/ ~/archive/` or `cp -r template/ /mnt/external/archive/`.
2. Drop dated files into the matching month: a file dated 2026-04-30 goes into `2026/2026-04/2026-04-30-<slug>.<ext>`.
3. When a new month begins, create the next directory in advance: `mkdir -p 2026/2026-06`. (You can script this in cron if you like a guaranteed-empty next-month bucket.)
4. Pair this with `principles/iso-date-formats/` so every filename inside the archive starts with `YYYY-MM-DD`.

## What to rename or remove

- Replace `2025/`, `2026/` with the actual years you have content in. Delete years you don't yet need.
- Delete `.gitkeep` files once a directory has at least one real file.
- Add new years (`2027/`) by creating the parent and a single month subdirectory; let new month directories accrue as you file new content.
- Remove this `README.md` once the template has been adapted; the verifier requires it while it sits in this repo.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until you no longer need the template.
