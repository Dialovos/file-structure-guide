## TL;DR

Bullet Journal (BuJo), invented by Ryder Carroll, is an analog method for capturing tasks, events, and notes in a single notebook using **rapid logging** — short signified entries with glyphs (`•` task, `○` event, `–` note, `*` priority). The digital adaptation keeps BuJo's structural ritual (Future Log → Monthly Log → Daily Log → Collections + Index) but trades pen-and-paper for Markdown, sync, and search. The trick is to **resist tooling**: BuJo's discipline is the migration ritual (carrying unfinished tasks forward each day/month), not the tooling. Don't add backlinks, tags, or queries until you've practiced the pure form for a month — most of BuJo's value comes from the friction of re-writing tasks, which forces you to drop ones that don't matter. This guide shows the digital BuJo layout: a `bujo/` folder with `future-log.md`, monthly logs, daily logs, collections, and an INDEX.md acting as Carroll's "Index" page. Sibling philosophies (Zettelkasten, evergreen, PARA) are richer for knowledge work, but BuJo wins for mixed task/event/note capture.

## Principles & why

The four BuJo modules are the structure; rapid logging is the syntax.

1. **Future Log** — the next 3-12 months at a glance, one section per month. Things that aren't this month yet: birthdays, deadlines, intentions. When a month opens, you migrate items from Future Log into the new Monthly Log.
2. **Monthly Log** — opens each month with a *calendar page* (each date listed) and a *task page* (this month's intentions). Carroll calls these "the monthly migration".
3. **Daily Log** — the workhorse. Each day gets a heading and rapid-logged entries. End of day: review, mark tasks complete, migrate unfinished tasks to tomorrow (the migration ritual is the heart of BuJo).
4. **Collections** — themed pages that aren't tied to dates. Books to read, project plans, habit trackers. The Index points to them by name and "page" (= filename in digital).

Rapid logging glyphs are minimal by design: `•` for tasks, `○` for events (things that happen at a time), `–` for notes (information). The variant `*` marks priority; `<` and `>` mark migration (`<` to Future, `>` to next day/month); `X` over `•` marks complete. Strikethrough means dropped. The discipline of writing the glyph forces you to classify each line as you write it — this is half of why BuJo works.

The Index (Carroll's page 1-4) is *not* a search engine. It's a hand-curated table of contents listing collection names and the page they live on. In digital BuJo this becomes `INDEX.md` linking to each collection file. You don't index daily logs (they're chronological); you do index every collection.

## When to use

- **Mixed task + event + note capture** — BuJo's killer feature is treating all three as first-class with cheap glyph syntax.
- **People who like the analog ritual but want sync/search** — BuJo on paper has zero search; digital BuJo keeps the ritual and adds find-in-vault.
- **Daily-driven workflows** — if your day starts by "what did I leave open yesterday?", BuJo's migration ritual is built for that.
- **Newcomers to note-taking** — BuJo is more legible than Zettelkasten and lower-stakes than PARA. Many people start here.
- **Hybrid with a knowledge layer** — pair BuJo for tasks/journal with a separate evergreen-notes vault for ideas. BuJo handles the timeline; evergreen handles the knowledge.

## When NOT to use

- **Heavy linking / PKM workflows** — BuJo's collections are weakly linked. If you want to compose ideas across dozens of notes, use Zettelkasten or evergreen-notes.
- **Pure task management** — if you don't journal or take notes, a real task manager (Things, Todoist, OmniFocus) is better. BuJo's value comes from mixing the three.
- **People who hate ritual** — the migration step is non-optional in real BuJo. If you skip migration, you've just made a date-stamped notes folder.
- **Long-form writing** — daily logs are not the place for essays. Keep prose in a separate `drafts/` folder or a different system.
- **Team collaboration** — BuJo is profoundly personal. The migration ritual doesn't survive shared editing.

## Tree diagram

```
bujo/
├── future-log.md           ← next 3-12 months, by month
├── monthly/
│   ├── 2026-04.md          ← calendar page + monthly tasks
│   └── 2026-05.md
├── daily/
│   └── 2026-04-30.md       ← rapid-logged: tasks, events, notes
├── collections/
│   ├── books-to-read.md
│   ├── habit-tracker-2026.md
│   └── trip-planning.md
└── INDEX.md                ← Carroll's "Index" page → collections
```

The directory shape mirrors the four BuJo modules. Daily logs go in `daily/`, monthly logs in `monthly/`, and Carroll's "Index" page lives at the root as `INDEX.md`.

## Naming rules

- **Daily logs**: `daily/YYYY-MM-DD.md` (ISO 8601). One file per day. Don't mix multiple days in one file — it breaks the migration ritual.
- **Monthly logs**: `monthly/YYYY-MM.md`. The file opens with a calendar table and a "monthly tasks" list.
- **Future log**: a single `future-log.md` at the root. Sections are months: `## 2026-05`, `## 2026-06`, etc. When a month arrives, migrate its items into the new monthly log and clear the section.
- **Collections**: `collections/<kebab-case-topic>.md`. Names should read as nouns: `books-to-read.md`, not `read-books.md`.
- **INDEX.md**: a flat list of collection links. Each entry: `- [Books to read](collections/books-to-read.md) — short description`.
- **Glyphs in entries**: `• task`, `○ event`, `– note`, `* priority`. Use Markdown-friendly versions if your editor mangles bullets (e.g., `- [ ] task` for checkboxes is acceptable).

## Worked example

Tasks live in five apps and a notes file; nothing reviews them.

1. Create `future-log.md` with headings for the next six months, and `monthly/2026-05.md` for the current month.
2. Each morning, create `daily/2026-05-14.md` and rapid-log with glyphs: `•` task, `○` event, `–` note, `*` priority.
3. At the end of the day, review: mark `x` for done, `>` for migrated to tomorrow, `<` for scheduled to the future log.
4. At month end, migrate open tasks to the new monthly page, and cancel what no longer matters (`~~text~~`); the act of choosing is the point.
5. Start collections as needed (`collections/books-to-read.md`) and list each in `INDEX.md` with a link.

Everything open is visible on today's page or this month's page, and nothing stays open without a decision.

## Anti-patterns

- **Skipping migration.** The single biggest BuJo failure mode. If you don't migrate unfinished tasks each day/month, your daily logs become a graveyard and the system collapses to "dated notes folder".
- **Adding backlinks too early.** People discover Obsidian and immediately wikilink everything. BuJo is *not* a graph — keep it linear for at least a month before adding any non-Index linking.
- **No Index.** Without `INDEX.md`, your collections become invisible. The Index is what gives BuJo its "table of contents" feel.
- **Mixing collections with dailies.** Don't put project notes in `daily/2026-04-30.md`. They go in `collections/<project>.md` and are referenced from the daily.
- **Using glyphs inconsistently.** Pick the four glyphs (or your variant) and stick to them. Inconsistent glyphs = no signifier system = unstructured notes.
- **Future Log sprawl.** The Future Log is for *fixed* future dates (birthdays, deadlines), not aspirations. "Someday/maybe" goes in a collection.

## Scaling & failure modes

- **Migration fatigue**: if the same task migrates three times, delete it or turn it into a project.
- **Glyph inflation**: keep to four or five signifiers; extra symbols slow logging.
- **Digital friction**: search and sync are strengths; don't recreate paper layouts (calendars drawn with tables) that a calendar app does better.
- **Archive**: monthly and daily files accumulate cheaply; keep them flat by date.

## Variants

- **Strict BuJo** (this guide) — faithful to *The Bullet Journal Method*: four modules, four glyphs, migration ritual, Index. The recommended starting point.
- **BuJo + evergreen** — keep BuJo for tasks/journal but link out from collections to atomic evergreen notes. The collection becomes a Map of Content (MOC) over evergreen notes. Best of both worlds for people who also do PKM.
- **Simplified BuJo** — drop the Future Log; keep Monthly + Daily + Collections + Index. Lower overhead; gives up long-horizon planning.
- **Roam-flavored BuJo** — daily pages with backlinks to collection pages (which auto-update). Loses the migration ritual but gains queryability. Closer to Logseq than canonical BuJo.
- **BuJo-on-paper + digital archive** — keep the analog notebook for ritual; periodically photograph or transcribe completed months into a digital archive for search. Carroll himself has expressed sympathy for this hybrid.

## Adoption checklist

- [ ] Today's daily log exists and uses the glyph set consistently.
- [ ] A monthly review migrates or cancels every open task.
- [ ] `future-log.md` covers the next several months.
- [ ] Every collection is linked from `INDEX.md`.
- [ ] Tasks migrated three times are reconsidered.

## Real-world projects using this

- **Ryder Carroll, *The Bullet Journal Method*** (Portfolio, 2018) — the canonical reference. The bulletjournal.com site has the full method overview.
- **bulletjournal.com** — Carroll's official site, including the original blog post that sparked the method and a video walkthrough.
- **Obsidian community templates** — search "Obsidian Bullet Journal" on the Obsidian forum (forum.obsidian.md) and GitHub; several open-source vaults implement digital BuJo with templates and dataview queries.
- **Notion BuJo templates** — Notion's template gallery has multiple Bullet Journal templates that mirror Carroll's structure (notion.so/templates).
- **r/bulletjournal** subreddit — large community sharing analog spreads; many threads on digital adaptations.

## Migration & references

- **From plain dated notes**: create `daily/`, `monthly/`, `collections/`, `INDEX.md`. Migrate today's notes into a daily log with glyphs. Move ongoing topical notes into collections. Stop creating new files outside this structure.
- **From a task manager (Todoist, Things)**: keep the task manager as your reminder system; use BuJo for journaling and reflection only. Don't double-log; pick one for tasks. BuJo's tasks shine when they're *thoughts* not *reminders*.
- **From Zettelkasten / evergreen**: don't migrate. Run BuJo for the timeline (daily/monthly/journal) and keep evergreen for the knowledge layer. Link from collections to evergreen notes when appropriate.
- **References**:
  - Ryder Carroll, *The Bullet Journal Method* (2018) — primary source.
  - bulletjournal.com — the official method site.
  - Sibling guides: `notes/daily-weekly-notes/` (BuJo's daily-log analog in PKM), `notes/maps-of-content/` (collections as MOCs), `notes/evergreen-notes/` (knowledge layer to pair with BuJo).
  - Anti-pattern reference: `ANTIPATTERNS.md` at repo root for common BuJo failure modes (skipping migration, glyph inconsistency).
