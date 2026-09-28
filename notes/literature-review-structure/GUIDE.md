## TL;DR

This is the academic-paper organization shape: **`papers/`** for the original PDFs, **`summaries/`** for one atomic note per paper, **`bib/`** for the BibTeX file(s), and **`themes/`** for cross-paper synthesis notes. Filenames are uniform across the first two: `<year>-<first-author-lastname>-<short-title-slug>.<ext>`, so `papers/2024-newport-deep-work-revisited.pdf` and `summaries/2024-newport-deep-work-revisited.md` line up one-to-one. The structure separates *sources* (immutable, citable artifacts), *summaries* (your reading notes, atomic and your-words-only), *citations* (machine-readable BibTeX for LaTeX/Markdown citation tooling), and *themes* (your synthesis across many summaries — the place where actual ideas form). It composes naturally with reference managers like **Zotero** and **Paperpile**, with citation plugins for Obsidian / VS Code, and with academic writing pipelines that use BibTeX. It is overkill for casual reading lists; for those, a single `reading-list.md` is fine. The shape pays off when you read papers regularly — for grad students, researchers, and knowledge workers writing literature reviews, it's the canonical layout.

## Principles & why

Four principles shape the directory.

1. **Source vs summary separation.** A paper PDF is an immutable artifact you don't modify; your notes about it are mutable, your-words-only, and atomic. Mixing the two in one file invites editing the wrong thing or misquoting. The `papers/`-vs-`summaries/` split makes the boundary physical.
2. **Atomic notes for summaries.** Each paper gets exactly one summary file, written in your own words, capturing claim / method / evidence / takeaways. You don't write three summary files for a paper; you don't pile two papers into one summary file. The atom is the paper. This is the same atomic-notes / Zettelkasten move applied to a literature review, and it makes summaries reusable across themes.
3. **Citations are machine-readable.** Researchers who write papers eventually need a `references.bib` file consumable by LaTeX, Pandoc, or a citation plugin. Keeping `bib/references.bib` in the repository (auto-exported from Zotero, or hand-curated) means your writing tooling can resolve citations without leaving the project.
4. **Themes are the synthesis layer.** A literature review's value isn't in the per-paper summaries; it's in the *cross-paper synthesis* — themes that cut across many sources. The `themes/` directory is where this synthesis lives, with each theme file linking to many summaries. This is also where Maps-of-Content / evergreen-notes ideas show up: a theme is an MOC over the summaries it cites.

The structural consequence: a paper that's truly novel might cause you to add one PDF, one summary, a few BibTeX entries, and edits to two or three theme files. The directories make every step have a clear home, and the paper/summary filename match makes cross-referencing painless.

A common variant: replace `papers/` with **Zotero** as the source-of-truth (Zotero attachments, accessed via its own filesystem or API). The `summaries/`, `bib/`, and `themes/` halves stay; `papers/` becomes "a Zotero collection". The conceptual shape doesn't change.

## When to use

- **Researchers and grad students.** You read papers as a primary input to your work; you write literature reviews and citation-heavy documents.
- **Knowledge workers reading academic / industry papers regularly.** Engineers tracking ML papers, designers tracking HCI work, anyone who reads more than a handful of formal papers per month.
- **You need machine-readable citations.** You'll eventually paste a `\cite{...}` or `[@key]` into a manuscript and want the BibTeX entry to resolve.
- **You synthesize across papers.** You're doing more than reading — you're building a model of a literature, a sub-field, or a debate.
- **You pair with Zotero / Paperpile.** Reference managers complement this layout cleanly; they own metadata and PDFs, you own summaries and themes.

## When NOT to use

- **Casual reading lists.** If you're tracking books or articles for personal reading, a single `reading-list.md` (or a Goodreads / Readwise / a `someday-maybe.md` entry) is enough. This structure is overkill.
- **Single-paper deep dives.** If you're studying one paper intensely (a textbook chapter, a single foundational work), a single annotated PDF and a single notes file beats a mini-archive.
- **Heavy reliance on Zotero's UI for everything.** If you're entirely happy reading and noting inside Zotero (with the Notes feature) and exporting to write, you may not need the markdown layer.
- **Notion-database users.** Some researchers prefer Notion's database-of-papers approach over flat files. The model is similar; the implementation is different. Pick one.
- **You don't synthesize.** If you only need to remember individual papers, the `themes/` layer is wasted. Drop it; what you have is just `papers/` + `summaries/` + `bib/`.

## Tree diagram

```
research/
├── papers/                          ← original PDFs, named: <year>-<first-author>-<short-title>.pdf
│   ├── 2024-newport-deep-work-revisited.pdf
│   └── 2023-kahneman-noise.pdf
├── summaries/                       ← one note per paper, atomic
│   ├── 2024-newport-deep-work-revisited.md
│   └── 2023-kahneman-noise.md
├── bib/
│   └── references.bib
└── themes/                          ← cross-paper syntheses
    ├── attention-economics.md
    └── ...
```

The summaries' filenames match the papers' filenames (just the extension differs). This 1:1 alignment makes opening "the notes for *this* paper" trivial — no lookup, just swap the extension.

## Naming rules

- **Papers and summaries**: `<year>-<first-author-lastname>-<short-title-slug>.<ext>`. Lowercase, kebab-case slug, four-digit year, single first-author last name. Examples: `2024-newport-deep-work-revisited.pdf`, `2023-kahneman-noise.pdf`. Two papers in the same year by the same author get a letter suffix (`2024a-...`, `2024b-...`), matching standard citation practice.
- **Multi-author papers**: still use first-author last name. Don't try to encode multiple authors in the filename — the BibTeX entry has the full author list.
- **Theme files**: kebab-case, descriptive — `attention-economics.md`, `replication-crisis.md`, `transformers-vs-rnns.md`. Avoid date prefixes; themes are not time-bounded.
- **BibTeX file**: `references.bib` (singular, conventional). Larger projects sometimes split into `papers.bib`, `books.bib`, `web.bib` — fine, but keep them all in `bib/`.
- **BibTeX citation keys**: most reference managers default to `firstauthor-year-firstword` (e.g., `newport2024deep`); pick a convention and let the manager generate consistently. Don't hand-edit keys after the fact — your manuscripts depend on them.
- **Subdirectories under `summaries/` or `papers/`**: only if the corpus is huge (hundreds of papers per sub-area). Then group by sub-field (`papers/ml/`, `papers/hci/`). For most projects, flat is fine; the prefix-by-year-author makes flat searchable.

## Worked example

A folder of 80 PDFs is named `paper (3).pdf`, `smith2020.pdf`, and `Kahneman Noise.pdf`.

1. Rename each PDF to `<year>-<first-author>-<short-title>.pdf`, for example `2023-kahneman-noise.pdf`.
2. Create a same-named summary: `summaries/2023-kahneman-noise.md` with sections for question, method, findings, limits, and quotes with page numbers.
3. Add the BibTeX entry to `bib/references.bib` using the same key (`kahneman2023noise`), and put the key in the summary's frontmatter.
4. Write theme notes in `themes/`, such as `attention-economics.md`, that cite summaries by key and state your synthesis.
5. Check consistency with a script that lists PDFs without summaries and summaries without a bib entry.

A search for a claim leads to a theme note, then to the summary, then to the exact page in the PDF.

## Anti-patterns

- **Editing PDFs in `papers/`.** PDFs are immutable artifacts. Annotations belong in a reference manager (Zotero, Mendeley) or as a separate `papers-annotated/` if you must keep both.
- **Mixing summaries and themes.** Summary files are paper-specific and atomic; theme files are cross-paper syntheses. Conflating them produces summaries that drift toward synthesis (and miss specifics) or themes that read like long lists of summaries (and miss insight).
- **Filenames mismatched between papers and summaries.** If `papers/2024-newport-deep-work.pdf` and `summaries/newport-deep-work-2024-notes.md` differ, you can't sort, can't cross-reference, can't script over the corpus. Keep the basename identical.
- **One giant `bibliography.md`.** Fine for personal taste; useless for tooling. If you'll write a manuscript with citations, you need real BibTeX in `bib/references.bib`.
- **Duplicate of paper content in the summary.** A summary should be in your own words, not a transcript. If you find yourself copy-pasting paper text, you're not summarizing — you're highlighting. Highlight in the PDF; summarize in the notes.
- **Themes that cite zero summaries.** A theme that doesn't link to specific summaries is a personal opinion, not a literature synthesis. If you write a theme, link the sources.

## Scaling & failure modes

- **Reference manager overlap**: Zotero or similar can own PDFs and BibTeX export; keep summaries and themes in your notes and point at the citation key.
- **Large PDFs** bloat git; keep `papers/` out of git or use git-lfs, and version only summaries and bib.
- **Duplicate papers** (preprint vs journal version) get separate summaries unless you decide otherwise; note the relationship.
- **Theme sprawl**: a theme per paper defeats synthesis; a theme needs at least three sources.

## Variants

- **Classic-paper-summary-bib** (this guide). Flat papers/summaries/bib/themes; works for most.
- **Zotero-as-source.** Replace `papers/` with a Zotero collection; everything else stays. Better-BibTeX exports `references.bib` continuously. The summaries refer to Zotero items by citation key.
- **Notion-database.** A Notion database of papers, with each row being a paper plus its summary; themes are pages that filter the database. Same model, different storage.
- **Roam-/Logseq-style.** Drop the directories; let each paper become a topical page (`[[2024 Newport — Deep Work]]`) and themes emerge from `[[bracket links]]` between them. Works if you're already living in a Roam-style outliner.
- **Annotated-PDF-centric.** If you do most of the thinking in PDF margins (Hypothes.is, GoodReader, ReadCube), the summary becomes lighter and the annotated PDF carries more weight. Keep `papers-annotated/` separate from `papers/`.

## Adoption checklist

- [ ] PDF and summary filenames match one-to-one.
- [ ] Every summary has a BibTeX key that exists in `bib/references.bib`.
- [ ] Quotes carry page numbers.
- [ ] A consistency script runs before writing sessions.
- [ ] Large PDFs are not committed to ordinary git.

## Real-world projects using this

- **Zotero + Better BibTeX** (zotero.org, retorque.re/zotero-better-bibtex) — the de facto reference-manager pipeline; auto-exports `references.bib` for LaTeX/Pandoc workflows.
- **Obsidian Citations plugin + Zotero** (github.com/hans/obsidian-citation-plugin) — wires a Zotero library to an Obsidian vault so you can `@cite` and link summaries to BibTeX entries.
- **Andy Matuschak's research-writing guides** (andymatuschak.org) — long-form writing on evergreen notes / atomic notes; the literature-review structure is the natural home for those notes when applied to academic reading.
- **Cal Newport's research practices** — Newport (a working academic) has written about his paper-tracking habits; consistent with the source/summary/theme split.
- **Paperpile** (paperpile.com) — managed reference manager that integrates with Google Docs / Markdown; structurally similar to Zotero in how it slots into this layout.

## Migration & references

- **From a flat folder of downloaded PDFs**: rename to the `<year>-<author>-<title>.pdf` convention (a small script does this), then create empty `summaries/<same-name>.md` files for the ones you've actually read. `bib/references.bib` is generated by Zotero from the imported PDFs.
- **From Zotero (everything in Zotero, nothing on disk)**: install Better BibTeX; configure auto-export to `bib/references.bib`. Zotero's storage stays the source-of-truth for PDFs; your `summaries/` and `themes/` live in markdown.
- **From Notion**: export the database as CSV + per-row markdown. Map columns to YAML frontmatter in summary files. Themes become standalone files.
- **References**:
  - `zotero.org` and `retorque.re/zotero-better-bibtex` — Zotero + Better BibTeX setup.
  - `andymatuschak.org` — evergreen-notes thinking applied to research.
  - Sibling guides: `notes/atomic-notes/` (each summary is an atomic note), `notes/maps-of-content/` (each theme is an MOC over summaries), `notes/zettelkasten-classic/` (the deeper philosophical home), `notes/evergreen-notes/` (themes evolve into evergreens over time).
