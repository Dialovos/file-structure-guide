# Folgezettel template

A minimal flat-directory slip box demonstrating Luhmann's branching ID scheme: two root threads (`1`, `2`), one branch (`1a`), one grandchild (`1a1`), plus an `INDEX.md` listing the roots.

## What's here

- `1 example-root.md` — first root thread.
- `1a example-branch.md` — first child of `1`.
- `1a1 example-leaf.md` — first child of `1a` (a grandchild of `1`).
- `2 second-thread.md` — an unrelated second root thread.
- `INDEX.md` — example top-of-vault map listing the root IDs and how to add new notes.
- `README.md` — this file.

The vault stays flat: every note is a sibling on disk, regardless of its position in the implicit ID tree.

## To adopt this template

1. Copy `template/` into your vault root:
   ```bash
   cp -r template/ ~/folgezettel/
   cd ~/folgezettel
   ```
2. Replace the example content with your real first thread (`1`) and a second thread (`2`) if you have one ready. The example notes are intentionally short — a few lines each, just enough to demonstrate the ID rhythm.
3. Add new notes as either children of an existing ID (`1a2`, `1b`, `1a1a`) or new root IDs (`3`, `4`).
4. Keep `INDEX.md` updated with new root threads.

## ID rules quick reference

- Root: integer (`1`, `2`, `3`, ...).
- Generation alternates letters and digits: `1` → `1a` → `1a1` → `1a1a`.
- Filename: `<ID> <slug>.md` (or `<ID>-<slug>.md`).
- No folders — all notes are siblings on disk.

## What to rename or remove

- All five example notes (`1`, `1a`, `1a1`, `2`) are placeholders to demonstrate the scheme. Replace their content; you may keep the IDs if you wish or rename to your own threads.
- `INDEX.md`'s thread list is illustrative; rewrite to match your real roots.
- Remove this `README.md` once the template is in use; the verifier needs it only while it lives in this repo.

## Verifier

`docs/superpowers/scripts/verify-guideline.sh notes/folgezettel` checks that this README, `GUIDE.md`, `tree.md`, and the `template/` directory all exist with the required sections.
