## TL;DR

Johnny Decimal (JD) is a hard-capped, ID-based filing system. Your whole life or workspace lives under at most **10 areas**, each numbered as a range like `10-19 life/`. Each area contains at most **10 categories** (`11 home/`, `12 health/`, ...), and each category contains at most **100 items** (`11.01 lease.md`, `11.02 utility-bills.md`). Every file therefore has a unique two-part ID — `11.01` — that you can speak, search, link, or print on a label. The cap is the entire point: when you can't find a place for a new note, the system forces you to either delete something or restructure deliberately, instead of letting the directory tree creep into infinity. The canonical reference is `johnnydecimal.com`, where Johnny Noble has been refining the scheme since 2006.

## Principles & why

JD takes the opposite stance from PARA. Where PARA optimises for low capture friction by giving you four buckets and a permissive interior, JD optimises for *retrieval* and *durability* by giving you an unyielding numeric grid. Three principles:

1. **Hard caps make you think.** Ten areas total. Ten categories per area. One hundred items per category. The caps are intentionally just-too-tight — if you bump up against them, the rule is "rebalance, don't expand". This forces the system to remain comprehensible to your future self ten years from now.
2. **IDs are the true name.** A note's filename starts with its JD ID (`11.01 lease.md`). The ID is permanent; the human-readable suffix can change without breaking links, scripts, or memory. You can speak the ID over the phone ("see one-one-oh-one"), grep for it across machines, even write it on a paper folder.
3. **Two-level, no deeper.** JD is exactly two levels of grouping: area, then category. Items live directly inside categories. The temptation to add a third level (sub-categories) is to be resisted; if a category needs further structure, that's a signal it should be split into two categories at the same level.

The philosophical opposite of "infinite folders" — JD treats your filing system the way an old library treats Dewey Decimal: a fixed grid you live inside, not a tree you grow.

## When to use

- Heavy filers, archivists, paralegals, accountants — anyone whose volume of long-lived documents has previously collapsed loose folder schemes.
- Households or small teams that need a shared, speakable filing convention. "Send me 21.04" is unambiguous in a way "send me the contract" is not.
- People who already track most of life by reference number (case files, project codes) and would rather extend that convention into notes.
- Hybrid digital-and-physical filing: the same `21.04` label goes on the digital file and the matching paper folder.
- Long-lived personal archives where the goal is *findability ten years from now*, not capture velocity today.
- Replacing a directory tree that has grown beyond your ability to mentally model. JD's caps are explicit limits; an unconstrained tree is just hope.

## When NOT to use

- Rapidly evolving project work where the topology shifts weekly. Renumbering is painful and you'll fight the system.
- Atomic-note workflows where the *links* are the structure, not the folders — use [`zettelkasten-classic`](../zettelkasten-classic/), [`folgezettel`](../folgezettel/), or [`evergreen-notes`](../evergreen-notes/).
- Tools that hide filenames (Notion, Bear). JD's whole power is the ID prefix being visible at a glance.
- Capture-heavy workflows where the cost of choosing an ID at write time is too high. Pair JD with an inbox if you must, but pure JD is for *filed* documents, not raw capture.
- Single-domain workspaces. JD's areas are designed for a whole life or whole org; using JD for one project is like using Dewey Decimal for one bookshelf.
- Small archives (< ~200 items). The discipline cost outweighs the benefit until the system has enough volume that linear search hurts.

## Tree diagram

```
vault/
├── 00-09 system/
│   └── 00 index/
│       └── 00.00 index.md
├── 10-19 life/
│   ├── 11 home/
│   │   ├── 11.01 lease.md
│   │   └── 11.02 utility-bills.md
│   └── 12 health/
└── 20-29 work/
    └── 21 client-a/
```

## Naming rules

1. **Areas** are named `XX-YY name/` where `XX-YY` is a 10-number block (`10-19`, `20-29`, ..., `90-99`). The space and lowercase name follow. `00-09` is conventionally reserved for system/meta files (the index, a README, a manual).
2. **Categories** are named `NN name/` where `NN` is the two-digit ID inside the area (`11` is the first category in `10-19`). Categories never repeat; once `11 home/` exists, that ID is taken even if the folder is later emptied.
3. **Items** are named `NN.MM short-name.ext`. `NN` is the category ID, `MM` is a two-digit serial number from `01` to `99` (so technically 99 items per category, not 100 — `00` is reserved). The human suffix is a short hyphenated name for legibility.
4. **`00.00 index.md`** at `00-09 system/00 index/00.00 index.md` is the canonical map of the whole system. Every JD vault has one and you maintain it by hand.
5. **No leading zeroes elsewhere.** Categories `01-09` are valid (e.g. `01 personal/` inside `00-09 system/`), but item IDs always pad to two digits.
6. **Short names use lowercase, hyphens for spaces.** `21.04 q4-tax-return.pdf`, not `21.04 Q4 Tax Return.pdf`. Whitespace between the ID and the name is allowed by convention but optional — pick one and be consistent.
7. **IDs are immutable.** When you rename the human suffix, keep the ID. When you move a file, update its ID — and that move should be rare.

## Worked example

A shared drive has 300 top-level folders and nobody knows where taxes are.

1. List everything at the top level and group into at most 10 areas; write them as ranges: `10-19 life`, `20-29 work`, and so on; reserve `00-09 system` for the index.
2. Under each area, create up to 10 categories, numbered within the range: `11 home`, `12 health`.
3. Inside a category, give each item the next number: `11.01 lease.pdf`, `11.02 utility-bills/`.
4. Write `00.00 index.md` listing every category and notable items with their IDs.
5. Refer to things by ID in chat and notes ("see 12.03"); put the ID in the file name.
6. If a category exceeds 100 items, split the category, never the numbering scheme.

Any file can be found by ID in seconds and the system can't grow into a maze because the caps are hard.

## Anti-patterns

- **Nesting a third level.** `11 home/01 utilities/11.01 electric.md` breaks the two-level rule. Either promote `01 utilities/` into its own category at the area level, or accept that all utility files share `11.0X` IDs.
- **Reusing IDs across areas.** `11.01` and `21.01` are *different* IDs because the category number differs; that's fine. But `11.01` referring to two different files at different times is corruption — old links break silently. Retire IDs, don't recycle them.
- **Inflating category names to evade the cap.** When `15 books/` overflows, splitting into `15 books-fiction/` and `16 books-non-fiction/` is the right move; renaming `15 books/` to `15 reading-material/` and stuffing more in is the wrong one.
- **Putting actual project work in JD.** JD is a *filing* system for long-lived references. Active project workspaces with rapidly changing structure belong in PARA's `1-projects/` or in a code repo.
- **Skipping the index.** `00.00 index.md` is what makes JD navigable without filename tools. A JD vault without a maintained index is just a numerically-prefixed folder dump.
- **Decimal over-precision.** `11.01.03.a` style sub-IDs are not part of canonical JD; they show up in homemade variants and tend to spiral. If you find yourself wanting them, see the `with-decimals` variant or reconsider whether JD is the right system.

## Scaling & failure modes

- **Hard caps feel constraining** at first; that's the mechanism. When something doesn't fit, it's a prompt to reconsider categories, not to extend them.
- **Assigning the first IDs** takes effort; do it once, in an afternoon, and put the index first.
- **Cross-cutting content** doesn't fit a single place; put it where you'd look first and link from the index.
- **Team use** needs one person to own the index, or IDs collide.

## Variants

- **strict-3-digit (this guide).** `XX YY.MM` two-level only. The reference implementation at johnnydecimal.com.
- **with-decimals.** Adds a third tier as letters or numbers (`11.01.a`, `11.01.b`). Useful when items themselves are document bundles. Departs from canonical JD; document the convention if you adopt it.
- **Johnny-Decimal-XL / 4-digit.** Extends to `XX-YY.NNN` for very large archives (legal practice, multi-decade research). Adds capacity at the cost of speakability.
- **JD-with-tags.** JD provides the address; tags or wikilinks provide cross-cutting views. Common when JD lives inside Obsidian.
- **JD-for-projects.** A short-lived JD slice (one area, one or two categories) for a single big project. Drops the "whole life" framing in exchange for the speakable IDs.

## Adoption checklist

- [ ] No more than 10 areas and 10 categories per area.
- [ ] Every item has a unique `AC.NN` ID, and IDs are in file names.
- [ ] `00.00` index exists and is current.
- [ ] Categories over 100 items are split.
- [ ] One person owns index changes if shared.

## Real-world projects using this

- **johnnydecimal.com** — the canonical site, maintained by Johnny Noble. Includes the official rules, examples, and FAQ.
- **JD on GitHub** — searching GitHub for `johnny-decimal` or `johnny decimal` returns dotfile and notes repos that follow the convention publicly.
- **Hacker News threads on JD** — multiple in-depth discussions over the years, including users who've run JD for 5+ years and report on what survived contact with reality.
- **Several public Obsidian vaults** apply JD as the folder layer beneath their notes, often combined with a tag- or MOC-based view for cross-cutting access.

## Migration & references

To start a JD vault from scratch:

```bash
mkdir -p "vault/00-09 system/00 index"
cd vault
cat > "00-09 system/00 index/00.00 index.md" <<'EOF'
# JD index

| ID    | Name      |
| ----- | --------- |
| 00-09 | system    |
| 10-19 | life      |
| 20-29 | work      |
EOF
```

To migrate from a flat or topical scheme:

1. **Inventory the top-level folders** in your current vault. Most fall naturally into 2-3 JD areas (life, work, system); a few outliers go into a 4th.
2. **Sketch the area/category grid before moving any files.** A pencil sketch on paper is faster than fighting with rename commands. Aim for fewer categories than feels comfortable — JD rewards leaving headroom.
3. **Start with the system area.** `00-09 system/00 index/00.00 index.md` is the very first thing you create; it grows alongside the migration.
4. **Migrate the most-referenced files first** so the ID-based muscle memory builds quickly.
5. **Resist the third-level urge** at every step. If a category feels overloaded, the answer is to split it, not to nest.
6. **Maintain the index by hand** as part of every move. The index is the system; without it the IDs are noise.

Further reading and adjacent guides:

- https://johnnydecimal.com — canonical site, with the rules and a worked example.
- The JD Discord / community space (linked from the site) — discussions of edge cases and variants.
- [`para`](../para/) — a softer, four-bucket alternative; some people use PARA at the active layer and JD at the archival layer.
- [`zettelkasten-classic`](../zettelkasten-classic/) — for atomic-note workflows that JD's two-level grid doesn't fit.
- [`folgezettel`](../folgezettel/) — another ID-based scheme but optimised for branching thought rather than filing.
