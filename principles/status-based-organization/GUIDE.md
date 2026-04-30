# Status-based organization

## TL;DR

Separate items by **lifecycle status** at the top of the tree — `active/`, `archive/`, optionally `someday/` — rather than by tagging filenames with `_done` or `_old`. The status of an item is a structural concern, not a suffix; the directory it lives in *is* its status.

## Principles & why

A folder of mixed-status items rots fast. Active work and finished work compete for the same eyeball-space, the active list grows visually heavier than it really is, and "is this still in play?" becomes a question you have to answer file-by-file. Filename-based status (`project-foo_DONE.md`, `idea-bar-archived.md`) makes it worse: every glance has to parse the suffix, and a stale suffix lies silently.

Status-based directories solve this by promoting status to a structural fact. `active/` only contains live work, so `ls active/` is your honest backlog. `archive/` is read-only by convention; you stop scanning it. `someday/` is a deliberately fuzzy holding pen so good-but-not-now ideas don't pollute either of the other two.

The deeper principle: **structure should reflect questions you actually ask.** "What am I working on?" is asked daily. "What have I shipped?" is asked monthly. They deserve different rooms, not different filename suffixes in the same room.

## When to use

Use status-based organization whenever items have a clear lifecycle:

- **Project portfolios** — every project is in flight, paused, or done. PARA's four-folder system (Projects/Areas/Resources/Archive) is a popular flavor.
- **Notes and drafts** — a daily-notes vault where today's thinking lives separately from last year's.
- **Spec/design docs** — `active/` for proposals under review, `archive/` for accepted-and-shipped, `someday/` for "we keep meaning to do this".
- **Scripts and tooling** — `active/` for things you'd actually run today, `archive/` for tools tied to dead pipelines.
- **Personal task lists** — GTD's "active projects" vs "someday/maybe" is the same idea.

The signal you need this: you find yourself wondering whether to delete or rename items just to clean visual noise. That's the moment a top-level `archive/` saves you.

## When NOT to use

Skip status partitioning when the content has only one status:

- **Immutable reference docs** — RFCs, standards, published papers. They don't have a lifecycle; date- or topic-based organization fits better.
- **Photos / media** — a photo isn't "active" or "archived" in any meaningful sense; date-based archive (`2026/04/`) is the natural axis.
- **Build artifacts** — handled by `dist/` vs source, not active/archive. See `principles/generated-vs-source-separation/`.
- **Highly transactional data** — logs, metrics, events. Time-series tooling already gives you the lifecycle view; folders are the wrong abstraction.
- **Tiny repos** — a five-project folder doesn't need three subdirs. Wait until the active list is hard to scan.

The fail-safe heuristic: if you've never wanted to "move this aside but not delete it", you don't need an `archive/` yet.

## Tree diagram

```
projects/
├── active/
│   ├── q2-redesign/
│   └── auth-rewrite/
├── archive/
│   ├── 2025/
│   │   └── q4-billing-revamp/
│   └── 2024/
│       └── q3-migration/
└── someday/
    └── grand-rewrite-idea/
```

## Naming rules

1. Status directories are lowercase, plural-or-singular by team taste but consistent: `active/`, `archive/`, `someday/`. Pick one form and don't mix `archive/` with `archived/`.
2. Inside `archive/`, group by year: `archive/2025/`, `archive/2024/`. A flat `archive/` becomes a drowning ground after a year or two.
3. Items themselves keep their original name when they move — don't append `_archived` to the directory you're moving. The path already encodes status.
4. `someday/` is for *ideas you'd commit to if priorities changed*. Not for "things I'll never do" — those get deleted.
5. The active set should fit on one screen of `ls`. If `active/` has 30 items, half of them are probably stale and belong in `archive/` or `someday/`.
6. Don't create deeper status splits (`active/in-progress/`, `active/blocked/`) unless your team is using the file system as a Kanban — most teams should not.

## Anti-patterns

- **`archive/` as a filename suffix** — `q4-billing-revamp_archive/` next to `auth-rewrite/` in one folder. Defeats the entire principle: the `ls` view is still mixed.
- **No archive at all, ever** — every project sits at the top level forever. After a year you can't find live work.
- **`old/` instead of `archive/`** — "old" is a vague vibe word. `archive/2025/` tells you when something stopped being active.
- **Multiple competing status conventions** — `archive/` *and* a `done/` *and* filename `_OLD` suffixes in the same repo. Pick one.
- **Stale items in `active/`** — the directory exists to be honest about live work. If a project hasn't moved in 90 days, it's not active; move it.
- **`someday/` as graveyard** — when `someday/` becomes a write-only pile of bad ideas, prune it. The whole point is that you'd genuinely revisit these.
- **Year-stamped names *inside* `archive/`** — `archive/q4-billing-revamp_2025/` plus the year directory is double-encoding. Pick the structural one.

## Variants

- **active-archive-only** (minimal) — just `active/` and `archive/`. Simplest; works for solo projects without the "maybe later" pile.
- **active-archive-someday** (PARA-flavored) — adds `someday/` for parked ideas. Best for personal portfolios and note vaults.
- **active-archive-someday-onhold** (richer lifecycle) — adds `on-hold/` for items paused on external blockers. Common in product/engineering teams.
- **PARA full** (Tiago Forte) — `Projects/`, `Areas/`, `Resources/`, `Archive/`. Status is implicit (Projects = active) plus orthogonal categorization.
- **GTD-style** — `next-actions/`, `waiting/`, `someday-maybe/`, `reference/`. Specifically tuned for task management rather than project work.
- **Time-decayed archive** — `archive/recent/` plus `archive/cold-storage/` for very old items. Useful when you want a fast-glance recent archive without scanning every year.

## Real-world projects using this

- **Tiago Forte's PARA method** — Projects / Areas / Resources / Archive. The de facto standard for personal knowledge management.
- **GTD (Getting Things Done) by David Allen** — "next actions" vs "someday/maybe" lists is the canonical lifecycle separation in productivity literature.
- **Apache Attic** (https://attic.apache.org) — explicit "archive of retired projects" subdomain at the foundation level. Same principle, ASF scale.
- **kernel.org's `linux-stable` vs `linux-next`** — lifecycle separation by repository: `linux-next` is active integration, `linux-stable` is the released line.
- **Cookiecutter project templates** — many include an `archive/` subdir for retired template versions while `templates/` holds the live ones.
- **Obsidian community vaults** — most published vaults use an `Archive/` folder following PARA conventions for daily notes that aged out.

## Migration & references

To migrate an existing flat-projects folder:

```bash
# 1. Make the structure
mkdir -p projects/{active,archive,someday}

# 2. Move obviously-finished projects into a year bucket
mkdir -p projects/archive/2025
mv projects/q4-billing-revamp projects/archive/2025/

# 3. Sweep stale items into someday/ rather than deleting
mv projects/grand-rewrite-idea projects/someday/
```

Audit script — find projects in `active/` that haven't been touched in 90 days:

```bash
find projects/active -maxdepth 1 -mindepth 1 -type d -mtime +90 \
  -printf '%TY-%Tm-%Td  %p\n'
```

Triage by hand — old mtime alone isn't proof of inactivity, but it's a good prompt.

Further reading:

- Tiago Forte, *Building a Second Brain* — PARA method and the rationale for status-based separation.
- David Allen, *Getting Things Done* — the original "active projects" vs "someday/maybe" lifecycle.
- `principles/iso-date-formats/` — pairs with this rule because `archive/2025/` benefits from ISO subdirs.
- `principles/one-purpose-per-directory/` — `active/`, `archive/`, `someday/` each have one purpose; this is that principle in the small.
- `principles/stable-vs-volatile-separation/` — adjacent idea: separate things that change daily from things that change yearly.
