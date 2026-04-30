# Project archive

## TL;DR

Split your projects directory in two: `active/<project>/` for what you currently work on and `archive/<YYYY>/<project>/` for what's finished or paused. Moving a project from one to the other is the explicit ritual of "I'm done with this for now." `active/` stays small enough to scan; `archive/` keeps everything retrievable without polluting today's mental space.

## Principles & why

The single biggest cause of personal-projects-directory rot is *active* and *finished* sharing one tree. After a year, half the directories are stale, but `ls` still pages through them, fuzzy-finders still match them, and `cd` still autocompletes them. The cognitive cost of every interaction climbs.

A status-based split solves this with one move command per project transition. The `active/` tree is bounded by the human capacity to actually pursue work — typically 3–10 projects at most. The `archive/` tree is unbounded but partitioned by year so any individual year stays scannable.

The year subdivision matters: a single flat `archive/` of 80 finished projects is almost as bad as the original problem. `archive/2025/` is bounded by what you finished in one year (typically 5–25 projects), which fits in one `ls` page. The same year-bucket approach works for journals, receipts, and photos — see `files/date-archive/`.

The ritual itself has psychological value: deliberately moving a project to `archive/` is the moment you decide "this is done" and can stop holding it open in your head.

## When to use

- Any environment where projects accumulate over years: consulting work, freelance jobs, academic research projects, side hustles, hobby builds.
- Personal `~/projects/` or `~/code/` directories where active work mixes with old experiments.
- A team's shared "case studies" or "client work" folder that grows indefinitely.
- Note repositories using PARA's `1-projects/` scheme — pair `active/` (the live PARA project list) with `archive/4-archive/<YYYY>/`.
- Research labs that accumulate code from past papers — `active/` for current projects, `archive/<year>/` for shipped publications.

## When NOT to use

- Projects you actively merge into a single canonical repo — let your VCS do the archiving via tags and branches; don't duplicate by moving directories.
- Solo single-product work with one or two long-running projects — there's nothing to separate, so the split is theatre.
- Org-managed monorepos where every project is a workspace — the monorepo tooling already segments live vs. retired.
- When you'd archive *to* a separate medium (a NAS, an external drive) — the on-disk archive directory is unnecessary; do the move once at retirement.
- Source-controlled projects where the only artifact worth archiving is the git history itself — push to a long-term remote and delete locally.

## Tree diagram

```
projects/
├── active/
│   └── q2-redesign/
└── archive/
    ├── 2025/
    │   ├── q4-billing-revamp/
    │   └── side-project-foo/
    └── 2024/
        └── q3-migration/
```

## Naming rules

1. Top-level split is exactly `active/` and `archive/`. Synonyms (`current/`, `done/`, `old/`) defeat habits — pick the canonical names and keep them.
2. Inside `active/`, projects use kebab-case slugs and may include a quarter or release tag if that's how you index them: `q2-redesign/`, `v3-migration/`.
3. Inside `archive/`, projects nest under the year they were *retired*, not the year they started: `archive/2025/q3-migration/` if you stopped working on it in 2025.
4. Long-running projects that span years stay in `active/` until retired; you do not split them across multiple `archive/<year>/` buckets.
5. If a project has both code and notes that you want to keep together, archive the whole directory; don't leave half in `active/` and half in `archive/`.
6. Re-activated projects move *back* to `active/` rather than living in both. The history of moves can be reconstructed from `git log --follow` or filesystem mtimes if needed.

## Anti-patterns

- **`active/`, `pending/`, `someday/`, `done/`** — too many stages; the boundaries blur and projects get stuck in an intermediate state for years.
- **No year subdivision under `archive/`** — a flat `archive/` of 80+ projects is unscannable; year-buckets cap each list at one `ls` page.
- **Archiving by topic** (`archive/work/`, `archive/personal/`) — duplicates an axis your filenames already encode and makes "what did I finish in 2025?" unanswerable.
- **Moving without a commit message** — if your projects directory is itself in git, leave a one-line note when you move (`chore: archive q4-billing`); it pays off when you go searching years later.
- **Leaving symlinks behind in `active/`** — every script that crawls `active/` will follow them; either move cleanly or copy if you genuinely need both.
- **Mixing finished projects with finished one-off scripts** — scripts go in `~/bin/` or `dotfiles/`; only project-shaped work belongs in this archive.

## Variants

- **archive-by-year** (this guide) — `archive/2025/<project>/`. Best default; matches journals and receipts.
- **archive-by-status-then-year** — `archive/shipped/2025/`, `archive/abandoned/2025/`. Useful when funders or employers want a "completed vs. cancelled" report.
- **single-flat-archive** — one big `archive/<project>/`. Works only for small portfolios (≤30 lifetime projects).
- **archive-with-tombstones** — leave a one-line `archive/<year>/<project>.md` stub in place of the dir (move the project elsewhere). Compact when projects are huge but you want them indexed.
- **PARA `4-archive/`** — the Tiago Forte scheme; equivalent to this guide with the `archive/` directory named `4-archive/`.

## Real-world projects using this

- **Tiago Forte's PARA** — codifies `4-archive/` as the destination for retired projects; spec is in *Building a Second Brain*.
- **GTD's "completed projects" list** — David Allen's *Getting Things Done* recommends a single archived-projects list, conceptually identical.
- **Academic researchers' `old-projects/` directories** — common convention in research-software groups; many lab-handbook templates document it.
- **Pinboard / Pocket archive states** — retired bookmarks move to `archive/` rather than being deleted; same pattern at the individual-link level.
- **Notion / Obsidian PARA templates** — popular community templates for both apps default to a `4-archive/` folder.
- **Personal-blog "drafts/published/" patterns** — many static-site blogs (Hugo, Jekyll) split posts into directories indexed by completion year.

## Migration & references

To convert a flat `projects/` into this layout:

```bash
# Identify finished projects (no commits in the last N months) and move them
THRESHOLD_DAYS=180
for d in projects/*/; do
  age=$(stat -c %Y "$d")
  cutoff=$(( $(date +%s) - THRESHOLD_DAYS*86400 ))
  if [ "$age" -lt "$cutoff" ]; then
    yr=$(date -d @"$age" +%Y)
    mkdir -p "projects/archive/$yr"
    git mv "$d" "projects/archive/$yr/"
  fi
done
mkdir -p projects/active && mv projects/!(active|archive) projects/active/
```

Adjust the threshold to your own pace; six months of inactivity is a defensible default.

Further reading:

- `principles/status-based-organization/` — the underlying principle this layout instantiates.
- `files/date-archive/` — the same year-bucketing applied to receipts, scans, and journals.
- Tiago Forte, *Building a Second Brain* (PARA, 2022).
- David Allen, *Getting Things Done* (GTD, original 2001; revised 2015).
- `principles/stable-vs-volatile-separation/` — `active/` is volatile, `archive/` is stable; the split is the point.
