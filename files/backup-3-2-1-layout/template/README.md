# backup-3-2-1-layout — template

A backup-plan directory: path lists, a restic-based script, a manifest, and a restore-test log. Nothing here contains secrets; configure repositories through environment variables.

## What to rename

- Repository names in `manifest.md` to your real locations

## What to fill

- `backup-paths.txt` — what to back up, relative to your home directory
- `manifest.md` — where each copy lives
- Environment variables `RESTIC_REPOSITORY` and `RESTIC_PASSWORD_FILE` (in your scheduler, not in git)

## What to delete

- Example paths and exclusions that don't apply to you

## First run

```bash
restic init  # once per repository, with RESTIC_REPOSITORY set
./backup.sh
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../../cloud-sync-structure/` — why sync is not backup
