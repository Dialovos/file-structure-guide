# Naming-conventions template

A tiny tree showing the kebab-case rule and the documented-exception pattern.

## What's here

- `good-example/` — a kebab-case directory. Endorsed default: lowercase, hyphen-separated, ASCII only.
- `bad-rename-this/` — placeholder name. Pretend it was originally `BadRenameThis/` or `bad_rename_this/`. Rename it to whatever your real concept is in kebab-case.
- `python-package-snake-exception/` — illustrates a documented ecosystem exception. Inside a Python project this directory would actually be `customer_onboarding/` (snake_case) because the directory name is the import path. The kebab-case slug here is just the *placeholder* for the slot; real Python packages must keep snake_case and the project's `CONTRIBUTING.md` should record the deviation.

## To adopt this template

1. Copy the directory into your repo: `cp -r template/ <your-target>/`.
2. Rename `good-example/` to whatever your first feature folder is (still kebab-case).
3. Delete `bad-rename-this/`. It exists only to demonstrate the renaming workflow:
   ```bash
   git mv BadRenameThis bad-rename-this   # if you find one of these in the wild
   ```
4. Decide if you need `python-package-snake-exception/`. If you have no Python (or .NET, or Java) subtree, delete it. If you do, rename it to your real package and add a note to that subtree's `CONTRIBUTING.md` explaining why it doesn't follow kebab-case.
5. Delete this `README.md` last (or replace it with your own per-directory readme — see `principles/readme-placement/`).

## Verifier check

After copying, the verifier in `docs/superpowers/scripts/verify-guideline.sh` checks that this `template/README.md` exists. Don't delete it before you've replaced it.
