# engineering-work-log — template

A work-log skeleton with daily, weekly, wins, meetings, incidents, and projects templates.

## What to rename

- Year and week numbers in the sample filenames

## What to fill

- `log/YYYY/` — add one file per working day from the daily template
- `wins/` — accomplishments with impact and links

## What to delete

- Folders you don't use (for example `incidents/` if you're not on call)

## First run

```bash
cp templates/daily.md log/2026/$(date +%F).md
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../daily-weekly-notes/` — the rhythm
