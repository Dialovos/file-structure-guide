## TL;DR

**CODE** is Tiago Forte's four-stage workflow for personal knowledge management: **Capture / Organize / Distill / Express**. It's the *verb* layer — what you do — paired most often with **PARA** as the *noun* layer (where stuff lives). CODE flows information from input (Capture: highlights, clippings, voice memos) through storage (Organize: into Projects / Areas / Resources / Archive) through synthesis (Distill: progressive summarization into "intermediate packets") and out into deliverables (Express: drafts, posts, talks). The pipeline is the point: a Second Brain that only Captures becomes a junk drawer; one that only Expresses runs out of material; CODE forces the middle steps. This guide shows the workflow as a vault layout: a `0-inbox/` for capture, the four PARA folders for organization, plus `distilled/` for the Distill output and `output/` for Express deliverables. PARA is one supported organizer (others: LYT, ACCESS, plain folders).

## Principles & why

The four CODE stages each address a different failure mode of knowledge work.

1. **Capture** answers "stop forgetting what you read." The principle is *capture cheaply, anywhere, with no organizing decision*. Your captured items land in a single inbox (`0-inbox/`); no tagging, no folder choice. Friction kills capture; defer the organizing decision to the next stage.
2. **Organize** answers "where does this go so I can find it when I need it?" PARA is Forte's recommended scheme: **Projects** (active, with deadlines), **Areas** (ongoing responsibilities), **Resources** (topical libraries), **Archive** (everything else). The genius of PARA is that the organizing question becomes "is this *actionable* right now?" rather than "what topic is this?" — actionability is more decidable than topic.
3. **Distill** answers "raw notes don't compose into outputs." Forte's technique is *progressive summarization*: bold the important sentences on first re-read, highlight a subset on second re-read, and write a few-line executive summary on third re-read. The result is an "intermediate packet" — a self-contained, reusable distillation. Skip Distill and your notes never become input to writing.
4. **Express** answers "the goal of a Second Brain is shipping, not collecting." Express is where intermediate packets get composed into deliverables: blog posts, presentations, course modules, client memos. If your vault has no Express output for six months, your Second Brain has become a graveyard.

The crucial framing in *Building a Second Brain*: **CODE is the verbs; PARA is the nouns.** You can pair CODE with non-PARA organizers (LYT's MOCs, ACCESS, even plain folders). What's non-negotiable is the four-stage flow.

The order is not strict — Distill and Organize loop. Capture is always first; Express is always last; the middle two oscillate.

## When to use

- **Knowledge-worker pipeline** with a production goal: writers, course creators, consultants, podcasters, researchers. CODE shines when you have audiences.
- **Newsletter / content cadence** — CODE is essentially a content engine. The Express stage maps directly to "what am I publishing this week?"
- **Mixed-media capture** — articles, podcasts, books, voice memos, meeting notes all funnel through `0-inbox/`. CODE doesn't care about source.
- **People who Capture-too-much** — the structural pressure of Distill and Express is the cure for hoarding.
- **Teams adopting personal-PKM patterns** — CODE generalizes well to team knowledge bases (each role has Captures, the team has shared Distills, and Express maps to deliverables).

## When NOT to use

- **No production goal.** If you don't write, ship, teach, or otherwise express, the back half of CODE has no purpose. Capture-only systems (commonplace book, BuJo) are fine for many people; don't over-process.
- **Pure long-form research** — academics writing one paper over months don't need the Distill machinery; their drafts ARE the Distill. Use a citation manager + outline tool instead.
- **Daily-journal-only** workflows — CODE assumes durable knowledge accumulating across years. A pure journal is a different shape.
- **Allergic to folder structure.** CODE pairs naturally with PARA, which is folder-based. If you reject folders entirely (Roam-style graph-only), CODE-with-LYT or CODE-only-by-stage variants exist but are harder.
- **Highly collaborative teams.** PARA is personal; "my Projects" don't fit a team vault. Adapt with care.

## Tree diagram

```
vault/
├── 0-inbox/                ← Capture (no organizing decision yet)
├── 1-projects/             ← Organize: PARA — active with deadlines
├── 2-areas/                ← Organize: PARA — ongoing responsibilities
├── 3-resources/            ← Organize: PARA — topical libraries
├── 4-archive/              ← Organize: PARA — inactive
├── distilled/              ← Distill output (intermediate packets)
└── output/                 ← Express (drafts, posts, exports, talks)
```

The numbered prefixes (`0-` through `4-`) are a usability trick — they keep the inbox + PARA folders sorted at the top of every file picker. `distilled/` and `output/` sit alongside without numeric prefixes, signaling they're workflow stages rather than storage.

## Naming rules

- **`0-inbox/`** — captured items. Filenames as captured: source-domain-slug, kebab-case, date-prefix optional. Examples: `nyt-attention-economy.md`, `2026-04-30-podcast-cal-newport.md`.
- **`1-projects/<project-name>/`** — one folder per active project. Project name in kebab-case, prefixed with deadline if useful: `2026-q2-vault-redesign/`. Inside: working notes, Distilled summaries scoped to the project, references.
- **`2-areas/<area-name>/`** — one folder per ongoing area: `health/`, `finance/`, `team-lead/`. Areas have no deadlines.
- **`3-resources/<topic>/`** — topical libraries: `attention/`, `pkm/`, `system-design/`. Stuff you're interested in but not actively working on.
- **`4-archive/<original-path>/`** — when a project finishes or an area becomes inactive, *move* (don't copy) it here. Preserve the original path inside `4-archive/` so retrieval is obvious.
- **`distilled/<topic-or-source>.md`** — intermediate packets. One file per source (`distilled/deep-work-newport.md`) or one per synthesis topic (`distilled/attention-residue-synthesis.md`).
- **`output/<deliverable>.md`** — drafts and final pieces. Filename matches the publication: `output/blog-attention-tax-2026-05.md`. Once published, archive a copy with the publication date.
- **Markdown only at root of each PARA folder.** Sub-folders allowed *inside* a project/area/resource. Don't nest PARA folders inside each other.

## Anti-patterns

- **Skipping Distill.** Capturing and Organizing without ever Distilling means your `1-projects/` folders fill with raw clippings that never compose into drafts. The Distill stage is the most-skipped and the most valuable.
- **Forever-projects.** A project with no deadline is an Area. If `1-projects/learn-rust/` is still there after 18 months with no end in sight, it's mis-classified — move to `2-areas/skill-development/` or finish it.
- **Inbox-as-everything.** Letting `0-inbox/` accumulate hundreds of items "for later" defeats the system. Process the inbox weekly: each item moves to PARA, distilled/, or trash.
- **Resources mistaken for Areas.** `2-areas/javascript/` is wrong — JavaScript is a resource (a topic library), not a responsibility. Areas are roles or commitments (`2-areas/parenting/`, `2-areas/team-lead/`).
- **Outputs left in `1-projects/`.** When a project finishes and ships an output, move both: the project folder to `4-archive/`, and the output file to `output/`. Don't leave deliverables stranded inside the project folder.
- **Distilling without later re-reading.** Progressive summarization is for *future re-reading*. If you never re-open `distilled/`, the bolding was busywork.

## Variants

- **CODE + PARA** (this guide) — the canonical Forte pairing. Recommended default.
- **CODE + LYT** — replace PARA with Linking Your Thinking's Maps of Content + Calendar + Notes. Less folder-driven; more graph-driven. Same four stages, different storage.
- **CODE + ACCESS** — Nick Milo's ACCESS framework as the storage layer. Resource-flavored; works well for academics.
- **CODE-only (no PARA)** — folders by stage only: `0-inbox/`, `distilled/`, `output/`. Skip the PARA layer entirely. Simplest; loses PARA's actionability heuristic.
- **CODE-Lite** — drop Distill as an explicit stage; do progressive summarization inline in your notes instead of producing separate intermediate packets. Lower overhead; less reusable output.

## Real-world projects using this

- **Tiago Forte, *Building a Second Brain*** (Atria, 2022) — the book; the canonical CODE source.
- **Forte Labs course "Building a Second Brain"** (fortelabs.com) — paid course; Forte's blog has many free articles introducing CODE and PARA.
- **Forte Labs YouTube channel** — videos walking through CODE in Notion, Evernote, Obsidian.
- **Public BASB/PARA vaults on GitHub** — search "BASB Obsidian" or "PARA template Obsidian"; multiple open-source vaults exist.
- **Notion's "Second Brain" templates** in their template gallery (notion.so/templates) — multiple BASB/PARA implementations.

## Migration & references

- **From a single-folder dump**: create `0-inbox/`, `1-projects/`, `2-areas/`, `3-resources/`, `4-archive/`, `distilled/`, `output/`. Move everything to `0-inbox/` first. Then process: each item → PARA folder, deleted, or archived. Don't try to perfect-classify on day one; the inbox-then-process flow is part of the design.
- **From PARA-only (no CODE)**: add `0-inbox/`, `distilled/`, `output/`. Start every new note in `0-inbox/`. Pull intermediate packets from your existing PARA notes into `distilled/` as you re-read them. Express output gets its own folder rather than living inside project folders.
- **From Zettelkasten**: keep the Zettelkasten as your `3-resources/zettelkasten/` library. Wrap it with the rest of CODE: capture goes to `0-inbox/`, projects in `1-projects/`, output in `output/`. Zettel ideas feed Distill; CODE doesn't replace Zettelkasten.
- **References**:
  - Tiago Forte, *Building a Second Brain* (2022) — primary text.
  - fortelabs.com — Forte's blog has the canonical PARA and progressive-summarization posts.
  - Sibling guides: `notes/para/` (the storage layer in detail), `notes/atomic-notes/` (the unit BASB calls "intermediate packets"), `notes/lyt-linking-your-thinking/` (alternate storage for CODE).
  - Anti-pattern reference: `ANTIPATTERNS.md` for "forever projects" and "inbox-as-everything".
