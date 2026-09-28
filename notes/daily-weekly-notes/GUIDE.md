## TL;DR

Daily/weekly notes give every day and week its own canonical file: `daily/2026-04-30.md` for the day, `weekly/2026-W18.md` for the week. The daily file is the **temporal entry point** — capture lands here first, links flow outward to atomic notes once a thought earns its own life. ISO 8601 dates and ISO weeks (`YYYY-Www`) keep filenames sortable everywhere. The weekly review aggregates the seven dailies into highlights/lowlights/next-week, providing the loop that pure daily notes lack. This pattern is *not* an organisational system on its own — it's a temporal layer that pairs with any topical scheme (PARA, LYT, evergreen-notes, ACCESS) as the layer where capture happens before things get filed.

## Principles & why

The pattern rests on four claims:

1. **Time has its own dimension.** Topical organisation answers "where does this go?" Date organisation answers "when did I think this?" Both questions matter; conflating them loses information. A daily note is a timestamp-shaped container that any kind of capture can land in without prior commitment to topic.
2. **The daily file is the entry point, not the destination.** Things start in the daily note (today's meeting, today's idea, today's gripe). Things that survive get extracted into linked atomic notes; things that don't decay in place. The daily note is *processed*, not *archived*.
3. **The weekly review is the loop that closes.** Without a weekly aggregation, daily notes become a dust storm — searchable but not synthesised. The Friday/Sunday review reads back through the week, captures highlights and lowlights, and seeds the next week's plan. This is the rhythm that makes daily notes worth the effort.
4. **ISO dates are non-negotiable.** `2026-04-30.md` sorts correctly anywhere. `April-30-2026.md`, `04-30-2026.md`, `30-Apr-2026.md` all break sort order or international portability. ISO weeks (`YYYY-Www`, where W18 is the 18th week of 2026) similarly sort correctly and align with calendar tooling.

The wager: most notes are touched once and forgotten. Time-shaped capture is the shape that catches everything *before* you decide whether it's worth more.

## When to use

- Journaling, work logs, time-tracking, learning logs — any practice where "what did I do/think today?" is a recurring question.
- As the temporal layer in a larger system: pairs with [`para`](../para/), [`lyt-linking-your-thinking`](../lyt-linking-your-thinking/), [`evergreen-notes`](../evergreen-notes/), [`access-framework`](../access-framework/), or any vault.
- Tools with first-class daily-note features: Obsidian (Daily Notes plugin), Logseq (daily journal is the default home), Roam Research (daily pages), Tana, Reflect.
- Solo workflows. Date files are personal; the daily note is your scratch pad, not a shared doc.
- People who already journal in paper Bullet Journals or planners and want a digital equivalent — the daily/weekly cadence translates directly.
- Capture-first workflows: you want a frictionless place to dump anything without first deciding where it belongs.

## When NOT to use

- Pure reference vaults. If your notes are clipped articles, recipes, scanned PDFs — there's nothing temporal to capture. Use a folder taxonomy.
- You don't actually journal. Empty daily notes accumulate and demoralise. Drop the layer; use [`evergreen-notes`](../evergreen-notes/) or [`para`](../para/) directly.
- Team-shared note systems. Daily notes are per-person; sharing them creates coordination friction.
- You hate the temporal/topical mix. Some people find it disorienting to have one thought split between today's daily note and a topical evergreen note. Pure-topic systems may suit you better.
- Very high-volume capture with no review cadence. If you write 50 things a day and never review, the dailies become a write-only log. Either commit to the weekly review or stop the practice.
- Tools without good date-templating. Manually creating `2026-04-30.md` every morning is enough friction to kill the habit.

## Tree diagram

```
vault/
├── daily/
│   ├── 2026-04-29.md
│   ├── 2026-04-30.md
│   └── 2026-05-01.md
├── weekly/
│   ├── 2026-W17.md
│   └── 2026-W18.md
└── notes/
    └── (linked from daily/weekly)
```

`daily/` and `weekly/` are siblings. `notes/` (or whatever your topical layer is named) holds anything extracted from the dailies that earned its own home.

## Naming rules

1. **Daily filenames:** `YYYY-MM-DD.md`. ISO 8601, zero-padded month and day. `2026-04-30.md`, not `2026-4-30.md`.
2. **Weekly filenames:** `YYYY-Www.md`. ISO 8601 week numbering. `2026-W18.md`, not `2026-week-18.md` or `2026-w18.md`. The capital `W` is the ISO convention.
3. **Folder names:** `daily/` and `weekly/`, lowercase. Some workflows split further (`2026/04/2026-04-30.md`) — see Variants.
4. **No underscores in dates.** `2026-04-30.md`, not `2026_04_30.md`. Hyphens are the ISO standard.
5. **Templates folder, optional.** `templates/daily.md` and `templates/weekly.md` hold the boilerplate applied to each new file. Tool-managed in Obsidian/Logseq.
6. **One file per day, one per week.** Resist `2026-04-30-morning.md` + `2026-04-30-evening.md`. The whole point is one canonical capture surface per day.
7. **No timezone or offset in filename.** Date is local-time-of-the-author. If you travel across timezones, pick a rule (home timezone, current local) and stick to it.

## Worked example

Daily thoughts are scattered and there is no rhythm for turning them into anything.

1. Create `daily/` and `weekly/`. Use a template for the daily file (`daily/2026-04-30.md`) with three headings: Plan, Log, Links.
2. During the day, capture into the Log section; when a thought deserves its own life, create a note in `notes/` and link it from the day.
3. Once a week, create `weekly/2026-W18.md` and read that week's seven dailies.
4. Fill the weekly template: Highlights, Lowlights, Next week; link to any dailies or notes that matter.
5. Promote at least one item from the week into a permanent note or a project.

Capture is easy because the destination is always today's file, and the weekly review makes sure it goes somewhere.

## Anti-patterns

- **Daily notes as kitchen sink that never gets processed.** If thoughts only live in `daily/` and never get extracted, the practice has decayed into a write-only log. The fix is the weekly review.
- **Skipping weekly reviews.** Without aggregation, dailies become noise. Block 30 minutes every Friday/Sunday or drop the layer.
- **Non-ISO date formats.** `Apr-30-2026.md`, `30.04.2026.md`, `4-30-26.md` — all break sort order somewhere. ISO 8601 is the only date format you should ever use in filenames.
- **Manual file creation.** If you have to type `2026-04-30.md` by hand every morning, you'll skip days. Use the tool's daily-note hotkey or template.
- **Multiple files per day.** Splitting morning/afternoon/evening defeats the canonical-entry-point property.
- **Daily notes pretending to be evergreen.** A daily note about a recurring topic gets re-written every day and never becomes refined. Extract the durable claim into `notes/topic.md` and link from the daily.
- **Forgetting to link.** Daily notes should link generously to atomic notes; otherwise the linkage is one-way and search-only.

## Scaling & failure modes

- **Empty days**: don't create files for days without entries; a template-on-demand keeps the folder honest.
- **Volume**: 365 files a year is fine for search but poor for browsing; rely on weekly notes and links as the entry point.
- **ISO weeks** can belong to the adjacent calendar year around New Year (2026-W01 may start in December 2025); use a generator, not mental math.
- **Review debt**: skipped weeklies pile up; a shorter template beats no review.

## Variants

- **daily-only.** Drop `weekly/`. Loses the synthesis loop; common in tools that don't support week-numbering well.
- **daily-and-weekly (this guide).** The recommended baseline.
- **daily-weekly-monthly.** Adds `monthly/2026-04.md` for monthly retrospectives. Useful for goal tracking and quarter-aligned reviews.
- **daily-with-templates.** Each new daily file is pre-seeded by `templates/daily.md` — sections like `## Today / ## Done / ## Captured / ## Notes`. Reduces capture friction.
- **year-month nested.** `daily/2026/04/2026-04-30.md` instead of flat `daily/2026-04-30.md`. Useful when daily count exceeds 1000+ files.
- **daily-as-only-folder.** Some Logseq/Roam workflows put *everything* in dailies — no `notes/` folder; topical notes live as wikilinked pages auto-created from dailies. Different system; this guide assumes a separate topical layer.

## Adoption checklist

- [ ] Daily files use `YYYY-MM-DD.md` and weekly files use `YYYY-Www.md`.
- [ ] Templates exist for both and are used.
- [ ] Each weekly review promotes something out of the dailies.
- [ ] Ideas that outlive the day live in their own notes, linked back.
- [ ] Week numbers are generated by tooling.

## Real-world projects using this

- **Obsidian Daily Notes plugin** — https://help.obsidian.md/Plugins/Daily+notes — first-party, ships with Obsidian.
- **Logseq** — https://logseq.com — daily journal is the default home page; the entire app is built around the daily-page primitive.
- **Roam Research** — https://roamresearch.com — daily pages are the canonical entry point; topical pages emerge from `[[wikilinks]]` typed in dailies.
- **Tana** — https://tana.inc — modern daily-note-first PKM tool.
- **Reflect** — https://reflect.app — Roam-derived daily-note app focused on journalling.
- **Bullet Journal** by Ryder Carroll — https://bulletjournal.com — the analog ancestor; daily/weekly/monthly logs.
- **org-mode date trees** in Emacs — `~/org/journal.org` with `* 2026-04-30` headlines is the same pattern in plain text.
- **Hundreds of public Obsidian/Logseq vaults on GitHub** demonstrate the pattern — search "obsidian daily notes vault" or "logseq vault".

## Migration & references

To start daily/weekly notes from scratch:

```bash
mkdir -p vault/{daily,weekly,notes,templates}
cd vault
TODAY=$(date +%Y-%m-%d)
WEEK=$(date +%Y-W%V)
cat > "daily/${TODAY}.md" <<'EOF'
# Daily — DATE

## Today
- ...

## Done
- ...

## Captured
- ...

## Notes
- ...
EOF
cat > "weekly/${WEEK}.md" <<'EOF'
# Weekly review — WEEK

## Highlights
- ...

## Lowlights
- ...

## Next week
- ...
EOF
```

In Obsidian, configure Daily Notes plugin: Settings → Daily Notes → Date format `YYYY-MM-DD`, New file location `daily/`. Add a template at `templates/daily.md` and point the plugin at it.

In Logseq, daily journal is automatic; configure `:journal/file-name-format` to `yyyy-MM-dd` in `config.edn` for ISO filenames.

To migrate from a journal app:

1. **Export to markdown.** Day One, Bear, Notion all support markdown export.
2. **Rename files to ISO dates.** Many apps use `April-30-2026.md` or similar; rename to `2026-04-30.md`.
3. **Bulk-import into `daily/`.** Then run a one-shot weekly-review script that summarises each week into a `weekly/YYYY-Www.md` file (or do it by hand for the most recent year only).
4. **Set up the daily template.** Pick the sections that match your existing journalling habit; don't import a stranger's template.

Further reading and adjacent guides:

- [`lyt-linking-your-thinking`](../lyt-linking-your-thinking/) — uses `Calendar/` for the same role.
- [`access-framework`](../access-framework/) — uses `4-entries/` for the same role.
- [`para`](../para/) — daily/weekly slot in as a parallel layer to PARA's four buckets.
- [`evergreen-notes`](../evergreen-notes/) — the topical layer dailies feed.
- [`maps-of-content`](../maps-of-content/) — weekly reviews can themselves be MOCs.
- ISO 8601 standard — https://www.iso.org/iso-8601-date-and-time-format.html — week-numbering reference.
- Ryder Carroll, *The Bullet Journal Method* (2018) — analog daily/weekly source material.
