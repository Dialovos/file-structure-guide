# Dotfiles-chezmoi template

A minimal but realistic chezmoi source tree showing the project's most-used naming conventions: `dot_*` for leading-dot targets, `private_*` for 0600/0700 modes, `*.tmpl` for templated content, and `.chezmoiignore` for conditional exclusion.

## What's here

- `dot_bashrc` — literal (non-templated) example. Renders to `~/.bashrc`.
- `dot_config/git/config.tmpl` — templated git config. Renders to `~/.config/git/config` with `{{ .name }}`, `{{ .email }}`, and per-OS credential helper.
- `dot_config/nvim/init.lua` — minimal Neovim config stub. Renders to `~/.config/nvim/init.lua`.
- `private_dot_ssh/config.tmpl` — SSH config; renders to `~/.ssh/config` at mode 0600 inside `~/.ssh/` at mode 0700. Demonstrates per-host conditional blocks.
- `.chezmoiignore` — example ignore file with Go-template conditionals for platform-specific files.
- `README.md` — this file.

## Naming convention quick reference

| Source-tree name              | Target after `chezmoi apply` | Notes                                    |
| ----------------------------- | ---------------------------- | ---------------------------------------- |
| `dot_bashrc`                  | `~/.bashrc`                  | leading dot rendered                     |
| `dot_config/git/config.tmpl`  | `~/.config/git/config`       | `.tmpl` stripped after rendering         |
| `private_dot_ssh/config.tmpl` | `~/.ssh/config` (0600)       | parent dir 0700, file 0600               |
| `executable_dot_local/bin/x`  | `~/.local/bin/x` (0755)      | mode +x                                  |
| `encrypted_dot_age.key`       | `~/.age.key` (decrypted)     | requires age/gpg config                  |

## To adopt this template

1. Install chezmoi (https://www.chezmoi.io/install/):
   ```
   brew install chezmoi              # macOS
   sudo pacman -S chezmoi            # Arch
   sh -c "$(curl -fsLS get.chezmoi.io)"  # any Unix
   ```
2. Initialise the chezmoi source directory and copy this template into it:
   ```
   chezmoi init                              # creates ~/.local/share/chezmoi/
   cp -r template/. ~/.local/share/chezmoi/
   ```
3. Configure chezmoi data (`chezmoi edit-config` opens `~/.config/chezmoi/chezmoi.toml`):
   ```
   [data]
   name    = "Your Name"
   email   = "you@example.com"
   profile = "personal"          # or "work"
   ```
4. Preview the changes chezmoi will make to your home directory:
   ```
   chezmoi diff
   ```
5. Apply:
   ```
   chezmoi apply
   ```
6. Check in to git:
   ```
   chezmoi cd
   git init && git add -A && git commit -m "Initial dotfiles"
   git remote add origin git@github.com:<you>/dotfiles.git
   git push -u origin main
   ```

## Editing workflow

- `chezmoi edit ~/.bashrc` — opens the source file (`dot_bashrc`) in your editor.
- `chezmoi diff` — shows what would change on apply.
- `chezmoi apply` — writes the rendered files into `$HOME`.
- `chezmoi update` — `git pull` in the source tree, then `chezmoi apply`.
- `chezmoi cd` — opens a shell in `~/.local/share/chezmoi/`.

## What to rename or remove

- Edit `dot_bashrc`, `dot_config/git/config.tmpl`, etc., to match your real configuration.
- Add `*.tmpl` to any file that needs per-machine variation, and replace literal values with `{{ .name }}` etc.
- Add `private_` to anything that should be mode 0600 (SSH keys, AWS profile, GPG agent config).
- Remove sections of `.chezmoiignore` you don't need.
- Drop this `README.md` once the template has been adopted (the verifier requires it while it lives in this repo).

## Cloning onto a new machine

```bash
chezmoi init --apply git@github.com:<you>/dotfiles.git
```

That single command clones, prompts for any missing `chezmoi.toml` data, and applies. No follow-up steps.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.
