## TL;DR

An **engineering work log** is a private, plain-text record of your working life: what you did each day, what you decided and why, what went wrong, and what you achieved. Keep a **daily log** (`log/YYYY/YYYY-MM-DD.md`), a **weekly review** (`weekly/YYYY-Www.md`) that turns the week into a summary, a running **wins document** (`wins/YYYY-Qn.md`, sometimes called a brag document) that captures accomplishments with evidence as they happen, and small folders for **meetings**, **incidents**, and **projects**. The daily log costs a few minutes and pays back three times: fast standup answers, accurate status reports and reviews, and a searchable memory for "how did we fix that last time?" Write it for yourself first, keep confidential company data out of any copy that leaves your work machine, and follow your employer's policies on where work notes may be stored.

## Principles & why

1. **Capture while it's fresh.** Writing at the moment of the event costs a line; reconstructing it a month later costs an hour and loses detail.
2. **The log is for you.** A private, low-ceremony log gets written; a polished log gets skipped. Polish happens at review time, from the raw material.
3. **Achievements need evidence.** Record what you did, its impact, and a link (pull request, ticket, dashboard). "Reduced p95 latency from 800 ms to 350 ms" is usable in a review; "worked on performance" is not.
4. **Review turns entries into knowledge.** The weekly review extracts decisions, lessons, and follow-ups from the daily entries, which otherwise remain a stream.
5. **Separate the stream from the reference.** Daily entries are chronological; incidents, projects, and decisions are topical records you'll look up by name.
6. **Confidentiality is a design constraint.** Work notes may contain customer data, credentials, or secrets you must not keep; write around them and follow company rules.

## When to use

- **Software engineers and technical staff** with many small threads of work.
- **Anyone preparing for performance reviews, promotions, or interviews**, who needs evidence of impact.
- **On-call engineers**, who benefit from incident write-ups and searchable past fixes.
- **Team leads** tracking commitments, decisions, and one-on-one follow-ups.

## When NOT to use

- **As a team-wide system of record.** Team decisions belong in shared documents and ADRs (see `decision-records-adr`); this log is personal.
- **For confidential data.** Never paste secrets, customer records, or personal data into notes (see `config-and-secrets-placement`).
- **As a substitute for tickets and commit messages.** Link to them; don't duplicate them.
- **If your employer forbids external note storage.** Keep the log on approved systems only.

## Tree diagram

```
work/
├── README.md
├── log/
│   └── 2026/
│       ├── 2026-04-29.md              ← daily: plan, done, decisions, blockers
│       └── 2026-04-30.md
├── weekly/
│   └── 2026-W18.md                    ← weekly review: highlights, lessons, next week
├── wins/
│   └── 2026-Q2.md                     ← accomplishments with impact and links
├── meetings/
│   └── 2026-04-30-team-sync.md
├── incidents/
│   └── 2026-04-12-checkout-latency.md ← timeline, cause, fix, follow-ups
├── projects/
│   └── billing-migration/
│       └── README.md                  ← goal, status, links, open questions
└── archive/
    └── 2025/
```

## Naming rules

- **Daily files** are `YYYY-MM-DD.md` inside a year folder (see `iso-date-formats`); weekly files are `YYYY-Www.md`; the wins document is `YYYY-Qn.md`.
- **Meeting notes** are `YYYY-MM-DD-topic.md`, with the topic in kebab-case.
- **Incident records** are `YYYY-MM-DD-short-description.md`, using the date the incident started.
- **Project folders** use the project's common short name in kebab-case, with a `README.md` as the landing page.
- **People**: refer to colleagues by role or first name in the text; don't create per-person folders unless your organization allows it, and never record sensitive personal information.
- **Tags** in the text (`#decision`, `#lesson`, `#follow-up`) make review searches easy: `grep -rn "#follow-up" log/`.

## Worked example

A performance review is due in a week, and you cannot remember what you did in the last six months.

Going forward (the habit):
1. Each morning, create `log/2026/2026-04-30.md` from a template with three headings: **Plan**, **Done**, **Notes**.
2. During the day, add one line per meaningful thing, with a link: `- Fixed N+1 query in checkout (PR #482), p95 800 ms to 350 ms #win`.
3. Tag decisions (`#decision`), lessons (`#lesson`), and follow-ups (`#follow-up`).
4. Friday, write `weekly/2026-W18.md`: highlights, what slowed you down, lessons, and next week's top three. Search the week: `grep -h "#win" log/2026/2026-04-2*.md`.
5. Copy `#win` lines into `wins/2026-Q2.md` under a heading for the theme, adding impact and who benefited.

For the review this week (catching up):
1. Reconstruct from artifacts: your pull request list, ticket history, calendar, and chat threads. `git log --author="$(git config user.name)" --since=2025-11-01 --oneline` gives a starting list.
2. Group the results by theme (reliability, delivery, mentoring), and write each as *situation, action, result*.
3. From now on, keep the log so this takes ten minutes next time.

The review is assembled from evidence instead of memory.

## Anti-patterns

- **Writing a polished journal.** If a daily entry takes more than five minutes, it will stop happening.
- **Logging feelings and gossip** in a searchable work file. Keep it professional; assume it could be read by someone else.
- **Storing secrets, customer data, or credentials** in the log.
- **Recording tasks without outcomes.** "Worked on X" has no value later; write what changed.
- **Never reviewing.** A log that isn't read is a diary; the weekly and quarterly reviews create the value.
- **Duplicating tickets and pull requests** instead of linking to them.
- **Keeping it only on a work-managed system** that you will lose access to on leaving, without checking what you're allowed to retain.

## Scaling & failure modes

- **Volume**: a year of daily files is a few hundred small files, which is fine; rely on weekly reviews and `grep` rather than folders.
- **Role changes**: archive by year, and start a fresh `wins/` document per role if roles change.
- **Team adoption**: share the *templates* and the *habit*, not the logs; a team log becomes a status report and loses honesty.
- **Search**: keep tags consistent and a few standard verbs; tools like ripgrep or your editor's search do the rest.
- **On-call and incidents**: after every incident, write the record within a day; a searchable incident folder becomes the team's fastest runbook.
- **Long tenure**: write a yearly summary in `wins/` and `projects/` so older years can be skipped.

## Variants

- **Daily-only log**: the minimum viable version; add the rest as you feel the need.
- **Bullet-journal style**: task glyphs and migration (see `bullet-journal-digital`), useful if you also plan in the same file.
- **Single running file**: one `LOG.md` per project, appended in reverse chronological order; simpler, harder to search across projects.
- **Brag-document-first**: keep only `wins/` and a weekly note; suits people who log little but want evidence.
- **Team-shared standup notes**: a separate shared document; keep your personal log independent.

## Adoption checklist

- [ ] Today's daily file exists and has at least one line with a link.
- [ ] The weekly review happens and produces next week's top three.
- [ ] The wins document has impact and evidence, not only activity.
- [ ] Nothing confidential or secret is stored, and storage complies with employer policy.
- [ ] Incidents get a record within a day.
- [ ] Tags (`#win`, `#decision`, `#lesson`, `#follow-up`) are used consistently.

## Real-world projects using this

- **Julia Evans, "Get your work recognized: write a brag document"** popularized the wins-document practice.
- **Google's SRE book** ("Postmortem Culture") and **PagerDuty's incident response documentation** describe blameless incident write-ups that inform the `incidents/` records.
- **Bullet Journal method** (Ryder Carroll) and **daily notes** practices underlie the daily log; see `bullet-journal-digital` and `daily-weekly-notes`.
- **Engineering blogs** from many companies publish sample incident reports and postmortems worth reading.

## Migration & references

- **From scattered notes and chat DMs:** start the daily log now, and reconstruct only what you need from tickets and pull requests for the current review cycle.
- **From a task manager:** keep tasks there, and log outcomes in the daily file; link ticket IDs.
- **When leaving a job:** check what you may retain, and export only your own non-confidential accomplishments (for example, a sanitized wins summary), removing company-specific data.
- **References:**
  - `notes/daily-weekly-notes/` for the daily and weekly rhythm.
  - `principles/decision-records-adr/` for team-visible decisions.
  - `principles/iso-date-formats/` for filenames.
  - `notes/bullet-journal-digital/` for a task-oriented variant.
