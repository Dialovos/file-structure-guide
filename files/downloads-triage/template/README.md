# Downloads-triage template

A three-folder skeleton for converting `~/Downloads/` from a sprawl into an inbox. Drop the layout into place, point your browser at `inbox/`, and adopt a weekly triage routine.

## What's here

- `inbox/` — every new download lands here. Browser default goes here.
- `archive/` — files you've decided to keep but rarely re-open (installers, exports, reference PDFs).
- `_to-process/` — items that need follow-up action you aren't ready to take this week. Leading underscore sorts it last.
- `.gitkeep` files preserve the empty directories under version control.

## To adopt this template

1. Copy the layout into `~/Downloads/`:
   ```
   cd ~/Downloads
   cp -r /path/to/template/. .
   ```
2. Change your browser's default download location to `~/Downloads/inbox/`:
   - Firefox: `about:preferences` → "Save files to".
   - Chrome / Edge: Settings → Downloads → "Location".
   - Safari: Preferences → General → "File download location".
3. (Optional) configure mail-client and chat-app attachment locations to `~/Downloads/inbox/` as well, so everything funnels into one place.
4. Add a recurring calendar block: "Friday 16:00 — Downloads triage", 30 minutes.
5. Run the routine each cycle: open `inbox/`, decide each file (delete, move to project, archive, defer to `_to-process/`), end with `inbox/` empty.

## What to rename or remove

- The three folder names are intentional and consistent across machines — keep them.
- Add subdirectories under `archive/` only if a flat listing exceeds ~50 items (`archive/installers/`, `archive/research/`).
- Remove `.gitkeep` placeholders once real files arrive.
- Drop this `README.md` once the template has been adopted (the verifier requires it while it lives in this repo).

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.
