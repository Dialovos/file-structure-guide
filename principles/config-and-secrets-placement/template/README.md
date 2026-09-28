# config-and-secrets-placement — template

A minimal, safe config layout: committed defaults, a documented example environment file, and ignore rules that keep real values out of git.

## What to rename

- `ACME_` in `.env.example` and `config/default.yaml` to your application prefix

## What to fill

- `.env.example` — every variable your code reads, with no values
- `config/default.yaml` — non-secret defaults

## What to delete

- Variables and config keys your project doesn't use

## First run

```bash
cp .env.example .env  # then fill in real values locally; never commit .env
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../../gitignore-and-keep-files/` — ignore patterns
