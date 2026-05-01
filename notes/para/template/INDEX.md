# PARA index

This vault is organised around Tiago Forte's PARA scheme. Every note lives in exactly one of the four numbered buckets at the root.

## The four buckets

- **1-projects/** — short-term efforts with an explicit finish line. Each project is its own folder named after the outcome (e.g. `q2-redesign/`, `learn-rust/`). When done, move the folder into `4-archive/`.
- **2-areas/** — ongoing standards or roles you maintain (e.g. `health/`, `finance/`, `home/`). No end date. If an area genuinely retires (you no longer rent that apartment), move it to `4-archive/`.
- **3-resources/** — reference material you might consult later. Topical names are fine here (`design-references/`, `papers-on-attention/`). Prune anything untouched in a year.
- **4-archive/** — finished projects, retired areas, and stale resources. Sub-organised by year (`2024/`, `2025/`) or by source bucket — pick one and be consistent.

## How to decide where a new note goes

Ask: *is this driving an active outcome with a deadline?*

- Yes → `1-projects/<project>/`.
- No, but it's something I'm responsible for keeping current → `2-areas/<area>/`.
- No, just reference → `3-resources/<topic>/`.
- It used to belong in 1 or 2, but the work is done → `4-archive/`.

## Weekly review

Every week, walk through the four buckets:

1. Did any project finish? Move the folder to `4-archive/<year>/`.
2. Are all areas still current? Retire any that aren't.
3. Did any resource graduate into a project (you started actively using it)? Move it.
4. Skim the top of `4-archive/` for anything that should come back.

## Conventions in this vault

- File names use lowercase-hyphenated words, except dates which use `YYYY-MM-DD`.
- Each project folder usually contains a `README.md` describing the outcome and a list of artefacts.
- Each area folder usually contains a `README.md` describing the standard you're maintaining.
- Wikilinks (`[[note-title]]`) are preferred over relative paths so notes survive moves between buckets.
