# Ebook library (Calibre)

## TL;DR

Calibre's canonical layout is `Author Name/Title (Series N)/Title - Author.epub` plus a sibling `cover.jpg` and `metadata.opf`. The structure is auto-managed when Calibre owns the directory — you do not move or rename files yourself; Calibre rewrites the path whenever metadata changes. The shape is worth understanding anyway, because portability across e-reader sync (KOReader, Calibre-Web, COPS) and disaster recovery without Calibre's database (`metadata.db`) both depend on knowing what's where. The triple of `.epub` + `cover.jpg` + `metadata.opf` is the unit that makes a book recoverable from a bare filesystem.

## Principles & why

Calibre solves an awkward retrieval problem: books have multiple identities (author, series, title, ISBN), readers want to browse by any of them, and the on-disk layout has to pick one to dominate. Calibre picks author-first because:

1. **Authors are the most stable identity.** Series get re-numbered (the *Earthsea Cycle* has been published as 4, 5, and 6 books); titles get translated, retitled, and abridged; ISBNs are per-edition. The author name is the closest thing to a primary key for fiction.
2. **The series number lives in the directory name, not the filename.** `A Wizard of Earthsea (Earthsea 1)/` means a directory listing of an author shows the right reading order at a glance — `(Earthsea 1)`, `(Earthsea 2)`, `(Earthsea 3)`. Sorting by directory name gives you the chronological series read.
3. **Every book directory is self-describing.** The `.epub` carries the content, `cover.jpg` carries the artwork, `metadata.opf` carries the OPF-format metadata that Calibre wrote. Together, those three files let you reconstruct a Calibre library from scratch even if `metadata.db` is gone — which matters when you migrate, restore from backup, or sync to an e-reader that doesn't speak Calibre's protocol.

The layout is therefore not just a presentation choice; it's a recovery format. Treat it as such: never delete the `.opf` thinking it's vestigial, and never reorganise the directories by hand.

## When to use

- Calibre-managed libraries on desktop, server, or NAS — Calibre maintains this layout automatically.
- Calibre-Web installations — the open-source web frontend reads this exact layout to serve books over HTTP/OPDS.
- COPS (Calibre OPDS Server) — lightweight PHP server that reads `metadata.db` plus the directory tree.
- KOReader on Kindle/Kobo with Calibre wireless sync — it understands the `metadata.opf` files for metadata override.
- Multi-device households where the same library serves Kindle, Kobo, iPad, and phone reading apps — the format is the most-supported common denominator.
- Long-term archival — the layout survives decades of Calibre upgrades and remains recoverable without the application.

## When NOT to use

- Throwaway PDFs of one-off articles or downloaded references — those belong in `files/scanned-documents/` or a flat `~/Documents/` tree; investing Calibre overhead is wasteful.
- Academic paper collections — papers have first-class metadata (DOI, BibTeX) that Zotero, Paperpile, or a literature-review structure handles better than Calibre.
- Comic books and manga — Calibre has comic support but most users prefer Komga or Kavita with their own `Series/Volume/` layout (see comic-archive variants).
- Audiobooks — Calibre tolerates them but Audiobookshelf or similar uses `Author/Series/Book` with `.m4b` files; better suited to spoken content.
- Massive shared libraries (10k+ books) where multiple users edit metadata concurrently — Calibre's SQLite database doesn't handle multi-writer well; use a server-mode tool (calibre-server, Calibre-Web).

## Tree diagram

```
Calibre Library/
├── Ursula K Le Guin/
│   └── A Wizard of Earthsea (Earthsea 1)/
│       ├── A Wizard of Earthsea - Ursula K Le Guin.epub
│       ├── cover.jpg
│       └── metadata.opf
└── Ted Chiang/
    └── Stories of Your Life and Others/
        └── Stories of Your Life and Others - Ted Chiang.epub
```

## Naming rules

1. The library root is the directory you point Calibre at on first launch — typically `~/Calibre Library/` or `/mnt/books/Calibre Library/`. Treat this as Calibre's domain; manual edits inside risk corrupting `metadata.db`.
2. First level is the author directory: `<Author Name>/`. Calibre uses the full sortable name as displayed — `Ursula K Le Guin` not `Le Guin, Ursula K` (Calibre keeps both forms in the database; the directory uses the display form).
3. Multiple authors: Calibre files the book under the *first* listed author. Co-authored works have a single canonical directory; the secondary authors live only in metadata.
4. Book directory: `<Title>/` for standalones; `<Title> (<Series> <N>)/` for series entries. The series number goes inside parens, with the series name first.
5. Inside the book directory the convention is `<Title> - <Author>.<ext>` for the ebook file. The dash-separated form is Calibre's default and is what its own importer expects when re-scanning.
6. Sibling files: `cover.jpg` for artwork, `metadata.opf` for OPF metadata. Calibre rewrites both whenever you change tags. Never edit `metadata.opf` by hand while Calibre is running — it overwrites your edits.
7. Filename character substitution: Calibre replaces filesystem-illegal characters (`?`, `:`, `<`, `>`, `|`, `"`, `*`) with `_`. Do not "fix" these by hand; Calibre regenerates the path on every save.

## Anti-patterns

- **Hand-editing the directory structure** — Calibre's `metadata.db` indexes books by an internal ID and a relative path. Renaming directories from the shell decouples the database from the filesystem; books vanish from the GUI.
- **Deleting `metadata.opf`** — looks vestigial but is the disaster-recovery payload. Without it, rebuilding a Calibre library from a bare filesystem loses tags, ratings, and series info.
- **Deleting `cover.jpg` while keeping the embedded cover** — Calibre-Web and COPS read `cover.jpg` from disk first, embedded only as fallback. The web UI goes blank when you delete it.
- **Using Calibre's library directory as a sync target for cloud services** — Dropbox, iCloud, OneDrive may rename or normalise files mid-write, corrupting `metadata.db`. Sync the result of `calibredb export` or use Calibre's own sync, not the raw library directory.
- **Storing non-Calibre files in the library root** — `notes.md`, `to-read.txt` get scanned and appear as books on next library refresh.
- **Running two Calibre instances against the same library** — `metadata.db` is SQLite; concurrent writers corrupt it. Use Calibre Content Server for multi-user access.
- **Renaming author directories to match the surname-first form** (`Le Guin, Ursula K/`) — diverges from Calibre's display form; the `metadata.db` no longer matches and the GUI relocates everything on next launch.

## Variants

- **Calibre-default** — the layout described above; what you get if you let Calibre manage the library, which is the recommended mode.
- **By-genre-then-author** — `Fiction/<Author>/<Book>/...`. Calibre supports this via "save to disk" templates but it duplicates books in multiple genres and breaks Calibre's automated path management. Use only for export, not for the live library.
- **By-language-then-author** — `English/<Author>/...`, `Russian/<Author>/...`. Useful for multi-lingual readers but again, only as an export target.
- **Series-rooted** — `<Series>/<Author>/<Book>/...` for collectors who think in series first. Calibre's "save to disk" template can emit this; the live library cannot use it because standalones have no series.
- **ISBN-flat** — `9780441478125.epub` in a single directory; used by some library imports and by automation pipelines. Loses all browsability; recover with metadata fetch on import.
- **Plain-EPUB grids** (without `cover.jpg` or `.opf`) — produced by direct downloads. Run Calibre's "Add books" to upgrade them into the canonical layout.

## Real-world projects using this

- **Calibre** — desktop e-book manager; defines this layout. https://calibre-ebook.com/
- **Calibre-Web** — open-source web reader/server that reads a Calibre library directly. https://github.com/janeczku/calibre-web
- **COPS** (Calibre OPDS PHP Server) — lightweight read-only OPDS/HTTP server. https://github.com/seblucas/cops
- **calibre-server** — built-in Calibre Content Server; serves OPDS, web UI, and a remote database protocol.
- **KOReader** — Kindle/Kobo reader app that supports Calibre wireless sync; reads `metadata.opf` for richer metadata than the EPUB embeds.
- **Calibre Companion / Marvin** (iOS) — third-party readers that talk to Calibre Content Server.
- **Plato** — minimalist Kobo launcher with Calibre library sync support.
- **calibredb** — Calibre's CLI; the `add`, `export`, `set_metadata` subcommands all maintain the canonical layout.

## Migration & references

To migrate a flat collection into Calibre:

```bash
# Add a directory of EPUBs in bulk; Calibre will fetch metadata + cover
calibredb add --recurse --library-path ~/Calibre\ Library/ ~/inbox/books/

# Force-fetch metadata and covers for everything missing them
calibredb fetch_news --library-path ~/Calibre\ Library/
```

To export a sub-set into a portable directory tree (for non-Calibre tools):

```bash
calibredb export --library-path ~/Calibre\ Library/ \
  --to-dir /mnt/usb/books \
  --template "{author_sort}/{title}/{title}"
```

To rebuild `metadata.db` from a directory tree of `.opf` files (after disaster recovery):

```bash
# In Calibre GUI: Library Maintenance → Restore database
# Or from CLI:
calibredb restore_database --library-path ~/Calibre\ Library/
```

Further reading:

- Calibre user manual — https://manual.calibre-ebook.com/
- Calibre-Web project README — https://github.com/janeczku/calibre-web
- COPS documentation — https://blog.slucas.fr/en/oss/calibre-opds-php-server
- KOReader Calibre integration — https://github.com/koreader/koreader/wiki/Calibre-companion
- `files/scanned-documents/` — for one-off PDFs that don't belong in Calibre.
- `principles/iso-date-formats/` — useful when adding publication dates to imported metadata.
- `principles/one-purpose-per-directory/` — Calibre's per-book directory holds exactly the recovery triple.
