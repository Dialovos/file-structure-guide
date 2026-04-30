# Versioning-in-paths template

A two-sided template: a small `good/` tree showing canonical filenames, and a
deliberately-named `bad-do-not-do-this/` tree carrying the anti-pattern with
a comment explaining why it's wrong. Use the contrast as a teaching aid in
your own repo.

## What's here

- `good/config.yaml` — canonical config; no version suffix; history lives in git.
- `good/api-spec.md` — canonical spec; same rule. Includes a "Versioning policy" section that documents *where* versioning happens (URL namespace) and *where it doesn't* (this file).
- `bad-do-not-do-this/config_v2.yaml` — a `_v2`-suffixed copy with a long comment block explaining what's wrong and the migration steps to fix it.

## To adopt this template

1. Copy `good/` into your repo (rename as appropriate). The names — `config.yaml`, `api-spec.md` — should be what your project actually calls them.
2. **Do not copy** `bad-do-not-do-this/`. It exists in this template purely as a negative example. Leaving it in your real repo would defeat the entire principle.
3. Adapt the file contents: replace the example app/service config with your real fields.
4. Search your existing repo for the anti-pattern — see the audit script in `../GUIDE.md` under "Migration & references".

## What to rename, fill, delete

- **Rename**: `config.yaml` and `api-spec.md` to whatever your project's canonical names are (`docker-compose.yaml`, `openapi.yaml`, `proposal.md` — whatever).
- **Fill**: replace the placeholder content with real config / real spec content.
- **Delete**: the entire `bad-do-not-do-this/` directory before committing this template into your project. It's a teaching artifact, not production content.

## Migration if you already have versioned filenames

If you found `config_v1.yaml`, `config_v2.yaml`, `config_v2_FINAL.yaml` in your tree:

1. Identify which is the canonical version (usually the most recent).
2. `git mv config_v2_FINAL.yaml config.yaml`.
3. `git rm config_v1.yaml config_v2.yaml`.
4. Tag previous releases if needed: `git tag v1.0.0 <old-sha>`.
5. Update any references (CI, docs, deploy scripts) that pointed at the old names.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this file to exist. Don't delete it before replacing.
