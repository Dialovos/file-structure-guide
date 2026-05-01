# Logseq graph — template

A working skeleton of a Logseq graph: journal-first, outliner-driven,
local Markdown. See `../GUIDE.md` for the full reasoning.

## Layout

```
graph/
├── journals/
│   └── 2026_04_30.md       ← Logseq uses `_` not `-`
├── pages/
│   └── example-page.md     ← created from a `[[wikilink]]` in a journal
├── assets/                 ← attachments (Logseq auto-fills)
├── logseq/
│   └── config.edn          ← Logseq config (EDN, not JSON)
└── .gitignore
```

## The naming gotcha

**Journal filenames use underscores, not dashes:** `2026_04_30.md`.
This is the default Logseq convention. If you rename them with dashes,
Logseq treats them as ordinary pages and you lose the calendar /
journal features.

The page *title* that renders in the Logseq UI is derived (e.g.,
"Apr 30th, 2026"); the underscore form is just the on-disk format.

## Daily ritual (the journal-first workflow)

1. Open Logseq — it lands you on today's `journals/YYYY_MM_DD.md`.
2. Outline whatever's on your mind. Each line is a block (start with `- `).
3. Write `[[topic name]]` to either link to or create a topical page.
   Logseq creates `pages/topic-name.md` automatically.
4. Use `TODO` at the start of a block for a task; Logseq tracks state.
5. Use `((block-uuid))` to transclude a single block from another page.

## Why blocks not pages

The unit of thought in Logseq is a *block* (a single bullet line),
not a note. Every block has a UUID and can be:

- Referenced from another page with `((uuid))`
- Embedded such that edits propagate live
- Moved between pages without losing references

This is why journal entries can capture an idea now and a topical
page can transclude that exact block later — you don't duplicate.

## What this template includes

- **`journals/2026_04_30.md`** — a sample journal page with the
  outline structure, links to topical pages, a TODO, and inline
  comments explaining the syntax.
- **`pages/example-page.md`** — a sample topical page (`deep-work`)
  showing how a page is just an outline of bullets with links.
- **`logseq/config.edn`** — minimal sample config with the journal
  filename format set to `yyyy_MM_dd`, Markdown as the preferred
  format, and `assets/` configured.
- **`.gitignore`** — Logseq-flavored: ignores `logseq/bak/` and
  `logseq/version-files/` (auto-backups that bloat the repo).

## Day-one configuration

After cloning into a directory and opening it as a graph:

1. Logseq will create `logseq/config.edn` if it doesn't exist;
   if you started with this template's config, Logseq picks it up.
2. The first time you paste an image, `assets/` gets populated.
3. Open today's journal — `journals/<today>.md` is created on demand.

## Pair this with

- `../../atomic-notes/` — Logseq blocks are atomic at the bullet
  level; this guide explains the discipline.
- `../../daily-weekly-notes/` — the journal-first concept.
- `../../topic-vs-date-organization/` — Logseq is the canonical
  "intentional mix": dailies + topical pages emerging from links.

## Sync recommendations

- **Git** is the most conflict-aware option for solo Logseq graphs.
- **Logseq Sync** (paid, official) handles concurrency correctly.
- **Avoid Dropbox/iCloud** for active multi-device editing — the
  Logseq database can corrupt on simultaneous writes.
