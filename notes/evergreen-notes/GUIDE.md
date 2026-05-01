## TL;DR

Evergreen notes is Andy Matuschak's discipline for writing notes that *compound over time*. Four rules govern every note: it must be **atomic** (one idea), **concept-oriented** (not project-, source-, or person-oriented), have a **declarative title** (a complete claim, not a topic word), and live in **dense linkage** with other notes — both citing and being cited. The directory structure is intentionally flat; the structure of the knowledge lives in the links, in Maps of Content, and in the slow refinement of titles. Where Zettelkasten asks you to capture-then-process, evergreen notes asks you to *write only when you have a claim worth refining* — and to keep refining it across months and years until it stabilises into something you'd quote in your own essay.

## Principles & why

The system encodes a wager: a note's value is roughly proportional to how often it's been edited *and* how many other notes link to it. From this fall four rules:

1. **Atomic.** One concept per note. If a note grows past a few hundred words or starts hedging between two ideas, split it. Atomicity is what makes a note linkable from many contexts; a hybrid note can be cited from none cleanly.
2. **Concept-oriented, not project- or source-oriented.** "Things to do for the redesign" is a project artefact, not a concept. "Newport's argument about deep work" is source-oriented. The evergreen version is *your* claim, derived from Newport but expressed independently: `deep-work-requires-uninterrupted-time-blocks`.
3. **Declarative titles.** The title is a *complete claim*. `attention-residue.md` is a topic; `attention-residue-tax-from-task-switching.md` is a claim. Declarative titles force you to take a position at write time — and once you've taken it, every future link to this note re-asserts that position. Topic-titled notes accumulate sludge; claim-titled notes either survive scrutiny or get rewritten.
4. **Densely linked.** A note with no links is dead weight. The discipline is to add at least 2-3 links every time you touch a note: incoming (this claim is referenced by...) and outgoing (this claim depends on...). Over time, the link graph becomes the structure that the directory structure deliberately abdicates.

The pay-off compounds: notes that have been refined and linked over years become writing material. Andy Matuschak's published notes (notes.andymatuschak.org) are an example of the same discipline producing both private thinking artefacts and public reference content with no separate "publishing" step.

## When to use

- Notes are an investment, not a backlog. You expect the same notes to still be useful in five years.
- Long-form writing pipeline: notes feed essays, papers, talks, books. The compound interest is the point.
- Researchers, essayists, programmer-writers, technical leaders — anyone whose output is partly *a portfolio of stable claims*.
- You've outgrown timestamp-based Zettelkasten and want stronger discipline on *what makes it into the canon*.
- You use a tool with first-class linking and backlinks (Obsidian, Logseq, The Archive, Roam, Notion with `@` references).
- You're willing to publish, or at least share, your notes to a small audience — the public-facing pressure tightens the discipline.

## When NOT to use

- Short-term task management. Use [`gtd-digital`](../gtd-digital/) or [`para`](../para/).
- Idea capture without intent to refine. Evergreen notes refuses cheap capture by design; if you want a dump, use a fleeting `inbox/` and process selectively. See [`zettelkasten-classic`](../zettelkasten-classic/).
- Daily journaling. The format is wrong; use [`daily-weekly-notes`](../daily-weekly-notes/) or a separate `journal/` parallel to your evergreen vault.
- Tools without backlinks. The whole system relies on bidirectional linkage; in a tool that only resolves outgoing links, half the value is missing.
- High-volume reference archives (clipped articles, recipes). Evergreen titles for thousands of items become a chore. Use [`access-framework`](../access-framework/) or a flat reference folder.
- Multi-author note-taking. Declarative titles encode *your* claims; collaborative editing of a claim collides with the personal-voice property.

## Tree diagram

```
notes/
├── attention-is-our-most-precious-resource.md
├── attention-residue-tax-from-task-switching.md
├── deep-work-requires-uninterrupted-time-blocks.md
├── notes-should-be-densely-linked.md
└── INDEX.md     ← optional MOC
```

Titles are **declarative claims**, not topics. `attention-residue-tax-from-task-switching.md` not `attention-residue.md`.

## Naming rules

1. **Filenames are claims.** `deep-work-requires-uninterrupted-time-blocks.md`, not `deep-work.md`. Use lowercase, hyphenated. Aim for 4-9 words; longer is fine if shorter would lose the claim.
2. **One claim per file.** If a title contains "and" between two distinct claims, split into two files.
3. **No date or ID prefix.** The title *is* the address. Two claims with the same title would collide — that's a feature, not a bug, and a signal that one note absorbs the other.
4. **Flat directory.** All evergreen notes are siblings on disk. The link graph is the structure.
5. **Optional `INDEX.md`** acts as a top-level Map of Content, listing the most useful entry-point notes (often themselves MOCs). MOCs *are* evergreen notes; they just happen to be MOC-shaped.
6. **Source notes are separate** — keep a `literature/` or `sources/` folder if you want to retain raw extracts, distinct from evergreen claims. The evergreen note *cites* the source note, not vice versa.
7. **Refinement marks aren't in the filename.** Don't append `-v2` or `-final`. The note's age and refinement live in the file's modification history, not in its name.

## Anti-patterns

- **Topic-only titles.** `attention.md`, `productivity.md`, `databases.md` are dumping grounds masquerading as notes. They accumulate disjoint claims and become unlinkable. Replace with declarative titles.
- **Source-shaped notes.** `notes-from-deep-work.md` is a literature note, not an evergreen note. Extract the actual claims into separately titled evergreen notes that link to the literature note.
- **Project-shaped notes.** `q2-redesign-notes.md` belongs in `1-projects/` (PARA), not the evergreen folder. Promote durable claims out of project notes and let the rest decay.
- **Sparse linkage.** A note with one link is barely connected; with zero, it's not yet evergreen. Set a minimum (2-3 outgoing links per note) and enforce it during the weekly review.
- **Folders by topic.** `evergreen/health/`, `evergreen/work/` re-creates the taxonomy you escaped. Topics live in MOCs.
- **Treating notes as "done".** Evergreen notes are *never* finished — they reach stability through years of small edits. The rule is: every time you cite a note, consider tightening it.
- **Confusing length with quality.** A great evergreen note is often short — one screen, three links, a clear claim. Length without refinement is sludge.

## Variants

- **strict-Matuschak (this guide).** Flat directory, declarative titles, no folders, optional `INDEX.md`.
- **evergreen-with-tags.** Adds a tag system (`#status/seedling`, `#status/sapling`, `#status/evergreen`) so notes' refinement state is queryable. Common when the vault is also a digital garden.
- **evergreen-with-MOC-folder.** Splits MOCs into their own `mocs/` folder so the main evergreen folder stays purely claim-shaped. Slight friction, slight clarity gain.
- **evergreen-plus-fleeting.** Pairs a separate `fleeting/` folder for raw capture with the strict evergreen folder; entries either graduate or rot. Bridges Zettelkasten's inbox with evergreen's discipline.
- **evergreen-public.** A subset of notes is published as a digital garden ([`digital-garden`](../digital-garden/)). The publishing pressure tightens the writing further, at the cost of not all notes being shareable.

## Real-world projects using this

- **Andy Matuschak's notes** — https://notes.andymatuschak.org — the canonical public example. Notes published as they're refined, with declarative titles and dense backlinks visible.
- **Bob Doto's writing** at https://writing.bobdoto.computer/ — long-form essays comparing evergreen practice with classic Zettelkasten.
- **Maggie Appleton's digital garden** — https://maggieappleton.com — overlapping practice; explicitly tags note maturity and discusses how evergreen notes feed her essays.
- **Linking Your Thinking (Nick Milo)** — https://linkingyourthinking.com — covers evergreen notes alongside MOC-driven approaches; relevant comparison material.
- **Many public Obsidian vaults** styled as digital gardens use the evergreen discipline; search GitHub for "obsidian digital garden" or "evergreen notes" for examples.
- **Joel Hooks' notes** at https://joelhooks.com/notes — another working example of evergreen practice in public.

## Migration & references

To start an evergreen vault from scratch:

```bash
mkdir -p evergreen/
cd evergreen
cat > INDEX.md <<'EOF'
# Evergreen index

Map of Content for this vault. Entry-point notes are listed below.
EOF
cat > attention-is-finite-renewable-and-easily-leaked.md <<'EOF'
# Attention is finite, renewable, and easily leaked

Replace with a real claim. Declarative title; one idea per note.

Outgoing links: ...
EOF
```

To migrate from a topic-foldered or topic-titled vault:

1. **Inventory titles, not files.** Walk through your existing notes and ask of each: is this a claim or a topic? Topics get rewritten as one or more claim-titled notes that link to the original.
2. **Move slowly.** Rewrite 5-10 notes a week, not the whole vault at once. Each rewrite tightens what survives and discards what doesn't.
3. **Keep originals during transition.** Maintain an `archive/` of the pre-evergreen versions until you're sure the rewrites carry forward everything you need. Then prune.
4. **Resist the folder reflex.** When a topic accumulates many evergreen notes, write a MOC. Don't make a folder.
5. **Build the link graph.** Every new evergreen note must link to at least 2-3 existing ones; if it can't, the topic isn't connected enough to your existing thinking yet — that's information.
6. **Publish (privately or publicly) for accountability.** Even a friend-only Obsidian Publish, a static site, or a shared folder raises the floor on note quality.

Further reading and adjacent guides:

- Andy Matuschak's "Evergreen notes" entry — https://notes.andymatuschak.org/Evergreen_notes — the source-of-truth statement of the discipline.
- *How to Take Smart Notes* — Sönke Ahrens; the Zettelkasten lineage from which evergreen-notes diverged.
- [`zettelkasten-classic`](../zettelkasten-classic/) — the predecessor; useful if evergreen-notes' "no inbox" stance feels too strict.
- [`maps-of-content`](../maps-of-content/) — pairs naturally with evergreen notes for navigation.
- [`atomic-notes`](../atomic-notes/) — the underlying philosophy without the full evergreen discipline.
- [`digital-garden`](../digital-garden/) — public-facing variant of the practice.
