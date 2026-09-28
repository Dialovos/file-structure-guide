# monorepo-vs-polyrepo — template

A starting point for recording the repository-boundary decision and enforcing ownership inside a monorepo.

## What to rename

- `acme-` prefix in `README.md` and `CODEOWNERS` to your organization's prefix

## What to fill

- `README.md` — the placement rule and the decision date
- `CODEOWNERS` — one line per directory with a real owner

## What to delete

- `packages/` or `apps/` entries you don't use, once you know the shape

## First run

```bash
git init && git add . && git status  # then push and confirm CODEOWNERS review requests appear
```

## Pair this with

- `../GUIDE.md` — the decision criteria
- `../../../code/turborepo-monorepo/` — JavaScript monorepo tooling
