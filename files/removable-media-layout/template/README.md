# Removable-media-layout template

A skeleton showing the `~/imports/` root with one example import directory and an `archive/` for post-processing keepers.

## What's here

- `camera-sd-example-2026-04-30/.gitkeep` — placeholder for an import session directory in the `<label>-<YYYY-MM-DD>/` form. The label (`camera-sd-example`) names the physical card; the date is the *import date*, not the photo date.
- `archive/.gitkeep` — placeholder for the post-processing-keepers archive. After culling and curation, surviving files migrate from `imports/<label>-<date>/` into `imports/archive/<label>-<date>/`.

The `.gitkeep` files exist only because git does not track empty directories. Delete them once real content arrives.

## To adopt this template

1. Copy the structure into your home: `cp -r template/ ~/imports/` (the contents — not nesting under `template/`).
2. Physically label each removable card/stick with the slug you'll use in directory names (`camera-sd`, `usb-talk-handout`, `cf-drone`). Use a label printer, paint pen, or durable Sharpie.
3. On each import, run a script (sample below) that creates a fresh `~/imports/<label>-<today>/` and `rsync`s the entire card contents into it.
4. Do not rename files during import. Preserve the camera/device's original filenames and directory structure.
5. After post-processing, move keepers into `~/imports/archive/<label>-<date>/` or further into purpose-driven trees (`~/photos/2026/2026-04 wedding/`, etc.).
6. Verify backup *before* wiping the original card.

## Import script

```bash
#!/usr/bin/env bash
LABEL="${1:?usage: $0 <label> <mount-point>}"
SOURCE="${2:?usage: $0 <label> <mount-point>}"
DEST="$HOME/imports/${LABEL}-$(date +%Y-%m-%d)"
mkdir -p "$DEST"
rsync -a --info=progress2 "$SOURCE/" "$DEST/"
echo "Imported to: $DEST. Verify before wiping the card."
```

Save as `~/bin/import-card.sh` and run as `import-card.sh camera-sd /Volumes/UNTITLED`.

## What to rename or remove

- Rename `camera-sd-example-2026-04-30/` to a real import directory matching one of your physical cards, or delete it once you've imported a real card.
- Delete the `.gitkeep` files once each directory has real content.
- Drop this `README.md` once the template has been adapted (the verifier requires it while it lives in the repo).

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.

## Optional: maintain `~/imports/INDEX.md`

If you have more than ~3 cards in rotation, maintain a manual index mapping each label to a physical card description:

```markdown
| Label             | Physical card             | First import | Last import |
|-------------------|---------------------------|--------------|-------------|
| camera-sd         | SanDisk Extreme 64GB #1   | 2024-03-12   | 2026-04-29  |
| camera-sd-bw      | SanDisk Extreme 64GB #2   | 2025-06-01   | 2026-03-22  |
| usb-presentations | Kingston DataTraveler 32GB| 2024-09-15   | 2026-01-08  |
```

This is the audit trail your future self will thank you for.

## Why "imports" not "card-dumps" or "ingest"

`imports/` is the term used by Lightroom, darktable, and digiKam — staying in their vocabulary makes the layout legible to anyone with photo-management experience. `ingest/` is reserved (in some workflows) for *automatic* watch-folder pipelines; this layout is for *manual* imports.
