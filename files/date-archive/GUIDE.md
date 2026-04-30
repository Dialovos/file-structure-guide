# Date archive

## TL;DR

For any append-only stream of dated content — receipts, scanned letters, journal entries, exported chats, downloaded statements — use a two-level skeleton: `archive/YYYY/YYYY-MM/<YYYY-MM-DD>-<slug>.<ext>`. The year directory keeps top-level density manageable; the year-month directory keeps each year browsable; ISO date prefixes keep filenames sorted chronologically inside each month.

## Principles & why

A flat archive of "everything I ever filed" is unmanageable past a few hundred items: directories slow down, file pickers stutter, fuzzy search matches across years. A purely calendar-based hierarchy (`YYYY/MM/DD/`) is the opposite extreme — three levels deep before any filename appears, and most days have zero entries.

The two-level `YYYY/YYYY-MM/` skeleton is the empirically-derived sweet spot. It keeps each directory's child count bounded (≤12 for a year, typically 5–60 files for a month), keeps lexicographic sort identical to chronological sort at every level, and lets you grep across an entire year (`rg -g '2025/**' …`) without descending into noise.

Repeating the year inside the month directory (`2026/2026-04/` rather than `2026/04/`) buys two things: the directory name is unambiguous when you see it out of context (a screenshot, a search result, a `cd` history entry), and a flat global listing of all month-directories sorts correctly without their parents.

## When to use

- Receipts, invoices, and statements you keep for taxes — these accumulate forever and you query them by date.
- Personal journals and daily notes — pairs naturally with `principles/iso-date-formats/`.
- Scanned letters, paper mail, and physical-document captures — keep the dated filename even though the document itself is undated.
- Exported chat histories, social-media data dumps, or platform-takeout archives — the export already groups by date.
- Long-running pipelines that output dated artifacts (backups, reports, dumps) — `backup/2026/2026-04/2026-04-30-*.tar.zst`.
- Any append-only stream where the past doesn't move and the future is unbounded.

## When NOT to use

- Topic-driven content where you don't reach for things by date — manuals, reference docs, recipes. Use a topic taxonomy instead.
- Content with frequent retroactive updates — if last year's records get edited routinely, the `YYYY/` boundary is just a chore. Use a flat or topic layout.
- Tiny archives (under ~50 items total) — the hierarchy adds clicks without buying retrieval. Stay flat until volume justifies splitting.
- Photo libraries with mixed events and daily shots — use `files/photos-by-date-and-event/` instead, which adds an event slug to the day-level directory.
- Pipelines that already produce structured per-record dirs (e.g. `s3://bucket/year=2026/month=04/day=30/`) — don't double-encode the date.

## Tree diagram

```
archive/
├── 2025/
│   ├── 2025-11/
│   │   └── 2025-11-12-tax-return.pdf
│   └── 2025-12/
└── 2026/
    ├── 2026-01/
    ├── 2026-04/
    │   ├── 2026-04-15-rent-receipt.pdf
    │   └── 2026-04-29-doctor-visit.pdf
    └── 2026-04-XX-still-deciding/    ← acceptable placeholder
```

## Naming rules

1. Top-level directory is the four-digit year: `2026/`. Two-digit years are forbidden (avoid the YY/MM/DD ambiguity entirely).
2. Second level repeats the year and adds the month with a hyphen: `2026/2026-04/`. The month is two digits, never one.
3. Filenames inside a month start with the full ISO date `YYYY-MM-DD`, then a kebab-case slug describing the contents, then the extension: `2026-04-29-doctor-visit.pdf`.
4. If the exact date is unknown, use `YYYY-MM-XX-<slug>` and let it sort to the end of the month. Resolve it later.
5. Empty directories that exist only to receive future content carry a `.gitkeep` file (when archived in git) or simply remain empty (when on a local disk).
6. Do not create `YYYY-MM-DD/` directories unless a single day produces multiple files that warrant grouping (e.g. one event with several scans).

## Anti-patterns

- **`YYYY/MM/`** without year-prefixing the month — sorts correctly under its parent but a directory listing of all months across years jumbles them.
- **`MM-YYYY/`** — places month before year, breaking lexicographic sort entirely.
- **Mixing `YYYY-MM/` and `YYYY/MM/` in one tree** — two equivalent layouts shouldn't coexist; pick one.
- **Filing by topic at top level then by date below** — `archive/taxes/2026/` works for taxes but creates many parallel hierarchies. Better: file flat by date, tag by topic.
- **Adding a `current/` symlink that drifts** — tools that follow symlinks pick up stale content; rotate by date instead.
- **Storing months as words** — `2026/April/` doesn't sort and forces locale handling. ISO numerics only.

## Variants

- **`YYYY/YYYY-MM/`** (this guide) — most readable; canonical for personal archives.
- **`YYYY/MM/`** — less self-describing dirs but identical sort under their parent. Good for tools that always render the parent.
- **`YYYY/YYYY-Q[1-4]/`** — quarterly buckets instead of monthly; suits accounting and reporting.
- **`YYYY/MM-month-name/`** (`04-april/`) — adds redundant month name for human readability; trades some sortability for skim-ability.
- **`YYYY/YYYY-WW/`** — ISO week numbering; useful for content driven by weekly cadence (sprints, status reports).
- **Single flat year** — for low-volume archives, skip the month layer until the year holds more than ~50 items.

## Real-world projects using this

- **Apple Photos export** — defaults to `YYYY/YYYY-MM-DD/` for exported sessions.
- **Google Takeout** — chat, location, and Photos exports use ISO-style date prefixes; Photos additionally splits by year.
- **Adobe Lightroom** — default folder template `%Y/%Y-%m-%d/` is one click away in import settings.
- **Tiago Forte's PARA system** — `4-archive/` is conventionally split by year for personal projects.
- **`borg`/`restic`/`kopia` snapshot listings** — surface dates as ISO strings, encouraging matching directory layouts on the consumer side.
- **Many newsroom and journalism archives** — published-by-year top-level (`2025/`, `2026/`) is the de facto standard for editorial CMSs.

## Migration & references

To migrate a flat archive into `YYYY/YYYY-MM/`:

```bash
# Move every file with an ISO date prefix into its YYYY/YYYY-MM/ bucket
for f in archive/*.pdf; do
  base=$(basename "$f")
  yr="${base:0:4}"; ym="${base:0:7}"
  mkdir -p "archive/$yr/$ym"
  git mv "$f" "archive/$yr/$ym/$base"
done
```

If filenames lack an ISO date, derive one from filesystem mtime (`stat -c %y`) before renaming. For paper documents scanned with OCR, embed the date in the OCR pass so it lands in the filename automatically.

Further reading:

- `principles/iso-date-formats/` — the filename rule that makes this layout sortable.
- `principles/depth-vs-breadth/` — why two levels is empirically the right depth.
- `files/photos-by-date-and-event/` — the event-aware variant for photo libraries.
- `files/project-archive/` — a parallel scheme for finished projects rather than dated artifacts.
- Tiago Forte, *Building a Second Brain* — popularised the year-segmented archive in PARA.
