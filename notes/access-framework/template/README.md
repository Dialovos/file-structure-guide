# ACCESS framework template

A starter ACCESS vault — six numbered top-level folders plus an `INDEX.md` MOC at the root. Action / Categories / Concepts / Entries / Search / Sources, in that order.

## What's here

- `INDEX.md` — top-level MOC explaining the six-bucket scheme and entry points.
- `1-action/` — placeholder for active projects (one folder or file per project).
- `2-categories/` — placeholder for durable area-of-life MOCs.
- `3-concepts/` — placeholder for evergreen atomic notes (your claims).
- `4-entries/` — placeholder for daily/weekly/journal notes.
- `5-search/` — placeholder for saved indexes and Dataview pages.
- `6-sources/` — placeholder for literature notes (others' ideas).
- `README.md` — this file.

## To adopt this template

1. Copy `template/` into your vault root:
   ```bash
   cp -r template/ ~/access-vault/
   cd ~/access-vault
   ```
2. Open in Obsidian (or any markdown editor with backlinks).
3. Start by adding one item per folder so the framework is concretely populated:
   - `1-action/q2-redesign.md` — a project you're actively working on.
   - `2-categories/health.md` — a long-running area.
   - `3-concepts/attention-residue.md` — a claim you've started refining.
   - `4-entries/2026-04-30.md` — today's daily note.
   - `5-search/all-concepts.md` — a saved index (Dataview if available).
   - `6-sources/newport-2016-deep-work.md` — a literature note.
4. Update `INDEX.md` to link to your real entry points.

## Conventions

- **Numeric prefixes are required.** `1-action/`, not `action/`. Tools sort alphabetically; numbers force semantic order.
- **Concepts vs sources is a hard split.** Your idea → `3-concepts/`; someone else's text → `6-sources/`.
- **Action is transient.** Move completed projects to an archive sub-folder periodically.
- **Six folders is the cap.** Sub-folders inside any of the six are fine; a seventh top-level is drift.

## What to rename or remove

- The `INDEX.md` is a working starter — edit it once your vault has real content.
- Remove this `README.md` once the template is in use; the verifier needs it only while it lives in this repo.
- The `.gitkeep` files exist to preserve empty folders in git; delete them once you have real content in each folder.

## Verifier

`docs/superpowers/scripts/verify-guideline.sh notes/access-framework` checks that this README, `GUIDE.md`, `tree.md`, and the `template/` directory all exist with the required sections.
