## TL;DR

LYT — *Linking Your Thinking* — is Nick Milo's framework for personal knowledge work. It rejects deep folder hierarchies in favour of **Maps of Content (MOCs)** — explicit hub notes that connect related atomic notes. Folders exist (`+ Spaces/`, `Calendar/`, `Notes/`, `Resources/`) but they're coarse buckets; structure is in the links, not the path. Daily entries land in `Calendar/`, atomic notes accumulate in `Notes/`, and MOCs in `+ Spaces/` connect them into navigable areas-of-life. The `+` prefix sorts MOCs to the top of any folder listing and signals "start here". The result is a vault that emerges as you write rather than one you architect upfront — which is the whole point: pre-decided taxonomies trap thinking, link-first taxonomies follow it.

## Principles & why

LYT is built on four interlocking commitments:

1. **MOCs are first-class, not afterthought.** A Map of Content is a note whose body is mostly links to other notes — a self-curated index. Unlike a folder, a MOC can live in many contexts at once, can be cited as itself, and rewards the same atomic-note discipline as anything else. You write MOCs the way you write notes: a few lines of orientation followed by linked entry points. The `+` prefix (`+ Home.md`, `+ Career.md`) makes them sort to the top and signals their hub role.
2. **Folders are coarse, links are fine.** The four canonical folders (`+ Spaces/`, `Calendar/`, `Notes/`, `Resources/`) carry semantic load only at the highest level. Inside `Notes/`, files are mostly flat — the structure is in the MOCs that link to them, not in subfolders. This is the deliberate inverse of PARA, which puts structure in folders.
3. **Calendar is the temporal entry point.** `Calendar/2026-04-30.md` is the day's diary; `Calendar/2026-W18.md` is the week's review. The daily/weekly notes are where capture *starts* — today's thoughts go in today's note, with links out to atomic notes once a thought has earned its own file. See [`daily-weekly-notes`](../daily-weekly-notes/).
4. **Spaces are areas of life, not projects.** `+ Spaces/+ Career.md` is a long-lived MOC about your career — it accumulates over years. Projects are short-lived; they live as notes inside Spaces or in their own MOCs that get archived when complete. The Spaces folder is the seven-or-so areas your life is actually about, mirroring David Allen's "Areas of Focus" without PARA's strict folder semantics.

The wager: structure imposed before content is content-shaped wrong. Structure that emerges from links is shaped by what you actually wrote.

## When to use

- Obsidian-first or Logseq-first workflow. The framework assumes first-class wikilinks, backlinks, and a MOC-friendly editor.
- You want emergent organisation. You don't know in advance what your folders should be — you want them to surface from the notes themselves.
- You journal daily and want the journal to feed long-form output. LYT pairs Calendar with Notes in a way that makes capture-to-evergreen a single fluid path.
- You've tried PARA and found the folder-first approach fights you when notes don't fit a single bucket.
- You're a writer, researcher, knowledge worker, or solo creator whose vault is for thinking out loud — not archiving.
- You're comfortable with the `+` prefix as a visual marker for hubs (sorts to top in alphabetical listings).

## When NOT to use

- File-system-first archival workflows. If your notes are mostly clipped articles, recipes, scanned PDFs — use a folder taxonomy or [`access-framework`](../access-framework/), not LYT.
- You hate emergent structure. If you find unstructured note-piles stressful, PARA's four-bucket discipline will feel safer.
- You don't journal. Calendar is half the framework; if you don't write daily notes, you'll only use half the system.
- You're working in a tool without backlinks. LYT depends on bidirectional linkage; one-way links lose half the value.
- Multi-author or team-shared vaults. MOCs encode personal navigation; consensus MOCs become a coordination tax.
- You want strict separation of project/area/resource/archive. That's [`para`](../para/), not LYT — though [`access-framework`](../access-framework/) splits the difference.

## Tree diagram

```
vault/
├── + Home.md                       ← top-level MOC
├── + Spaces/
│   ├── + Career.md                 ← space MOC
│   └── + Hobbies.md
├── Calendar/
│   ├── 2026-04-30.md
│   └── 2026-W18.md
├── Notes/
│   ├── deep-work.md
│   └── attention.md
└── Resources/
    └── books/
```

`+ Home.md` is the master MOC — opening your vault drops you here. Everything else is one click away through it.

## Naming rules

1. **MOCs use `+ Title.md`.** The leading `+ ` (plus, space) sorts them to the top of any alphabetical listing and visually distinguishes hubs from regular notes. Use Title Case after the plus: `+ Career.md`, not `+ career.md`.
2. **Notes use lowercase-hyphenated.** `deep-work.md`, `attention-residue.md`. Title Case is reserved for MOCs.
3. **Calendar uses ISO dates and ISO weeks.** `Calendar/2026-04-30.md` for daily, `Calendar/2026-W18.md` for weekly. No `April-30-2026.md` — sort order matters.
4. **Folders are top-level only.** `Notes/` is flat — don't create `Notes/career/deep-work.md`. If you find yourself wanting that, write a `+ Career.md` MOC instead and link from there.
5. **Resources can have light substructure.** `Resources/books/`, `Resources/courses/` is acceptable when items have intrinsic categories. The MOC discipline still applies — `+ Books to read.md` lives in `+ Spaces/` or as a MOC alongside.
6. **One MOC per Space.** `+ Spaces/+ Career.md`, `+ Spaces/+ Health.md`, `+ Spaces/+ Hobbies.md` — about 5-10 spaces total. More than 12 means you're confusing projects with spaces.
7. **Home MOC is canonical entry.** `+ Home.md` lives at vault root and links to every space MOC. Treat it as your dashboard.

## Worked example

A vault of 400 notes has many links but no obvious starting points.

1. Create `+ Home.md` as the entry MOC and a `+ Spaces/` folder for area MOCs (`+ Career.md`, `+ Hobbies.md`).
2. For each cluster of at least 5 related notes, create a MOC that groups them with one-line reasons.
3. Link every MOC from `+ Home.md`, and link each note from at least one MOC.
4. Keep the folders coarse: `Calendar/` for dailies, `Notes/` for ideas, `Resources/` for external material.
5. Find orphans with a search for notes not linked from a MOC and file them at your next review.
6. Let MOCs grow with the topic; when one passes about 50 links, split it into sub-MOCs.

You enter the vault at `+ Home.md` and can reach any topic in two or three clicks.

## Anti-patterns

- **Deep folder hierarchies inside `Notes/`.** Defeats the entire framework. Notes are flat; structure lives in the MOC.
- **No MOCs.** A vault with only atomic notes and no hubs is a maze. The MOC is the navigation; without it, you're relying on search.
- **MOCs that are just dumps.** A MOC should be opinionated — start with a paragraph of orientation, then organise links into 3-7 sections. A flat list of every note in a topic is a tag, not a MOC.
- **Spaces full of projects.** `+ Spaces/+ Q2-2026 Redesign.md` is a project MOC, not a Space. Keep Spaces durable; project MOCs go elsewhere or get archived after completion.
- **Daily notes as kitchen sink.** If every thought lives only in `Calendar/`, nothing graduates to atomic notes and the Notes folder dies. The discipline is to extract claims from daily notes into linked atomic notes.
- **Ignoring the `+` prefix.** Without it, MOCs sort alphabetically among regular notes and lose their hub-marker function. The convention is small but cumulative.
- **Building the perfect MOC before writing notes.** MOCs grow with the vault; pre-architecting an empty MOC produces taxonomy that doesn't match the eventual content.

## Scaling & failure modes

- **MOC decay**: stale hubs mislead; touch the MOC whenever you add related notes.
- **Premature MOCs** with three links add noise; wait for a real cluster.
- **Naming**: the `+` prefix keeps hubs at the top of listings in Obsidian; other tools may sort it differently.
- **Team vaults**: shared MOCs need an owner or become inconsistent.

## Variants

- **LYT-classic (this guide).** Four folders, MOCs in `+ Spaces/`, daily notes in `Calendar/`, flat `Notes/`.
- **LYT-PARA-hybrid.** Use PARA's four buckets (`1-Projects/`, `2-Areas/`, `3-Resources/`, `4-Archive/`) for folder structure, then layer LYT-style MOCs on top. Concrete and emergent — pay both costs.
- **LYT-with-Dataview.** Adds Obsidian's Dataview plugin to auto-generate parts of MOCs from queries (`tasks where ...`, `pages tagged ...`). Reduces hand-curation, increases tool-lock-in.
- **LYT-IMF (Ideaverse / Idea Mass Framework).** Milo's later evolution — adds an `Atlases/` folder for source-derived concept maps. Most useful for researchers.
- **LYT-Lite.** Drop `+ Spaces/` and put MOCs directly in vault root with `+` prefix. Simpler for small vaults; loses the spaces-vs-MOCs distinction.

## Adoption checklist

- [ ] `+ Home.md` links to every space MOC.
- [ ] Every note is reachable from some MOC.
- [ ] MOCs have short reasons next to links, not bare lists.
- [ ] MOCs over about 50 links are split.
- [ ] An orphan check is done periodically.

## Real-world projects using this

- **Linking Your Thinking** — https://linkingyourthinking.com — Nick Milo's official site, courses, and the LYT Kit (a starter Obsidian vault demonstrating the framework).
- **Obsidian community vaults** styled on LYT — search GitHub for "obsidian LYT vault" or "linking your thinking vault" for public examples.
- **Nick Milo's YouTube channel** — long-form videos walking through LYT vaults and MOC techniques on real notes.
- **The LYT Kit** — Milo's downloadable starter vault, available via the LYT website; demonstrates the `+ Spaces/`, `+ Home.md`, and MOC patterns end-to-end.
- **Ideaverse** — Milo's commercial IMF vault, the LYT successor product; same DNA, more layers (Atlases, Cards).
- **Many Obsidian YouTubers** (Bryan Jenks, Justin DiRose, FromSergio) have published LYT-derived vaults and walkthroughs.

## Migration & references

To start an LYT vault from scratch:

```bash
mkdir -p vault/{+\ Spaces,Calendar,Notes,Resources}
cd vault
cat > "+ Home.md" <<'EOF'
# + Home

Top-level MOC. Spaces:

- [[+ Career]]
- [[+ Hobbies]]
EOF
cat > "+ Spaces/+ Career.md" <<'EOF'
# + Career

Space MOC. Add links here as career-related notes accumulate.
EOF
```

To migrate from a folder-heavy vault:

1. **Don't move files yet.** First, audit your folders. Each one becomes a candidate MOC. List them.
2. **Create the four canonical folders** (`+ Spaces/`, `Calendar/`, `Notes/`, `Resources/`) alongside the existing structure. Don't delete anything yet.
3. **For each old folder, write a MOC.** `health/` becomes `+ Spaces/+ Health.md` with links to the actual notes. Then move the notes into `Notes/` (flat) and update the MOC links.
4. **Move daily notes into `Calendar/`.** Rename to `YYYY-MM-DD.md` if they aren't already.
5. **Drop the `+ ` prefix on Spaces only.** Inside `Notes/`, files stay lowercase-hyphenated.
6. **Build `+ Home.md` last.** Once your spaces exist, link them from the home MOC.

Further reading and adjacent guides:

- Nick Milo's *Linking Your Thinking* course — https://linkingyourthinking.com — the canonical resource.
- [`maps-of-content`](../maps-of-content/) — deeper treatment of MOCs as a primitive.
- [`evergreen-notes`](../evergreen-notes/) — Andy Matuschak's parallel discipline; LYT cites and incorporates evergreen ideas.
- [`para`](../para/) — folder-first alternative; pairs well via the LYT-PARA-hybrid variant.
- [`access-framework`](../access-framework/) — six-bucket alternative when LYT feels too loose.
- [`daily-weekly-notes`](../daily-weekly-notes/) — the temporal layer LYT's `Calendar/` implements.
- [`zettelkasten-classic`](../zettelkasten-classic/) — the historical predecessor of evergreen-notes-flavoured frameworks like LYT.
