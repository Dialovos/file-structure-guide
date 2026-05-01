# Screenshots-auto-flow template

A skeleton for the inbox-triage-archive screenshot flow. Three directories, three states.

## What's here

- `inbox/.gitkeep` — empty directory placeholder. After OS-config, every screenshot you take lands here automatically.
- `reference/.gitkeep` — destination for triaged keepers. Subdivide by *purpose*, not by date: `reference/api-design-snippets/`, `reference/ui-inspiration/`.
- `archive/2026-04/.gitkeep` — long-term storage for screenshots you no longer actively reference. One directory per `YYYY-MM/`.

The `.gitkeep` files exist only because git does not track empty directories. Delete them once real content arrives.

## To adopt this template

1. Copy the structure into your Pictures directory: `cp -r template/ ~/Pictures/Screenshots/` (the contents — not nesting it under `template/`).
2. Configure your OS to save screenshots into `inbox/`:

   **macOS:**
   ```bash
   defaults write com.apple.screencapture location ~/Pictures/Screenshots/inbox
   killall SystemUIServer
   ```

   **Windows:** Settings > System > Storage > Advanced > "Where new content is saved" → set screenshots destination, or configure your screenshot tool (ShareX, Greenshot, Snipping Tool) to point at `inbox/`.

   **Linux:** Configure `gnome-screenshot`, Flameshot, or Spectacle to save to `~/Pictures/Screenshots/inbox/`.

3. Schedule a weekly triage reminder. Open `inbox/`, decide for each file: delete, or move to a purpose-named `reference/<slug>/` subdirectory.
4. Migrate stale `reference/` subdirectories (untouched for 6+ months) into `archive/YYYY-MM/`.

## The triage flow

```
[capture] → inbox/ → [weekly triage] → reference/<purpose>/  (keep)
                                    ↘ delete                  (most cases)

[no use for 6+ months] → archive/YYYY-MM/
```

The bias is toward *delete*. If you can't label a screenshot in 5 seconds during triage, you don't need it.

## What to rename or remove

- Delete the `.gitkeep` files once each directory has real content.
- Add new `archive/YYYY-MM/` directories monthly as old `reference/` material ages out.
- Add `reference/<purpose>/` subdirectories as new visual-reference threads emerge.
- Drop this `README.md` once the template has been adapted (the verifier requires it while it lives in the repo).

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.

## Auto-cleanup

A safe weekly cron to age out anything in the inbox older than 14 days (the assumption being that if you didn't triage it in two weeks, you don't want it):

```bash
find ~/Pictures/Screenshots/inbox -type f -mtime +14 -delete
```

Run it manually first to verify it doesn't catch anything you wanted to keep, *then* schedule it.
