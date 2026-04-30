# Indexes and MOCs

## TL;DR

When a directory grows past ~7 immediate children, add an `INDEX.md` (code/files context) or a Map of Content (MOC, notes context) so a reader sees a curated entry point instead of an alphabetical wall of `ls`. The index gives meaning; the directory gives the files.

## Principles & why

Human working memory caps out around seven items at a glance. Past that, an `ls` is no longer a *view* — it's a search problem. Readers either skim, miss things, or default to the alphabet. None of those are choices the directory's author would make if asked.

An index is a deliberate alternative: the author picks the *order*, the *grouping*, and the *commentary*. A reader landing in `notes/` with thirty files gets a one-paragraph orientation, three or four sections (recent, perennials, drafts), and an opinionated table of links. That's a different reading experience from "alphabetized chronological dump".

The principle generalizes the README rule (`principles/readme-placement/`). A README orients you to a directory's *purpose*. An INDEX orients you to its *contents*. They overlap when the directory is small — one file does both. They split when the directory is large enough that a separate index earns its keep.

In notes vaults this same pattern is called a **MOC** (Map of Content) — popularized by Nick Milo and the LYT framework. Same mechanic: a curated, hand-edited entry page that links the items in a meaningful order, replacing the file manager's alphabetical default.

## When to use

Add an `INDEX.md` (or MOC) when any of these holds:

- The directory has ≥7 immediate children **and** order or grouping matters. A flat alphabetical sort would mislead.
- Readers need an *opinionated entry point* — "start here, then go to X, then Y" — that the filesystem can't express.
- The directory has multiple distinct subtopics that deserve a heading (`## Recent decisions`, `## Active drafts`, `## Reference`).
- The directory mixes content types (specs, drafts, archived items, exports) and a reader benefits from seeing them sorted by *role* rather than name.
- A README would be too short to do the job — an index is a 30-row table of links, not a 5-line orientation.
- You already find yourself answering the same "where's the X about Y?" question repeatedly. That's the index trying to be born.

## When NOT to use

Skip the index when the directory is already self-organizing:

- **Date-named journals.** `2026-04-29-...md`, `2026-04-30-...md` — chronological order *is* the index. Adding `INDEX.md` adds maintenance for no reading gain.
- **Single-purpose containers.** `assets/icons/` with only `.svg` files; `migrations/` with timestamped `.sql` files. The naming scheme is the index.
- **Tiny directories.** Under ~7 children, a README is enough. An index is overkill.
- **Auto-generated trees** where any human-curated index would be stale within a week.
- **Directories whose contents change hourly.** A hand-curated index decays faster than it can be edited; either auto-generate or skip.
- **Directories where the README already lists the contents.** Don't double up; expand the README into an INDEX if it grew past five lines, or split the contents into subdirs.

## Tree diagram

```
notes/
├── INDEX.md                ← curated table of contents
├── 2026-04-30-bookstore-idea.md
├── 2026-04-29-meeting-with-alex.md
├── 2026-04-28-design-review.md
├── 2026-04-27-walking-thoughts.md
├── 2026-04-26-budget-spreadsheet.md
├── 2026-04-25-sentry-hoa-naming.md
├── 2026-04-24-friday-notes.md
└── reading-list.md
```

## Naming rules

1. The file is named `INDEX.md` (uppercase) for code and file contexts; `MOC.md` or `<topic>-MOC.md` for notes contexts. Don't mix conventions in one tree.
2. One index per directory, at its root. If you need two, the directory should split.
3. Keep the index *opinionated* — sort by importance or topic, not alphabet (the file system already gives you alphabet).
4. Each entry is a link plus one line of context. "What is this and why might I care?" is the question the line answers.
5. Group by section if the directory has natural subtopics. `## Active`, `## Recent`, `## Reference` is a typical shape.
6. Keep each section ≤ ~10 entries. If a section grows beyond that, the directory probably wants subdirs.
7. The first link in each entry is the file's full name — readers should be able to identify the file from the index without clicking.

## Anti-patterns

- **`INDEX.md` that just runs `ls`.** If the index is identical to the alphabetical file listing, it adds nothing. Delete it; it'll only go stale.
- **Stale index.** A curated list that no longer matches the directory's contents. Worse than no index — readers act on wrong info.
- **Auto-generated index without an opinion.** `markdown-toc` dumps every heading in alphabetical order. Useful as scaffolding, but if you stop there you've reinvented `ls`.
- **Index *and* README repeating each other.** Pick one job per file. README = purpose; INDEX = contents.
- **Hand-maintained index in a fast-churning dir.** If the directory adds three files a day, the index is broken before lunch. Either auto-generate or accept that this directory doesn't get one.
- **Index buried in a subdirectory.** `notes/_meta/INDEX.md` — readers won't find it. The index lives at the directory's root.
- **One giant root-level index for the whole repo.** That's the README's job, and at scale that's a MOC vault, not an index. Multiple smaller indexes scale; one giant index doesn't.

## Variants

- **Hand-curated** — every entry is hand-written. Maximum quality, maximum maintenance cost. Best for stable directories.
- **Auto-generated index** — pre-commit hook or CI step regenerates the file from front-matter, headings, or a script. Stays fresh; loses opinionated ordering unless you embed sort hints.
- **Hybrid** — auto-generated body with a hand-written intro section. Top of file describes the *why*; the table below is regenerated.
- **MOC (Map of Content)** — notes-vault flavor; the "index" is itself a first-class note that other notes link to as a hub. Common in Obsidian and LYT vaults.
- **Sectioned MOC** — a hub note with multiple `##` sections, each its own mini-MOC. Used when the topic has natural subtopics that don't quite warrant separate directories.
- **External catalog** — for very large vaults, the "index" is a database query (Dataview in Obsidian, Logseq queries) rather than a file. Live, never-stale, but tied to the tooling.

## Real-world projects using this

- **Wikipedia "Outline" articles** — every major topic has an `Outline of <topic>` article curating the topic's other articles. A MOC at Wikipedia scale.
- **Awesome-* GitHub repos** (`sindresorhus/awesome`, etc.) — the README is itself the index for the linked content. Hand-curated, opinionated, highly readable.
- **Obsidian + LYT framework** (Nick Milo) — popularized the MOC pattern in personal knowledge management.
- **Every monorepo's root README** — `kubernetes/kubernetes/README.md`, `facebook/react/README.md` — a curated entry point to a directory that would otherwise be unreadable.
- **Docusaurus / MkDocs sidebars** — the `sidebar.json` or `mkdocs.yml` nav is essentially an index file in another format. Same role.
- **Awesome Lists project** (https://github.com/sindresorhus/awesome) — meta-index of curated indexes; the canonical example of "curate, don't enumerate".

## Migration & references

To find directories that *should* have an index:

```bash
# Directories with ≥ 7 immediate non-hidden children, no INDEX.md
find . -type d -not -path './.git/*' | while read d; do
  count=$(find "$d" -maxdepth 1 -mindepth 1 -not -name '.*' | wc -l)
  if [[ $count -ge 7 && ! -f "$d/INDEX.md" && ! -f "$d/MOC.md" ]]; then
    echo "candidate: $d ($count children)"
  fi
done
```

Triage by hand. Some hits are date-named directories where chronological order is already the index — leave them.

To bootstrap a new index, the minimal shape:

```markdown
# <directory> — index

Brief one-paragraph orientation: what's here, in what shape, who it's for.

## <section heading>

- [`file-1.md`](file-1.md) — one-line description.
- [`file-2.md`](file-2.md) — one-line description.

## <next section>

- [`file-3.md`](file-3.md) — one-line description.
```

Further reading:

- Nick Milo's LYT framework (https://www.linkingyourthinking.com) — origin of the MOC vocabulary in personal knowledge management.
- "Awesome Lists" pattern (https://github.com/sindresorhus/awesome) — exemplar of curated indexes at scale.
- `principles/readme-placement/` — index and README are siblings; this guide assumes you've decided when to use which.
- `principles/depth-vs-breadth/` — when an index gets too long, it's a signal the directory should split into subdirs.
- Diátaxis framework (https://diataxis.fr) — taxonomy of doc types; index files map most cleanly to the "explanation" / "reference" axes.
