## TL;DR

A **Git worktree** is an additional working directory attached to the same repository, so you can have several branches checked out at once, without stashing, re-cloning, or losing your build state. Give worktrees a predictable home: keep the **main checkout** where it is (`myapp/`) and put every extra worktree in a **sibling directory named after the repository** (`myapp.worktrees/<branch>/`), or inside the repository in a gitignored `.worktrees/` folder. One worktree per branch or task; **create with `git worktree add`, remove with `git worktree remove`**, and prune stale entries. Each worktree has its own working files, index, and (usually) its own dependency directories and virtual environments, but shares the object database, so it costs little disk and needs no network. It is especially useful for reviewing a pull request while your own work continues, running a long test on one branch while coding on another, and letting AI coding agents work on separate branches in parallel without stepping on each other.

## Principles & why

1. **One branch, one directory.** Git refuses to check out the same branch in two worktrees, which prevents the most common mistake: editing the same branch state in two places.
2. **Shared history, separate working state.** Worktrees share commits and branches, but each has its own files, index, and `HEAD`. Changes in one are invisible in the others until committed.
3. **Predictable location beats clever location.** A fixed convention for where worktrees live means you can find, list, and clean them up; scattered worktrees turn into forgotten directories.
4. **Worktrees are disposable.** They exist for a task. When the branch is merged or abandoned, remove the worktree (the branch itself is a separate decision).
5. **Environments are per worktree.** Dependency directories (`node_modules/`, `.venv/`) and build outputs don't transfer between worktrees; plan for one environment per worktree, or share caches.
6. **Worktrees are not submodules or clones.** Don't nest independent repositories inside worktrees, and don't use worktrees to separate different projects.

## When to use

- **Working on several branches at once** without stashing: a feature, a hotfix, and a review.
- **Reviewing pull requests** in a real checkout while your own work stays untouched.
- **Long-running builds or tests** on one branch while you continue on another.
- **Parallel AI coding agents**, each in its own worktree and branch, to avoid conflicting edits.
- **Comparing behavior across versions**, by keeping a release branch checked out beside `main`.

## When NOT to use

- **Multiple unrelated projects.** Each project is its own repository (see `workspace-root-layout`).
- **Repositories with huge dependency setup** where each worktree needs gigabytes of `node_modules` or a slow build; consider a shared cache or a single checkout with quick branch switches.
- **Long-lived parallel copies** of a branch you'd rather keep as a separate release repository.
- **Shallow, quick branch switches**, where `git switch` is faster and simpler than a second directory.

## Tree diagram

```
Sibling layout (recommended):

projects/
├── myapp/                         ← main checkout (usually main)
│   ├── .git/                      ← the real repository
│   └── src/
└── myapp.worktrees/               ← every extra worktree lives here
    ├── feature-login/             ← branch feature/login
    ├── fix-timeout/               ← branch fix/timeout
    └── review-pr-482/             ← temporary, for reviewing a pull request

In-repository layout (alternative):

myapp/
├── .git/
├── .gitignore                     ← contains `.worktrees/`
├── .worktrees/                    ← gitignored
│   └── feature-login/
└── src/

Bare-repository layout (advanced):

myapp/
├── .bare/                         ← bare repository
├── .git                           ← file pointing to .bare
├── main/                          ← worktree
└── feature-login/                 ← worktree
```

## Naming rules

- **The worktree parent** is `<repo>.worktrees/` beside the repository, or `.worktrees/` inside it (gitignored); choose one convention for all repositories.
- **Worktree directories** are the branch name with slashes replaced by dashes (`feature/login` becomes `feature-login/`), so they are flat and shell-friendly.
- **Temporary review trees** use a clear prefix (`review-pr-482/`), which signals that they can be removed freely.
- **Branch names** follow your usual convention (`feature/...`, `fix/...`); don't put the machine or person in the branch name to distinguish worktrees.
- **Never reuse a directory name** for a different branch without removing the old worktree first.
- **Environment directories** stay inside each worktree with their usual names (`.venv/`, `node_modules/`) and are gitignored (see `gitignore-and-keep-files`).

## Worked example

You're mid-feature on `feature/login` when a teammate asks for an urgent review of pull request 482, and a hotfix is also due.

1. From the main checkout, list what exists: `git worktree list`.
2. Create a worktree for the review: `git fetch origin pull/482/head:review-pr-482 && git worktree add ../myapp.worktrees/review-pr-482 review-pr-482`. (On GitHub, `gh pr checkout 482` inside a worktree also works.)
3. Open that directory, install dependencies, and run tests there; your feature work is untouched in the main checkout.
4. For the hotfix: `git worktree add -b fix/timeout ../myapp.worktrees/fix-timeout origin/main`. Fix, commit, push, and open the pull request from that directory.
5. Return to your feature; your uncommitted changes never moved.
6. Clean up when the pull requests are merged or reviewed: `git worktree remove ../myapp.worktrees/review-pr-482` (add `--force` only if you are sure you don't need uncommitted changes), then `git branch -d review-pr-482`. Run `git worktree prune` to remove records of directories that were deleted by hand.
7. Check the result: `git worktree list` should show only what you're still using.

Three tasks proceeded in parallel with no stashing and no re-cloning.

## Anti-patterns

- **Deleting a worktree directory with `rm -rf`** instead of `git worktree remove`. Git keeps a stale record; run `git worktree prune`, and remember that uncommitted work is gone.
- **Scattering worktrees** across the disk. Use one parent directory per repository so you can find and clean them.
- **Forgotten worktrees** that accumulate and hold branches from months ago. Review `git worktree list` regularly.
- **Trying to check out the same branch twice.** Git prevents it for good reason; create a new branch (`-b`) or detach (`--detach`).
- **Nested independent repositories** or submodules inside worktrees, which confuse both Git and tooling.
- **Sharing a virtual environment or `node_modules`** across worktrees. Tools embed absolute paths; give each worktree its own environment or use a shared package cache.
- **Sync clients over worktree directories.** Don't place them in cloud-sync folders (see `cloud-sync-structure`).

## Scaling & failure modes

- **Many parallel tasks or agents**: use a naming convention with task IDs (`fix-1234-timeout`), a script to create them, and a scheduled cleanup for merged branches (`git branch --merged`).
- **Disk use**: worktrees share objects but duplicate working files and environments; large repositories multiply quickly. Use sparse checkout or shallow worktrees where supported, and share package caches.
- **Tooling and editors**: IDEs treat each worktree as a separate project; open each in its own window, and exclude the `.worktrees/` folder from the main project's indexing.
- **Hooks and config**: hooks and most config are shared through the main repository's `.git`, so a hook path setting applies to all worktrees; per-worktree config is available if enabled (`extensions.worktreeConfig`).
- **CI and scripts**: scripts that assume the repository root is `.git`'s parent must use `git rev-parse --show-toplevel`, because in a linked worktree `.git` is a file.
- **Locking**: `git worktree lock` protects worktrees on removable or network storage from being pruned.

## Variants

- **Sibling layout** (this guide): `<repo>.worktrees/<branch>/` beside the repository.
- **In-repository `.worktrees/`**: convenient, must be gitignored, and some tools scan into it.
- **Bare repository plus worktrees**: no privileged main checkout; every branch is a worktree. Cleaner for people who always work in parallel, but unusual for tools that expect a normal clone.
- **Temporary worktrees** in a system temp directory for a single review or test run, deleted when done.
- **Agent-managed worktrees**: coding tools that create and remove a worktree per task; apply the same naming and cleanup conventions.

## Adoption checklist

- [ ] All worktrees for a repository live under one parent directory following one naming convention.
- [ ] `git worktree list` shows only worktrees you are actively using.
- [ ] Worktrees are removed with `git worktree remove`, not by deleting directories.
- [ ] Each worktree has its own environment (`.venv/`, `node_modules/`), or a shared cache is configured.
- [ ] The worktree parent (if inside the repository) is gitignored.
- [ ] Merged branches and their worktrees are cleaned up regularly.

## Real-world projects using this

- **The Git documentation** (the `git worktree` manual page) describes `add`, `list`, `remove`, `prune`, `lock`, and the shared-object model.
- **AI coding tools** increasingly use worktrees to isolate parallel agent sessions; their documentation describes per-task worktree creation and cleanup.

## Migration & references

- **From multiple clones of the same repository:** confirm nothing unpushed lives in the extra clones (`git status`, `git log origin/main..`), create worktrees for the branches you still need, and delete the extra clones after verifying content.
- **From stash-heavy workflows:** replace `git stash` around interruptions with a worktree for the interruption.
- **To a bare layout:** clone with `git clone --bare <url> .bare`, create the `.git` pointer file, and add worktrees for `main` and each active branch.
- **References:**
  - `files/workspace-root-layout/` for where repositories live.
  - `principles/gitignore-and-keep-files/` for ignoring `.worktrees/`.
  - `principles/generated-vs-source-separation/` for per-worktree environments and build output.
  - `files/project-archive/` for retiring finished projects.
