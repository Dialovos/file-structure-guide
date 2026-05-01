# Second Brain — CODE workflow + PARA storage

Tiago Forte's CODE pipeline (Capture / Organize / Distill / Express)
on top of PARA folders. See `../GUIDE.md` for the full reasoning.

## Layout

```
vault/
├── 0-inbox/         ← Capture
├── 1-projects/      ← Organize (PARA — active w/ deadlines)
├── 2-areas/         ← Organize (PARA — ongoing responsibilities)
├── 3-resources/     ← Organize (PARA — topical libraries)
├── 4-archive/       ← Organize (PARA — inactive)
├── distilled/       ← Distill output (intermediate packets)
└── output/          ← Express (drafts, posts, talks)
```

The numbered prefixes (`0-` through `4-`) keep the inbox + PARA
folders sorted at the top of every file picker. `distilled/` and
`output/` sit alongside without numbers, signaling workflow stages
rather than storage.

## Mapping CODE (verbs) → folders (nouns)

| Stage    | Verb                       | Lives in            |
|----------|----------------------------|---------------------|
| Capture  | Save it cheaply, anywhere  | `0-inbox/`          |
| Organize | Sort by actionability      | `1-projects/`–`4-archive/` |
| Distill  | Progressive summarization  | `distilled/`        |
| Express  | Compose into deliverables  | `output/`           |

## Weekly review (the loop that keeps it alive)

1. **Process `0-inbox/`** — every item moves to PARA, `distilled/`, or trash.
2. **Audit `1-projects/`** — anything without a near-term deadline → `2-areas/` or `4-archive/`.
3. **Re-read** something in `distilled/` or `3-resources/` — bold sentences, highlight a subset, write a 2-3 line summary at the top.
4. **Ship something to `output/`** — even a small piece. The Express habit is what keeps the system alive.

## PARA decision rule (Forte's heuristic)

When organizing, ask: **"Is this actionable?"**

- Active goal w/ deadline → `1-projects/`
- Ongoing responsibility (no deadline) → `2-areas/`
- Topic of interest, no current action → `3-resources/`
- None of the above → `4-archive/`

Topic is *not* the deciding question. Actionability is.

## What's in this template

- Seven empty folders (each with `.gitkeep`) — the CODE+PARA skeleton.
- This README — the workflow walkthrough.

## Adding your first content

1. Drop a captured article or note into `0-inbox/some-source.md`.
2. During weekly review, decide: is this for an active project?
   `1-projects/<project>/`. An ongoing area? `2-areas/<area>/`. A
   library topic? `3-resources/<topic>/`. None of those? `4-archive/`.
3. When you re-read a source and bold/highlight it, the resulting
   "intermediate packet" gets a copy in `distilled/`.
4. When you write a piece, draft in `output/<deliverable>.md`.

## Pair this with

- `../../para/` — PARA storage in depth.
- `../../atomic-notes/` — atomic discipline at the leaf level (BASB
  calls these "intermediate packets").
- `../../maps-of-content/` — useful for stitching `3-resources/`
  topics together.
