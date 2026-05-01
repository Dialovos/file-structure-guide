# Digital Bullet Journal — template

A working skeleton of Ryder Carroll's Bullet Journal method, adapted
for Markdown. See `../GUIDE.md` for the full reasoning.

## Layout

```
bujo/
├── future-log.md           ← next 3-12 months, by month
├── monthly/                ← one file per month
│   ├── 2026-04.md
│   └── 2026-05.md
├── daily/                  ← one file per day, rapid-logged
│   └── 2026-04-30.md
├── collections/            ← themed pages (books, habits, trips, ...)
│   └── example.md
└── INDEX.md                ← Carroll's "Index" page → collections
```

## Daily ritual (the heart of BuJo)

1. **Open** `daily/YYYY-MM-DD.md` and rapid-log the day with glyphs:
   `•` task, `○` event, `–` note, `*` priority.
2. **End-of-day**: review entries. For each unfinished task:
   - mark `X` if complete
   - strike through if dropped
   - migrate `>` to tomorrow's daily log
   - migrate `<` to the Future Log if dated > 30 days out
   - migrate up to the Monthly Log if it's a multi-day intention
3. **End-of-month**: open next month's `monthly/YYYY-MM.md`,
   migrate unfinished monthly tasks, and re-check the Future Log
   for items now within range.

## Glyph legend

| Glyph | Meaning   |
|-------|-----------|
| `•`   | task      |
| `○`   | event     |
| `–`   | note      |
| `*`   | priority  |
| `<`   | migrated from Future Log |
| `>`   | migrated to next day/month |
| `X`   | complete  |
| ~~strikethrough~~ | dropped |

## What's in this template

- **`future-log.md`** — six months of skeleton sections.
- **`monthly/2026-04.md`** and **`2026-05.md`** — calendar + monthly tasks +
  a worked example of monthly migration from April → May.
- **`daily/2026-04-30.md`** — a complete worked daily log with the glyph
  legend at top, morning/afternoon/evening sections, and end-of-day
  migration block.
- **`collections/example.md`** — a "Books to read" collection.
- **`INDEX.md`** — Carroll's Index, listing all collections.

## Adapting it

- Substitute `- [ ]` Markdown checkboxes for `•` tasks if your editor
  doesn't render bullet glyphs nicely. Keep `○` `–` `*` for the others.
- If you use Obsidian / Logseq, point that vault's "daily notes" template
  at `daily/`. Don't break the migration ritual by auto-generating empty
  files — write only when you actually log.
- Pair with `../../evergreen-notes/` if you want a knowledge layer:
  link from collections to atomic notes.

## What this template deliberately does NOT include

- **Backlinks / wikilinks** — BuJo is linear. Add them only after a
  month of pure-form practice.
- **Tags / metadata frontmatter** — Carroll's method has no tagging.
  Resist the temptation until you've felt the friction.
- **Auto-generated daily files** — write a daily file *only* on days
  you actually log. Empty stubs erode the ritual.
