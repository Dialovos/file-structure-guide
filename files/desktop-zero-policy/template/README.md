# Desktop-zero-policy template

This template ships *only* the staging area, not the Desktop itself. The whole point is that `~/Desktop/` should remain empty — the "content" of the Desktop is its emptiness, and there's nothing meaningful to put in a template directory for an empty thing.

## What's here

- `desktop-staging/.gitkeep` — placeholder for the sibling-of-Desktop staging area. Real staging-session subdirectories (`2026-04-29-from-desktop/`, etc.) appear inside this directory as needed.

That's it. There is intentionally no `Desktop/` subdirectory in this template, because the rule is *not* "create a Desktop directory" — your OS already has one — it's "keep your existing `~/Desktop/` empty".

## To adopt this template

1. Copy the staging directory into your home: `cp -r template/desktop-staging ~/`. (You're copying just the `desktop-staging/` directory, not nesting under `template/`.)
2. Sweep your current Desktop into a dated staging subdir to start fresh:
   ```bash
   DATE=$(date +%Y-%m-%d)
   mkdir -p ~/desktop-staging/${DATE}-from-desktop
   mv ~/Desktop/* ~/desktop-staging/${DATE}-from-desktop/ 2>/dev/null
   ```
3. Redirect every default that targets Desktop:
   - **Screenshots** — see `files/screenshots-auto-flow/` for the OS-specific defaults.
   - **Downloads** — set browser/OS download default to `~/Downloads/`, never Desktop.
   - **"Save to Desktop"** prompts in apps — choose a real destination instead.
4. Within 24 hours of anything landing on Desktop, move or delete it. Use `desktop-staging/` only for genuinely-transient files.
5. Schedule a monthly purge of staging:
   ```bash
   find ~/desktop-staging -mindepth 1 -maxdepth 1 -type d -mtime +30 -exec rm -rf {} +
   ```

## What "empty" means

- **Strict-empty:** `ls ~/Desktop` produces no output (or only `.DS_Store` on macOS, which is OS-managed and you can ignore or hide via shell config).
- **Allow-N variant:** up to 5 icons with a weekly sweep — looser but easier.
- **Staging-only variant:** allow only `~/Desktop/inbox/` to exist; everything else in `inbox/` gets cleared weekly.

Pick one variant and stick with it. Switching modes weekly defeats the calming effect.

## What to rename or remove

- Delete the `.gitkeep` once `desktop-staging/` has real session directories.
- Drop this `README.md` once the template has been adapted (the verifier requires it while it lives in the repo).

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.

## Why no `Desktop/` directory in this template

A `Desktop/` placeholder would be self-defeating: shipping a directory whose canonical state is empty teaches the wrong lesson. Your OS already provides `~/Desktop/`; this template provides only the *additional* infrastructure (`desktop-staging/`) that the policy depends on.

## The 24-hour rule

The shortest discipline that actually holds: anything that lands on the Desktop must be moved or deleted within 24 hours. It's not arbitrary — past 24 hours, you forget why the file is there, and within a week it becomes invisible scenery you never act on. The 24-hour SLA exists because that's how long your *intent* about the file stays fresh.
