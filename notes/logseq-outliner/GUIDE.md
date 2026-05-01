## TL;DR

Logseq is an **outliner-first**, local-first knowledge tool where the unit isn't a *note* but a *block* (a single bullet, often a sentence or fragment). The canonical entry point is the **daily journal**: every day Logseq opens to a fresh `journals/YYYY_MM_DD.md` and you outline whatever's on your mind. **Topical pages emerge** from `[[wikilinks]]` you write in journal blocks — the moment you write `[[deep work]]` in a journal, Logseq creates `pages/deep-work.md`. The structure is therefore minimal-by-design: `journals/`, `pages/`, `assets/`, plus a `logseq/` config dir. Naming gotcha: Logseq uses underscores in journal filenames (`2026_04_30.md`), not the dashes most other systems use. The model fits people who think in bullets, who want block-references over note-references, and who like the Roam-style daily-page workflow but want their data in a local Markdown folder. It fits poorly for people writing long-form prose — outliners constrain paragraphs.

## Principles & why

Three Logseq design choices drive the whole structure.

1. **Block-first.** Every bullet is addressable: every block has a UUID and can be transcluded into other pages with `((block-uuid))`. This pushes the unit of thought down from "note" to "bullet". You can move a single block between pages; you can embed a block from a journal entry into a topical page; the topical page reflects edits to the original block automatically. The structural consequence: page-level granularity matters less than in note-first tools.
2. **Daily-journal as canonical entry.** Logseq opens to today's journal. You're meant to start there, not at a topic page. Topical pages are a *byproduct* of journaling: as you write `[[attention residue]]` in a daily journal block, Logseq creates the page on demand and lists every block linking to it. This inverts the Obsidian/PARA workflow where you'd start by opening or creating a topical note.
3. **Local-first Markdown.** Despite its database feel, Logseq stores everything as plain Markdown (or Org-mode) files in a folder. `journals/` and `pages/` are real Markdown, syncable via git, Dropbox, Syncthing. The database is rebuilt from the files on every open. This means you can do the bulk operation by editing the files directly — but Logseq's outliner-specific bullet format (`- block` indented for hierarchy) must be preserved, or the database won't parse them as outlines.

The minimum viable Logseq graph is just `journals/` + `pages/` + the `logseq/config.edn`. The `assets/` folder appears as soon as you paste an image. The `logseq/bak/` and `logseq/version-files/` directories appear as soon as Logseq runs, holding auto-backups; both should be gitignored.

The naming gotcha: **Logseq uses underscores in journal filenames** (`2026_04_30.md`), not the ISO `2026-04-30.md` everyone else uses. This is because page titles in Logseq are derived from filenames, and the journal *page title* renders as "Apr 30th, 2026" — the underscore is just a sentinel for "this is a journal page". If you rename them with dashes, Logseq treats them as regular pages. This trips up everyone migrating in or out.

## When to use

- **You like outlining as the unit of thought.** Bulleted, indented hierarchy is your default writing mode.
- **You want block-references over note-references.** Quoting a single bullet from elsewhere should be cheap and live-updating.
- **Roam-style workflow.** You read about Roam, found the price-or-cloud-only situation off-putting, and want the same model in a local file system.
- **Daily journal is your front door.** You open the tool to "what's today?" not "what topic do I want to find?"
- **Mixed quick-capture and structured thinking.** Logseq's outliner is fast to capture into and equally fast to refine in place. The daily-page workflow handles both.

## When NOT to use

- **Long-form prose.** Outliners feel constraining for paragraph writing. If your notes are full sentences and paragraphs, Obsidian or plain Markdown is more comfortable.
- **You want full visual flexibility in note layout.** Logseq's outline shape is non-negotiable; you can't have a free-form note structure inside a Logseq page.
- **Heavy mobile-first capture.** Logseq's mobile apps have improved but lag desktop; if you live on mobile, Bear or Obsidian Sync is smoother.
- **Team / shared knowledge bases.** Logseq is fundamentally personal; the database-from-files model doesn't merge well across collaborators.
- **You hate the `2026_04_30.md` filename convention.** This is non-trivial — fighting it (using ISO dashes) breaks the journal feature. If you can't accept underscores, choose Obsidian.

## Tree diagram

```
graph/
├── journals/
│   ├── 2026_04_30.md       ← Logseq uses `_` not `-` here
│   └── 2026_05_01.md
├── pages/
│   ├── deep-work.md        ← created on demand from `[[deep work]]`
│   └── attention.md
├── assets/                 ← attachments — Logseq auto-creates this
├── logseq/
│   └── config.edn          ← Logseq config (EDN, not JSON)
└── .gitignore              ← ignore logseq/bak/ and logseq/version-files/
```

Logseq creates `journals/`, `pages/`, `assets/`, and `logseq/` automatically on first run. Don't create them manually with non-standard names — Logseq looks for these specific directories.

## Naming rules

- **Journal pages**: `journals/YYYY_MM_DD.md` — **underscores**, not dashes. The Logseq date format is configurable, but underscores are the default and the most-supported format. The page title that renders in Logseq is derived (e.g., "Apr 30th, 2026").
- **Topical pages**: `pages/<page-name>.md`. The filename is the page name with characters Logseq sanitizes (spaces become `_`, certain special chars get URL-encoded). Logseq generates the filename from your `[[wikilink]]`; don't fight it.
- **Hierarchical pages**: Logseq supports hierarchical page names with `/` in the title, which becomes `___` in the filename. `[[productivity/deep work]]` → `pages/productivity___deep_work.md`. Use sparingly; it confuses some sync tools.
- **Assets**: `assets/<descriptor>_<timestamp>.<ext>`. Logseq generates these names automatically when you paste an image. Don't rename — Logseq uses the path inside Markdown links and renaming breaks the references.
- **Config**: `logseq/config.edn` (EDN syntax — Clojure data format, not JSON, not YAML).
- **Block UUIDs**: Logseq inserts `id::` properties at block level when a block is referenced elsewhere. Don't strip these — they're load-bearing.

## Anti-patterns

- **Renaming journal files to `2026-04-30.md` (dashes).** Logseq stops treating them as journal pages; the calendar view and daily features break. The format is configurable but if you change it, change the config setting too — don't just rename files.
- **Editing files outside Logseq while Logseq is open.** The internal database can desync. Close Logseq, edit, reopen — Logseq re-parses on open.
- **Committing `logseq/bak/` and `logseq/version-files/`.** Logseq writes auto-backups of every page edit; committing them produces enormous diffs and bloats the repo. Always gitignore.
- **Treating `pages/` as Obsidian-style notes.** A Logseq page is meant to be an outline of bullets, not paragraph prose. If you write paragraph notes inside Logseq pages, you'll fight the outliner constantly.
- **Sync conflicts from cloud sync.** Logseq's database can corrupt if two clients write simultaneously via Dropbox/iCloud. Use Logseq Sync (paid) or git for conflict-aware syncing. Avoid simultaneous-edit clouds.
- **Manual `id::` removal.** Block UUIDs exist because something references them. Removing them breaks transclusions silently.

## Variants

- **Logseq-default-Markdown** (this guide) — the recommended default. Markdown files, EDN config, journal-first.
- **Logseq-Org-mode** — change `:preferred-format` in `config.edn` to `:org`. Files become `.org` instead of `.md`. Better for Emacs users; isolated from the Markdown ecosystem.
- **Logseq-DB version** — the newer SQLite-backed storage Logseq is rolling out (still considered experimental at the time of writing). Single `.db` file replaces the `journals/`/`pages/` Markdown structure. Not recommended yet for git-synced graphs.
- **Logseq + companion Markdown vault** — keep Logseq for journal-driven thinking, Obsidian for long-form / publishing. They can share an `assets/` directory if configured carefully.
- **Public-published graph** — Logseq supports static-site export. The published graph becomes a digital garden; structure stays the same but pages get publish-ready.

## Real-world projects using this

- **Logseq official documentation** (docs.logseq.com) — the source-of-truth for journal format, config.edn, and graph structure.
- **Logseq forum** (discuss.logseq.com) — many graph-structure threads, especially in #share and #help.
- **Logseq GitHub repository** (github.com/logseq/logseq) — open-source codebase; the README and examples define canonical conventions.
- **Public Logseq graphs on GitHub** — search "Logseq graph" or "Logseq notes"; multiple people publish their working graphs as references.
- **logseq-publish examples** — the published-graph showcase on the Logseq site links to working public graphs that demonstrate the structure end-to-end.

## Migration & references

- **From Roam Research**: Logseq has a Roam JSON importer (`Settings → Import → Roam EDN/JSON`). The journal-first model maps directly. Block references generally survive; some plugins / queries don't translate.
- **From Obsidian**: keep your `attachments/` content; Logseq will read Markdown. But: **rename `daily/2026-04-30.md` to `journals/2026_04_30.md`** for journal features to work. Pages mostly map across, but Obsidian's bracket-link `[[...]]` and Logseq's are compatible. Watch for Markdown-formatted notes that aren't bullet outlines — Logseq displays them but you lose block-level features.
- **From plain Markdown folders**: drop them into `pages/` (filenames as-is, with spaces → `_`). They'll appear in Logseq immediately. Don't expect block-references until you re-write content as outlined bullets.
- **References**:
  - docs.logseq.com — official docs.
  - github.com/logseq/logseq — source and issues.
  - Sibling guides: `notes/daily-weekly-notes/` (the journal-first concept generally), `notes/topic-vs-date-organization/` (Logseq is "intentional mix": date-driven journal + topic-driven pages emerging from links), `notes/atomic-notes/` (block-as-atom maps to Logseq's block model).
