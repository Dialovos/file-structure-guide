# Folgezettel index

A flat-directory slip box where note IDs encode the lineage of an idea. This index lists the root threads only — the children unfold by ID.

## Threads

- [[1 example-root]] — the first thread; refinements as `1a`, `1b`, ...
- [[2 second-thread]] — an unrelated thread.

## How to add a note

1. Decide whether the new note continues an existing thread or starts a new one.
2. If continuing: pick the parent (e.g. `1a`) and add the next available child suffix (`1a1`, `1a2`, ...).
3. If starting a new thread: use the next integer (`3`, `4`, ...) and add a row here.
4. Filename format: `<ID> <slug>.md` (single space) or `<ID>-<slug>.md` (dash). Pick one and stick with it.

## How to read a thread

- Open the root (`1`).
- Children appear adjacent in filename order: `1a`, `1a1`, `1a2`, `1b`, `2`.
- The IDs left-to-right walk back up to the root: `1a1 → 1a → 1`.
