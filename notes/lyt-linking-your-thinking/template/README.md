# LYT (Linking Your Thinking) template

A starter LYT vault: a top-level `+ Home.md` MOC plus the four canonical folders (`+ Spaces/`, `Calendar/`, `Notes/`, `Resources/`). The `+` prefix sorts MOCs to the top of any folder listing.

## What's here

- `+ Home.md` — top-level MOC, the entry point to the vault.
- `+ Spaces/` — placeholder for space MOCs (e.g. `+ Career.md`, `+ Hobbies.md`).
- `Calendar/` — placeholder for daily (`YYYY-MM-DD.md`) and weekly (`YYYY-Www.md`) notes.
- `Notes/` — placeholder for flat atomic notes.
- `Resources/` — placeholder for external/reference material (books, articles, PDFs).
- `README.md` — this file.

## To adopt this template

1. Copy `template/` into your vault root:
   ```bash
   cp -r template/ ~/lyt-vault/
   cd ~/lyt-vault
   ```
2. Open the folder as a vault in Obsidian (recommended) or any wikilink-capable tool.
3. Create your first space MOC: `+ Spaces/+ Career.md`. Mirror the structure of `+ Home.md`.
4. Start a daily note today: `Calendar/2026-04-30.md` (use today's actual date).
5. As thoughts in the daily note earn their own life, extract them into atomic notes in `Notes/` and link them from the relevant space MOC.

## Conventions

- **MOC filenames:** `+ Title Case.md`. The leading `+ ` is required.
- **Atomic notes:** `lowercase-hyphenated.md`. No subfolders inside `Notes/`.
- **Calendar:** `YYYY-MM-DD.md` for daily, `YYYY-Www.md` for weekly (ISO 8601).
- **Resources:** can have one level of subfolders (`Resources/books/`) — keep it shallow.

## What to rename or remove

- The `+ Home.md` example links (`[[+ Career]]`, `[[+ Hobbies]]`) — replace with your actual spaces.
- Remove this `README.md` once the template is in use; the verifier needs it only while it lives in this repo.
- The `.gitkeep` files in `+ Spaces/`, `Calendar/`, `Notes/`, `Resources/` exist to preserve empty directories in git; delete them once you have real content.

## Verifier

`docs/superpowers/scripts/verify-guideline.sh notes/lyt-linking-your-thinking` checks that this README, `GUIDE.md`, `tree.md`, and the `template/` directory all exist with the required sections.
