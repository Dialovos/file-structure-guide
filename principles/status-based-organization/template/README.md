# Status-based organization template

A copy-paste skeleton for a portfolio organized by lifecycle status. The three
directories (`active/`, `archive/`, `someday/`) are the structural commitment;
fill them with your actual projects.

## What's here

- `active/` — empty, with `.gitkeep` so the directory survives git. This is where live work lives. One subdir per in-flight project.
- `archive/2025/` — the year-bucketed archive, pre-seeded for the current year. Add older years as you accumulate them (`archive/2024/`, `archive/2023/`).
- `someday/` — empty, with `.gitkeep`. The deliberate "good idea, not now" pile. Different from a wishlist: items here would actually get worked on if priorities shifted.

## To adopt this template

1. Copy the whole directory into your repo: `cp -r template/ <your-repo>/projects/` (renaming the destination as appropriate).
2. Delete the `.gitkeep` files in any directory that already has a real project inside — they're just placeholders.
3. Move existing projects into `active/`, `archive/<year>/`, or `someday/` based on their current status. The principle: status is *where it lives*, not a filename suffix.
4. If you don't need `someday/`, delete it. The minimal variant is `active/` + `archive/` only.
5. As projects finish, move their directories into `archive/<current-year>/`. Don't rename them with `_done` or `_archived` suffixes — the path is the status.

## What to rename, fill, delete

- **Rename**: nothing in this template needs renaming. The `active/`, `archive/`, `someday/` names are the convention.
- **Fill**: put real project directories inside `active/` and `archive/<year>/`. Each project is itself a subtree (its own `README.md`, files, etc.).
- **Delete**: the `.gitkeep` files once a directory has real content. `someday/` itself if you don't use that variant.

## Maintenance rhythm

- Quarterly sweep: move stale items out of `active/`. A directory there with no commits in 90 days is probably done or paused.
- Annual rollover: when a year ends, the next year's `archive/<year>/` directory gets created lazily — first time you archive something from that year.
- `someday/` review: skim every few months. Items you'd no longer commit to: delete. Items priorities now allow: promote to `active/`.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this `README.md` to exist. Don't delete it before replacing with your own intro.
