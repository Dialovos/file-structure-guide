## TL;DR

This is **Getting Things Done** (David Allen's productivity methodology) implemented in flat markdown files, no app. The four canonical lists each become a single file: `inbox.md`, `next-actions.md`, `waiting-for.md`, `someday-maybe.md`. Each open project gets its own file in `projects/` with the project's *outcome* and *next physical action* explicit at the top. Reference material — anything not actionable but worth keeping — lives in `reference/`. Inside `next-actions.md`, items group by **context** (`@home`, `@office`, `@calls`, `@errands`, `@computer`) so when you're at a particular context you can scan only what's actionable there. The directory shape mirrors GTD's own architecture: capture → process → organize → review → engage. The structure stays minimal; the *practice* (weekly review, two-minute rule, well-defined next actions) carries the weight. This pairs naturally with daily/weekly notes for review cadence and with PARA if you want a richer reference layer. It is *not* a substitute for the full GTD system if your projects are heavy and shared with others — a real GTD app (Things, OmniFocus, Todoist) buys you mobile capture, recurring tasks, and review-friendly UI that flat markdown approximates only with effort.

## Principles & why

GTD as a methodology has five steps (capture, clarify, organize, reflect, engage) and depends on three structural commitments. The directory shape encodes those.

1. **One trusted system.** GTD's foundational claim is that the mind is bad at remembering and reminding; the value of an external system is taking that burden off so the mind is free to think. The implication for filesystem shape: there must be a small, fixed set of always-present files, and they must cover everything. `inbox.md`, `next-actions.md`, `waiting-for.md`, `someday-maybe.md` plus the `projects/` directory are the canonical answer.
2. **Next action is a physical act.** A "project" in GTD is anything requiring more than one action. The discipline is that for each open project, *the very next physical action* is named explicitly. That's why each project file in `projects/` starts with two sections: outcome (the desired done-state) and next action (the single physical thing you'd do if you sat down right now).
3. **Context defines availability.** Different actions are doable in different physical or logistical contexts: `@home` (when you're at home), `@office`, `@calls` (when you can talk on the phone), `@errands` (when you're out and can hit a store), `@computer` (when you have a laptop), `@waiting` (deferred to others). The `next-actions.md` file groups by context heading so you can scan to the section that matches your current circumstance.

The structural consequence: the four list files plus the per-project files plus the reference area is the entire system. That's by design — GTD's power is in the practice (especially the weekly review), not in elaborate folder structures. Adding more file types or deeper hierarchies tends to dilute the discipline.

The companion practice is the **weekly review**: every week, walk through the four files, every project file, and the calendar; clear the inbox; confirm every project has a current next action. The flat-markdown form makes this easy because every relevant file is grep-able and small.

## When to use

- **You're a GTD practitioner who prefers plain text** over apps. You've tried Things, OmniFocus, or Todoist and want something simpler, lighter, and version-controlled.
- **You want a system that survives tool changes.** Flat markdown is the longest-lived format on the planet; your GTD system can outlive any app.
- **You pair it with a daily-weekly note system.** GTD's weekly review wants a stable home; daily/weekly notes give it one.
- **Solo workflows.** GTD originated for individuals; flat markdown leans into that.
- **You like the discipline of writing.** Defining "next action" forces clarity. Doing it as a sentence in markdown is friction in a useful direction — apps that auto-prompt for it are great, but writing it by hand cements the habit.

## When NOT to use

- **You already use a real GTD app (Things, OmniFocus, Todoist) and like it.** The app is the system. Don't double-track. The cognitive cost of two systems is higher than the value either provides alone.
- **You need mobile capture as a primary surface.** Markdown editors on mobile have caught up, but app-based GTD (Things in particular) is still smoother for "voice-capture, then later triage."
- **Your projects are heavily collaborative or shared.** GTD is fundamentally personal; collaborative project tracking belongs in Linear, Asana, or similar. You can keep your *personal* GTD layer in markdown and let the team tools own the shared layer, but don't try to make markdown the team tool.
- **You want recurring tasks and reminders.** Markdown can fake this with a script or a calendar integration, but it's not native; an app does this naturally.
- **You can't sustain the weekly review.** GTD without weekly review devolves into a stale checklist. If the practice won't stick, the structure won't help.

## Tree diagram

```
gtd/
├── inbox.md
├── next-actions.md           ← contexts inside (`@home`, `@office`, `@calls`)
├── waiting-for.md
├── someday-maybe.md
├── projects/
│   ├── q2-redesign.md
│   └── learn-rust.md
└── reference/
    └── (filed reference material)
```

The four list files at the root are non-negotiable. `projects/` holds one file per active project. `reference/` holds non-actionable filed material — small here, can grow into PARA's reference area if needed.

## Naming rules

- **The four lists**: `inbox.md`, `next-actions.md`, `waiting-for.md`, `someday-maybe.md`. Lowercase, hyphen-separated, exactly these names. They're the canonical GTD list names; don't rename.
- **Project files** in `projects/`: kebab-case, descriptive — `q2-redesign.md`, `learn-rust.md`, `kitchen-remodel.md`. Avoid date prefixes unless the project is naturally time-bounded; GTD projects are *outcome*-bounded, not date-bounded.
- **Context headings** inside `next-actions.md`: `## @home`, `## @office`, `## @calls`, `## @errands`, `## @computer`. The leading `@` is the GTD convention. Use it; tools and your own muscle memory will thank you.
- **Reference files** in `reference/`: free-form. The reference area is meant to be a low-friction filing cabinet, not a structured library. Use kebab-case filenames; subfolder when the area grows.
- **Done items**: don't leave them cluttering the lists. Either delete on completion (most common in GTD) or move to a `done/` log file if you want a record. Don't move project files for completed projects out of `projects/` until the next weekly review.

## Worked example

Commitments live in email flags, sticky notes, and memory.

1. Create `inbox.md`, `next-actions.md`, `waiting-for.md`, `someday-maybe.md`, `projects/`, and `reference/`.
2. Capture everything into `inbox.md` with no organizing.
3. Process the inbox top to bottom: if it's not actionable, delete it, file it in `reference/`, or add to `someday-maybe.md`; if it takes under two minutes, do it; otherwise, decide the next physical action.
4. For anything needing more than one step, create `projects/<name>.md` with the outcome sentence and a next action at the top; copy that next action into `next-actions.md` under a context (`@computer`, `@calls`, `@errands`).
5. Move delegated items to `waiting-for.md` with a date and the person.
6. Do a weekly review: empty inbox, check each project has a next action, scan waiting-for and someday-maybe.

Every open loop has a home, and the weekly review keeps the lists trustworthy.

## Anti-patterns

- **Vague next actions.** "Plan vacation" is not a next action; "look up Iceland flights on Skyscanner" is. The most common GTD failure is leaving next actions abstract.
- **Inbox staleness.** `inbox.md` exists to be *cleared* — emptied, every item triaged into one of the other lists, on a regular cadence. An inbox left full for weeks defeats the system.
- **Skipping the weekly review.** GTD without the weekly review collapses into a stale to-do list. Schedule it, do it, defend it.
- **Letting projects file lack a next action.** Every active project file should have a current named next action. If it doesn't, either the project is stalled (move to `someday-maybe.md`) or the project is done (close it).
- **Over-indexing on `someday-maybe.md`.** It's meant to be a catch-all for "not now, but maybe someday" so capture stays low-friction; it's not a wishlist to manicure. Glance at it during weekly review; don't groom it.
- **Mixing `next-actions.md` and project task lists.** Each project file lists *all* the tasks that move the project forward; `next-actions.md` lists only the *single current* next action per project. Conflating the two duplicates work and breaks the model.
- **Hiding `waiting-for.md`.** "Waiting for" is the discipline of tracking what you're owed; if you don't review it, the asks fall through the cracks. Make it part of the weekly review.

## Scaling & failure modes

- **List bloat**: `next-actions.md` with more than about 60 items means projects lack focus or the review is being skipped.
- **Context lists** are optional; with a single device or a small list, one flat list is fine.
- **Stalled projects**: a project without a next action is a signal; the review catches these.
- **Tool fit**: plain files lack reminders; pair with a calendar for date-specific commitments only.

## Variants

- **Classic-list** (this guide). The four canonical lists plus per-project files. Most faithful to David Allen's book.
- **GTD + PARA**. Replace `projects/` with PARA's `1-Projects/`, add `2-Areas/`, `3-Resources/`, `4-Archives/` for richer reference. The four GTD lists stay as-is. Useful if your reference material is substantial.
- **GTD + Bullet Journal hybrid.** Use a bullet journal (paper or digital) for daily ritual and rapid logging; mirror only project files and reference into markdown. Common for paper-leaning GTDers.
- **GTD via Org-mode.** Emacs Org-mode has first-class GTD support: task-state keywords, `:context:` tags, `agenda` views. Same conceptual model, different syntax. See dedicated org-mode-GTD writeups (Bernt Hansen's "Organize Your Life In Plain Text!" is canonical).
- **GTD + tickler file.** Add a `tickler/` directory with date-named files (`2026-05-15.md`) for items that should resurface on a future date. Approximates GTD's 43-folders concept.

## Adoption checklist

- [ ] The inbox is empty after processing, not merely small.
- [ ] Every project file states the outcome and has a next action listed in `next-actions.md`.
- [ ] `waiting-for.md` entries have dates and names.
- [ ] A weekly review happens and takes under an hour.
- [ ] Calendar holds only hard-date items.

## Real-world projects using this

- **David Allen's *Getting Things Done*** (book, 2001; revised 2015) — the canonical reference. Don't substitute summaries for the book; the practice nuances are in the prose.
- **GettingThingsDone.com** — David Allen's company; the public site has free articles that explain the methodology canonically.
- **Bernt Hansen's "Organize Your Life In Plain Text!"** (doc.norang.ca/org-mode.html) — a very thorough Org-mode-GTD setup; the structure is the same as flat markdown with Org's task-state machinery on top.
- **GitHub markdown-GTD repos** — search "markdown gtd" or "gtd plaintext"; multiple practitioners publish their working systems as templates.
- **GTD subreddit and forums** — long-standing communities discuss flat-markdown vs app implementations; the discussions surface common failure modes worth knowing.

## Migration & references

- **From an app (Things / OmniFocus / Todoist)** to flat markdown: export the app's tasks (most have CSV/JSON), and write a small script to demultiplex into the four list files plus per-project files. The hard part isn't the export — it's deciding to commit to markdown and abandoning the app's mobile capture. Plan for friction.
- **From Org-mode to flat markdown**: the conceptual model survives; the syntax doesn't (Org's task-state and agenda machinery has no markdown equivalent). Translate by hand or with `pandoc`.
- **Adopting alongside an app**: keep the app for live task management and use flat markdown only for project-outcome documents and weekly review notes. This sidesteps the double-tracking trap.
- **References**:
  - *Getting Things Done* (David Allen, 2015 revised edition) — the book.
  - `gettingthingsdone.com` — official site.
  - `doc.norang.ca/org-mode.html` — Bernt Hansen's Org-mode GTD writeup.
  - Sibling guides: `notes/daily-weekly-notes/` (the review-cadence companion), `notes/para/` (richer reference layer underneath GTD), `notes/atomic-notes/` (next actions are the atomic unit).
