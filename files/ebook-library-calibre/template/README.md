# Calibre ebook library template

A skeleton showing the recovery triple — `<book>.epub`, `cover.jpg`, `metadata.opf` — under the canonical `<Author>/<Title>/` directory shape that Calibre auto-generates and that Calibre-Web, COPS, and KOReader all read directly.

## What's here

- `Author Name/Book Title/Book Title - Author Name.epub` — a zero-byte placeholder for the ebook content. The filename convention is `<Title> - <Author>.<ext>` and is what Calibre's own scanner expects when re-importing.
- `Author Name/Book Title/cover.jpg` — a zero-byte placeholder for cover art. Calibre-Web and COPS prefer this on-disk cover over the embedded one.
- `Author Name/Book Title/metadata.opf` — a zero-byte placeholder for OPF-format metadata. This is the disaster-recovery payload; without it, rebuilding a library from a bare filesystem loses tags, ratings, and series info.

The placeholders are intentionally empty — they exist to demonstrate the path shape, not to open in a reader.

## To adopt this template

1. **Easier path: let Calibre own the layout.** Install Calibre, point it at an empty directory, and use `Add books` from the GUI or `calibredb add --recurse --library-path <dir> <inbox>` from the CLI. Calibre will produce this exact layout automatically.
2. **Manual path: only useful if you're feeding Calibre-Web/COPS without Calibre itself.** Copy this template, rename `Author Name/`, `Book Title/`, and the three placeholder files, then drop a real `.epub`, `cover.jpg`, and a hand-written `metadata.opf` into place. Calibre-Web reads them directly.
3. For series entries, name the book directory `<Title> (<Series> <N>)/` so directory listings sort in reading order.

## What to rename or remove

- Always rename `Author Name/` and `Book Title/` to real values immediately on import — placeholder names corrupt the database when you later run a real Calibre import on top.
- Replace all three zero-byte files with real content; do not leave the empty `metadata.opf`, as Calibre will treat it as a malformed metadata file on import.
- Drop this `README.md` once the template is adapted (the verifier requires it while it lives in the repo).

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.

## Manual edits and Calibre

If Calibre is managing this directory, do not edit the structure from the shell — Calibre's `metadata.db` indexes books by relative path and a hand-rename will decouple the database from the filesystem. Use the Calibre GUI or `calibredb` instead. Manual edits are only safe when Calibre is not running and you accept that you'll need to use Library Maintenance → Restore database afterwards.
