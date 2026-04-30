# Photos by date and event

## TL;DR

Two complementary buckets, both under a year directory. Daily-life shots (couch dog, weekday lunches, accidental shutter taps) flow into a monthly bucket: `YYYY/YYYY-MM/`. Events worth retrieving by name (a hike, a wedding, a vacation week) get their own dated directory: `YYYY/YYYY-MM-DD-event-name/`. EXIF stays the source of truth for in-shot metadata; filenames and directory names carry the *human* metadata — what you'll type in a search box years later. Naming applies to directories, not individual files: cameras and phones name files unpredictably (`IMG_4321.HEIC`, `DSC09134.ARW`), and renaming directories is enough.

## Principles & why

A photo library has two retrieval modes, and they don't share a layout:

1. **By time** — "what did I shoot last April?" — handled by date-prefixed monthly buckets that sort chronologically.
2. **By memory** — "where are the wedding photos?" — handled by event-named directories that show up in fuzzy search.

Forcing every shot into the same scheme breaks one mode. A month-only layout (`2026-04/`) buries event photos in the same bucket as your dog and your dinner. An event-only layout has nowhere to put the daily-life shots that don't form an event. The hybrid is the only layout that handles both modes naturally.

Keeping EXIF as the source of truth for capture date matters because filesystems lie. `mtime` changes when you copy or rsync; `ctime` resets on filesystem moves; even `birthtime` (where supported) is unreliable across cloud sync. EXIF, embedded in the file, survives. Rename directories using EXIF, not filesystem dates.

## When to use

- Any personal photo library where you take both daily-life shots and event-driven photos.
- Family photo archives that are passed down — descendants need to find "the 2003 trip to Italy" without learning your tagging system.
- Phone exports — Apple Photos and Google Photos both default to date-grouped exports that map cleanly onto this layout.
- Lightroom import workflows — set the import folder template to `%Y/%Y-%m-%d` and rename the directory after the import to add the event slug.
- Shared family-cloud storage — directory names are the universal index across iOS, Android, Windows, and macOS browsers.

## When NOT to use

- Topical galleries — an artist's portfolio organises by subject (`portraits/`, `landscapes/`, `still-life/`) rather than date, because no one searches a portfolio by year.
- Stock-photography style libraries — keyword-driven retrieval; metadata in EXIF/IPTC and a DAM index do all the work.
- Professional event-photography deliverables — typically `YYYY-MM-DD-client-event/` with no daily-life bucket; pure event mode.
- Tiny libraries (under ~200 photos) — flat by date is fine; the year/month structure adds friction without buying retrieval.
- Sensor data and timelapses — these are dataset-shaped, not memory-shaped; use a flat ISO timestamp scheme without the event slug.

## Tree diagram

```
photos/
├── 2026/
│   ├── 2026-04/                    ← daily-life shots
│   ├── 2026-04-15-spring-walk/
│   └── 2026-04-22-anniversary/
└── 2025/
    └── 2025-12-25-christmas/
```

## Naming rules

1. Top-level is always the four-digit year: `2026/`. Mirrors `files/date-archive/` and `principles/iso-date-formats/`.
2. Daily-life buckets use the year-month form: `YYYY/YYYY-MM/`. One bucket per month.
3. Event directories nest at the same level as monthly buckets: `YYYY/YYYY-MM-DD-event-name/`. The event slug is kebab-case, lowercase, ASCII.
4. Multi-day events use the *start* date: `2026-07-04-vacation-rome/` covering July 4–11. If continuity matters, append a duration hint: `2026-07-04-vacation-rome-week/`.
5. Don't rename camera filenames. Cameras emit unpredictable names (`IMG_4321.HEIC`, `DSC09134.ARW`); renaming risks duplicates and breaks raw-file pairing.
6. The event slug is the title you'd type into search five years later — concrete nouns, not vibes. `2026-04-22-mom-birthday/` beats `2026-04-22-special-day/`.

## Anti-patterns

- **Flat dump under a single year** — `2026/IMG_4321.HEIC, IMG_4322.HEIC, ...` defeats both retrieval modes; you can't find events, can't find dates without opening files.
- **Event without date** — `spring-walk/` floats in time; you can't tell which year. Always prefix with the date.
- **Tag-driven directories** — `family/`, `friends/`, `pets/` overlap (a family member is also a friend; a pet is in a holiday photo). Use EXIF tags or a DAM, not directories.
- **Renaming individual files to match the directory** — `2026-04-22-anniversary-001.jpg`, `…-002.jpg`. Time-consuming, breaks raw-file pairing, no retrieval benefit over EXIF + directory.
- **Mixing month-only and event directories under one parent** without the year prefix — `04/`, `04-22-anniversary/` doesn't sort correctly when years pile up.
- **Letting cloud sync flatten the structure** — many sync services lose subdirectories under "Camera Roll." Confirm your sync preserves directory shape before relying on it.

## Variants

- **Date only** (`YYYY/YYYY-MM-DD/`) — pure date layout; loses event-name retrieval but is what most photo apps emit by default.
- **Date and event** (this guide) — hybrid; retrieval by time *and* by name.
- **Date, event, and camera** (`2026-04-22-anniversary-canon-r6/`) — adds the camera body for multi-camera shoots; useful for photographers reviewing per-body output.
- **Year quarter** (`2026/Q2/2026-04-22-anniversary/`) — extra grouping level; rarely worth it for personal libraries.
- **Trip-rooted** (`trips/2026-07-04-rome/` outside the main `photos/` tree) — separates major-event photos from everyday flow; some photographers find this clearer.
- **Year of capture vs. year of edit** — keep originals under capture-year directories; export edits to a parallel `edits/<year>/` tree to avoid re-processing churn.

## Real-world projects using this

- **Apple Photos export** — exporting a Library produces `YYYY/YYYY-MM-DD/` directories by default.
- **Adobe Lightroom Classic** — import preset `%Y/%Y-%m-%d/` ships built-in; widely customised to add event slugs.
- **Google Photos Takeout** — produces year-grouped, date-prefixed folders for downloaded archives.
- **digiKam** — open-source DAM; ships with an "albums by date" mode that yields this exact layout.
- **Shotwell** (GNOME photo manager) — default library layout is `Pictures/YYYY/MM/DD/`.
- **darktable** — defaults to year-grouped imports; users routinely append event slugs.

## Migration & references

To impose this layout on an existing flat library, drive the rename from EXIF (not filesystem dates):

```bash
# Requires exiftool. For each photo, derive YYYY/YYYY-MM/ from EXIF DateTimeOriginal.
exiftool '-Directory<DateTimeOriginal' \
         -d 'photos/%Y/%Y-%m' \
         -r path/to/flat/library
```

For event directories, after the bulk move, rename specific month-bucket subsets:

```bash
mv photos/2026/2026-04 photos/2026/2026-04-15-spring-walk   # if every shot in that month is the event
# Or move only matching files:
mkdir -p photos/2026/2026-04-15-spring-walk
exiftool '-Directory=photos/2026/2026-04-15-spring-walk' \
         -if '$DateTimeOriginal =~ /^2026:04:15/' \
         photos/2026/2026-04
```

Further reading:

- `principles/iso-date-formats/` — the date-prefix convention this layout depends on.
- `files/date-archive/` — the same year/month skeleton applied to non-photo content.
- ExifTool documentation (Phil Harvey) — the canonical tool for EXIF-driven renames.
- digiKam Handbook chapter on collection organisation.
- Apple Photos and Google Photos Takeout documentation — both define their export layouts publicly.
