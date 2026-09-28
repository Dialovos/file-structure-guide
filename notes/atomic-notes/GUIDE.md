## TL;DR

The **atomic-note rule** is a discipline, not a layout: *one note = one idea, small enough to be embedded fully into another note*. It's the philosophy underneath Zettelkasten, evergreen-notes, and Building a Second Brain's "intermediate packets" — but those are tooling-flavored. This guide is the pure rule, tool-neutral. The test: if you can't fully quote a note inline somewhere else without losing context or bringing along irrelevant material, it's not atomic. Atomic discipline is the single highest-leverage habit in personal knowledge management — it's what makes a vault scale past a few hundred notes without becoming a swamp. Bundling ideas ("my thoughts on productivity today") feels efficient at write time but compounds into unsearchable mush. The cost is real: atomic notes require a title decision per idea, which is the friction. The payoff is real too: every atomic note becomes a reusable building block.

## Principles & why

The atomic rule rests on three claims that justify its friction.

1. **Composability.** A note that contains exactly one idea can be cited, embedded, transcluded, or linked from any other note. A note with five ideas can't — citing it forces the reader to pick which idea you meant. Composability is what makes a knowledge graph add up to more than the sum of its notes.
2. **Re-findability.** When you search "attention residue", you want one canonical note titled `attention-residue.md`, not five mentions buried in `productivity-thoughts-2026-03.md`. Atomic titles act as a hand-curated search index. The note's title *is* the query.
3. **Edit pressure.** Bundled notes resist editing — you have to re-read the surrounding ideas to update one of them. Atomic notes invite editing because each one is small. Edit pressure is what turns capture into knowledge: you'll re-write an atomic note many times over its life. You'll never re-write a 5,000-word "thoughts" note.

The corollary: atomicity is *not* about word count. A 1,500-word note about a single mechanism is atomic. A 200-word note bundling three observations is not. The unit is the idea, not the size.

The hardest part of the rule is **deciding when one idea ends and another begins**. The practical heuristic: if you can imagine wanting to link to part-X of the note from somewhere else, part-X is its own note. If part-X always travels with part-Y, they're one idea.

Atomicity belongs to the **knowledge layer**. The capture layer (daily journal, fleeting notes) is allowed to be messy and bundled — that's where ideas first land. The discipline kicks in at refinement time: as you migrate fleeting capture into the durable knowledge layer, you split bundles into atoms.

## When to use

- **Whenever you're starting a notes system.** Establish the rule on day one. Retrofitting atomicity onto a 2,000-note swamp is brutal; doing it from the start costs nothing.
- **Knowledge work that compounds** — research, technical writing, course creation, consulting practice. Atomic notes pay off when ideas get reused.
- **Pair with any tool** — Obsidian, Logseq, Bear, plain folders. The rule is tool-agnostic.
- **Pair with any organizational philosophy** — Zettelkasten, evergreen, PARA, ACCESS, LYT, Johnny Decimal. They all assume atomicity at the leaf level; this guide just states the rule explicitly.
- **When notes feel hard to find.** Search keeps surfacing the same big "thoughts" note where the answer is buried in paragraph 7? That's the symptom — atomicize.

## When NOT to use

- **Long-form drafts in progress.** Atomicity is for the knowledge layer, not the writing layer. Drafts live in `drafts/` (or `output/` in BASB) and should be as long as they need to be. Atomicity applies *before* and *after* the draft, not during it.
- **Capture / inbox / fleeting layer.** When you're capturing fast (daily journal, meeting notes, fleeting thoughts), bundling is fine — it's faster to write and you'll process it later. The rule applies at processing time.
- **Reference material you didn't write.** A PDF article, a book chapter, a saved page — these are atomic at *their* level (one PDF = one source) but their *contents* aren't your notes. Don't atomize someone else's prose; extract atomic claims into your own notes that cite the source.
- **Project working docs.** A live project doc with a checklist + notes + decisions is supposed to be a working bundle. Don't atomize it until the project is done; then extract the durable claims into the knowledge layer.
- **People who never refine.** If your workflow is pure capture with no refinement step, atomicity buys you nothing — you'll never link or compose. Use a journal-first system (BuJo, daily notes) instead.

## Tree diagram

```
notes/
├── single-idea-per-note.md            ← OK: atomic (one mechanism)
├── attention-residue-tax.md           ← OK: atomic (one phenomenon)
├── deep-work-vs-shallow-work.md       ← OK: atomic (one distinction)
└── productivity-thoughts.md           ← BAD: not atomic — 5 ideas bundled
```

The leaf layout is what matters; this guide doesn't dictate folders. Pair atomic notes with any organizational system above (Zettelkasten, evergreen, PARA leaves, etc.). The layout shows the *rule*, not a folder convention.

## Naming rules

- **Title = the idea.** A noun phrase or short claim, not a topic. Good: `attention-residue-is-a-tax-on-context-switching.md`. Bad: `productivity.md`.
- **Kebab-case filenames.** `single-idea-per-note.md`, not `Single Idea Per Note.md`. Easier to link, easier to grep.
- **No date in the filename** — atomic notes are durable; dates belong on capture/journal layers, not the knowledge layer. (Folgezettel IDs are a different system; see `notes/folgezettel/`.)
- **Title resolves the question "is this one idea?"** If you can't write the title without using "and" or "&" twice, you have multiple ideas — split.
- **Permanent titles.** Once a note is linked from elsewhere, don't rename casually — every link breaks. If you need to rename, update all backlinks atomically.
- **No version suffixes.** `attention-v2.md` is a smell. The note is itself; new ideas are new notes that link to the old one.

## Worked example

A note called `productivity-thoughts.md` holds five ideas over 900 words.

1. Underline each distinct idea: task-switching cost, time-blocking, energy vs time, email batching, weekly review.
2. Create one note per idea with a specific title (`task-switching-has-a-recovery-cost.md`).
3. Write each in your own words, 100 to 300 words, so it can be embedded elsewhere without its neighbors.
4. Replace the original note with a short MOC that links to the five new notes.
5. Add at least two links from each new note to related notes, and say why in a sentence.
6. Test: embed one note inside another; if it drags in unrelated material, split again.

Each idea can now be cited, embedded, and improved on its own.

## Anti-patterns

- **The "thoughts" note.** `my-thoughts-on-X.md` is almost always a bundle. Split it.
- **Daily-style file in the knowledge layer.** `2026-04-30-ideas.md` mixes the date layer with the knowledge layer. Capture in dailies, then extract atoms.
- **Atomicity by line count.** Splitting a long single-idea note into pieces because it "feels too long" — the test is the *idea*, not the size.
- **Over-atomization.** A note that says only "Attention residue exists." with no claim, mechanism, or source isn't atomic; it's empty. The minimum is one *substantive* idea.
- **Topic notes as atomic notes.** A note titled `productivity.md` containing "Productivity is when you get things done." is a topic, not an idea. Topics belong in MOCs (`notes/maps-of-content/`), not as atomic notes.
- **Forgetting the rule applies to refinement, not capture.** If you try to write your daily journal in atomic form, you'll stop journaling. Bundle in dailies; atomize in refinement.

## Scaling & failure modes

- **Over-atomization**: fragments too small to make sense on their own are worse than one clear paragraph. The unit is an idea, not a sentence.
- **Link maintenance** grows with note count; favor few, meaningful links over automatic ones.
- **Discoverability** falls without hubs; pair with `maps-of-content`.
- **Imports** (clippings, highlights) aren't atomic; keep them in a source folder and derive atomic notes from them.

## Variants

- **Strict-atomic** (this guide) — one idea per note, period. The default for serious knowledge work.
- **Paragraph-atomic** — one idea per *paragraph*, multiple paragraphs per note allowed if they all develop the same root idea. Less strict; works for people whose ideas tend to come with elaboration.
- **Micro-atomic** — one *sentence* per note. Endorsed by some Logseq/Roam users; usually over-discipline. Friction exceeds payoff for most people.
- **Section-atomic** — one idea per Markdown `##` section, multiple sections per file. Common in working docs and project notes; not recommended for the durable knowledge layer because it loses the linkability of file-level atoms.
- **Atomic claims (not notes)** — a Niklas Luhmann-flavored variant where the unit is a *claim* (a defensible statement) rather than just an idea. Forces sharper notes; harder to write.

## Adoption checklist

- [ ] Each note states one idea and can be embedded without losing meaning.
- [ ] Titles are specific enough to distinguish the note from siblings.
- [ ] Each note links to at least two others, with a reason.
- [ ] Bundled notes have been split and replaced by a MOC.
- [ ] Source material is kept apart from your own notes.

## Real-world projects using this

- **Sönke Ahrens, *How to Take Smart Notes*** (2017) — the most cited modern source for the atomic-note rule, framed in Zettelkasten terms.
- **Andy Matuschak, "Evergreen notes"** (notes.andymatuschak.org) — public worked example. The published note "Evergreen notes should be atomic" is the canonical short form of the rule.
- **Tiago Forte's "Distill" step** in CODE / Building a Second Brain — atomic "intermediate packets" are the unit BASB ships through Capture → Organize → Distill → Express.
- **Niklas Luhmann's Zettelkasten** (the actual paper one) — every Zettel was atomic; this is where the modern rule traces back to.
- **Maggie Appleton's digital garden** (maggieappleton.com) — public garden built on atomic notes; great worked example of the discipline at scale.

## Migration & references

- **From bundled "thoughts" notes**: pick one bundle. Identify each distinct idea (you'll usually find 3-7 per bundle). Create a new atomic note per idea. Link them from each other where the originals implied connections. Archive the bundle (don't delete — keep as a fossil).
- **From topic-named notes** (`productivity.md`, `attention.md`): the file is probably a Map of Content. Convert it: rename to `productivity-MOC.md`, replace its contents with links to atomic notes. See `notes/maps-of-content/`.
- **From a journal-only system**: don't migrate the journal. Start a new `notes/` folder for atomic notes, keep journaling, and extract atoms during weekly review. The journal stays bundled by design.
- **References**:
  - Sönke Ahrens, *How to Take Smart Notes* (2017) — primary text.
  - Andy Matuschak, evergreen notes site (notes.andymatuschak.org).
  - Sibling guides: `notes/evergreen-notes/` (atomic + linking, tooled for Obsidian-style vaults), `notes/zettelkasten-classic/` (the Luhmann lineage), `notes/maps-of-content/` (composing atomic notes into navigable structure).
  - Anti-pattern reference: `ANTIPATTERNS.md` at repo root, "bundled thoughts notes" entry.
