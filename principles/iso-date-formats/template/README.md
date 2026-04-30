# ISO date formats template

A two-folder example demonstrating ISO 8601 date naming for daily notes and for
timestamped binary content.

## What's here

- `journal-example/` — `YYYY-MM-DD.md` daily notes. Try `ls journal-example/` and notice the chronological order is also the lexicographic order. That's the whole point.
- `screenshot-example/` — a zero-byte file named `2026-04-30T14-22-08.png` showing the date-time form. The `T` is a literal separator and the time uses hyphens (not colons) because most filesystems disallow `:` in filenames.

## To adopt this template

1. Copy the relevant directory into your repo: `cp -r template/journal-example/ <your-target>/journal/`.
2. Replace the example dates with today's date in the same format: `2026-04-30.md`. On most shells:
   ```bash
   touch "$(date +%F).md"      # GNU/BSD date
   ```
3. For screenshots and other timestamped binaries, use `YYYY-MM-DDTHH-MM-SS.<ext>`. On Linux:
   ```bash
   touch "$(date +%FT%H-%M-%S).png"
   ```
4. If your tool natively names files (camera firmware, screenshot util), keep its output and let this rule apply only to *your* manual files.
5. Delete `screenshot-example/2026-04-30T14-22-08.png` (it's only a placeholder) before you ship your template downstream.

## What to remove

- The two example notes in `journal-example/` once you have at least one real note.
- The placeholder PNG in `screenshot-example/` once you have at least one real screenshot.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this `template/README.md` to exist. Don't delete it before replacing.
