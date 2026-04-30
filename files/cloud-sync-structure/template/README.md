# Cloud-sync-structure template

A skeleton for namespacing every cloud-sync provider under `~/cloud/<provider>/`. Drop into `$HOME`, reconfigure each sync client to point its root at the matching subdirectory, and the layout is in place.

## What's here

- `dropbox/` — placeholder for Dropbox sync root.
- `icloud/` — placeholder for iCloud Drive (or a symlink to `~/Library/Mobile Documents/com~apple~CloudDocs/` on macOS, since Apple does not allow relocation).
- `google-drive/` — placeholder for Google Drive for Desktop.
- `.gitkeep` files preserve the empty directories under version control. Replace as you populate real content.

## To adopt this template

1. Copy the layout into place:
   ```
   cp -r template/ ~/cloud/
   ```
   or `mkdir -p ~/cloud/{dropbox,icloud,google-drive}`.
2. For each provider you actually use:
   - **Dropbox** — Preferences → Sync → "Dropbox folder location" → `~/cloud/dropbox/`.
   - **OneDrive** — Settings → Account → "Choose folders" / "Unlink", re-add at `~/cloud/onedrive/`.
   - **Google Drive for Desktop** — Preferences → "Google Drive" tab → folder location → `~/cloud/google-drive/`.
   - **Box Drive** — Preferences → Box folder → `~/cloud/box/`.
   - **iCloud Drive (macOS)** — cannot be relocated. Symlink instead:
     ```
     ln -sfn "$HOME/Library/Mobile Documents/com~apple~CloudDocs" ~/cloud/icloud
     ```
3. Inside each provider directory, create purpose-named subdirectories (`shared-with-spouse/`, `work-handoff/`, `archive/`).
4. Update any backup tool's exclude/include paths to use `~/cloud/<provider>/` patterns.
5. Update editor "open recent" muscle memory and any scripts that referenced `~/Dropbox/` etc.

## What to rename or remove

- Remove `dropbox/`, `icloud/`, or `google-drive/` if you don't use that provider.
- Add a directory for any provider you do use that isn't here (`onedrive/`, `box/`, `proton-drive/`, `mega/`, etc.).
- Inside each provider, replace `.gitkeep` with real purpose subdirectories (`shared-with-spouse/`, `work-handoff/`).
- Drop this `README.md` once the template has been adopted (the verifier requires it while it lives in this repo).

## Caveats

- **Quit the sync client before moving its folder.** Mid-flight relocation corrupts state on every provider tested.
- **iCloud Drive cannot be relocated on macOS.** Use a symlink. Test the symlink with `ls -la ~/cloud/icloud/` to confirm it resolves.
- **Corporate-managed clients (managed OneDrive, enterprise Dropbox)** may have admin-locked paths. Check with IT before relocating.
- **Don't put git repos inside `~/cloud/`.** Sync clients corrupt `.git/` directories under heavy churn. Use a real git remote.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.
