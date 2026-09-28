# workspace-root-layout — template

A workspace skeleton with the standard top-level folders, a map README, and a shared `AGENTS.md`.

## What to rename

- The folder name `workspace/` to whatever you prefer

## What to fill

- `README.project-example.md` — copy to `README.md` and edit the map
- `AGENTS.md` — your real rules

## What to delete

- Top-level folders you will never use (keep the set small)

## First run

```bash
cp -r template ~/workspace
cd ~/workspace && ls -A
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../../../principles/monorepo-vs-polyrepo/` — why projects are separate repositories
