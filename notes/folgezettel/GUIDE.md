## TL;DR

Folgezettel is Niklas Luhmann's *actual* ID system, the one he used to organise 90,000 paper slips into a working second brain. Each note has a branching alphanumeric ID — `1`, `1a`, `1a1`, `1a2`, `1b`, `2` — that encodes its position in a thread of thought. `1a` is a continuation or refinement of `1`; `1a1` continues `1a`; `1b` is a sibling branch off `1`. Filenames sort lexicographically into the logical thread without folders. The whole vault is a single flat directory, but the IDs render an implicit tree of arguments. Where timestamp IDs ([`zettelkasten-classic`](../zettelkasten-classic/)) are arbitrary and require Maps of Content for navigation, Folgezettel IDs *are* the navigation: open the file before the one you're reading and you'll land on its parent in the argument.

## Principles & why

Folgezettel pushes a stronger claim than classic Zettelkasten: that the *structure of thought is itself a kind of address*. Three principles:

1. **The ID encodes the genealogy.** A new note doesn't get a fresh timestamp — it gets an ID derived from the note it answers, refines, or branches from. `1a1` is the first child of `1a`, which was the first child of `1`. Reading IDs left-to-right walks back up the lineage.
2. **Sort order = thread order.** Because filenames lead with the ID, lexicographic sort presents the notes in their argumentative order. `1`, `1a`, `1a1`, `1a2`, `1b`, `2` is exactly how the thread reads: the root claim, its first refinement, two consequences of that refinement, a sibling refinement, and an unrelated next root.
3. **Branching, not nesting.** The system is *flat* on disk. `1a1` and `1b` are siblings of `1`, not subdirectories. This is critical: it means any note can be opened, linked, or grepped without filesystem ceremony, and the relational structure lives entirely in the IDs and links.

The cost of all this: ID assignment requires *thought at write time*. You have to know where the new note slots in, which means you have to read the chain. Luhmann did this on paper; modern Folgezettel users do it with plugins (Obsidian Folgezettel, Zettlr's outline, The Archive). Without tooling, the discipline is heavy enough that classic timestamp Zettelkasten is a more popular starting point.

## When to use

- You've already used a classic Zettelkasten for a while and want stronger structural signal in IDs.
- You write long argumentative chains where parent-child-sibling relationships matter (philosophy, theory, structured essay drafts).
- You're committed enough to maintain branching IDs by hand, or your tool generates them automatically (Obsidian Folgezettel plugin, Zettlr).
- You prefer a single flat directory over folders — backups, grep, and version control all behave more predictably.
- You think in terms of intellectual lineage: "this note refines that one" rather than "this note is in topic X".
- You want the property that printing the vault in filename order produces a readable thread.

## When NOT to use

- You're new to Zettelkasten. Start with [`zettelkasten-classic`](../zettelkasten-classic/) and timestamp IDs; add Folgezettel later if you find yourself wanting it.
- You change the topology of your notes often. Renaming a Folgezettel ID propagates through links, and unlike timestamps, the new ID has to mean something. Frequent restructuring is painful.
- Your tool can't generate or render branching IDs and you're allergic to manual ID management. Without plugin support the friction is high.
- Your notes are mostly atomic-but-independent (e.g. a recipe collection, a glossary). Folgezettel's whole value is encoding lineage; without lineage, the IDs are noise.
- You want notes to be findable by topic search rather than by following a thread. Folgezettel doesn't help with topical navigation; pair it with [`maps-of-content`](../maps-of-content/) if you need that.
- Multi-author collaboration. Two people generating IDs in parallel will collide; coordination overhead defeats the system.

## Tree diagram

```
zettelkasten/
├── 1 deep-work-overview.md
├── 1a attention-residue.md
├── 1a1 task-switching-cost.md
├── 1a2 context-rebuild-time.md
├── 1b prerequisites-for-deep-work.md
├── 2 shallow-work-tax.md
└── INDEX.md
```

## Naming rules

1. **Root notes** are pure integers: `1`, `2`, `3`, .... Each starts a new thread.
2. **Children** alternate between letters and digits as the depth increases. The first generation under `1` is `1a`, `1b`, `1c`. The second generation under `1a` is `1a1`, `1a2`. The third under `1a1` is `1a1a`, `1a1b`. So depth alternates `<root><letter><digit><letter>...`.
3. **Filename** is `<ID> <slug>.md` with a single space separator: `1a1 task-switching-cost.md`. Some users prefer a dash: `1a1-task-switching-cost.md`. Pick one and be consistent.
4. **Slugs** are lowercase-hyphenated and describe the claim, not the topic.
5. **Sibling order matters.** `1a1` is the first thing branched off `1a`, `1a2` the second. The order is roughly chronological at write time, but you can re-letter if a more important child arrives — at the cost of updating every link and every descendant ID.
6. **Pure-numeric variant** uses `1.1.1`, `1.1.2`, `1.2`, with no letters. Easier to type but loses the visual rhythm Luhmann's original alternation provided.
7. **No folders.** All Folgezettel notes live in one directory. The tree is virtual, expressed by IDs.
8. **`INDEX.md`** is optional but useful — list the root IDs (`1`, `2`, `3`) with one-line descriptions so a reader knows where to enter.

## Anti-patterns

- **Re-using a retired ID.** If you delete `1a3`, do not assign that ID to a later note. Every retired ID stays retired so links don't silently re-point.
- **Re-lettering aggressively.** Inserting `1a` between existing `1a` and `1b` means renaming `1b → 1c`, `1c → 1d`, and every descendant. Do it when a new root-level child arrives, but think twice for deeper edits — the cost compounds.
- **Folders as escape hatch.** The temptation to file `1`-thread notes into a `thread-1/` folder defeats the system. Stay flat; the IDs are the structure.
- **Mixing Folgezettel and timestamp IDs.** Either the ID encodes lineage or it doesn't. Picking one note at a time defeats the discipline.
- **Treating IDs as hierarchical paths.** `1a1` is *related* to `1a` but it isn't *contained* by it. The "tree" is conceptual, not physical. Code that treats IDs as paths will mis-handle siblings.
- **Long IDs.** A 14-character ID like `1a1b2c3a1b1a2c` indicates the chain has grown into a private maze. Fork into a new root (`14`) and use links instead of more characters.

## Variants

- **strict-Luhmann (this guide).** Alternating letters and digits, single flat directory, no folders. Faithful to the paper original.
- **simplified.** Date-prefix plus hand-numbered tail: `2026-04-30-1a`, `2026-04-30-1b`. Adds creation date back, useful when chronology matters.
- **pure-numeric.** `1.1.1`, `1.1.2`, `1.2`. No letters. Easier to type, harder to read deep chains. Common in Zettlr outline view.
- **dotted-letter.** `1.a.1` instead of `1a1`. Some users find dots more readable; Obsidian Folgezettel plugin supports both.
- **Folgezettel-with-MOC.** Pure Folgezettel for the body, plus a small set of `MOC-<topic>.md` notes that link in by ID. Keeps the flat directory while adding topical entry points.
- **Folgezettel-on-top-of-Zettelkasten.** Use timestamp IDs for raw permanent notes; assign a Folgezettel ID *additionally* when a note enters an argumentative thread. Two coordinate systems — heavier, but reflects how Luhmann actually worked late in his career.

## Real-world projects using this

- **Niklas Luhmann's archive** at Universität Bielefeld — https://niklas-luhmann-archiv.de/ — the original 90,000-card Zettelkasten, now being digitised. The branching IDs are visible in the scanned slips.
- **Zettlr** (https://www.zettlr.com) — open-source Zettelkasten editor with built-in Folgezettel-style outlining and BibTeX integration.
- **Obsidian Folgezettel plugin** — community plugin that generates branching IDs and renders the implicit tree.
- **Christian Tietze's writing** at https://zettelkasten.de — extensive English-language essays on Folgezettel theory and practice, including critiques of common misuse.
- **Daniel Lüdecke's documentation** — Lüdecke maintains a long-running Zettelkasten reference site that includes Folgezettel discussion.
- **Nick Milo's comparison content** at https://linkingyourthinking.com — covers Folgezettel alongside timestamp-based and MOC-based alternatives.

## Migration & references

To start a Folgezettel vault from scratch:

```bash
mkdir -p folgezettel/
cd folgezettel
cat > "1 root-claim-here.md" <<'EOF'
# Root claim

The first thread starts here. Children become 1a, 1b, ...
EOF
cat > INDEX.md <<'EOF'
# Folgezettel index

- [[1 root-claim-here]] — first thread
EOF
```

To migrate from a classic timestamp Zettelkasten:

1. **Don't rename existing notes.** Timestamps are durable IDs. Instead, *augment*: add a Folgezettel ID as a metadata field or a wikilink alias, leaving the timestamp filename intact. Once the dual-IDs prove valuable, you can decide whether to move to pure Folgezettel.
2. **Identify your strongest thread.** The thread you've cited from most often is `1`. Its key children become `1a`, `1b`, etc. Work outward from there.
3. **Maintain a separate `INDEX.md`** that maps Folgezettel IDs to timestamp filenames during the transition — that way old links still resolve.
4. **Resist letter-shuffling.** Re-lettering is the most painful operation in this system. Once a child has descendants, treat its ID as immutable.
5. **Tool support is essential.** Without a plugin or script that suggests the next available ID, manual assignment becomes tedious and error-prone.

Further reading and adjacent guides:

- [`zettelkasten-classic`](../zettelkasten-classic/) — start here if Folgezettel feels like too much up-front investment.
- [`evergreen-notes`](../evergreen-notes/) — Andy Matuschak's flat-directory + densely-linked alternative; drops IDs in favour of declarative titles.
- [`maps-of-content`](../maps-of-content/) — pairs well with Folgezettel for topical navigation.
- *How to Take Smart Notes* — Sönke Ahrens; touches on Folgezettel but advocates the timestamp variant for newcomers.
- The Niklas Luhmann archive (https://niklas-luhmann-archiv.de/) for the original source material.
