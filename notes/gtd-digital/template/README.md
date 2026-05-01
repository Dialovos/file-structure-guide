# GTD in flat markdown — template

A working skeleton of David Allen's **Getting Things Done** in plain
markdown: the four canonical lists at the root, per-project files in
`projects/`, and a `reference/` filing area. See `../GUIDE.md` for
the full reasoning.

## Layout

```
gtd/
├── inbox.md                 ← capture surface; gets cleared, never grows
├── next-actions.md          ← single physical next action per project, by context
├── waiting-for.md           ← items you're waiting on others for
├── someday-maybe.md         ← parking lot for "not now, maybe later"
├── projects/                ← one file per active project
│   └── example-project.md   ← shows the outcome + next-action structure
└── reference/               ← non-actionable filed material
```

## The minimum daily ritual

1. Anything new goes into `inbox.md`. No thinking.
2. At least once a day, **clear** `inbox.md`. Each item:
   - Trash, or
   - Do in two minutes (then delete from inbox), or
   - Promote to `next-actions.md` with a `@context`, or
   - Promote to a new project file in `projects/`, or
   - File in `reference/`, or
   - Defer to `someday-maybe.md` or `waiting-for.md`.

## The minimum weekly review

Every week (Friday afternoon or Sunday evening are common):

1. Re-read every project file in `projects/`. Confirm each has a
   currently-stated **next action** that's mirrored in
   `next-actions.md`. Close completed projects.
2. Walk through `waiting-for.md`. Nudge anyone who's gone silent.
3. Skim `someday-maybe.md`. Promote anything ripe.
4. Empty `inbox.md` to zero.
5. Glance at the calendar two weeks ahead.

The weekly review is the load-bearing practice. Without it, the
files become a stale list and the system fails. Defend the time.

## Why one file per project

Each project file is the *full* task list for that project, plus the
project's outcome and current next action. The four root list files
(`next-actions.md` etc.) only show the *single current* next action
for each project — they're the at-a-glance scan surface. The project
file is the deep view.

This split avoids a common GTD failure: trying to manage all project
internals from a single big task list. Keep the breadth in
`next-actions.md`, the depth in `projects/<name>.md`.

## Contexts inside `next-actions.md`

The `next-actions.md` file groups by `@context` heading:

- `@home` — actions doable when you're at home
- `@office` — when you're at your work location
- `@calls` — anything that's a phone call
- `@errands` — when you're out, at a store, etc.
- `@computer` — at a laptop / desktop
- `@anywhere` — mobile-doable anything

Add or rename contexts based on your life. The key is having a small
fixed set so you can scan to "what can I do *right now, here*?"

## What this template includes

- **`inbox.md`** — sample with a few captured items showing the
  pre-triage shape.
- **`next-actions.md`** — fully populated with `@context` headings
  and sample actions in each.
- **`waiting-for.md`** — sample showing the date — who — what format
  with a resolved-this-week section.
- **`someday-maybe.md`** — sample with a few possible projects,
  purchases, and learning items.
- **`projects/example-project.md`** — sample project file showing
  outcome, next action, full task list, reference links, decisions.
- **`reference/.gitkeep`** — placeholder; this is your reference
  filing area.

## Pair this with

- `../../para/` — if your reference material is substantial, replace
  `reference/` with PARA's full reference layer.
- `../../daily-weekly-notes/` — the natural home for the weekly-review
  ritual.
- `../../bullet-journal-digital/` — many GTDers also keep a bullet
  journal for daily logging; the two compose well.

## When NOT to use this template

If you already use Things, OmniFocus, or Todoist and like it — don't
double-track. The app *is* your system. Use flat markdown only for
project-outcome docs and weekly-review notes. Trying to mirror your
app inventory into markdown is a recipe for staleness in both.
