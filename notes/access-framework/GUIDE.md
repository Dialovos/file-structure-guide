## TL;DR

ACCESS — *Action / Categories / Concepts / Entries / Search / Sources* — is a six-folder framework for personal vaults that have outgrown PARA's four buckets. The split makes explicit what PARA leaves implicit: **concepts** (your ideas) live separately from **sources** (other people's ideas), **entries** (timestamped notes) live separately from **categories** (durable areas), and **search** (saved queries / Dataview indexes) gets its own first-class home so the vault can self-index. Numeric prefixes (`1-action/` ... `6-sources/`) force a stable sort order that mirrors the conceptual flow from doing → being → thinking → living → finding → reading. The cost is one more folder than PARA; the benefit is no more "is this a project or an area, or is it just a reference?" decision paralysis.

## Principles & why

ACCESS makes six commitments that PARA collapses into four:

1. **Action and Categories are separated.** PARA's "Projects" and "Areas" both live as parallel folders, but they conflate "what I'm doing this quarter" with "who I am over years". ACCESS makes Action explicitly transient (`1-action/q2-redesign/`) and Categories explicitly durable (`2-categories/health/`, `2-categories/career/`). Archiving a project doesn't touch a category; deprioritising a category doesn't archive its projects.
2. **Concepts and Sources are separated.** This is the killer feature for researchers. `3-concepts/attention-residue.md` is *your* claim, refined over time. `6-sources/newport-2016-deep-work.md` is the literature note — direct extracts from Newport's book. Evergreen-notes purists do this informally; ACCESS makes it structural. Concepts cite sources; sources do not pretend to be concepts.
3. **Entries are first-class temporal storage.** Daily notes, weekly reviews, journal — anything timestamped — lives in `4-entries/`. The folder is allowed to grow large; size is a feature here, not a smell.
4. **Search is a folder.** Saved queries, Dataview pages, smart indexes — anything that *finds* notes rather than *being* a note — gets its own home in `5-search/`. This pulls navigation infrastructure out of the rest of the vault and admits, structurally, that good vaults need explicit indexing.
5. **Numeric prefixes are deliberate.** `1-action/` always sorts above `2-categories/` in any tool. The numbers encode workflow: you act before you reflect on areas, you have areas before you abstract concepts, etc. Alphabetical sort would shuffle these.
6. **Six is the cap.** The framework explicitly resists growing past six folders. If you need more, you're modelling something else; sub-folders within the six are fine and expected.

The wager: PARA's elegance is also its weakness — four buckets can't represent the difference between "my idea" and "Newport's idea", and most vaults eventually need that distinction.

## When to use

- Vaults with hundreds-to-thousands of notes that have outgrown PARA's four buckets.
- Heavy researchers who want explicit "concepts" vs "sources" separation. Anyone writing literature reviews or theses benefits.
- Vaults that have started to need explicit indexes (saved Dataview queries, table-of-contents notes). ACCESS gives them a home.
- Knowledge workers who journal heavily — a dedicated `4-entries/` keeps journal pollution out of the rest of the vault.
- Anyone who finds PARA's "projects vs areas" decision genuinely hard. ACCESS lets you defer it: action is action, categories are categories, no overlap.
- Solo vaults, not teams. The six-fold split encodes one person's mental model.

## When NOT to use

- Small vaults (<200 notes). The extra folders cost more than they save; [`para`](../para/) or even a flat structure is plenty.
- You don't read sources. If your vault is purely original notes (essays, code, designs), the Concepts/Sources split is wasted; use [`evergreen-notes`](../evergreen-notes/).
- You don't journal. `4-entries/` becomes vestigial; [`para`](../para/) is fine.
- You hate numeric prefixes. The framework loses its workflow encoding without them; consider [`lyt-linking-your-thinking`](../lyt-linking-your-thinking/).
- Team vaults. Six buckets is one person's taxonomy; teams need negotiated structure.
- File-system-first archival. Use a domain folder layout, not ACCESS.

## Tree diagram

```
vault/
├── 1-action/           ← active to-dos and projects
├── 2-categories/       ← stable area-of-life MOCs
├── 3-concepts/         ← evergreen notes (claims/ideas)
├── 4-entries/          ← daily/weekly notes, journal
├── 5-search/           ← saved queries, dataview indexes
└── 6-sources/          ← external references, literature notes
```

The numbers force the order. Anything inside each folder follows that folder's discipline (atomic notes in `3-concepts/`, daily files in `4-entries/`, etc.).

## Naming rules

1. **Top-level folders are numbered:** `1-action/`, `2-categories/`, `3-concepts/`, `4-entries/`, `5-search/`, `6-sources/`. The dash-after-number is required for cross-tool compatibility.
2. **Inside `1-action/`:** one folder or note per active project — `1-action/q2-redesign/` or `1-action/q2-redesign.md`. Lowercase-hyphenated.
3. **Inside `2-categories/`:** one MOC or sub-folder per durable area — `2-categories/health.md`, `2-categories/career.md`, or `2-categories/career/index.md`. Categories are stable across years.
4. **Inside `3-concepts/`:** evergreen-notes-style atomic claims, lowercase-hyphenated, declarative titles preferred — `3-concepts/attention-residue-tax-from-task-switching.md`. Flat (no sub-folders).
5. **Inside `4-entries/`:** ISO date filenames — `4-entries/2026-04-30.md`, `4-entries/2026-W18.md`. Optionally split into `4-entries/daily/` and `4-entries/weekly/` if volume warrants.
6. **Inside `5-search/`:** descriptive index names — `5-search/all-evergreen-by-recency.md`, `5-search/incomplete-projects.md`. Often Dataview-driven in Obsidian.
7. **Inside `6-sources/`:** one note per source — `6-sources/newport-2016-deep-work.md`, `6-sources/matuschak-evergreen-notes.md`. Author-year-title is conventional but not required.
8. **`INDEX.md` at vault root** is recommended — it's a top-level MOC that links to entry points across all six folders.

## Worked example

A PARA vault's `3-resources/` holds book highlights, half-written ideas, and dashboards in one pile.

1. Sort resources by whose thinking it is: yours (`3-concepts/`) or someone else's (`6-sources/`).
2. Move dated captures (journal, meeting logs) to `4-entries/`; keep durable life-area hubs in `2-categories/`.
3. Move current to-dos and active projects to `1-action/`.
4. Put saved queries and dashboards (Dataview blocks, search notes) in `5-search/`, so they don't pose as content.
5. Add one category hub per area, for example `2-categories/health.md`, that links to concepts, sources, and open actions.
6. Cap it: six folders, no seventh. New kinds of things go into an existing folder or become tags.

Ideas you wrote yourself and quotes from books are no longer mixed, so citing and reusing both gets easier.

## Anti-patterns

- **Putting concepts in sources.** `6-sources/my-thoughts-on-attention.md` — that's a concept, move it. The split's value collapses if you blur it.
- **Putting sources in concepts.** `3-concepts/notes-from-deep-work.md` — that's a literature note, move to `6-sources/`. Then extract the actual claims into separately titled concept notes.
- **Adding a seventh top-level folder.** `7-archive/` is the most common drift; either make it `0-archive/` (sorts above) or keep archives inside each folder (`1-action/archive/`).
- **Forgetting `1-action/` is transient.** Old projects pile up; periodically move completed projects to an archive sub-folder or remove entirely.
- **Categories full of dead areas.** A category should be alive; if you haven't touched `2-categories/skiing/` in three years, archive it. Categories aren't a graveyard.
- **No `5-search/` content.** If `5-search/` is empty, you're not using the framework — saved indexes are the *point* of having a search folder.
- **Skipping numbers.** `action/`, `categories/` without numeric prefixes loses the workflow ordering. Tools sort alphabetically; numbering forces semantic order.

## Scaling & failure modes

- **Boundary disputes** (is this a concept or a source?) recur; use the test "could someone else have written it?" If yes, it's a source.
- **Concept folder growth**: past a few hundred notes, rely on category hubs and MOCs instead of subfolders.
- **Entries pile up** as dated files; they're cheap, so leave them flat and prune by review.
- **Tool coupling**: the search folder assumes a tool with queries (Dataview or similar); without one it stays empty and can be dropped.

## Variants

- **ACCESS-strict (this guide).** Six folders, numbered prefixes, hard separation.
- **ACCESS-without-search.** Five folders — drop `5-search/` and rely on tool features (Obsidian search, Dataview embedded in MOCs). Simpler, less self-indexing.
- **ACCESS-with-archive.** Seven folders — adds `0-archive/` or `7-archive/` for fully cold material. Useful if you compulsively delete; keeps a graveyard outside the active six.
- **ACCESS-PARA-hybrid.** Use PARA's `1-Projects / 2-Areas / 3-Resources / 4-Archive` for the action/category/source axis, then add `Concepts/`, `Entries/`, `Search/` as parallel non-numbered folders. Concrete and emergent — pay both costs.
- **ACCESS-with-evergreen-flat.** Inside `3-concepts/`, enforce strict [`evergreen-notes`](../evergreen-notes/) discipline (declarative titles, dense linkage, no sub-folders). Common pairing.

## Adoption checklist

- [ ] Exactly six top-level folders with numeric prefixes.
- [ ] Every note in `3-concepts/` is your own claim; quotes live in `6-sources/`.
- [ ] Each category has one hub note linking concepts, sources, and actions.
- [ ] Saved searches are kept in `5-search/`, not among concepts.
- [ ] The framework is described in a short `README` at the vault root.

## Real-world projects using this

- **Obsidian community discussions** of ACCESS as a PARA alternative — search the Obsidian forum and Reddit `r/ObsidianMD` for "ACCESS framework" or "ACCESS folder structure".
- **The LYT community** (Linking Your Thinking) — Nick Milo's forum and Discord have surfaced ACCESS as one of several alternatives to pure PARA.
- **Public Obsidian vaults on GitHub** — searching "ACCESS framework obsidian" turns up working examples; many bloggers in the PKM space have published their ACCESS vaults.
- **YouTube walkthroughs** by PKM creators (search "ACCESS framework Obsidian") — most demonstrate variants on the strict six-folder layout.
- **Bryan Jenks' content** has touched on six-bucket alternatives to PARA; not strict ACCESS but conceptually close.
- **The framework is folk-developed** rather than owned by a single creator, so attribution is diffuse — the conceptual roots trace through PARA, LYT, and broader PKM community.

## Migration & references

To start an ACCESS vault from scratch:

```bash
mkdir -p vault/{1-action,2-categories,3-concepts,4-entries,5-search,6-sources}
cd vault
cat > INDEX.md <<'EOF'
# Vault index

Six-folder ACCESS layout. Top-level entry points:

- [[1-action/]] — active projects
- [[2-categories/]] — areas of life
- [[3-concepts/]] — evergreen claims
- [[4-entries/]] — journal
- [[5-search/]] — saved indexes
- [[6-sources/]] — literature notes
EOF
```

To migrate from PARA:

1. **Map the buckets.** PARA `1-Projects/` → ACCESS `1-action/`. PARA `2-Areas/` → ACCESS `2-categories/`. PARA `3-Resources/` splits into ACCESS `3-concepts/` (your ideas) + `6-sources/` (others' ideas). PARA `4-Archive/` becomes optional `0-archive/` or sub-folder archives.
2. **The hard split is Resources.** Walk every file in PARA's `3-Resources/` and ask: is this *my claim* or *someone else's text*? Concepts go to `3-concepts/`; sources go to `6-sources/`. Mixed notes get rewritten into one of each.
3. **Carve out entries and search.** Pull daily notes / weekly reviews into `4-entries/`. Create your first saved index in `5-search/` (e.g. "all evergreen by recency").
4. **Renumber.** Add the `1-`, `2-`, ... prefixes. Most tools handle the rename gracefully.
5. **Build `INDEX.md`** at vault root once the six folders have content.
6. **Resist seventh-folder drift.** When something doesn't fit, it usually belongs as a sub-folder, not a new top-level.

Further reading and adjacent guides:

- [`para`](../para/) — the four-bucket predecessor; ACCESS extends it.
- [`evergreen-notes`](../evergreen-notes/) — the discipline that fits naturally inside `3-concepts/`.
- [`zettelkasten-classic`](../zettelkasten-classic/) — overlaps with concepts/sources separation.
- [`lyt-linking-your-thinking`](../lyt-linking-your-thinking/) — alternative emergent-structure approach.
- [`daily-weekly-notes`](../daily-weekly-notes/) — the temporal layer that fills `4-entries/`.
- [`maps-of-content`](../maps-of-content/) — MOC discipline applies inside `2-categories/` and `5-search/`.
- Tiago Forte, *Building a Second Brain* (2022) — the PARA source material from which ACCESS evolves.
