# Video library template

A skeleton showing the Plex/Jellyfin-compatible split between `Movies/` and `TV Shows/`, with one placeholder of each type. The structure is what the metadata scrapers expect; deviations from this shape cause silent matching failures.

## What's here

- `Movies/Example (2024)/Example (2024).mkv` — a zero-byte placeholder demonstrating the per-movie directory and filename. Both directory and file repeat the title and year.
- `TV Shows/Example Show/Season 01/Example Show - s01e01.mkv` — a zero-byte placeholder for an episode. Show root, then `Season XX/`, then the episode file with the `sXXeYY` format.

The placeholders are intentionally empty — they exist to show the path shape, not to play.

## To adopt this template

1. Copy the structure into your media root: `cp -r template/ /mnt/media/` or wherever your Plex/Jellyfin library lives.
2. Rename `Example (2024)/` to a real movie title with year in parentheses (`Inception (2010)`).
3. Rename `Example Show/` to the real series name; rename the episode file (`Show Name - s01e01.mkv`).
4. Replace the `.mkv` placeholders with real video files. Match the directory's title-and-year exactly in the filename for movies.
5. Add `Season 02/`, `Season 03/`, etc. as new TV seasons arrive.
6. Trigger a library scan in Plex/Jellyfin; the scrapers will populate metadata, posters, and chapter art.

## What to rename or remove

- Always rename `Example (2024)/` and `Example Show/` immediately on import — leaving placeholder names produces ghost entries in the library.
- Delete the zero-byte `.mkv` files once real content is in place; the empty stubs will refuse to play and pollute "Recently Added" lists.
- Drop this `README.md` once the template is adapted (the verifier requires it while it lives in the repo).

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.

## Spaces and parentheses in paths

Directory and file names contain spaces and parentheses on purpose — that is what the Plex/Jellyfin scrapers regex against to extract title and year. Quote paths in shell scripts (`"Movies/Inception (2010)/Inception (2010).mkv"`); never substitute dots or underscores for spaces, and never drop the parentheses around the year.
