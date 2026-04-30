# Dotfiles-bare-git template

Real (functional) starter files for adopting the bare-git dotfiles pattern. Copy this template into place, run `setup.sh`, and you have a working dotfiles repo at `~/.dotfiles/` plus a `dotfiles` shell alias.

## What's here

- `setup.sh` — runnable bootstrap script. Initialises `~/.dotfiles/` as a bare repo, sets `core.worktree=$HOME` and `status.showUntrackedFiles=no`, appends the `dotfiles` alias to `~/.bashrc`. Idempotent — safe to re-run.
- `bashrc-snippet.sh` — the single alias line that goes in `~/.bashrc`. `setup.sh` adds it automatically; this file is here for reference if you'd rather paste it manually.
- `gitignore-template` — example `~/.gitignore` patterns to keep `dotfiles status` and explicit `dotfiles add` paths from picking up caches, history files, and secrets.
- `README.md` — this file.

## To adopt this template

1. Copy the template into place (anywhere temporary is fine):
   ```
   cp -r template/ ~/dotfiles-template/
   cd ~/dotfiles-template/
   ```
2. Make `setup.sh` executable and run it:
   ```
   chmod +x setup.sh
   ./setup.sh
   ```
3. Open a new shell (or `source ~/.bashrc`) so the `dotfiles` alias is loaded.
4. Verify the setup:
   ```
   dotfiles status
   ```
   You should see `On branch master / nothing to commit (working tree clean)` and *no* untracked-file noise.
5. (Optional) drop `gitignore-template` to `~/.gitignore` and tell git about it:
   ```
   cp gitignore-template ~/.gitignore
   dotfiles config --local core.excludesFile $HOME/.gitignore
   ```
6. Start tracking files explicitly:
   ```
   dotfiles add ~/.bashrc
   dotfiles add ~/.config/git/config
   dotfiles commit -m "Initial dotfiles"
   ```
7. Push to a remote when ready:
   ```
   dotfiles remote add origin git@github.com:<you>/dotfiles.git
   dotfiles push -u origin main
   ```

## What to rename or remove

- Edit `setup.sh` if you want a different alias name (e.g. `dot`, `cfg`) or a different bare-repo location (e.g. `~/.cfg/`).
- Edit `gitignore-template` to suit your machine — remove patterns for tools you don't use, add patterns for ones you do.
- After adoption, delete this `template/` directory; everything you need is in `~/.dotfiles/` and `~/.bashrc`.
- Drop this `README.md` once the template has been used (the verifier requires it while it lives in this repo).

## Cloning onto a new machine

Once your repo lives on a remote:

```bash
git clone --bare git@github.com:<you>/dotfiles.git $HOME/.dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
# Resolve any conflicts with files already in $HOME, then:
dotfiles checkout
dotfiles config --local status.showUntrackedFiles no
```

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.
