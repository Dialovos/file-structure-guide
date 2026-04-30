# Project archive template

An empty-tree skeleton for `active/` + `archive/<year>/<project>/`. Use it to bootstrap a personal `projects/` directory, a consulting-work folder, or a research-lab code root.

## What's here

- `active/` — your live projects live here. The directory is empty by default; populate as projects start.
- `archive/2025/example-finished-project/` — placeholder showing the year-bucket shape and one example finished-project directory.

`.gitkeep` files preserve the empty shape so the structure can be checked into git or cloned freshly.

## To adopt this template

1. Copy the structure into your projects root: `cp -r template/ ~/projects/` (or `~/code/`, `~/work/`, etc.).
2. Drop new projects into `active/<project-slug>/`. Use kebab-case for project names, optionally prefixed with a quarter or release tag (`q2-redesign/`, `v3-migration/`).
3. When a project finishes or pauses, move it to `archive/<year-of-retirement>/<same-slug>/`:
   ```bash
   mkdir -p archive/$(date +%Y)
   git mv active/q2-redesign archive/$(date +%Y)/
   ```
4. If `projects/` is itself a git repo, commit the move with a one-line message (`chore: archive q2-redesign`) so the move shows up in history.

## What to rename or remove

- Rename `example-finished-project/` to a real archived project, or delete it once you have at least one real entry.
- Add new year directories (`archive/2026/`, `archive/2027/`) as needed; they don't have to be pre-created.
- Delete `.gitkeep` files once a directory holds real content.
- Drop this `README.md` once the template has been adapted (the verifier requires it while the template lives in this repo).

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep this file in place until you no longer need the template.
