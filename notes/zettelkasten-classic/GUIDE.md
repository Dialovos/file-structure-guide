## TL;DR

The classic Zettelkasten ("slip box") is Niklas Luhmann's note system, adapted to plain text and folders. Three working folders carry the load: `inbox/` for raw capture, `permanent/` for atomic, evergreen notes that have earned their place, and `literature/` for source-extraction notes (one per book/article/paper). A `references.bib` BibTeX file holds the citation graph and an `INDEX.md` exposes Maps of Content as the navigable entry points. The discipline isn't the folders — it's the routine of *processing* `inbox/` items into refined `permanent/` notes, each one atomic, densely linked, and cited. Luhmann's original Zettelkasten produced 90,000 notes and a sociological corpus of 70 books; the digital version uses the same workflow with timestamped filenames or [`folgezettel`](../folgezettel/) IDs as the durable address.

## Principles & why

A Zettelkasten is a *thinking partner*, not a filing cabinet. The classic three-folder layout exists to enforce a workflow:

1. **Capture is cheap; refinement is expensive.** `inbox/` exists so you can dump a half-formed thought without choosing where it lives. The cost of organising is paid later, deliberately, when the thought is fresh enough to expand and old enough to evaluate.
2. **One idea per permanent note.** The atomic discipline is not aesthetic. It enables the same idea to be linked from many contexts — if a note conflates two ideas, neither can be cited cleanly. The directory structure can't enforce atomicity; the writing routine does.
3. **Source ≠ thought.** `literature/` notes summarise a single source (book chapter, paper, talk). `permanent/` notes are *your* claims that *cite* literature notes. Conflating the two — common in flat notebooks — turns your vault into an archive of other people's thinking instead of a record of your own.
4. **Linking, not foldering, is the structure.** Folders distinguish the three workflow states (capture, source, idea). Within `permanent/`, structure emerges from links. There is no "topic folder" — topics live in [`maps-of-content`](../maps-of-content/) entries listed under `INDEX.md`.

The trade-off vs PARA: a Zettelkasten is *worse* for active project work and date-driven journaling, and *much better* for long-term knowledge that you intend to write from. It is a writing system, not an organisation system.

## When to use

- Long-term knowledge work where notes are an investment, not a backlog.
- Academic research, dissertation writing, book-length non-fiction projects.
- Writing-as-thinking workflows where draft chapters emerge from chains of permanent notes (Sönke Ahrens' *How to Take Smart Notes* is the modern playbook).
- Researchers, essayists, and engineers who routinely cite primary sources and want a clean separation between source extraction and original argument.
- Anyone whose previous note system became a graveyard of half-formed thoughts that they no longer trust as a basis for writing.
- Tools with first-class wikilink and backlink support: Obsidian, Logseq, The Archive, Zettlr.

## When NOT to use

- Short-term project work — use [`para`](../para/) or [`gtd-digital`](../gtd-digital/).
- Daily journaling or habit tracking — use [`daily-weekly-notes`](../daily-weekly-notes/) or [`bullet-journal-digital`](../bullet-journal-digital/).
- Pure reference dumping (saved articles, recipes) — the refinement workflow is overhead you don't need; use a flat reference folder or [`access-framework`](../access-framework/).
- Tools without bidirectional linking (Apple Notes, Bear before plugins) — Zettelkasten without backlinks is half a system.
- Capture-only workflows that never refine — you'll just have a giant `inbox/`. Either commit to processing or pick a system that doesn't require it.
- People who haven't yet developed a writing habit. The system is built for writers; it doesn't manufacture the writing impulse.

## Tree diagram

```
zettelkasten/
├── inbox/                  ← capture; daily/weekly process to permanent
│   └── 2026-04-30 quick-thought.md
├── permanent/              ← evergreen notes, atomic, dense links
│   ├── 202604301421 attention-as-currency.md
│   └── 202604301425 deep-work-prerequisites.md
├── literature/             ← per-source extraction notes
│   ├── newport-deep-work.md
│   └── kahneman-thinking-fast-slow.md
├── references.bib          ← BibTeX entries
└── INDEX.md                ← MOC entry-points
```

## Naming rules

1. **Permanent notes** use a 12-digit timestamp ID prefix: `YYYYMMDDhhmm short-slug.md`. Example: `202604301421 attention-as-currency.md`. The timestamp guarantees uniqueness without collisions and is stable forever.
2. **Inbox notes** use a date prefix and freer naming: `2026-04-30 quick-thought.md` or just `2026-04-30-attention.md`. They're temporary, so investment in a perfect ID is wasted.
3. **Literature notes** are named after the source, not by date: `newport-deep-work.md`, `kahneman-thinking-fast-slow.md`. The convention `<author>-<short-title>.md` matches BibTeX cite keys.
4. **Cite keys** in `references.bib` should match the literature filename (`newport2016deep` ↔ `newport-deep-work.md`) so a wikilink and a citation both resolve.
5. **Slugs** are lowercase-hyphenated and *describe the claim*, not the topic: `attention-as-currency` not `attention`. (See [`evergreen-notes`](../evergreen-notes/) for the strict version of this rule.)
6. **Links** prefer `[[short-slug]]` over `[[202604301421 attention-as-currency]]`. Most tools resolve the short form to the full filename. The full ID is the durable address; the slug is the human handle.
7. **MOC notes** in `INDEX.md` (and any sub-MOCs) are themselves permanent notes — they have IDs and live in `permanent/`. `INDEX.md` is the entry list of the most useful MOCs.

## Worked example

You read a book and want its ideas to become part of your thinking, not a pile of highlights.

1. Capture: jot fleeting thoughts in `inbox/` as they come, with the date.
2. Literature note: write `literature/newport-deep-work.md` in your own words, with page references and a BibTeX key from `references.bib`.
3. Permanent notes: from that literature note, write atomic notes in `permanent/` with a timestamp ID: `202604301421 attention-as-currency.md`. One idea each.
4. Link each permanent note to at least one existing note, and say why in a sentence.
5. Add entry points to `INDEX.md` (a few well-linked starting notes per topic).
6. Process the inbox daily or weekly; anything not processed in a month gets deleted.

The book leaves a small number of linked notes in your own words that connect to what you already know.

## Anti-patterns

- **Skipping inbox processing.** A `inbox/` with 800 items isn't a Zettelkasten, it's a graveyard. Either schedule weekly processing or change your capture habits.
- **Topical sub-folders inside `permanent/`.** `permanent/attention/`, `permanent/management/` reintroduces the taxonomy problem the system was built to escape. Topics belong in MOCs, not folders.
- **Filing source quotes as permanent notes.** A quote from Newport is *literature*, not your own atomic claim. Extract it into `literature/newport-deep-work.md`; the matching permanent note expresses *your* position on it.
- **Permanent notes longer than a screen.** Atomicity is the contract. If a permanent note grows past ~300 words, it's almost always two or three notes glued together; split them and link.
- **No backlinks in your tool.** A Zettelkasten without backlinks is just a folder of files. Use a tool that surfaces incoming links (Obsidian, Logseq, Zettlr, The Archive).
- **Mixing daily journaling into `permanent/`.** Daily entries are time-bound, not atomic-claim notes. Run a separate `daily/` folder or use a different system entirely.
- **Treating MOCs as folders.** A MOC is a *note*, not a directory. Linking from a folder name forces tool-specific magic; linking from a note works in any wiki.

## Scaling & failure modes

- **Inbox rot**: unprocessed captures become guilt; delete freely after a deadline.
- **Timestamp IDs** are simple but carry no structure; hubs and links provide the structure. If you want position in the ID, consider `folgezettel`.
- **Literature notes vs highlights**: copying passages isn't note-making; write in your own words.
- **Vault size**: a few thousand notes work with search and index notes; don't expect folders to help.

## Variants

- **classic-3-folder (this guide).** `inbox/`, `permanent/`, `literature/`. Faithful to Ahrens' presentation.
- **4-folder.** Splits `permanent/` into `permanent/` and `evergreen/` — the latter for notes that have stabilised over many revisions. See [`evergreen-notes`](../evergreen-notes/) for the discipline that backs this split.
- **folgezettel-IDs.** Replaces timestamp IDs with branching IDs (`1`, `1a`, `1a1`, `2`) per Luhmann's original method. See [`folgezettel`](../folgezettel/).
- **with-fleeting.** Adds a `fleeting/` folder for *very* raw capture, with `inbox/` reserved for items already worth processing. Two-stage triage.
- **single-folder.** Drops the folder split and uses tags (`#permanent`, `#literature`, `#inbox`) instead. Common in Logseq and tag-first tools; loses some clarity but reduces moves.
- **academic.** Adds `projects/` for in-progress papers, each cross-linking to permanent and literature notes. Bridges Zettelkasten with project-based organisation.

## Adoption checklist

- [ ] Every permanent note has a unique timestamp ID and one idea.
- [ ] Every permanent note links to at least one other note, with a reason.
- [ ] Literature notes cite a key in `references.bib`.
- [ ] The inbox is emptied on a schedule.
- [ ] `INDEX.md` lists entry points per topic.

## Real-world projects using this

- **Sönke Ahrens, *How to Take Smart Notes* (2017)** — the canonical modern reference for digital Zettelkasten practice.
- **Niklas Luhmann's archive** at Universität Bielefeld, currently being digitised — https://niklas-luhmann-archiv.de/
- **The Archive** (https://zettelkasten.de) — a Mac-native Zettelkasten app maintained by Christian Tietze and Sascha Fast; their site is one of the deepest English-language resources on the practice.
- **Zettlr** (https://www.zettlr.com) — open-source, cross-platform Zettelkasten and academic writing app; ships with first-class BibTeX integration.
- **Obsidian Zettelkasten plugins and community vaults** — search GitHub for "obsidian zettelkasten" for several public examples.
- **Andy Matuschak's notes** (https://notes.andymatuschak.org) — a refinement of the classic system into [`evergreen-notes`](../evergreen-notes/), but the lineage is direct.

## Migration & references

To start a Zettelkasten from scratch:

```bash
mkdir -p zettelkasten/{inbox,permanent,literature}
cd zettelkasten
cat > references.bib <<'EOF'
% BibTeX entries for sources cited in literature/ notes.
EOF
cat > INDEX.md <<'EOF'
# Zettelkasten index

Maps of Content (MOCs) live in `permanent/`; this file lists them.
EOF
```

To migrate from a flat note vault:

1. **Create the three folders** at the root and a backup of your current vault.
2. **Triage** existing notes into `inbox/` first — don't try to classify on day one.
3. **Process inbox in waves.** Each session, take 5-10 inbox notes and decide: throw away, keep as-is in `permanent/` (rare), or rewrite into a new atomic permanent note that links to the original. Source extracts go to `literature/`.
4. **Build MOCs as you go.** When 5-7 permanent notes share a thread, write a MOC that links them. Add it to `INDEX.md`.
5. **Keep BibTeX in sync.** Every literature note should have a BibTeX entry; cite keys match filenames.
6. **Don't aim for completeness.** A 200-note Zettelkasten you've worked on is more valuable than a 5,000-note one you've imported. Most flat-vault material can stay where it is and be brought in only when actively cited.

Further reading and adjacent guides:

- *How to Take Smart Notes* — Sönke Ahrens (2017).
- https://zettelkasten.de — long-form essays and forum.
- [`folgezettel`](../folgezettel/) — Luhmann's original ID system; pairs with classic Zettelkasten when timestamps feel arbitrary.
- [`evergreen-notes`](../evergreen-notes/) — Andy Matuschak's refinement of the permanent-notes discipline.
- [`maps-of-content`](../maps-of-content/) — the navigation pattern Zettelkasten relies on once `permanent/` grows large.
- [`literature-review-structure`](../literature-review-structure/) — heavier-weight literature side for thesis work.
