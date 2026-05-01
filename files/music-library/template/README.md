# Music library template

A skeleton showing the canonical Beets-compatible layout: artist directory, year-prefixed album directory, two-digit track-number filename, and album-art sibling.

## What's here

- `Artist/Year - Album/01 Track.flac` — a zero-byte placeholder demonstrating the per-track layout. Replace `Artist`, `Year - Album`, and `01 Track.flac` with real names.
- `Artist/Year - Album/cover.jpg` — a zero-byte placeholder for album art. Drop a real JPEG (or PNG) here; most players also accept `folder.jpg`.

The placeholders are intentionally empty — they exist to demonstrate the path shape, not to play. Replace them with real files as you import.

## To adopt this template

1. Copy the structure into your library root: `cp -r template/ ~/Music/` or `cp -r template/ /mnt/music/`.
2. Rename `Artist/` to a real album-artist name and `Year - Album/` to `<year> - <title>` (e.g. `1997 - OK Computer`).
3. Replace `01 Track.flac` with real track files using the `NN Title.ext` form. Keep the two-digit zero-padded track number.
4. Drop a real cover image at `cover.jpg` or `folder.jpg`.
5. If you use Beets, point `directory:` and `paths:` at this layout (see `GUIDE.md` for the snippet).

## What to rename or remove

- Rename `Artist/` and `Year - Album/` immediately on import — leaving placeholder names confuses every music player.
- Delete `01 Track.flac` and `cover.jpg` once real files are in place; the zero-byte stubs will refuse to play and confuse album-art scrapers.
- Drop this `README.md` once the template is adapted (the verifier requires it while it lives in the repo).

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.

## Spaces in paths

Directory and file names contain spaces because they mirror human-readable metadata. Quote paths in shell scripts (`"Artist/Year - Album/01 Track.flac"`) or rely on tab-completion; do not substitute hyphens or underscores for spaces.
