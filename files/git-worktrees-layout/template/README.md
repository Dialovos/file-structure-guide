# git-worktrees-layout — template

A helper script that creates a worktree in the sibling `<repo>.worktrees/` directory, plus an ignore snippet for the in-repository variant.

## What to rename

- Branch naming in `new-worktree.sh` if you use a different convention

## What to fill

- Copy `new-worktree.sh` into your tools directory or a repository's `scripts/`

## What to delete

- `gitignore-snippet.txt` if you use the sibling layout (nothing to ignore)

## First run

```bash
./new-worktree.sh feature/login   # run from inside the repository
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../../workspace-root-layout/` — where repositories live
