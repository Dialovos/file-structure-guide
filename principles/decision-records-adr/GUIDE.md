## TL;DR

An **Architecture Decision Record (ADR)** is a short, dated, numbered document that captures one significant decision: the context, the options considered, the choice, and its consequences. Keep them in the repository, in `docs/adr/`, one file per decision, named `NNNN-short-title.md`. Records are **append-only**: you never rewrite an accepted decision to match new reality; you write a new ADR that supersedes it and mark the old one as superseded. The payoff is institutional memory that lives next to the code: a new engineer learns why the system is shaped as it is in minutes, and old debates don't get relitigated for lack of a record. Aim for one page per record, written when the decision is made, and kept small enough that writing one is never a chore.

## Principles & why

1. **Decisions outlive their authors.** Code shows what was built, not why. The reasoning disappears with people and chat history unless it's written down.
2. **One decision per record.** Small records are easy to write, link, and supersede. A record that covers five decisions can't be partially replaced.
3. **Append-only history.** Old records are marked `Superseded by ADR-0012`, never edited into agreement. The history of changing minds is part of the value.
4. **Context before choice.** A record that only states the decision is a rule; a record that states constraints and rejected alternatives is understanding.
5. **Consequences are honest.** Include the downsides accepted, so later readers know which trade-offs were intended.
6. **Live next to the code.** Records in the repository are reviewed with the change they justify, versioned with it, and found by anyone who clones.

## When to use

- **Any decision that is expensive to reverse**: language, framework, data store, service boundaries, authentication approach, repository layout.
- **Decisions people keep asking about**: "why don't we use X?"
- **Teams with turnover, remote members, or multiple contributors** who cannot ask the original author.
- **Solo and personal projects**, where a record spares future-you the same investigation.

## When NOT to use

- **Don't write an ADR for every choice.** Naming a variable or picking a formatter setting doesn't need one; a rule of thumb is that a decision qualifies if reversing it would take more than a few days.
- **Don't use ADRs as task tracking or meeting notes.** They record decisions, not discussion transcripts or to-dos.
- **Don't write them after the fact as justification.** A record written months later drifts into rationalization; write it at decision time, even if short.
- **Don't let them replace design docs** for large proposals; an ADR can summarize the outcome and link to the longer document.

## Tree diagram

```
docs/
└── adr/
    ├── README.md                       ← index: number, title, status
    ├── 0001-record-architecture-decisions.md
    ├── 0002-use-postgresql-for-primary-storage.md
    ├── 0003-adopt-monorepo-layout.md
    ├── 0004-use-event-queue-for-billing.md   ← Status: Superseded by 0007
    └── 0007-replace-event-queue-with-outbox.md
```

Numbers are never reused, and superseded records stay in place.

## Naming rules

- **Directory** is `docs/adr/` (or `doc/adr/`, matching the tools you use). Choose once.
- **Files** are `NNNN-title-in-kebab-case.md`, with a zero-padded four-digit sequence number (`0007-...`), assigned in order of creation.
- **Titles** state the decision in the imperative or as a noun phrase: `use-postgresql-for-primary-storage`, not `database`.
- **Status values** are a small fixed set: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.
- **Dates** in ISO format (`2026-04-30`) at the top of each record (see `iso-date-formats`).
- **Index** is `README.md` inside the directory, with one line per record (see `indexes-and-mocs`).

## Worked example

A team keeps debating whether to move from REST to GraphQL, and nobody remembers the last time it was discussed.

1. Create `docs/adr/` and write `0001-record-architecture-decisions.md` explaining that the team will keep ADRs.
2. Copy a template (see the one in this guide's template directory) with sections: Status, Date, Context, Options considered, Decision, Consequences.
3. Write `0002-keep-rest-api-for-public-clients.md`:
   - Context: mobile app team wants flexible queries; three client teams; current API has 40 endpoints.
   - Options: keep REST, add GraphQL alongside, replace REST with GraphQL.
   - Decision: keep REST for public clients; revisit if endpoint count passes 100 or client requests diverge.
   - Consequences: no new infrastructure; over-fetching remains a known cost; revisit trigger stated.
4. Open a pull request so the decision is reviewed like code; merge with status `Accepted`.
5. Add the record to `docs/adr/README.md`.
6. Six months later, when the debate returns, link the record and check whether the revisit trigger has been met; if the decision changes, write `0015-adopt-graphql-for-mobile.md` and mark `0002` as `Superseded by 0015`.

The debate now starts from the recorded reasoning and trigger, not from scratch.

## Anti-patterns

- **Editing accepted records** to match reality. Supersede instead; the trail is the point.
- **Writing ADRs for everything.** Volume kills the habit; keep them for decisions with real cost of reversal.
- **Records with no alternatives.** "We chose X" without what else was considered is a decree, not a record.
- **Hidden in a wiki or chat.** Off-repository records go stale and get lost; keep them in git.
- **No index and no statuses.** A folder of 60 unlabeled files can't be used; maintain the README table.
- **Renumbering.** Numbers are identifiers; changing them breaks links from code comments and pull requests.

## Scaling & failure modes

- **Hundreds of records**: the index needs grouping (by area or status) or tags in frontmatter, and a script to check that every file appears in it.
- **Multiple repositories or services**: use per-repo ADRs for local decisions and a central repository for cross-cutting ones, referencing each other by link.
- **Review overhead**: keep records short; a pull request template that asks "does this change need an ADR?" builds the habit.
- **Stale decisions**: add a review date or a revisit trigger to decisions with a shelf life.
- **Searchability**: use consistent status words and descriptive titles so `grep` finds them.

## Variants

- **Nygard format** (the original): Title, Status, Context, Decision, Consequences.
- **MADR** (Markdown Any Decision Records): adds explicit options with pros and cons, and decision drivers.
- **Y-statements**: a one-sentence form: "In the context of X, facing Y, we decided Z, to achieve A, accepting B."
- **Lightweight log**: a single `DECISIONS.md` file for very small projects; graduate to one file per record when it exceeds a page or two.
- **RFC/design-doc process**: for large, cross-team proposals; ADRs record the outcome.

## Adoption checklist

- [ ] `docs/adr/` exists with `0001` recording the decision to use ADRs.
- [ ] Every record has a status, an ISO date, context, options, decision, and consequences.
- [ ] Superseded records point to their successors.
- [ ] `docs/adr/README.md` lists every record.
- [ ] Pull requests for architecture-affecting changes link the relevant ADR.
- [ ] Numbers are sequential and never reused.

## Real-world projects using this

- **Michael Nygard's "Documenting Architecture Decisions"** (2011) introduced the lightweight ADR format.
- **adr-tools** (Nat Pryce) and the successor **log4brains** provide command-line and static-site tooling.
- **MADR** (adr.github.io/madr) is a widely used template with options and drivers.
- **Public repositories** including many open-source projects and government digital services publish ADRs alongside code; reading a few shows the range of formats.
- **The ADR GitHub organization** (adr.github.io) collects templates, tools, and examples.

## Migration & references

- **From wiki or chat history:** pick the five to ten decisions people still ask about, write short retrospective records marked with the actual decision date if known, and stop; don't try to backfill everything.
- **From a single `DECISIONS.md`:** split into numbered files, keeping the original order, and build the index.
- **From design docs:** write an ADR summarizing the outcome and link to the long document.
- **References:**
  - `principles/readme-placement/` for the index README.
  - `principles/iso-date-formats/` for dates.
  - `principles/indexes-and-mocs/` for keeping the list navigable.
  - `principles/monorepo-vs-polyrepo/` as an example of a decision worth recording.
  - `notes/engineering-work-log/` for the daily log that feeds decisions.
