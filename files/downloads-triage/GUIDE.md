# Downloads triage

## TL;DR

Treat `~/Downloads/` as an inbox, not a permanent home. Browsers and most apps drop new files into `inbox/`, you do a recurring (e.g. weekly) triage that moves each file to its real destination — a project tree, a permanent archive, the trash, or `_to-process/` for things that need action you can't do right now. Three subdirectories — `inbox/`, `archive/`, `_to-process/` — replace the usual sprawl of seven-year-old PDFs and three copies of the same installer. The inbox-triage discipline matters more than the directory layout; the layout exists to make the discipline obvious every time you open the folder.

## Principles & why

`~/Downloads/` is the most-abused directory on most personal machines because two forces collide: every browser, mail client, and chat app uses it as the default save target, and almost no one has a routine to clear it. Files accumulate forever; meaningful items get buried under thirty redundant ones; you waste minutes re-downloading things you already had.

The fix is to apply the GTD "physical inbox" pattern to a digital location:

1. **One place for new arrivals.** Rather than letting downloads splat at the top of `Downloads/`, configure your browser's default download path to `~/Downloads/inbox/`. The bare `~/Downloads/` directory becomes a *namespace*, not a dumping ground.
2. **A scheduled triage step.** Pick a recurring slot (Friday afternoon, end-of-month) and process the inbox: each item gets moved to its project, dropped into `archive/`, deleted, or parked in `_to-process/` if it requires more thought.
3. **A holding pen for "I'll get to it".** `_to-process/` exists so you can clear `inbox/` without committing to filing decisions you aren't ready to make. The leading underscore sorts it last.
4. **An infrequently-touched archive.** `archive/` holds installers, exports, and downloads you want to keep findable but rarely re-open. Subdivide it lazily — only when something already in `archive/` would benefit.

The directory shape is a behavioral nudge: every time you `cd ~/Downloads`, you see three folders and your mental model is "what's in inbox today?", not "what does this 1,400-file mess hide?".

## When to use

- Anyone whose `~/Downloads/` has more than ~100 unsorted items, or anyone who's caught themselves re-downloading a file they already had.
- People who want a system without a tool — this is a discipline-plus-three-folders, no software to install.
- Combine with a recurring "Friday triage" calendar block, a Sunday-evening review, or a once-a-month batch session.
- Households or shared accounts where multiple people save into `~/Downloads/` — the inbox/archive split makes "what's mine vs theirs" easy.
- As a precursor to writing automation rules (Hazel, Maid) — the manual workflow teaches you what rules to write.

## When NOT to use

- If you already use a tool like **Hazel** (macOS) or **Maid** with stable rules — your automation likely already routes files at download time, making this layout redundant.
- If your browser writes elsewhere — Firefox's per-site download paths, Safari's quarantine handling, or Windows's `%USERPROFILE%\Downloads\` may need different setup.
- If you save almost nothing — empty layout for empty problem.
- On a shared work machine where IT mandates a different layout (corporate DLP, OneDrive Known Folder Move). Follow the corporate rule first.
- For files that should never have hit `Downloads/` in the first place — `git clone` outputs go in your projects directory; let `Downloads/` be for ad-hoc browser saves only.

## Tree diagram

```
~/Downloads/
├── inbox/              ← browser default; everything lands here
├── archive/            ← occasionally-needed installers, exports
└── _to-process/        ← stuff explicitly waiting on you
```

## Naming rules

1. The three folder names — `inbox/`, `archive/`, `_to-process/` — are fixed. Don't rename them across machines; the muscle memory matters more than aesthetics.
2. The leading underscore on `_to-process/` is deliberate: it sorts after `archive/` and `inbox/` in alphabetical listings, putting the "do later" pile visually last.
3. Inside `inbox/`, do not create subdirectories — the whole point is that you scan a flat list once a week and act on each item.
4. Inside `archive/`, subdivide by purpose only when the flat list exceeds ~50 items: `archive/installers/`, `archive/tax-exports/`, `archive/research-pdfs/`. Avoid `archive/2024/` style date subdivisions unless you find yourself searching by year.
5. Inside `_to-process/`, optionally append a date prefix to the filename (`2026-04-30-tax-doc.pdf`) so you notice items that have lingered too long.
6. Never rename `Downloads/` itself — your browser, mail client, and OS expect that exact path.

## Worked example

`~/Downloads/` has 3,000 files going back seven years, mixing installers, receipts, and half-read PDFs.

1. Create `inbox/`, `archive/`, and `_to-process/` inside it.
2. Move everything old into `archive/legacy-2026-04/` in one command and stop sorting it. If you need something, search there.
3. Point the browser's download location at `~/Downloads/inbox/` (and chat apps if they support it).
4. Once a week, list what's waiting: `find ~/Downloads/inbox -type f -mtime -14 | sort`. For each file, choose: delete, move to its real home (project, `finance/`, `scans/`), or move to `_to-process/` if it needs an action you can't do now.
5. Delete `_to-process/` entries older than a month unless they got done.
6. Reduce inflow: use "ask where to save" for anything that isn't disposable.

Downloads becomes a queue that empties each week.

## Anti-patterns

- **Letting `Downloads/` become a permanent storage tier.** If you find yourself "looking for that PDF I downloaded six months ago" inside `Downloads/`, the system has failed — that file should have been moved to a project tree or `archive/` long ago.
- **Empty triage with no destination.** Triage that moves files from `inbox/` to `archive/` without judgment is just relocation. The point is to delete, file to project, or commit to `_to-process/` with intent.
- **Subdividing `inbox/`.** A subdivided inbox defeats the "one flat list, scan, act" workflow. Keep it flat; subdivide `archive/` instead.
- **Letting `_to-process/` outgrow `inbox/`.** If `_to-process/` has more than ~20 items, you're using it as a graveyard. Run a separate dedicated session: each item gets a do/delete/defer decision.
- **Synchronising `Downloads/` to cloud storage.** Cloud-sync of an inbox produces conflict files (`file (1).pdf`, `file (Hoang's MacBook).pdf`). Sync the destinations (`Documents/`, project trees), not the inbox.
- **Mixing automated rules with the manual layout halfway** — pick one. If you adopt Hazel, write rules for everything; don't leave a manual `inbox/` and a parallel rule-driven flow that argue with each other.

## Scaling & failure modes

- **Installers and ISO files** eat space; delete after installing, and keep only what's hard to fetch again.
- **Auto-cleanup scripts** that delete old files risk removing the only copy; move to `archive/` first and purge from there after a grace period.
- **Multiple browsers/profiles** each have their own download setting; set all of them.
- **Sensitive downloads** (statements, IDs) shouldn't sit in the inbox; file them the same day.

## Variants

- **inbox-archive-toprocess (this guide)** — three folders, manual weekly triage. Best for people who want zero tooling.
- **inbox-only** — single `inbox/` directory; every file is moved to its project or deleted, no `archive/`. Strict, low-overhead, requires discipline.
- **date-stamped-inbox** — `inbox/2026-04/` rolls over monthly so old months become archive candidates. Useful for people whose triage cadence is monthly, not weekly.
- **automation-driven (Hazel/Maid)** — rules sort files at write time by extension, source URL, or filename pattern. No `inbox/` exists; files land in their final home immediately. Highest leverage; highest setup cost.
- **GTD-style with project folders** — `inbox/`, plus `_to-process/` is replaced by project-named folders (`_clientA/`, `_house-purchase/`) for active workstreams. Best when triage often produces multi-item project bundles.

## Adoption checklist

- [ ] Browsers and chat apps save to `~/Downloads/inbox/`.
- [ ] A weekly triage is scheduled and takes under 10 minutes.
- [ ] `_to-process/` items have a monthly expiry.
- [ ] Sensitive documents are filed the day they arrive.
- [ ] The legacy pile is archived, not re-sorted.

## Real-world projects using this

- **Hazel rules (macOS)** — the canonical "automate Downloads" tool; many published rule sets implement an inbox/archive split with software, not folders.
- **Maid** — cross-platform, Ruby-based file-organising tool; rule examples on GitHub mirror the inbox-archive-toprocess pattern.
- **GTD's "physical inbox" pattern (David Allen, _Getting Things Done_)** — the conceptual ancestor. Allen's "in basket" is `inbox/`; the weekly review is the triage step.
- **Many published "dotfiles" repos and personal-Mac setup guides** — search GitHub for "Downloads triage" or "downloads inbox" and you'll find scripts, Keyboard Maestro macros, and Alfred workflows that build on this skeleton.
- **Corporate IT laptop layouts** — managed Macs at large firms often pre-create `~/Downloads/inbox/` plus a Hazel rule set and a quarterly review prompt.

## Migration & references

To migrate an existing `~/Downloads/` to this layout:

```bash
cd ~/Downloads
mkdir -p inbox archive _to-process
# Move everything currently at the top level into inbox for triage
find . -mindepth 1 -maxdepth 1 \
  ! -name inbox ! -name archive ! -name _to-process \
  -exec mv -t inbox/ {} +
```

Then change your browser's default download path to `~/Downloads/inbox/`:

- **Firefox** — `about:preferences` → "Save files to" → choose `~/Downloads/inbox/`.
- **Chrome / Chromium / Edge** — Settings → Downloads → "Location".
- **Safari** — Preferences → General → "File download location".
- **macOS Mail / Outlook** — separate settings; redirect attachment downloads to the same `inbox/`.

For the recurring triage:

- Block 30 minutes on Friday afternoon. Open `~/Downloads/inbox/`, sort by date, decide each file: delete, move to project, archive, or defer to `_to-process/`.
- Once a quarter, do a `_to-process/` clean-out: every item gets a real decision, no parking allowed.

Further reading:

- David Allen — _Getting Things Done_, chapter on "Collect" and the physical inbox pattern.
- Hazel rules library — https://www.noodlesoft.com/manual/hazel/working-with-rules/ (macOS).
- Maid project — https://github.com/benjaminoakes/maid (cross-platform).
- `principles/status-based-organization/` — the "by status, not by topic" idea this guideline builds on.
- `principles/stable-vs-volatile-separation/` — `inbox/` is volatile, `archive/` is stable; the split is an instance of that principle.
