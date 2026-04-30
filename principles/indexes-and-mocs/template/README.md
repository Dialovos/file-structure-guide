# Indexes-and-MOCs template

A minimal directory illustrating the index/MOC pattern: an `INDEX.md` that
*curates* the directory's contents, and a handful of placeholder note files
the index points at. Use it as the seed for a notes vault, a docs section,
or any directory that's outgrown the "alphabetical `ls` is enough" stage.

## What's here

- `INDEX.md` — the curated index. Two sections, four entries. Edit it as the directory grows.
- `note-1.md`, `note-2.md`, `note-3.md` — placeholder notes referenced by `INDEX.md`. Empty on purpose; replace with real content.
- `reading-list.md` — placeholder for the "Reference" section's perennial entry. Empty.

## To adopt this template

1. Copy this directory into your repo: `cp -r template/ <your-repo>/notes/`.
2. Replace the placeholder notes with your real ones — keep the names or rename freely; just update `INDEX.md` to match.
3. Edit `INDEX.md`'s prose to describe *your* directory's purpose and organising sections.
4. As you add files, add an entry to the index. As you remove, remove. The index is hand-edited by design.
5. If you'd rather call the file `MOC.md` (notes-vault convention) than `INDEX.md`, rename it. The verifier doesn't enforce either name; pick one and stay consistent across your repo.

## What to rename, fill, delete

- **Rename**: `note-1.md` → real note titles. `INDEX.md` → `MOC.md` if you prefer that convention.
- **Fill**: each note's body. Update the one-line description in `INDEX.md` for each.
- **Delete**: `reading-list.md` if you don't have a reference section. Adjust `INDEX.md` accordingly.

## When the directory outgrows one index

Once you're past ~15 entries or three sections feel cramped, split. Move
related notes into subdirectories (`notes/meetings/`, `notes/journals/`,
`notes/projects/`) and give each its own `INDEX.md`. The root `INDEX.md`
then points at the sub-indexes — a tree of opinionated entry points rather
than one giant flat list.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this `README.md` to exist. Don't delete it before replacing.
