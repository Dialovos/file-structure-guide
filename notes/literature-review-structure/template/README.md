# Literature review structure — template

A working skeleton for an academic-paper organization shape:
`papers/` for original PDFs, `summaries/` for per-paper atomic notes,
`bib/` for machine-readable citations, `themes/` for cross-paper
synthesis. See `../GUIDE.md` for the full reasoning.

## Layout

```
research/
├── papers/                  ← original PDFs (immutable, citable artifacts)
│   └── .gitkeep             ← drop your PDFs here, named per the convention
├── summaries/               ← one atomic note per paper, your-words-only
│   └── .gitkeep
├── bib/
│   └── references.bib       ← BibTeX, auto-exported from Zotero or hand-curated
└── themes/                  ← cross-paper synthesis
    └── .gitkeep
```

## The naming convention

Papers and their corresponding summary share a basename:

```
papers/2024-newport-deep-work-revisited.pdf
summaries/2024-newport-deep-work-revisited.md
```

Format: `<year>-<first-author-lastname>-<short-title-slug>.<ext>`.

- Lowercase, kebab-case slug.
- Four-digit year.
- Single first-author last name.
- Two papers in the same year by the same author get a letter suffix
  (`2024a-...`, `2024b-...`) — same convention as standard citations.

The 1:1 filename alignment makes "open the notes for this paper"
trivial — swap the extension.

## What goes where

- **`papers/`** — the original PDF (or HTML, EPUB, etc.). Immutable.
  Don't annotate in place; do that in your reference manager.
- **`summaries/`** — your reading notes. One file per paper, atomic,
  in your own words. A summary should typically include: claim
  (one-line), method, evidence, takeaways for your work, and links
  to relevant theme files in `../themes/`.
- **`bib/references.bib`** — BibTeX entries. Generated automatically
  from Zotero via the Better BibTeX extension is the recommended
  setup; hand-curated also works.
- **`themes/`** — cross-paper synthesis. Each theme file is an MOC
  (Map-of-Content) over the summaries it cites. This is where ideas
  actually form, not just where you remember papers.

## Composing with a reference manager

The recommended setup for academic users:

1. **Zotero** owns the PDFs and metadata. Add papers there; let
   Zotero download them.
2. **Better BibTeX** (Zotero plugin) auto-exports to
   `bib/references.bib` on every change.
3. Cite by key in your manuscripts (`\cite{newport2024deep}` or
   `[@newport2024deep]` for Pandoc) — the plugin resolves it.
4. **Summaries** live in this folder, in markdown. Use a citation
   plugin (Obsidian Citations, VS Code Pandoc plugin) to cross-link
   summaries to BibTeX entries.

If you don't use Zotero, hand-curate `bib/references.bib`. The
template's stub shows the entry format.

## Atomic-note discipline for summaries

A summary is **about exactly one paper** and is **in your own words**.
If you find yourself copy-pasting paper text, you're highlighting,
not summarizing. Highlight inside the PDF (in your reference manager);
summarize in markdown.

A typical summary looks like:

```markdown
---
title: 2024 Newport — Deep Work, Revisited
citekey: newport2024deep
---

## Claim

One-sentence version of the paper's main claim.

## Method

How they made the claim.

## Evidence

What they showed; counter-evidence; limits.

## Takeaways

What this changes for my work.

## Related

- See [[../themes/attention-economics]]
- Builds on [[2016-newport-deep-work]]
- Counters [[2022-author-paper]]
```

## When to skip the `themes/` layer

If you only need to remember individual papers, drop `themes/`.
What you have left is `papers/` + `summaries/` + `bib/` — a perfectly
good "I read papers and take notes" setup. Add `themes/` when you
start synthesizing across many sources.

## What this template includes

- **`papers/.gitkeep`** — placeholder for your PDFs. Drop them in,
  named per the convention.
- **`summaries/.gitkeep`** — placeholder for your per-paper notes.
- **`bib/references.bib`** — empty stub with a comment showing the
  BibTeX entry format and a recommendation to auto-export from Zotero.
- **`themes/.gitkeep`** — placeholder for your synthesis files.
- **`README.md`** — this file.

## Pair this with

- `../../atomic-notes/` — each summary is an atomic note.
- `../../maps-of-content/` — each theme is an MOC.
- `../../zettelkasten-classic/` — the philosophical home.
- `../../evergreen-notes/` — themes evolve into evergreens over time.
