# Scanned documents

## TL;DR

OCR'd PDFs of physical paper land under a `scans/YYYY/YYYY-MM/` date-archive shape with filenames in the form `YYYY-MM-DD - source - description.pdf`. The triple `<date> - <source> - <description>` answers the three questions you'll have years later — *when was it, who sent it, what was it about?* — without opening a single file. The leading ISO date keeps everything sorted chronologically; the source-then-description order means scrolling a directory groups all your utility-co bills together visually even before searching. Pair this layout with an OCR engine (paperless-ngx, Apple Notes scanner, ScanTailor + tesseract) so the PDFs themselves are full-text searchable; the directory is the index, OCR is the search.

## Principles & why

A scanned-document archive serves three retrieval modes that all rely on the same path encoding:

1. **By date** — "show me everything from April 2026" — solved by the `YYYY/YYYY-MM/` directory structure plus the date-leading filename.
2. **By source** — "find every bill from the utility co" — solved by the second segment of the filename being the source slug. A directory listing sorted lexicographically clusters bills from the same source even within a busy month.
3. **By topic** — "find that lab result" — solved by the third segment, the description, plus full-text OCR fallback when the description was too terse.

The order matters. Date first because `ls` and every file manager sort lexicographically and we want chronology to win. Source second because clustering by sender is the second-most-common query and putting it second keeps the cluster visible in any directory listing. Description last because it's the longest field and the most variable; pushing it to the end keeps the alignment of the date and source columns readable.

Why store under `scans/` instead of mixing with born-digital documents: the OCR-and-rename workflow is different. Born-digital PDFs already have a filename, often have embedded text, and rarely benefit from OCR. Scans need ingestion, OCR, and renaming as a single pipeline. Keeping them separate lets you point your scanner-watcher tool (paperless-ngx, Hazel, a custom inotify script) at one directory without it churning over your existing documents.

## When to use

- Anyone digitising household paper — receipts, contracts, medical records, vehicle paperwork, tax documents.
- paperless-ngx or paperless-ng users — the date-prefix and source-tag conventions map directly to paperless's tag and correspondent fields.
- Apple Notes "Scan Documents" workflow — export to PDF, then drop into this layout via a Hazel rule or Shortcut.
- Anyone who legally must keep records for a period (tax: ~7 years; medical: lifetime; warranty: until expiry) — the chronological layout makes "everything from FY 2018" trivially exportable.
- Multi-person households where partners need to find each other's documents — the path is human-readable enough that "search for `landlord`" works without a tagging system.

## When NOT to use

- Born-digital documents — PDFs you downloaded from a portal already have provenance and titles; they live in `~/Documents/` with topic-driven organisation, not date-flat archives.
- Sensitive originals you must keep on paper for legal reasons — wills, original deeds, signed contracts. Scan as a backup but do not rely on the digital copy as the primary record.
- Receipt-only collections for expense tracking — those go to a tool like Expensify or Wave with its own database; the directory archive is overkill if every receipt feeds an expense report.
- Photos of objects (parts diagrams, whiteboard captures) — those are not documents and don't need OCR; use `files/photos-by-date-and-event/` extended with topical event names.
- Rapidly-evolving project documents — those need a working tree under `files/project-archive/`, not an immutable date archive.

## Tree diagram

```
scans/
└── 2026/
    ├── 2026-04/
    │   ├── 2026-04-12 - utility-co - electric-bill.pdf
    │   ├── 2026-04-15 - landlord - lease-renewal.pdf
    │   └── 2026-04-22 - hospital - lab-results.pdf
    └── 2026-05/
```

## Naming rules

1. Top-level is `scans/` (not `Documents/` — keep it separate from born-digital).
2. Year directory: `YYYY/` (four-digit). Mirrors `files/date-archive/` and `principles/iso-date-formats/`.
3. Month directory: `YYYY-MM/` inside the year. The redundant year prefix prevents ambiguity if a month directory ever moves out of the year hierarchy.
4. Filename form: `YYYY-MM-DD - source - description.pdf`. The separator is space-dash-space — three characters, easy to eyeball.
5. The date is the *document date* (when the bill was issued, when the appointment occurred), not the scan date. If the document has no date, use the scan date and append a `~` marker: `2026-04-22~ - source - description.pdf`.
6. Source slug is kebab-case lowercase ASCII, short (under 20 chars). Pick one form per source and stick with it: `utility-co`, not `utility_co` and `utility co` interchangeably.
7. Description is whatever you'd type into a search box years later — concrete nouns over vibes. `electric-bill` beats `april-bill`; `lab-results-cbc` beats `medical-thing`.
8. Multi-page documents stay in one PDF. Splitting a five-page lease into five PDFs loses the document boundary.
9. Append page count or revision in parens only when needed: `2026-04-12 - utility-co - electric-bill (revised).pdf`.

## Worked example

A stack of paper letters and bills needs to become searchable.

1. Scan at 300 dpi, black and white or grayscale, to PDF, using the scanner or a phone app.
2. Run OCR so text is selectable: `ocrmypdf --deskew --rotate-pages --optimize 1 in.pdf out.pdf`.
3. Rename to `YYYY-MM-DD - source - description.pdf`, using the document's own date: `2026-04-12 - utility-co - electric-bill.pdf`.
4. File under `scans/2026/2026-04/`.
5. Test the payoff: `pdftotext file.pdf - | grep -i "account number"` or search with your desktop indexer.
6. Shred or keep the paper according to the legal category (tax and property documents often must be kept).

Anything can be found by date, sender, or text within seconds.

## Anti-patterns

- **No date in the filename** — `electric-bill.pdf` becomes ambiguous after the third one; you can't tell which year without opening it.
- **Date at the end** — `electric-bill 2026-04-12.pdf` defeats lexicographic sort; bills shuffle randomly in the directory.
- **US-format date** (`04-12-2026`) — sorts incorrectly; April sorts before everything else regardless of year. Always ISO 8601.
- **Inconsistent source slugs** — `utility-co`, `utilityco`, `Utility Co`, `utility_co` for the same sender; breaks lexicographic clustering.
- **Description-only filenames** — `electric-bill-from-the-utility-co-april.pdf` works once but hides the date from sort, and you'll spell it differently next month.
- **Mixed-up document and scan dates** — using "today's date" for everything makes the chronology useless when you scan a stack of old papers in one session.
- **Skipping OCR** — image-only PDFs cannot be searched. Always run OCR on ingestion (`ocrmypdf`, `tesseract`, paperless-ngx's pipeline).
- **Filing originals before they're stable** — scanning a draft contract that gets revised three times leaves three near-identical PDFs in the archive. Wait for "final" before filing.

## Scaling & failure modes

- **Language packs** for OCR (`ocrmypdf -l eng+deu`) matter for non-English documents; bad OCR makes files unsearchable.
- **Storage**: high-resolution color scans get large; grayscale 300 dpi is enough for text.
- **Multi-page and mixed batches**: split batches by document; use a scanner's blank-page split or a tool like `pdfsandwich`/`pdfseparate`.
- **Privacy**: scans include IDs and account numbers; encrypt backups and restrict sync.

## Variants

- **date-source-description** (this guide) — the recommended form; balances retrievability and brevity.
- **date-source-only** — `2026-04-12 - utility-co.pdf`. Faster to file but loses the topic question; only viable when one source sends one document type.
- **date-tag-tag-description** — `2026-04-12 - bills - utility-co - electric.pdf`. Adds a category prefix; useful for very large archives but introduces redundancy with the source field.
- **paperless-managed flat directory** — a single directory of arbitrarily-named files; paperless-ngx maintains the index. Loses filesystem-level browsability.
- **Year-flat without month directories** — `2026/2026-04-12 - source - desc.pdf`. Works for low-volume archives (under ~50 docs/year); month subdirectories help past that.
- **Per-source top-level** — `scans/utility-co/2026-04-12 - electric-bill.pdf`. Inverts the hierarchy; better when most queries are by source and chronology matters less.
- **encrypted archive** — `scans-encrypted.tar.gz.gpg` with the same internal layout; for sensitive medical or legal documents at rest.

## Adoption checklist

- [ ] Every scan is OCR'd and searchable by text.
- [ ] Filenames use the document date, source, and description.
- [ ] The paper-retention rule per document type is written down.
- [ ] Backups are encrypted and tested.
- [ ] OCR language matches the documents.

## Real-world projects using this

- **paperless-ngx** — the leading open-source document management system; uses date + correspondent + tags as its core taxonomy. https://github.com/paperless-ngx/paperless-ngx
- **paperless-ng** — paperless-ngx's predecessor; same conventions.
- **DEVONthink** (macOS, commercial) — Smart Rules and AI classification produce a similar layout; the database stores documents but the export is date-led.
- **Hazel** (macOS) — rule-based file mover; the canonical Hazel use case is "watch `~/Inbox/Scans` and rename incoming PDFs into `~/Documents/Scans/YYYY/YYYY-MM/`".
- **Apple Notes scanner** — built-in iOS scan-to-PDF feature; pair with Shortcuts to drop into this layout.
- **ScanTailor + ocrmypdf** — open-source pipeline for cleaning and OCR'ing scanned pages.
- **Dokuments / Mayan EDMS / Teedy** — alternative open-source DMS tools that index a similar tree.
- **Johnny.Decimal** — adjacent organisational system; some users combine its `AC.ID` codes with this date-prefixed scheme.

## Migration & references

To impose this layout on an existing flat scan directory, drive the rename from PDF metadata or document content:

```bash
# Rename PDFs by their internal CreationDate to the YYYY-MM-DD prefix
for f in inbox/*.pdf; do
  date=$(pdfinfo "$f" | awk -F': +' '/^CreationDate/ {print $2}' | \
         python3 -c 'import sys,datetime;print(datetime.datetime.strptime(sys.stdin.read().strip(),"%a %b %d %H:%M:%S %Y").strftime("%Y-%m-%d"))')
  echo mv "$f" "scans/${date:0:4}/${date:0:7}/${date} - unknown - $(basename "$f")"
done
```

For OCR + filing in one step:

```bash
# ocrmypdf adds a text layer in place
ocrmypdf input.pdf output.pdf
# Then file with paperless-ngx's consume directory or a Hazel rule
mv output.pdf "scans/2026/2026-04/2026-04-22 - hospital - lab-results.pdf"
```

For paperless-ngx ingestion, drop files into the `consume/` directory and configure correspondents and document types in the web UI; paperless will rename per its template.

Further reading:

- paperless-ngx documentation — https://docs.paperless-ngx.com/
- ocrmypdf — https://ocrmypdf.readthedocs.io/
- Hazel rules examples — Noodlesoft's official documentation and community recipes.
- Apple Notes "Scan Documents" support page.
- `files/date-archive/` — the date-rooted directory layout this guide nests inside.
- `principles/iso-date-formats/` — the YYYY-MM-DD convention and rationale.
- `principles/naming-by-purpose-not-type/` — why the source slug is part of the name, not a sibling tag file.
