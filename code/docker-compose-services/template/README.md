# docker-compose-services — template

A working two-service stack (a tiny web service plus a cache) with base and development override files.

## What to rename

- `services/web/` and the `web` service name to your real services

## What to fill

- `.env` (copy from `.env.example`) — real values
- `services/web/Dockerfile` — your runtime and dependencies

## What to delete

- The example `web` service and the `redis` service if you don't need them

## First run

```bash
cp .env.example .env
docker compose up --build
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../../../principles/config-and-secrets-placement/` — environment files
