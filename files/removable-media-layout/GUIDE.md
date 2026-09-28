# Removable media layout

## TL;DR

Every USB stick, SD card, and external drive gets a *physical label* (a Brother label printer, a Sharpie, a piece of masking tape — anything durable). On import, the entire contents land in `~/imports/<label>-<YYYY-MM-DD>/` so the directory name preserves both the source identity and the import date forever. Post-processing keepers move into `archive/<label>-<date>/` or migrate further into purpose-driven trees (photos, scans, notes). The whole flow keeps **provenance** — *which device this came from, when* — even after the original media is wiped, lost, or reformatted. Without provenance, two SD cards' worth of similarly-named `IMG_0001.JPG` files become indistinguishable; with it, every file is traceable to its origin.

## Principles & why

Removable media is unusual among storage layers because the device itself is *transient* — it gets wiped and reused — but the *content* may be archival. The layout has to bridge that gap. Three principles drive the design:

1. **Provenance is the invisible field that solves duplicate-name collisions.** A camera SD card and a phone export both produce `IMG_0001.JPG`, `IMG_0002.JPG`, ad nauseam. Without recording where each file came from, you can't tell them apart, you can't deduplicate intelligently, and you can't fix corrupt camera metadata by referring back to the original card. The `<label>-<date>/` directory name *is* the provenance: it tells you the physical source and the import session in one path component.

2. **Imports are atomic and immutable.** When you import a card, you copy the entire card contents — including DCIM, MISC, METADATA, anything the camera wrote — into one new directory. You don't merge into an existing import. You don't rename files during import. The import directory is a *snapshot* of the device at that moment. Post-processing happens in copies, downstream; the original import is read-only by convention.

3. **Triage and curation happen *after* import, not during.** Trying to decide what's worth keeping while files are still on the card mixes two cognitive tasks (transfer + curation) and risks losing things accidentally (you delete from the card thinking it's already imported when it isn't). Always: full import first, then curate the imported copy, then optionally wipe the card.

The label discipline is what turns an undifferentiated pile of "camera-sd, that-other-camera-sd, the-grey-one" into a stable identity scheme. Print labels and put them on the cards. The labels match the slugs you use in directory names, so a card you pull out of a drawer in three years can still be linked to its imports. Without physical labels, this scheme breaks down within a year.

## When to use

- Photographers (DSLR, mirrorless, drone) who shoot to SD/CF/CFexpress and import to a computer for processing.
- Podcasters and audio engineers who record to SD cards in field recorders (Zoom, Tascam, Sound Devices).
- Anyone using SD cards or USB sticks as transfer media between physically-isolated systems (kiosks, conference computers, TV media players).
- Researchers and journalists doing field collection where chain-of-custody matters — the directory name is your evidence log.
- Anyone with multiple cameras, multiple cards per camera, or a card-rotation workflow where mixing up imports would cause confusion.
- Pair with `files/photos-by-date-and-event/` (the long-term home of photo keepers post-import) and a backup verification routine.

## When NOT to use

- Casual users with one device that auto-imports to Apple Photos / Google Photos / Lightroom — those tools have their own ingestion workflow and their own provenance metadata, mostly invisible but functional.
- Imports that go directly into a finished archive structure with no post-processing (e.g., moving raw mp3s straight to a music library) — overhead exceeds value.
- Single-card, single-shoot workflows where there's no risk of confusing sources — just import to a date-archive directly.
- Mobile-first photo workflows where the phone *is* the camera and there's no removable medium.
- Cloud-synced cameras (Eyefi cards, wifi-direct DSLRs) that bypass the manual-import flow.
- Heavy users of professional digital asset management (Lightroom Catalog, Capture One Catalog) where the catalog database holds provenance metadata robustly.

## Tree diagram

```
~/imports/
├── camera-sd-2026-04-29/
│   ├── DCIM/
│   └── METADATA/
├── usb-talk-handout-2026-03-15/
│   └── slides.pdf
└── archive/
    └── camera-sd-2025-12-10/      ← post-processing keepers
```

## Naming rules

1. Top-level is `~/imports/`. One root for all device imports across all card/stick types.
2. Each import session is one directory: `<label>-<YYYY-MM-DD>/`. The label is a *kebab-case identifier* you've also affixed physically to the card; the date is the *import date* (when the data hit your computer), not the date the data was created.
3. Label slugs follow a small vocabulary you maintain: `camera-sd`, `camera-sd-bw` (a second card you label "BW"), `usb-presentations`, `usb-talk-handout`, `cf-drone`. Pick names short enough to type and distinct enough to identify physically.
4. Multiple imports of the same card on the same day are deduplicated with a session marker: `camera-sd-2026-04-29-am/` and `camera-sd-2026-04-29-pm/`. Don't overwrite — you lose the prior import.
5. Inside the import directory, *do not rename files*. Preserve the camera/device's original filenames (`IMG_0001.JPG`, `MOV_0001.MP4`, etc.) plus the original directory structure (`DCIM/100CANON/`, `MISC/`, `METADATA/`). The import is the device's view of itself at import time.
6. Once curation is done and keepers have migrated to `archive/<label>-<date>/` (or onward to `~/photos/2026/2026-04 wedding-shoot/`), the original `~/imports/<label>-<date>/` may be deleted *only after* a backup verification step. Until then, treat it as the source of truth.
7. Archive subdirectories under `~/imports/archive/` use the same `<label>-<YYYY-MM-DD>/` naming. The archive holds *post-processing keepers* — culled, lightly-organised, but still preserving the original-import provenance.
8. A `~/imports/INDEX.md` file maintained by hand listing each label, the physical card it refers to, and the date(s) of imports is highly recommended for long-running setups (>10 cards in rotation).

## Worked example

An SD card from a camera is about to be formatted.

1. Label the physical card (`camera-sd`) and note it in a list of media if you own several.
2. Copy everything, don't move: `rsync -a --info=progress2 /media/$USER/CARD/ ~/imports/camera-sd-2026-04-29/`.
3. Verify the copy: `diff -rq /media/$USER/CARD ~/imports/camera-sd-2026-04-29` prints nothing.
4. Process from the imports folder: move keepers into the photo library (see `photos-by-date-and-event`); leave the rest.
5. After a second backup exists, format the card. Once processed, move the import folder into `~/imports/archive/` or delete it.
6. Keep a one-line `PROVENANCE.txt` in each import if the source is worth remembering.

The origin and date of every file remain traceable until you decide to discard them.

## Anti-patterns

- **No physical label** — within a year, you'll forget which card was the BW card and which was the colour card. Print labels. Use a paint pen if your cards are too small for printed labels.
- **Renaming files during import** — once you've renamed `IMG_0001.JPG` to `wedding-001.jpg`, you've lost the link back to the camera's metadata. Keep originals untouched in `imports/`; rename in copies during post-processing.
- **Importing into a flat date archive** (`~/photos/2026-04-29/`) — collapses provenance; if you import two different cards on the same day, you can't separate them.
- **Importing on top of an existing directory** — `cp -r card/* ~/imports/camera-sd-2026-04-29/` when that directory already exists from yesterday's import overwrites or merges silently. Always create a new dated directory.
- **Wiping the card before backup verification** — the import directory is one copy; the card is another. Never wipe the card until you've verified the import landed correctly *and* a backup ran successfully.
- **Skipping the label** — using `random-card-2026-04-29/` because you're in a hurry. The cost shows up later; build the habit.
- **Filing keepers but keeping the import directory forever** — `~/imports/` should not grow without bound. After post-processing and verified backup, delete the import; the archive plus the curated tree is the long-term record.
- **Date-only import directories** (`2026-04-29/`) — convenient but loses provenance the moment you have two cards from the same day.
- **Trusting card-internal date metadata** — many cameras have wrong clocks. The *import* date is the only date you can trust; preserve it in the directory name.

## Scaling & failure modes

- **Bit rot and failing media**: cards and cheap USB sticks fail without warning; copy first, verify, and don't treat them as storage.
- **Unlabeled media**: identify by a label; assign one at first import.
- **Large imports** eat local disk; process and prune promptly.
- **Unknown sources** (found drives, other people's media) can carry malware; scan before opening files.

## Variants

- **label-date** (this guide) — the recommended form; preserves both physical-source identity and import time.
- **label-only** — `~/imports/camera-sd/` flat, with files inside; loses session boundaries and you can't tell which import session a file belongs to without checking timestamps.
- **date-only** — `~/imports/2026-04-29/`; loses provenance entirely. Don't use when more than one card might be imported per day.
- **label-date-purpose** — `~/imports/camera-sd-2026-04-29-bali-trip/`; adds a purpose suffix during import. Useful when you're confident of the purpose at import time, but most users defer purpose-naming to the archive step.
- **session-numbered** — `~/imports/camera-sd-001/`, `camera-sd-002/`; numbered sequentially, with the date hidden in the directory metadata. Compact but requires looking up which session is which date.
- **per-device subtree** — `~/imports/camera-sd/2026-04-29/` instead of flat. Useful for very high-volume photographers; nests the date under the device.
- **mounted-as-source** — never import; just mount the device and read directly. Only viable for devices that stay connected (external drives, not removable cards).
- **DAM-managed** — Lightroom or Capture One catalogs handle import and provenance internally; the filesystem layout still benefits from this guide's date+label scheme as the catalog's underlying file path.

## Adoption checklist

- [ ] Every device has a physical label and matching import folder names.
- [ ] Copies are verified (`diff -rq` or checksums) before media is wiped.
- [ ] Two copies exist before formatting.
- [ ] Imports are processed and cleared on a schedule.
- [ ] Unknown media is scanned first.

## Real-world projects using this

- **Adobe Lightroom Classic import workflow** — Lightroom's "Copy" or "Move" import dialog defaults to a date-based directory structure but supports a "{date}-{cardlabel}" template that aligns with this guide. https://helpx.adobe.com/lightroom-classic/help/import-photos-catalog.html
- **Capture One** (Phase One) — has a customisable session-and-import structure that often uses card label as a token. https://www.captureone.com/
- **darktable** (open-source RAW processor) — its import dialog supports a `${YEAR}-${MONTH}-${DAY}_${IMPORT_NAME}` token that produces label-date import directories. https://www.darktable.org/
- **digiKam** (open-source photo manager) — explicit support for "device albums" with date+label naming on import. https://www.digikam.org/
- **rsync** with a cron-driven import script — the most common DIY approach; simple `rsync -a /Volumes/CARD/ ~/imports/$(label)-$(date)/` invocations.
- **Photo-import workflow guides for podcasters** — the Sound Devices and Zoom recorder communities have well-documented session-folder workflows that map onto this scheme.
- **Audio engineering DAW project structures** — Pro Tools, Logic Pro, Reaper sessions traditionally include a `Recordings/<date>-<source>/` subdirectory; this guide's form generalises that practice to the OS level.
- **Chain-of-custody patterns from forensics** — adapted for personal use, the principle that "who/what/when must be encoded at the moment of receipt" is exactly this guide.

## Migration & references

A typical import session script:

```bash
#!/usr/bin/env bash
# import-card.sh - import a removable-media device to ~/imports/<label>-<date>/
# Usage: import-card.sh <label> <mount-point>
set -euo pipefail

LABEL="${1:?usage: $0 <label> <mount-point>}"
SOURCE="${2:?usage: $0 <label> <mount-point>}"
DATE=$(date +%Y-%m-%d)
DEST="$HOME/imports/${LABEL}-${DATE}"

if [[ -d "$DEST" ]]; then
  # Same-day reimport — append am/pm marker:
  HOUR=$(date +%H)
  if (( HOUR < 12 )); then SUFFIX="am"; else SUFFIX="pm"; fi
  DEST="${DEST}-${SUFFIX}"
fi

mkdir -p "$DEST"
rsync -a --info=progress2 "$SOURCE/" "$DEST/"

# Optional: capture device metadata for the audit trail
mount | grep "$SOURCE" > "$DEST/.import-mount-info.txt" || true
date -u +%FT%TZ > "$DEST/.import-completed-at.txt"

echo "Imported to: $DEST"
echo "Verify before wiping the card."
```

To migrate an existing flat-date import history into label-date form (best-effort; you'll need to manually identify which import was which card):

```bash
# Create label-date directories matching what you can reconstruct:
mkdir -p ~/imports/camera-sd-2026-04-29
mv ~/imports/2026-04-29/* ~/imports/camera-sd-2026-04-29/
rmdir ~/imports/2026-04-29
```

For the archive promotion step:

```bash
# After post-processing, move keepers into the archive while preserving provenance:
mkdir -p ~/imports/archive/camera-sd-2025-12-10
rsync -a ~/imports/camera-sd-2025-12-10/keepers/ ~/imports/archive/camera-sd-2025-12-10/
# Verify backup, then delete the original import once safe:
rm -rf ~/imports/camera-sd-2025-12-10
```

For the `~/imports/INDEX.md` audit file (highly recommended):

```markdown
# Removable media index

| Label             | Physical card             | First import | Last import |
|-------------------|---------------------------|--------------|-------------|
| camera-sd         | SanDisk Extreme 64GB #1   | 2024-03-12   | 2026-04-29  |
| camera-sd-bw      | SanDisk Extreme 64GB #2   | 2025-06-01   | 2026-03-22  |
| usb-presentations | Kingston DataTraveler 32GB| 2024-09-15   | 2026-01-08  |
```

Further reading:

- Lightroom Classic import documentation — https://helpx.adobe.com/lightroom-classic/help/import-photos-catalog.html
- digiKam handbook on importing from cameras — https://docs.digikam.org/
- darktable documentation on import — https://docs.darktable.org/
- `files/photos-by-date-and-event/` — the long-term home for curated photo keepers after import.
- `files/date-archive/` — the foundational date-based layout this guide's `archive/` subtree extends.
- `principles/iso-date-formats/` — the ISO date convention used throughout.
- `principles/stable-vs-volatile-separation/` — the import directory is volatile by design; the archive is stable.
