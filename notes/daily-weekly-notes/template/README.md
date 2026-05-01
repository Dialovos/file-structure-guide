# Daily/weekly notes template

A starter daily/weekly setup: one example daily note, one example weekly review, an Obsidian/Logseq-style template for new days, and a placeholder topical-notes folder.

## What's here

- `daily/2026-04-30.md` — example daily note showing the canonical sections.
- `weekly/2026-W18.md` — example weekly review covering the daily above.
- `templates/daily.md` — the template applied to each new daily file (placeholders are Obsidian-style `{{date:YYYY-MM-DD}}`).
- `notes/` — placeholder for the topical layer the dailies link out to.
- `README.md` — this file.

## To adopt this template

1. Copy `template/` into your vault root:
   ```bash
   cp -r template/ ~/journal/
   cd ~/journal
   ```
2. In Obsidian: Settings → Daily Notes plugin → Date format `YYYY-MM-DD`, Folder `daily/`, Template `templates/daily.md`. Set a hotkey for "Open today's daily note" — typically Ctrl/Cmd+Shift+T.
3. In Logseq: Settings → Edit config — set `:journal/file-name-format "yyyy-MM-dd"`. Daily journal is the home page by default.
4. Replace the example daily and weekly files with your real first day. Delete or repurpose them.
5. Establish a weekly review cadence (Friday afternoon or Sunday evening); create a new `weekly/YYYY-Www.md` from a template if you want consistency.

## Conventions

- **Filenames are ISO 8601.** `YYYY-MM-DD.md` for dailies, `YYYY-Www.md` for weeklies (capital W).
- **One file per day.** No morning/evening splits.
- **The daily is the canonical entry point** for capture. Things flow outward to atomic notes from there.
- **The weekly closes the loop.** Highlights, lowlights, next-week plan.

## What to rename or remove

- The example daily and weekly are illustrative — replace them with real content (or delete and start fresh).
- The `templates/daily.md` placeholders use Obsidian's `{{date:...}}` syntax — adjust if your tool uses different placeholders (Logseq: `<%date%>`; org-mode: `%U`; etc.).
- Remove this `README.md` once the template is in use; the verifier needs it only while it lives in this repo.
- The `notes/.gitkeep` exists to preserve the empty folder in git; delete it once you have real content.

## Verifier

`docs/superpowers/scripts/verify-guideline.sh notes/daily-weekly-notes` checks that this README, `GUIDE.md`, `tree.md`, and the `template/` directory all exist with the required sections.
