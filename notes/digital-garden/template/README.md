# Digital garden — template

A working skeleton for a publicly-published, slowly-tended garden of
notes spanning seedlings (rough), budding (in-progress), and evergreen
(refined). See `../GUIDE.md` for the full reasoning.

## Layout

```
garden/
├── seedlings/                  ← rough captures, a few sentences
│   └── example-seedling.md     ← sample
├── budding/                    ← in-progress drafts
│   └── .gitkeep
├── evergreen/                  ← refined, ready-to-recommend
│   └── .gitkeep
├── meta/                       ← about, colophon, RSS template
│   └── about.md                ← sample about page
└── INDEX.md                    ← garden home page
```

## The three statuses

The directory shape mirrors a publishing pipeline. Notes enter as
seedlings and (for the ones that survive) mature toward evergreens
over weeks or months.

- **`seedlings/`** — a few sentences or a paragraph. Honest about
  where the idea is. Visible to readers; that's the whole point.
- **`budding/`** — has structure, citations forming, not yet finished.
  The note is becoming an essay or a structured argument.
- **`evergreen/`** — refined, considered, ready to recommend.
  "Evergreen" is current polish, not frozen-forever — evergreens get
  edited as thinking evolves.

The status badge on the published site is computed from which folder
the note lives in. Don't encode status in the filename.

## Tending the garden

The practice of a garden is *tending* — not publishing, not writing,
not posting. Tending happens in batches:

1. Open `seedlings/` and skim recent ones.
2. Promote any that are ripe (rewrite, link to others, deepen) into
   `budding/`.
3. Prune dead seedlings — ones that no longer interest you.
4. If a `budding/` note has matured (cohesive argument, a few rounds
   of revision, you'd recommend it to a friend), move it to
   `evergreen/`.
5. Edit existing evergreens if your thinking has shifted.

A typical cadence: weekly. Don't ship without tending; don't tend
without occasionally shipping.

## What this template includes

- **`seedlings/example-seedling.md`** — a sample seedling on
  "attention residue", written at the appropriate level of polish
  (rough, two paragraphs, a question, a couple of links).
- **`budding/.gitkeep`** and **`evergreen/.gitkeep`** — placeholders
  for the maturation stages.
- **`meta/about.md`** — a stub about page describing the garden's
  philosophy. Edit to make it yours.
- **`INDEX.md`** — the garden home page that lists notes by status.
  Most static-site generators render this as the site's index.
- **`README.md`** — this file.

## Publishing this as a static site

This template is plain markdown; you bring the publisher. Common
choices, ranked by ease of "drop it in and go":

1. **Quartz** (jzhao.xyz/quartz) — designed exactly for this layout;
   resolves `[[wikilinks]]`, computes backlinks, renders status badges
   if you wire them up. Closest to "drop folder in, get garden out".
2. **Obsidian Publish** — works directly from an Obsidian vault. Pay
   per month; minimal config.
3. **Eleventy with plugins** — flexible, more setup, complete control.
   Several plugins exist for wikilink resolution and backlinks.
4. **Hugo / Astro / Next.js** — also doable; more wiring required to
   match the wiki feel (backlinks, status badges).

Whichever publisher: ensure the seedling/budding/evergreen folder
distinction shows up in the rendered site. The point of a garden is
that readers see status alongside content.

## Pair this with

- `../../evergreen-notes/` — the philosophy that powers the evergreen
  layer.
- `../../atomic-notes/` — the underlying note discipline.
- `../../maps-of-content/` — MOCs as navigation pages within a
  garden.
- `../../lyt-linking-your-thinking/` — Nick Milo's framework, a
  frequent garden underpinning.

## When NOT to use this template

- **Private notes only.** No need for the publishing pipeline; use
  Obsidian + PARA / LYT / etc. directly.
- **You only publish polished essays.** A blog (Hugo/Astro/Substack)
  is simpler; the seedling/budding stages are dead weight.
- **You're allergic to publishing unfinished work.** The garden's
  whole bet is that publishing seedlings is *good*. If that bet
  feels wrong to you, don't take it.
