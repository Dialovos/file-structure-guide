#!/usr/bin/env bash
# Create a worktree for a branch in the sibling <repo>.worktrees/ directory.
# Usage: new-worktree.sh <branch> [base]   (base defaults to main)
set -euo pipefail

branch="${1:?usage: new-worktree.sh <branch> [base]}"
base="${2:-main}"

repo_root="$(git rev-parse --show-toplevel)"
repo_name="$(basename "$repo_root")"
dest="$(dirname "$repo_root")/${repo_name}.worktrees/${branch//\//-}"

if git show-ref --verify --quiet "refs/heads/${branch}"; then
  git worktree add "$dest" "$branch"
else
  git worktree add -b "$branch" "$dest" "$base"
fi
echo "worktree ready: $dest"
