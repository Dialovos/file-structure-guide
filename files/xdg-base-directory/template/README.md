# XDG Base Directory template

An empty-tree skeleton that mirrors the four canonical XDG roots inside the user's home. The directories are present but contain no real configs — copy the shape into `$HOME` and let your tools populate it.

## What's here

- `.config/` — for files YOU edit (the dotfiles you'd put under version control).
- `.local/share/` — for files TOOLS write that you want to keep (databases, downloaded models, Steam libraries).
- `.local/state/` — for files TOOLS write that you don't actively edit (logs, shell history, last-known-window-position).
- `.cache/` — for files that can be rebuilt automatically on next run.

Each directory contains a `.gitkeep` placeholder so the empty shape survives a `git add`.

## To adopt this template

1. Make sure the four XDG variables are exported in your shell init (typically `~/.bashrc`, `~/.zshrc`, or `~/.config/fish/config.fish`):
   ```bash
   export XDG_CONFIG_HOME="$HOME/.config"
   export XDG_DATA_HOME="$HOME/.local/share"
   export XDG_STATE_HOME="$HOME/.local/state"
   export XDG_CACHE_HOME="$HOME/.cache"
   ```
2. Create the four roots in your real `$HOME` if they do not exist already: `mkdir -p ~/.config ~/.local/share ~/.local/state ~/.cache`.
3. As you install or migrate tools, drop each tool's directory under the matching root (e.g. `~/.config/nvim/`, `~/.local/share/nvim/`, `~/.cache/nvim/`).
4. If you maintain a dotfiles repo, target only `~/.config/` (and selected `~/.local/share/` subdirs) — never sync `~/.cache/`.

## What to rename or remove

- Nothing here is named for a specific tool, so there are no renames.
- Delete the four `.gitkeep` files once the corresponding directory has at least one real config tree inside it.
- This `README.md` is verifier-required while the template lives in this repo. Drop it once you've copied the structure into your own home.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep this file in place until you no longer need the template.
