# ISO date formats

## TL;DR

Every date that appears in a filename, directory, or note title is written as `YYYY-MM-DD` (ISO 8601, extended). It's the only date format that sorts correctly as plain text, is unambiguous worldwide, and survives every locale, shell, and search index unchanged.

## Principles & why

Dates are the most common sortable thing in a filesystem and the most common source of locale-driven ambiguity. `04/05/06` means three different days in three regions. `April 5, 2026` is unsortable as a filename. `5-Apr-26` cannot be diffed.

ISO 8601's date-first big-endian form (`YYYY-MM-DD`) puts the most-significant component first, so lexicographic order — what `ls` and every file picker uses — is also chronological order. It uses only ASCII digits and a hyphen, both of which are safe everywhere. It's the same format Wikipedia uses for revision logs, Keep-a-Changelog uses for entries, and ISO 8601 has standardised since 1988.

Pick this once at the repo level and you eliminate an entire category of locale bugs and "where's that file from last April?" searches.

## When to use

- Daily notes / journals: `2026-04-30.md`
- Meeting notes: `2026-04-30-design-review.md`
- Photo and screenshot dumps: `2026-04-30T14-22-08.png`
- Backup snapshots: `backup-2026-04-30/`
- Migration files: `2026-04-30-add-users-table.sql`
- Release tags and notes: `release-2026-04-30/`
- Any directory grouping content by date: `journal/2026/2026-04/`

If a name *could* sort by date, give it a date prefix. If a name is sometimes filtered by date (logs, exports, reports), put the date first.

## When NOT to use

The format itself is essentially universal, but a few systems impose their own date schema and you should not fight them:

- **Tools that name files for you** — keep what they emit. Photo apps that already use `YYYYMMDD_HHMMSS` (no separators) are safe to leave; they sort the same way. Don't manually normalize a pipeline's output.
- **Filenames where the date is *inside* the document** — a contract dated 2026-04-30 might be filed as `acme-msa-v3.pdf` because the contract's effective date is metadata, not file identity.
- **Ecosystem date formats** — `CHANGELOG.md` entries follow Keep-a-Changelog (also `YYYY-MM-DD`, so this is rarely a real exception); RFC-2822 email dates inside `.eml` files; HTTP `Last-Modified` headers. Don't normalize the *content* of files just because the rule applies to filenames.

## Tree diagram

```
journal/
├── 2026-04-29.md
├── 2026-04-30.md
└── 2026-05-01.md

photos/
└── 2026/
    └── 2026-04/
        └── 2026-04-29-spring-walk/

bad/
├── 04-29-26.md           ← MM-DD-YY ambiguous
├── 29 April 2026.md       ← unsortable, locale-dependent
└── 2026_04_29.md          ← underscore breaks dashed convention
```

## Naming rules

1. Date is always `YYYY-MM-DD` — four-digit year, two-digit month, two-digit day, hyphen separators.
2. Date comes first in the filename when chronological sort matters; date comes after the topic when topic-grouping matters more (`design-review-2026-04-30.md` is OK if the topic is the primary index).
3. For time, append `THH-MM-SS` using a literal `T` separator and hyphens (filesystems disallow `:`). Example: `2026-04-30T14-22-08.png`.
4. For UTC, add a trailing `Z` (`2026-04-30T14-22-08Z.png`); otherwise time is local and unmarked.
5. Year-only and year-month directories are valid containers: `2026/`, `2026-04/`. Do not nest deeper than `year/year-month/year-month-day/` without a content reason.
6. Never use `_` between date components; use `-` only. Never use `.` (collides with file extensions).

## Worked example

`reports/` holds `4-29-26.pdf`, `April 30 2026.pdf`, and `01-05-2026.pdf`. Nobody can tell whether the last one is January 5 or May 1.

1. Decide the true dates from file metadata or content; never guess from the ambiguous name. `stat -c %y file` and the PDF's own date help.
2. Rename with a script that prints the plan first: `for f in *.pdf; do echo "$f -> $(date -d "$(stat -c %y "$f")" +%F)-report.pdf"; done`.
3. Apply after reviewing the output. Use `mv -n` so nothing is overwritten.
4. Sort check: `ls` now lists files chronologically with no options.
5. For timestamps in filenames use `YYYY-MM-DDTHHMM` or `YYYYMMDD-HHMMSS`, and choose one across the tree.

Result: `2026-01-05-report.pdf`, unambiguous and sortable in every tool.

## Anti-patterns

- **`04-29-26.md`** or **`4/29/26`** — locale-dependent. A US reader sees April 29, 2026; a European reader sees a malformed day-month-year. Sorts wrong in every locale.
- **`29 April 2026.md`** — unsortable as plain text and forces shell quoting. A search for "April" misses every other month.
- **`2026_04_29.md`** — uses underscores instead of hyphens; breaks the rest of the repo's hyphen convention and looks like a snake_case identifier.
- **Two-digit years** — `26-04-30.md` looks like a YY-MM-DD until 2027 invalidates it; never compress the year.
- **Date *suffixed* on a sortable list** — `meeting-notes-2026-04-30.md` doesn't sort by date. Prefix instead.
- **Mixing date formats in one tree** — one directory with `2026-04-30.md` and another with `Apr-30-2026.md` defeats the entire reason for the convention.

## Scaling & failure modes

- **Time zones.** Dates near midnight differ by zone. Pick one (usually UTC for machine logs, local for personal notes) and write it down.
- **Two-level trees** like `2026/2026-04/` repeat the year on purpose so files stay unambiguous when moved out of context.
- **Week dates** use ISO week notation (`2026-W18`), and ISO weeks can belong to the neighboring calendar year around New Year.
- **Legacy data** with 2-digit years or mixed locales needs a one-time migration with a human check of the ambiguous rows.

## Variants

- **Date-only** (`YYYY-MM-DD`) — for daily content with at most one entry per day.
- **Date + topic slug** (`YYYY-MM-DD-some-topic.md`) — adds a kebab-case description; still sorts chronologically.
- **Date + time, T-separated** (`YYYY-MM-DDTHH-MM-SS`) — for high-frequency content (screenshots, logs, sensor data).
- **Date + time + zone** (`YYYY-MM-DDTHH-MM-SSZ` for UTC, or `…+00-00` for explicit offset) — for distributed systems where local time is meaningless.
- **Compact form** (`YYYYMMDD`) — no separators, used by some camera firmware and CI artifact stores. Sorts the same; less human-readable. Don't introduce it on purpose, but tolerate it from upstream tools.

## Adoption checklist

- [ ] `ls` in any dated directory sorts chronologically without flags.
- [ ] No filename has a two-digit year, month names, or a locale-specific order.
- [ ] Time-of-day format and time zone are documented once for the tree.
- [ ] Rename scripts print a dry-run plan and never overwrite.

## Real-world projects using this

- **ISO 8601** — the standard itself; ratified 1988, revised 2019.
- **Linux `journalctl`** — exposes timestamps in ISO format; system journal uses sortable date-time strings.
- **Obsidian Daily Notes** — default filename template is `YYYY-MM-DD`.
- **Hugo / Jekyll static site generators** — post filenames are conventionally `YYYY-MM-DD-title.md`.
- **`restic`, `borg`, `kopia`** — backup snapshot timestamps use ISO 8601.
- **Keep-a-Changelog** — every release header is `## [version] - YYYY-MM-DD`.
- **Apple Photos export, Google Takeout** — both default to ISO-style date prefixes.

## Migration & references

To rename a tree of legacy date-formatted files into ISO, a one-shot Python or shell script is usually safer than a manual sweep:

```bash
# Rename "Apr-30-2026.md" → "2026-04-30.md" using GNU date
for f in *.md; do
  iso=$(date -d "${f%.md}" +%F 2>/dev/null) || continue
  git mv "$f" "$iso.md"
done
```

For very large trees, prefer a separate commit per directory so `git log --follow` keeps each file's history intact.

Further reading:

- ISO 8601-1:2019 — the formal standard.
- W3C "Date and Time Formats" note (https://www.w3.org/TR/NOTE-datetime) — practical subset for the web; aligns with this rule.
- Keep-a-Changelog (https://keepachangelog.com) — uses the same format for entries.
- `principles/naming-conventions/` — kebab-case slugs combine cleanly with ISO date prefixes.
- `principles/stable-vs-volatile-separation/` — date-prefixed dirs are the canonical container for volatile content.
