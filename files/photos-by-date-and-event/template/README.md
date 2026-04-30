# Photos by date and event template

An empty-tree skeleton showing the two coexisting bucket types: a monthly bucket for daily-life shots, and a dated event directory.

## What's here

- `2026/2026-04/` — the monthly bucket for everyday shots in April 2026.
- `2026/2026-04-15-example-event/` — a placeholder event directory; rename with the real event slug or delete and create a new one.

`.gitkeep` files preserve the empty shape so the structure can be cloned or copied without losing directories.

## To adopt this template

1. Copy the structure into your photo root: `cp -r template/ ~/Pictures/` or `cp -r template/ /mnt/photos/`.
2. Configure your import tool (Lightroom, digiKam, darktable, Apple Photos export) to emit `%Y/%Y-%m/` directories on import.
3. After import, look at the just-imported month bucket and decide:
   - All shots are an event → rename the month directory to `YYYY-MM-DD-<slug>/`.
   - Shots are a mix of event + daily life → leave most in the month bucket and `mv` the event shots into a new `YYYY-MM-DD-<slug>/`.
4. Don't rename individual files; let cameras and EXIF handle that.

## What to rename or remove

- Rename `example-event/` to a real event slug (`2026-04-15-spring-walk`) or delete it and create new event directories as you need them.
- Add new month buckets (`2026-05/`, `2026-06/`) as the year progresses; they don't need to be pre-created.
- Delete `.gitkeep` files once a directory has at least one real photo.
- Drop this `README.md` once the template has been adapted (the verifier requires it while it lives in this repo).

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until you no longer need the template.
