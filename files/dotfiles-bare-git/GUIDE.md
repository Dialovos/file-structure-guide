# Dotfiles via bare git repo

## TL;DR

Manage `~/.bashrc`, `~/.config/`, and the rest of your dotfiles using a plain git repository whose `.git` directory lives at `~/.dotfiles/` (a *bare* git directory) and whose work-tree is `$HOME`. A shell alias — conventionally `dotfiles` — runs `git --git-dir=$HOME/.dotfiles --work-tree=$HOME`. The result: your home directory becomes a git work-tree without forcing every file into it. You set `status.showUntrackedFiles=no` so `git status` doesn't drown in noise. No symlinks, no extra tooling, no templating — just git. Atlassian's "Storing your dotfiles in a Bare Git Repository" guide popularised the pattern; many SREs and Drew DeVault use it because it survives platform changes that break heavier dotfile managers.

## Principles & why

The pattern leans on three properties of git that aren't widely used together.

1. **A bare git directory is just metadata.** Setting `--git-dir` to any path lets git operate on a work-tree elsewhere. There's no requirement that `.git` sit inside the work-tree.
2. **A work-tree of `$HOME` is legal.** Git doesn't care that `$HOME` contains thousands of files it knows nothing about — as long as you tell it not to recurse into them by default. `core.worktree` plus `status.showUntrackedFiles=no` makes this practical.
3. **An alias hides the awkward invocation.** Typing `git --git-dir=$HOME/.dotfiles --work-tree=$HOME status` every time would be unusable. `alias dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'` makes the workflow `dotfiles add ~/.bashrc && dotfiles commit -m "..."`.

The benefit over symlink-based managers (`stow`, `rcm`, custom scripts) is that there is no symlink farm to corrupt, no extra file format to learn, and no second binary to install. The benefit over chezmoi is simplicity: if you don't need templating or secrets, you don't need a tool. The cost is that your home directory must be a place where git operations are safe — no accidental `git add -A` from the wrong working directory.

## When to use

- Single-user, often single-machine setups where you want a versioned record of your dotfiles without templating.
- You're already a heavy git user and want zero new tools to learn.
- You're comfortable with `git status` showing only tracked-file changes, which means you accept that you'll never see "untracked file" warnings unless you explicitly ask.
- Servers or VMs where adding a Go/Python/Rust binary (chezmoi, dotbot) is friction; `git` is already there.
- Bootstrap scripts that need to clone-and-checkout in a single one-liner: `git clone --bare <url> ~/.dotfiles && dotfiles checkout`.

## When NOT to use

- Multiple machines with **different** values needing different content (e.g. work email vs personal email in `~/.gitconfig`). Bare git has no templating; you'd need branches or per-host commits, which gets messy. Use **chezmoi** instead.
- You need **secrets management** (SSH keys, API tokens) committed alongside dotfiles. Bare git plus `git-crypt` works but is fiddly; chezmoi+1Password or chezmoi+age is cleaner.
- You want to symlink-enable individual modules (only sync `nvim/` on this machine). `stow`, `rcm`, or chezmoi handle that better.
- You collaborate on dotfiles with others — the bare-git approach has only one home directory in mind. Shared/team dotfiles want a normal repo plus a bootstrap script that copies/symlinks.
- You routinely do destructive `git` operations and don't trust yourself to keep `dotfiles` and plain `git` separate. The cost of running `git reset --hard HEAD` in `$HOME` once is enormous.

## Tree diagram

```
$HOME/
├── .dotfiles/          ← the bare git dir
├── .bashrc             ← tracked
├── .config/
│   ├── git/config      ← tracked
│   └── nvim/init.lua   ← tracked
└── (everything else gitignored by default)
```

## Naming rules

1. The bare repo is conventionally named `.dotfiles/` and lives at `$HOME/.dotfiles/`. It is *not* a normal `.git` directory inside a work-tree; it is a top-level bare repo whose work-tree happens to be `$HOME`.
2. The shell alias is conventionally `dotfiles` (or `dot`, `cfg`, `dfm` — pick one and stick with it). Defined in `~/.bashrc`/`~/.zshrc`: `alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'`.
3. `core.worktree` inside `~/.dotfiles/config` should be set to `$HOME` (or left unset if you always pass `--work-tree`).
4. `status.showUntrackedFiles=no` should be set inside `~/.dotfiles/config` so `dotfiles status` only reports tracked-file changes.
5. Tracked files retain their natural names — `.bashrc`, `.config/git/config`, `.ssh/config`. There is no `dot_*` rename layer (that's chezmoi's convention).
6. The bootstrap script that creates `~/.dotfiles/` and the alias is conventionally `setup.sh` or `bootstrap.sh`, kept in the repo root for new machines.

## Anti-patterns

- **Running `dotfiles add -A` or `dotfiles add .` from `$HOME`** — would attempt to track tens of thousands of files. Always add by explicit path: `dotfiles add ~/.bashrc`.
- **Forgetting `status.showUntrackedFiles=no`** — `dotfiles status` becomes useless under a wall of "untracked" lines. Set the flag during bootstrap.
- **Initialising `.dotfiles/` as non-bare** — `git init` (not `git init --bare`) inside `~/.dotfiles/` puts a real work-tree there and breaks the pattern. Always `git init --bare`.
- **Confusing `dotfiles` and `git`** — running plain `git add` inside `$HOME` may pick up the *wrong* repo if you have a stray `.git/` somewhere else. Use the alias exclusively for dotfile work.
- **Tracking secrets unencrypted** — bare git is plain git: a private SSH key committed and pushed to GitHub is a leak. Never track unencrypted credentials; use `git-crypt`, `age`, or a separate non-git secrets store.
- **Symlinking `~/.dotfiles/` into the repo** — the bare directory is the repo. Symlinking it sideways adds a layer that breaks `git`'s assumptions about its own metadata layout.
- **Letting tracked files diverge from the actual file** — running `dotfiles checkout` is the only way to apply changes. Edit-the-file-then-commit is fine; never edit a copy elsewhere and expect git to notice.

## Variants

- **Bare-with-symlinks (legacy)** — bare repo plus a script that symlinks tracked files from elsewhere. Predates the `--work-tree=$HOME` trick. Avoid for new setups.
- **Pure-bare (this guide)** — repo at `~/.dotfiles/`, work-tree at `$HOME`, alias for ergonomics. The simplest form.
- **Bare-with-stow** — bare repo at `~/.dotfiles/<module>/`; `stow` symlinks each module into `$HOME`. Best for "enable nvim on this host, skip kitty". More moving parts.
- **Bare-with-git-crypt** — pure-bare plus `git-crypt init` to encrypt SSH keys and API tokens at rest. Solves the secrets problem without leaving git.
- **Bare-with-bootstrap-Makefile** — pure-bare plus a `Makefile` of post-checkout steps (install Homebrew packages, set macOS defaults). Pushes setup beyond just file checkout.

## Real-world projects using this

- **Atlassian Developer Blog** — "The best way to store your dotfiles: A bare Git repository" by Nicola Paolucci, 2016. The most-cited writeup of the pattern.
- **Drew DeVault's dotfiles** — `~drew/dotfiles` on `git.sr.ht`, uses the bare pattern; long-time maintainer of `sourcehut`.
- **Many SRE/devops dotfile repos on GitHub** — search for "bare git dotfiles" or "dotfiles --bare". The `git-bare-dotfiles` topic on GitHub aggregates dozens of public examples.
- **harfbuzz maintainer Behdad Esfahbod's dotfiles** — uses a `git --git-dir=... --work-tree=$HOME` alias.
- **Numerous "Atlassian-style" dotfile bootstrap scripts** circulating in HN, lobsters, and Reddit `/r/unixporn` posts since 2016.

## Migration & references

To bootstrap from scratch on a new machine:

```bash
# Initialise the bare repo
git init --bare $HOME/.dotfiles

# Define the alias for this session
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'

# Persist the alias
echo "alias dotfiles='/usr/bin/git --git-dir=\$HOME/.dotfiles/ --work-tree=\$HOME'" >> ~/.bashrc

# Quiet untracked-file noise
dotfiles config --local status.showUntrackedFiles no

# Start tracking files
dotfiles add ~/.bashrc
dotfiles commit -m "Add bashrc"
dotfiles remote add origin git@github.com:<you>/dotfiles.git
dotfiles push -u origin main
```

To clone onto a fresh machine:

```bash
git clone --bare git@github.com:<you>/dotfiles.git $HOME/.dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
# Move conflicting existing files out of the way, then:
dotfiles checkout
dotfiles config --local status.showUntrackedFiles no
```

Migrating from `stow`, `rcm`, or a symlink farm:

1. Copy each existing tracked file from its real location into `$HOME` (overwriting the symlink).
2. `dotfiles add <path>` for each.
3. Remove the old `~/dotfiles/` work-tree directory (or keep it as a backup until you're confident).

Further reading:

- Atlassian guide — "The best way to store your dotfiles" (2016).
- Hacker News thread "Storing dotfiles in a bare git repo" — search HN by title; multiple iterations on the pattern.
- `git help worktree` — a different feature with a similar name; not what this pattern uses.
- `files/dotfiles-chezmoi/` — the templated alternative when bare git isn't enough.
- `principles/hidden-files-policy/` — why `~/.dotfiles/` and `~/.bashrc` are dotfiles in the first place.
- `files/xdg-base-directory/` — where to put new dotfiles you create today (`~/.config/<app>/`, not `~/.<app>rc`).
