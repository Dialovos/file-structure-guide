# Roam-style daily pages — template

A reference template demonstrating the conventions you'd find in an
exported Roam graph: ISO-date daily pages, topical pages that emerge
from `[[bracket links]]`, and outline-shaped bullets throughout.
See `../GUIDE.md` for the full reasoning.

## Important: Roam is cloud-only

Roam Research itself does not run on local files — the product is a
hosted web app. **This template is for export / portability and to
demonstrate the conventions** you'd find in a Roam graph exported to
markdown, or that you'd mirror if you wanted a Roam-style workflow in
another tool.

If you want the Roam model on a local filesystem, use **Logseq** —
see `../../logseq-outliner/`. Logseq is explicitly a local-first
Roam-alike with the same daily-page-first model and block-reference
support.

## Layout

```
graph/
├── 2026-04-30.md            ← daily page; mostly outlined bullets
├── 2026-05-01.md
├── deep work.md             ← topical page; auto-created on first link
└── attention.md
```

The filesystem is flat. Roam doesn't introduce subfolders. Structure
lives in the link graph (`[[topic]]` links and `((block uuids))`)
and surfaces via backlinks and queries at runtime — features that
plain markdown can mimic only with extra tooling.

## The two page types

- **Daily pages** — filename is the ISO date (`2026-04-30.md`). The
  page UI renders the title as "April 30th, 2026" with ordinal
  suffixes. This is your default capture surface.
- **Topical pages** — filename is the human-readable topic with
  spaces preserved (`deep work.md`). Created automatically the first
  time you write `[[deep work]]` in a daily page.

## Reading the example files

- **`2026-04-30.md`** — a sample daily page with outlined bullets
  and `[[topic]]` links. The links to `[[deep work]]` and
  `[[attention]]` would each create a new topical page on first use.
- **`example-topic-page.md`** — a topical page corresponding to
  `[[deep work]]`. In the Roam UI, every block elsewhere mentioning
  `[[deep work]]` would appear under the page's "Linked References"
  panel — this is the bidirectional-backlinks model.

## Conventions to copy when mirroring Roam style elsewhere

1. **Outline shape** — bullets, indented as deep as needed. Don't
   write paragraph prose.
2. **Daily page is the default capture surface** — if it's a thought,
   it goes on today's page first; the topic page becomes a destination
   later, populated by mention.
3. **Use `[[bracket links]]` liberally** — they're cheap, they
   double as the topic-page-creation mechanism, and they make the
   backlinks panel useful.
4. **Hashtags vs links** — `#deep-work` and `[[deep work]]` are
   equivalent in Roam; pick one convention and stick to it. Most
   users default to `[[brackets]]` for navigation-worthy topics and
   `#tags` for ad-hoc faceting.
5. **Block references for live quotes** — `((block-uuid))` embeds
   another bullet by reference; edits propagate. Outside Roam, this
   is hard to replicate without a runtime.

## Migrating between tools

- **Roam → Logseq**: built-in Roam EDN/JSON importer. Daily pages
  and block refs survive cleanly.
- **Roam → Obsidian**: markdown export, drop into a vault. Block
  references degrade to plain quotes; backlinks reconstruct via
  Obsidian's own backlinks UI.
- **Plain-markdown → Roam-style**: copy this template's shape;
  adopt Logseq if you want the runtime experience.

## What this template includes

- **`2026-04-30.md`** — sample daily page demonstrating the
  outlined-bullet shape and inline `[[topic]]` links that drive
  emergent topical pages.
- **`example-topic-page.md`** — sample topical page showing what
  Roam auto-creates on first link, including the conceptual
  Linked-References zone.
- **`README.md`** — this file, explaining the conventions.

## Pair this with

- `../../logseq-outliner/` — local-first equivalent.
- `../../daily-weekly-notes/` — the daily-page concept generally.
- `../../atomic-notes/` — Roam's block-as-atom model.
- `../../topic-vs-date-organization/` — Roam as canonical
  "intentional mix" of date-driven dailies + topic-driven pages.
