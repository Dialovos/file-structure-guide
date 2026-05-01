## TL;DR

A *Map of Content* (MOC) is a note whose body is mostly links to other notes — a self-curated index for a topic. Treat MOCs as **first-class** by giving them their own folder (`MOCs/`) and a recognisable naming convention (`+ Topic.md` or `MOC - Topic.md`). One MOC per topic cluster; the MOC is the entry point you follow into a topic, the orientation page that distinguishes a knowledge graph from a junk drawer. MOCs are themselves notes — same atomicity discipline, same linking rules, same refinement-over-time wager — but they're shaped to be navigated rather than read. The pattern originated in Nick Milo's LYT framework but is a primitive that pairs with Zettelkasten, evergreen-notes, ACCESS, and any system that has more notes than browsing alone can manage.

## Principles & why

Three commitments make a MOC work:

1. **A MOC is opinionated, not exhaustive.** The temptation is to list every note in a topic. The discipline is to organise — open with a paragraph of orientation, then group links into 3-7 sections that reflect *how you think about the topic*, not *what's alphabetically there*. A flat list of every tagged note is a tag, not a MOC.
2. **MOCs are notes, not metadata.** Same naming rules, same Markdown, same refinement-over-time. A MOC about `attention-and-focus` should itself be evergreen — refined as your view of attention evolves. Storing MOCs as a separate file type (e.g. as Obsidian "frontmatter only") loses this.
3. **MOCs need a recognisable name.** The `+ ` prefix (LYT convention) sorts them to the top of any folder listing and visually marks them as hubs. Alternatives — `MOC - Topic.md`, `Topic.MOC.md` — also work; the requirement is *consistency*. Without a marker, MOCs blend into atomic notes and their hub function is invisible.
4. **One MOC per topic cluster.** Resist the temptation to make sub-MOCs of sub-MOCs. A single topic cluster (e.g. "writing process", "attention and focus") should have one canonical MOC. If it grows past ~50 links, that's a signal to split the topic, not to nest the MOC.
5. **MOCs link both up and down.** A MOC links *down* to atomic notes within its topic, and *up* to a higher-level home or domain MOC. The bidirectional linkage means a reader can drill in or zoom out from any MOC.

The wager: in a vault of >100 notes, atomic notes alone are unbrowseable. The MOC is the navigation layer that grows with you, written by you, in your shape — instead of search, tags, or folder breadcrumbs.

## When to use

- Vaults with >100 atomic notes where browsing alone breaks down — search finds notes, but doesn't orient you in a topic.
- LYT, Zettelkasten, evergreen-notes, or ACCESS workflows that need explicit hubs.
- Any topic cluster where you've found yourself thinking "I should write a 'where to start with X' page" — that's a MOC waiting to be written.
- Tools with first-class wikilinks: Obsidian, Logseq, Roam, The Archive, Foam, Tana, Reflect.
- Long-running personal knowledge bases where the link graph is the structure.
- When you want to publish/share a topic cluster — a MOC is the natural front door for an external reader.

## When NOT to use

- Small vaults (<50 notes). Tag-driven discovery is enough; MOCs are over-engineering.
- Pure reference vaults (clipped articles, recipes, scanned PDFs). Folder taxonomy works better there.
- Folder-first workflows where the folder name *is* the navigation. A `health/` folder doesn't need a `MOC - Health.md` if the folder lists everything.
- Tools without backlinks. MOCs depend on being themselves linked-from, so the bidirectional view is visible.
- Team-shared vaults. MOCs encode personal navigation; consensus MOCs are a coordination tax.
- Truly archival vaults. MOCs are for active thinking material; cold archives just need search.

## Tree diagram

```
vault/
├── notes/
│   ├── attention.md
│   ├── deep-work.md
│   └── flow-state.md
└── MOCs/
    ├── + attention-and-focus.md     ← links to all three notes above
    └── + writing-process.md
```

The `MOCs/` folder is parallel to `notes/`. The `+ ` prefix sorts MOCs to the top of any listing within their folder.

## Naming rules

1. **MOC filenames carry a marker.** Pick one and stick with it: `+ Topic.md` (LYT-style), `MOC - Topic.md`, or `Topic.MOC.md`. Don't mix conventions.
2. **Title Case after the marker.** `+ Attention and Focus.md`, not `+ attention-and-focus.md`. MOCs are titled like book chapters; atomic notes use lowercase-hyphenated.
3. **One MOC per topic cluster.** `+ Attention and Focus.md` covers attention, deep work, flow, focus, distraction. Don't make `+ Attention.md` and `+ Focus.md` if the notes overlap heavily.
4. **MOCs go in their own folder** (`MOCs/`, `+ MOCs/`, or `mocs/`). The dedicated folder is the recommended pattern; mixing with atomic notes in the same folder works only if the marker prefix is rigid.
5. **A home MOC at vault root.** `+ Home.md` or `INDEX.md` lives at the vault root and links to every domain MOC. This is the entry point.
6. **No date or ID prefix on MOCs.** A MOC is identified by its topic, not by when it was written.
7. **Refinement marks aren't in the filename.** Don't append `-v2` or `-2026-04`. The MOC's refinement lives in its content history.

## Anti-patterns

- **MOC as flat index.** A MOC that's just `- [[note1]]` `- [[note2]]` `- [[note3]]` for 200 notes is a tag — useful for completeness, useless for orientation. Group into sections.
- **No MOCs.** A vault of >200 notes with no MOCs is a maze. Search works but no map.
- **Sub-MOCs of sub-MOCs.** A four-level MOC hierarchy is a folder tree pretending to be a graph. Flatten.
- **Inconsistent naming.** Mixing `+ Topic.md`, `MOC-Topic.md`, and `topic_index.md` defeats the visual marker.
- **MOCs that are never updated.** A MOC written once and abandoned diverges from the actual notes. Touch each MOC at least quarterly.
- **MOCs in random folders.** A MOC in `notes/health/` plus another in `notes/career/` plus a third at vault root is hard to discover. Centralise in `MOCs/` or use the marker rigorously.
- **Auto-generated MOCs that replace human-written ones.** Dataview can generate flat lists, but a generated list isn't a MOC — the human curation is the value.

## Variants

- **dedicated-folder (this guide).** `MOCs/` parallel to `notes/`. Cleanest separation; recommended.
- **inline-MOCs.** MOCs live in the same folder as atomic notes, distinguished only by the prefix. Simpler if the marker discipline is rigid.
- **home-MOC-only.** A single `+ Home.md` at vault root linking to atomic notes directly, no domain MOCs. Works for small vaults; doesn't scale past ~50 notes.
- **MOC-per-folder.** Each top-level folder has its own MOC at the folder root (`notes/health/+ Health.md`). Marries folder structure and MOC structure; works in PARA-style vaults.
- **dataview-augmented.** A human-written MOC plus a Dataview query at the bottom that lists "all notes tagged X" or "all notes recently edited in topic Y". Combines curation with auto-completeness.
- **publish-ready MOCs.** Some MOCs are explicitly written to be the front door for external readers — formatted as essays with embedded links. Common in digital gardens.

## Real-world projects using this

- **Linking Your Thinking (Nick Milo)** — https://linkingyourthinking.com — the modern MOC concept's origin and ongoing development.
- **The LYT Kit** — Milo's downloadable Obsidian vault — demonstrates dozens of MOCs across spaces, shows the `+ ` prefix in action.
- **Andy Matuschak's evergreen notes** — https://notes.andymatuschak.org — entries titled "Evergreen note titles are like APIs" and "Evergreen notes" function as MOCs for their topic clusters.
- **Bob Doto's writing** — https://writing.bobdoto.computer — critical perspective on MOCs vs Folgezettel; useful contrast.
- **Maggie Appleton's digital garden** — https://maggieappleton.com — MOCs (called "patches" or "tendings") are the public-facing navigation surface.
- **Many Obsidian/Logseq YouTubers** — Bryan Jenks, FromSergio, Justin DiRose — publish vaults with extensive MOC structures.
- **GitHub: search for `obsidian MOC vault`** — many public templates demonstrate MOC patterns end-to-end.

## Migration & references

To start using MOCs in an existing vault:

```bash
mkdir -p vault/MOCs
cd vault
# Pick a topic cluster you have many notes about
cat > "MOCs/+ Attention and Focus.md" <<'EOF'
# + Attention and Focus

A map of notes about attention, deep work, distraction, and flow.

## Foundations
- [[attention]]
- [[attention-residue]]

## Practices
- [[deep-work]]
- [[flow-state]]
EOF
```

To add MOCs to an existing flat vault:

1. **List your topic clusters.** Look at your notes; identify 5-15 topics that have ≥5 notes each. These are your candidate MOCs.
2. **Write the home MOC first.** `+ Home.md` at vault root, just listing the candidate domain names. This is the dashboard.
3. **Write one domain MOC.** Pick the topic with the most notes. Write a paragraph orientation, then group existing notes into 3-7 sections.
4. **Resist completeness on first pass.** A MOC doesn't need to list every note in the topic on day one. Add as you write.
5. **Touch each MOC weekly.** During the weekly review, open one MOC and add any new notes that should be linked from it.
6. **Promote MOCs to atomic-note discipline.** Refine the orientation paragraph; tighten the section grouping; consider what the MOC is *not* covering.

Further reading and adjacent guides:

- [`lyt-linking-your-thinking`](../lyt-linking-your-thinking/) — the framework where MOCs are central.
- [`evergreen-notes`](../evergreen-notes/) — atomic notes that MOCs link to.
- [`access-framework`](../access-framework/) — uses `2-categories/` as a MOC layer.
- [`para`](../para/) — folder-first alternative; MOCs can be added on top.
- [`zettelkasten-classic`](../zettelkasten-classic/) — historically used "structure notes" as the MOC predecessor.
- [`indexes-and-mocs`](../../principles/indexes-and-mocs/) — the cross-cutting principle for indexing notes vs files.
- Andy Matuschak, "Evergreen note titles are like APIs" — https://notes.andymatuschak.org/Evergreen_note_titles_are_like_APIs — adjacent thinking on note interfaces.
