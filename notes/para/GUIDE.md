## TL;DR

PARA is Tiago Forte's four-bucket sorting system for any digital workspace: every note, file, or task lives in exactly one of `1-projects/`, `2-areas/`, `3-resources/`, or `4-archive/`. Projects are short-term efforts with a finish line; areas are ongoing standards you maintain (health, finance, a relationship); resources are reference material you might consult later; archive is the morgue for finished projects and retired areas. The numeric prefix is load-bearing — it forces alphabetical sort to render in priority order so the most actionable bucket is always on top, and it also makes PARA portable to file managers that don't honour custom sort. Originally designed for note tools (Evernote, Notion, Obsidian) but works equally well in the macOS Finder, Dropbox, or `~/Documents`.

## Principles & why

PARA exists because most personal-knowledge systems collapse into either a flat dump or a deep, topical taxonomy. Both fail. A flat dump can't separate "the lease I'm signing this week" from "an article I might read someday". A topical taxonomy ("Finance / Taxes / 2024 / Schedule-C") looks tidy but forces every capture to make a tiny ontological commitment up front, which kills capture velocity. PARA replaces the topical question ("where does this belong?") with an *actionability* question: is this driving an active outcome, supporting an ongoing standard, just-in-case reference, or done?

Three principles keep the system honest:

1. **Actionability gradient.** The four buckets descend from highest actionability (Projects) to lowest (Archive). Numbering preserves this order at file-system level.
2. **One home per item.** A note belongs to exactly one bucket at a time. Move it as its role changes (resource → project when you start using it; project → archive when you finish).
3. **Cross-tool consistency.** The same four directory names appear in your note app, your cloud drive, and your local `~/Documents`. Muscle memory transfers; the search command "look in projects" works everywhere.

The numeric prefix isn't decorative. Tools sort lexicographically by default. Without `1-`, `2-`, `3-`, `4-`, you'd see Archive first (alphabetical "A" wins), then Areas, Projects, Resources — exactly inverted from how you should think about your work.

## When to use

- General-purpose knowledge work where the same workspace mixes active deliverables, ongoing responsibilities, and reference material.
- Solo creators, knowledge workers, students, freelancers — anyone with more than one role and more than a year of accumulated notes.
- Tools with no built-in organization (Obsidian, plain folders, Bear, Apple Notes, Notion at the workspace level, even Google Drive).
- Migrating from a flat or topical scheme that has stopped scaling. PARA's small fixed top level is much easier to onboard than another nested taxonomy.
- Households or small teams who want a shared vocabulary across personal and shared drives.
- People who already use GTD for tasks and want a parallel structure for the *artefacts* those tasks produce.

## When NOT to use

- Pure reference systems where everything is already evergreen and there are no projects (a research bibliography, a recipe collection). Use [`zettelkasten-classic`](../zettelkasten-classic/) or [`access-framework`](../access-framework/) instead.
- Date-driven journaling where the canonical entry is "today" — see [`daily-weekly-notes`](../daily-weekly-notes/) or [`bullet-journal-digital`](../bullet-journal-digital/).
- Heavy filers who need stronger filing constraints than four buckets — Johnny Decimal will give you ID-based discipline that PARA deliberately avoids.
- Single-project knowledge bases (a thesis, a book) where the whole vault is one project; PARA's "projects" plural becomes ceremony.
- Public digital gardens where the audience expects topic-based navigation, not your private actionability state.
- Codebases. PARA is for notes and documents, not source. Source repos have their own conventions ([`code/`](../../code/)).

## Tree diagram

```
vault/
├── 1-projects/
│   ├── q2-redesign/
│   └── learn-rust/
├── 2-areas/
│   ├── health/
│   ├── finance/
│   └── home/
├── 3-resources/
│   ├── design-references/
│   └── papers-on-attention/
└── 4-archive/
    ├── 2025/
    └── 2024/
```

## Naming rules

1. Top-level directories are exactly `1-projects/`, `2-areas/`, `3-resources/`, `4-archive/` (lowercase, hyphenated, numeric prefix). Don't pluralise differently or skip the number.
2. Inside `1-projects/`, each project gets its own folder named after the outcome: `q2-redesign/`, `learn-rust/`, `apartment-move/`. Aim for verb-implied or deliverable-implied names; avoid generic ones like `work/`.
3. Inside `2-areas/`, each area is a noun: `health/`, `finance/`, `home/`, `career/`. Areas have no end date; if a folder ever feels "done", it belongs in archive.
4. `3-resources/` is topical — `design-references/`, `papers-on-attention/`, `cooking-techniques/`. These names look most like a traditional taxonomy because that's their job.
5. `4-archive/` is sub-organised by year of retirement (`4-archive/2024/`, `4-archive/2025/`) or by source bucket (`4-archive/projects/`, `4-archive/areas/`). Pick one and be consistent.
6. Per-note filenames follow the conventions of whatever tool you use (Obsidian wikilinks, Bear titles, Apple Notes — irrelevant to PARA).
7. Don't nest a fifth bucket. If you find yourself wanting `5-someday/`, that's an inbox; either fold it into `1-projects/someday/` or use [`gtd-digital`](../gtd-digital/) where a "someday" list is canonical.

## Worked example

A `Documents/` folder is organized by file type and projects get lost in it.

1. Create `1-projects/`, `2-areas/`, `3-resources/`, `4-archive/`.
2. List everything with a finish line and a deadline as a project: `1-projects/q2-redesign/`. Limit yourself to what you're actually working on.
3. Move ongoing responsibilities without an end date into areas: `2-areas/health/`, `2-areas/finance/`.
4. Move reference material to `3-resources/`, by topic.
5. Move finished or dormant items to `4-archive/2025/`.
6. Test each project against the question: what does "done" look like? If you can't say, it's an area.
7. Review weekly: finished projects go to the archive, new commitments get folders.

You can list active work with `ls 1-projects` and everything else stays out of the way.

## Anti-patterns

- **Topical sub-buckets inside Projects.** Putting `1-projects/work/` and `1-projects/personal/` undoes PARA's flatness. The whole point is that every project is one click from the root. Use tags or a status emoji on the folder name if you need a split.
- **Letting Areas accumulate dead folders.** Areas have no end date but they do retire — when you stop renting that apartment, `2-areas/apartment/` moves to `4-archive/`. Keeping it in Areas dilutes the signal that Areas are *current standards*.
- **Re-creating a deep taxonomy inside Resources.** It's tempting because Resources looks taxonomic. Resist; one or two levels of folder is plenty. If a Resource folder grows beyond ~30 items, split by *use case* (not finer topic) or convert it to a project.
- **Confusing Projects and Areas.** "Stay healthy" is an area. "Run a half marathon" is a project. The discriminator is *finish line*: a project ends, an area is permanently maintained.
- **Putting the inbox at the root.** PARA has only four siblings. If you need a capture inbox, use the [`PARA-with-inbox`](../para/) variant with an explicit `0-inbox/` rather than dumping into `1-projects/inbox/`.
- **Renumbering on whim.** Once you've used `1-`, `2-`, `3-`, `4-` for a year, your shell aliases, search filters, and muscle memory all assume them. Renaming costs more than the aesthetic upgrade is worth.

## Scaling & failure modes

- **Project vs area confusion** is the classic failure; apply the "finish line" test, and move things when they change type.
- **Resources as junk drawer**: without a topic name and an occasional prune, resources becomes the new Downloads.
- **Deep nesting**: keep each bucket's tree to one or two levels and use search for the rest.
- **Cross-tool consistency**: the same four buckets across notes, files, and email reduce lookup cost; sync the structure, not the content.

## Variants

- **classic-PARA (this guide).** Four numbered buckets. Works in any tool with no extra moving parts.
- **PARA-with-inbox.** Add a leading `0-inbox/` for capture; a weekly review processes inbox items into the four real buckets. Useful for capture-heavy workflows.
- **PARA-without-numbers.** Drop the numeric prefix when your tool sorts in a custom order anyway (e.g. Obsidian sidebar with manual ordering, Notion's drag-sortable workspace). You lose portability across tools but gain cleaner names.
- **PARA-by-year.** Sub-organise `4-archive/` by year (`2024/`, `2025/`) rather than mirroring source buckets. Most popular variant; lets you say "show me everything I shipped in 2024".
- **PARA-with-MOC.** Add a top-level `0-INDEX.md` (Map of Content) that links into the four buckets. Bridges PARA with [`maps-of-content`](../maps-of-content/) practice.
- **shared-PARA.** A household or team uses the same four buckets at the root of a shared drive. Personal PARA vaults sit beneath, and the four-bucket vocabulary is shared across team and individual.

## Adoption checklist

- [ ] Every project has a definition of done.
- [ ] `1-projects/` contains only active work with an end.
- [ ] Finished projects move to `4-archive/<year>/` at review time.
- [ ] Resources have topic names, not "misc".
- [ ] A weekly review updates the buckets.

## Real-world projects using this

- Tiago Forte's *Building a Second Brain* (the canonical book) and the Forte Labs blog at https://fortelabs.com/blog/para/.
- Many public Obsidian vaults on GitHub structured around PARA — search GitHub for "PARA vault" or "PARA Obsidian" for living examples.
- Joel Hooks' note-system writeups (https://joelhooks.com) which discuss PARA adoption and adaptations in practice.
- The Notion template gallery includes several official and community PARA templates.
- The Building a Second Brain alumni community publishes annual PARA review walkthroughs and case studies.

## Migration & references

To start a PARA vault from scratch:

```bash
mkdir -p vault/{1-projects,2-areas,3-resources,4-archive}
cd vault
echo "PARA vault — see notes/para/GUIDE.md" > INDEX.md
```

To migrate from a flat or topical vault:

1. **Don't reorganise everything at once.** Make the four buckets at the root and an `_unsorted/` sibling. Move only the files you touch this week into the right bucket; leave the rest in `_unsorted/` until they're touched naturally.
2. **Inventory your current top-level folders.** For each, ask: is this driving an outcome (→ Projects), an ongoing standard (→ Areas), reference (→ Resources), or done (→ Archive)?
3. **Move active projects first.** They're the smallest set and the most important to find quickly.
4. **Prune Resources hard.** Most flat vaults have huge "ideas" or "articles" folders that are 80% unused. Resist the urge to migrate everything — Archive what hasn't been touched in a year.
5. **Set up a weekly review.** PARA stays useful only if you periodically promote (Resource → Project), retire (Project → Archive), and check that Areas still have current standards. A 15-minute weekly review is the minimum.

Further reading and adjacent guides:

- *Building a Second Brain* — Tiago Forte (2022). Origin source for PARA.
- https://fortelabs.com/blog/para/ — the canonical online write-up.
- [`gtd-digital`](../gtd-digital/) — task-side counterpart; PARA holds the artefacts, GTD holds the actions.
- [`second-brain-code`](../second-brain-code/) — the CODE method (Capture / Organize / Distill / Express) layered atop PARA.
- [`zettelkasten-classic`](../zettelkasten-classic/) — alternative for pure-reference workspaces where Projects/Areas don't apply.
- [`maps-of-content`](../maps-of-content/) — composes well with PARA when you want navigable indexes per bucket.
