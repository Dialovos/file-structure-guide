#!/usr/bin/env bash
# setup.sh — bootstrap a bare-git dotfiles repo at $HOME/.dotfiles
#
# What this does:
#   1. Initialises a *bare* git repo at $HOME/.dotfiles
#   2. Sets core.worktree=$HOME so git operations target the home directory
#   3. Sets status.showUntrackedFiles=no so `dotfiles status` is usable
#   4. Appends the `dotfiles` alias to ~/.bashrc (skips if already present)
#
# Usage:  ./setup.sh   (run once on a new machine)
# Idempotent: re-running is safe; existing config is left in place.

set -euo pipefail

DOTFILES_DIR="${DOTFILES_DIR:-$HOME/.dotfiles}"
BASHRC="$HOME/.bashrc"
ALIAS_LINE="alias dotfiles='/usr/bin/git --git-dir=\$HOME/.dotfiles/ --work-tree=\$HOME'"

# 1. Initialise the bare repo if it doesn't already exist
if [[ ! -d "$DOTFILES_DIR" ]]; then
  echo "[setup] initialising bare repo at $DOTFILES_DIR"
  git init --bare "$DOTFILES_DIR"
else
  echo "[setup] $DOTFILES_DIR already exists, skipping init"
fi

# 2. Configure the bare repo
echo "[setup] configuring core.worktree and status.showUntrackedFiles"
git --git-dir="$DOTFILES_DIR" --work-tree="$HOME" config --local core.worktree "$HOME"
git --git-dir="$DOTFILES_DIR" --work-tree="$HOME" config --local status.showUntrackedFiles no

# 3. Append the alias to ~/.bashrc if not already present
if ! grep -Fq "alias dotfiles=" "$BASHRC" 2>/dev/null; then
  echo "[setup] appending dotfiles alias to $BASHRC"
  printf '\n# bare-git dotfiles repo\n%s\n' "$ALIAS_LINE" >> "$BASHRC"
else
  echo "[setup] dotfiles alias already in $BASHRC, skipping"
fi

cat <<EOF

[setup] done.

Next steps:
  source ~/.bashrc                          # or open a new shell
  dotfiles status                           # verify the alias works
  dotfiles add ~/.bashrc                    # start tracking files
  dotfiles commit -m "Add bashrc"
  dotfiles remote add origin <your-repo>    # optional
  dotfiles push -u origin main              # optional
EOF
