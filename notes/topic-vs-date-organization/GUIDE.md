## TL;DR

Topic vs date is a **decision**, not a layout — the most consequential one in any note system. **Topic-driven** organisation (`attention/`, `productivity/`) optimises for retrieval-by-subject and durable knowledge. **Date-driven** organisation (`2026-04-30.md`) optimises for capture-by-time and journalling. Both are valid; mixing them *without intent* is the trap. The recommended approach is the **intentional mix**: a `daily/` folder for date-driven journal/capture, plus a `topics/` folder (or evergreen-notes vault) for the topic-driven knowledge layer. Notes flow from the daily inbox into topical notes once they earn it. The anti-pattern is the *accidental* mix — random files some named `2026-04-30-meeting.md`, others `meeting-with-bob-about-q2.md`, with no rule for which goes where.

## Principles & why

Three orthogonal questions force the choice:

1. **What's the primary retrieval mode?** If you'll search for "everything about attention", topic-driven wins. If you'll search for "what did I think about this in April?", date-driven wins. Most people want *both*, which is why the intentional mix exists.
2. **Is the note durable or fleeting?** A meeting log is fleeting — it's relevant for a week, then dead. A claim about attention residue is durable — it should compound for years. Date-driven storage matches fleeting; topic-driven storage matches durable.
3. **What's the capture/refinement ratio?** If you capture much more than you refine (work logs, journal, daily standups), date-driven is the right shape — file names are auto-generated, no decision required at write time. If you refine much more than you capture (essays, theories, evergreen notes), topic-driven is the right shape — every note's title is curated.

The intentional mix admits both: capture goes to the daily file (zero-friction, no naming decision); refinement extracts durable claims into topical notes with curated titles. The handoff is the weekly review.

The accidental mix happens when there's no rule for which kind of note goes where. The result: today's thoughts split between `2026-04-30.md` and `attention-meeting.md`, with no way to know which is canonical. Search works; orientation doesn't. The fix is to *pick a rule and write it down* — even if the rule is "fleeting → date, durable → topic".

## When to use

- **Topic-driven:** essays, research, theory, evergreen notes, reference material, anything with multi-year half-life.
- **Date-driven:** journal, work log, daily standup, learning log, fleeting capture, anything where "when" matters more than "what".
- **Intentional mix:** the recommended default for personal knowledge work — a daily/journal layer + a topical/evergreen layer. Almost every modern note app supports this (PARA + daily notes; LYT's Calendar + Notes; ACCESS's `4-entries/` + `3-concepts/`).
- **Pure topic:** academic researchers writing for publication; technical leaders maintaining a personal reference; anyone whose vault is exclusively "stuff I want to find by subject".
- **Pure date:** Bullet Journalists going digital; people who keep a strict diary; some Roam/Logseq users who put everything in dailies and rely on backlinks for topical access.

## When NOT to use

- **Don't use pure-topic** if you also journal daily — you'll either break the rule (and slip into accidental mix) or feel friction every time you write a journal entry. Adopt the intentional mix.
- **Don't use pure-date** if your notes feed long-form output. Date-only loses the topical compounding that makes notes valuable in writing pipelines.
- **Don't use the intentional mix without a rule.** "Sometimes I file by date, sometimes by topic" without a rule is the accidental-mix anti-pattern in disguise. Write the rule down.
- **Don't pick based on trend.** Roam/Logseq made date-driven popular for a few years; LYT/PARA made topic-driven popular for others. Your retrieval pattern matters more than fashion.
- **Don't switch frequently.** Every switch costs migration effort. Pick once, commit for at least a year.

## Tree diagram

```
topic-driven/
├── attention/
│   ├── attention-residue.md
│   └── deep-work-blocks.md
└── productivity/
    └── pomodoro-experiments.md

date-driven/
├── 2026-04-30.md      ← contains all of today's thoughts
└── 2026-05-01.md

mixed (intentional)/
├── daily/             ← date-driven for journal/log
│   └── 2026-04-30.md
└── topics/            ← topic-driven for evergreen notes
    └── attention/
```

The intentional mix is two non-overlapping layers, each with a clear ownership rule.

## Naming rules

1. **Topic-driven filenames:** lowercase-hyphenated, descriptive, ideally declarative — `attention-residue.md` or (evergreen-style) `attention-residue-tax-from-task-switching.md`. No date prefix.
2. **Date-driven filenames:** ISO 8601 — `YYYY-MM-DD.md` for daily, `YYYY-Www.md` for weekly. No descriptive suffix; the date is the entire identity.
3. **Intentional mix uses both rules in their respective folders.** `mixed/daily/2026-04-30.md` and `mixed/topics/attention/attention-residue.md` — never `mixed/2026-04-30-attention-residue.md` (that's accidental mix).
4. **Folder naming:** `daily/` and `topics/` (or `notes/`) for the intentional mix. Some workflows use `journal/` and `evergreen/`; pick one.
5. **The rule of canonical location:** every note has exactly one home. If a thought lives in today's daily and you also extract a topical note, the daily entry should *link* to the topical note, not duplicate it.
6. **Don't let date prefixes leak into topical files.** `attention/2026-04-30-attention-residue.md` is the start of accidental drift — drop the date.
7. **Don't let topics leak into date files.** `daily/2026-04-30-q2-redesign.md` is similarly drift; the date file is `2026-04-30.md`, period.

## Anti-patterns

- **Accidental mix.** Some files named by date, some by topic, no rule. Search works but orientation breaks.
- **Date prefixes on topical notes.** `2026-04-30-attention-residue.md` looks tidy but locks the note to a moment, defeating the topical-discovery property.
- **Topic prefixes on date notes.** `daily-2026-04-30.md` is redundant if the file lives in `daily/` and a sort-killer if it lives at root.
- **No journal layer in a topic-driven vault.** All capture has to find a topical home, which adds friction to the point where capture stops happening.
- **No topical layer in a date-driven vault.** Notes stay locked to the day they were written; long-running thinking has nowhere to compound.
- **Switching strategies mid-vault.** Pre-2025 notes are date-driven, post-2025 are topic-driven, no migration. The vault becomes two vaults pretending to be one.
- **Folder-by-year as the only structure.** `2024/`, `2025/`, `2026/` is date-driven at folder level; if every year folder is a soup of mixed notes, the folders aren't doing useful work.

## Variants

- **pure-topic.** All notes named by subject; no daily layer. Suits researchers/essayists who don't journal.
- **pure-date.** All notes named by date; topical access via backlinks/tags. Suits Roam/Logseq users and Bullet Journal converts.
- **intentional-mix (this guide's recommendation).** A `daily/` layer + a `topics/` (or evergreen) layer, with a clear rule for which note goes where.
- **intentional-mix-with-area-folders.** Adds PARA-style or ACCESS-style area folders alongside the date+topic split. More structure; more decisions.
- **accidental-mix (the anti-pattern).** Listed for completeness as the case to avoid. Also called "muddled vault".
- **journal-as-index.** A pure-date variant where each daily note is heavily linked to topical notes that auto-emerge from wikilinks (Roam/Logseq style). Topical notes exist but are derivative — their content is mostly assembled from daily-note backlinks.

## Real-world projects using this

- **Roam Research** — https://roamresearch.com — pure-date by default; topical pages emerge from wikilinks typed in dailies. Influential example of date-driven done right.
- **Logseq** — https://logseq.com — same pattern as Roam, open-source.
- **Andy Matuschak's notes** — https://notes.andymatuschak.org — pure-topic evergreen-notes, no daily layer.
- **Obsidian community vaults** — most public Obsidian vaults on GitHub demonstrate the intentional-mix pattern (a `daily/` folder + a topical structure).
- **Bullet Journal** by Ryder Carroll — https://bulletjournal.com — the analog ancestor of pure-date organisation.
- **PARA + daily notes** (Tiago Forte, https://fortelabs.com) — canonical intentional mix: PARA folders for topics, separate daily-notes plugin for capture.
- **Linking Your Thinking** — https://linkingyourthinking.com — explicit `Calendar/` and `Notes/` folders implementing the intentional mix.

## Migration & references

To start an intentional-mix vault from scratch:

```bash
mkdir -p vault/{daily,topics}
cd vault
TODAY=$(date +%Y-%m-%d)
cat > "daily/${TODAY}.md" <<'EOF'
# ${TODAY}

Capture goes here. Things that earn their own life get extracted into topics/.
EOF
mkdir -p topics/example
cat > "topics/example/example-note.md" <<'EOF'
# Example note

A topical note that durable claims live in. Linked from daily notes that mention it.
EOF
```

To migrate from accidental mix:

1. **Identify the rule.** Ask: which of my files are about *when* (meetings, gripes, captures) and which are about *what* (claims, theories, references)?
2. **Move date-named files into `daily/`.** Anything named `2026-04-30.md` or `meeting-2026-04-30.md` belongs in the date layer.
3. **Strip date prefixes from topical files.** `2026-03-15-attention-residue.md` becomes `attention-residue.md`.
4. **Move topical files into `topics/`** (or your topical structure).
5. **Update wikilinks.** Any `[[2026-03-15-attention-residue]]` references need rewriting to `[[attention-residue]]`.
6. **Write down the rule.** Add a `RULES.md` or commit it to memory: "fleeting capture → daily/, durable claims → topics/".
7. **Hold the line.** New notes follow the rule from day one of the migration.

To migrate from pure-date to intentional-mix:

1. **Add a `topics/` folder.** Don't move anything yet.
2. **For each topic cluster you find yourself searching for repeatedly,** create a topical note in `topics/cluster-name.md` and copy the durable claims out of dailies into it.
3. **Backlink, don't duplicate.** The daily note can keep its original entry, but it should also link to the new topical note.
4. **Iterate weekly.** During the weekly review, promote durable claims out of the week's dailies.

Further reading and adjacent guides:

- [`daily-weekly-notes`](../daily-weekly-notes/) — date-driven layer specifics.
- [`evergreen-notes`](../evergreen-notes/) — topic-driven layer at its strongest.
- [`para`](../para/) — folder-first topical organisation.
- [`lyt-linking-your-thinking`](../lyt-linking-your-thinking/) — explicit intentional-mix framework.
- [`access-framework`](../access-framework/) — six-bucket variant of the intentional mix.
- [`zettelkasten-classic`](../zettelkasten-classic/) — topic-driven with timestamp IDs (a hybrid of sorts).
- [`folgezettel`](../folgezettel/) — topic-driven with hierarchical IDs.
- ISO 8601 — https://www.iso.org/iso-8601-date-and-time-format.html — the canonical date standard for filenames.
