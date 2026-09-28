# XDG Base Directory

## TL;DR

Stop letting tools dump dotfiles into `$HOME`. Put configuration under `$XDG_CONFIG_HOME` (`~/.config`), persistent app data under `$XDG_DATA_HOME` (`~/.local/share`), regenerable caches under `$XDG_CACHE_HOME` (`~/.cache`), volatile state under `$XDG_STATE_HOME` (`~/.local/state`), and per-session sockets under `$XDG_RUNTIME_DIR`. Your home directory becomes browsable again, backups become trivially scoped, and ricers can swap configs by symlinking one tree.

## Principles & why

The XDG Base Directory Specification exists for one reason: every Unix tool used to drop its own `~/.toolname/` dotfile or dotdir into `$HOME`, and home turned into landfill. The spec splits files by *intent* rather than *owner* — you do not back up cache, you do back up config, and runtime sockets are session-scoped — so a single layout can drive backup policy, sync rules, and reset workflows.

It also separates *what the user customises* (config) from *what the program writes back* (state, data). A common bug fixed by XDG is: a tool stores both your edits and its own derived index in the same `~/.toolname/`, so version-controlling the dir means tracking churn. With XDG, `~/.config/tool/` is yours to track in dotfiles; `~/.local/share/tool/` and `~/.cache/tool/` stay out of git.

Finally, the spec is environment-driven. A tool that respects XDG can be redirected per-invocation by exporting `XDG_CONFIG_HOME=/tmp/throwaway-config`, which is what every test harness, container, and `nix run` shim relies on.

## When to use

- Every Linux-leaning desktop or workstation setup. Treat XDG as the default and exceptions as the noise.
- Any CLI or TUI you author that touches the filesystem — read XDG vars first, fall back to the documented defaults, never hardcode `~/.toolname/`.
- Dotfiles repos managed with bare-git, GNU Stow, chezmoi, or yadm — they all map cleanly onto `~/.config/`.
- Containers and ephemeral environments — set `XDG_CONFIG_HOME` and `XDG_CACHE_HOME` to mounted paths to make state explicit and resettable.
- Multi-user shared hosts — XDG paths are per-user by construction, so you avoid `chown` surprises on shared `~/.local/`.

## When NOT to use

- Tools whose ecosystems hardcoded a different home before XDG existed — `~/.aws/`, `~/.ssh/`, `~/.docker/`, `~/.gnupg/`, `~/.kube/`. These predate the spec; their entire tooling chain reads the legacy path. Forcing them into `~/.config/` breaks third-party integrations and rarely buys anything.
- Apps that ship Electron config in `~/Library/Application Support` (macOS) or `%APPDATA%` (Windows) — the OS already provides an analog; do not retrofit XDG on top.
- Servers and daemons with system-wide config — `/etc/` is the right place; XDG is user-scoped.
- One-shot scripts where a relative `./.cache/` next to the script is clearer than reaching into the home tree.
- Tools whose maintainer has explicitly rejected XDG — opening an issue is reasonable; monkey-patching is not.

## Tree diagram

```
$HOME/
├── .config/
│   ├── git/config
│   ├── nvim/init.lua
│   └── alacritty/alacritty.toml
├── .local/
│   ├── share/        ← apps' data files
│   └── state/        ← logs, history, last-known-state
└── .cache/           ← throwaway, regenerable
```

## Naming rules

1. Each tool gets exactly one subdirectory under each XDG root, named for the tool in lowercase kebab-case (`~/.config/neovim/`, not `~/.config/Neovim/` or `~/.config/nvim_config/`).
2. Inside a tool's dir, follow that tool's own conventions — XDG dictates the *root*, not the *interior*. `~/.config/git/config` (not `~/.config/git/.gitconfig`) because the leading dot is no longer load-bearing.
3. Cache files under `~/.cache/<tool>/` must be safely deletable at any time; if your tool cannot rebuild on next launch, it does not belong in cache.
4. State files (history, last-window-position, undo files) go under `~/.local/state/<tool>/` so they are excluded from dotfiles tracking but preserved across reboots.
5. Runtime files (sockets, pid files, lock files) go under `$XDG_RUNTIME_DIR` (typically `/run/user/$UID/`); these are wiped at logout.
6. When a single tool produces both user-edited and tool-managed files, split them: editable in `config/`, tool-managed in `data/` or `state/`.

## Worked example

`ls -A ~` shows 60 dot entries, and you don't know which are configuration and which are cache.

1. Export the variables (most systems set them already; defaults are `~/.config`, `~/.local/share`, `~/.cache`, `~/.local/state`).
2. Find offenders: `ls -A ~ | grep '^\.'`, or run `xdg-ninja` for tool-specific advice.
3. Move what the tool supports: set env vars in your shell profile, for example `export HISTFILE="$XDG_STATE_HOME/bash/history"`, `export CARGO_HOME="$XDG_DATA_HOME/cargo"`, `export npm_config_userconfig="$XDG_CONFIG_HOME/npm/npmrc"`.
4. Move the existing data before the change, or the tool starts from scratch.
5. Delete `~/.cache` safely as a test; if something breaks, that tool stored state in the wrong place.
6. Scope backups: back up `~/.config` and `~/.local/share`, skip `~/.cache`, and decide about `~/.local/state`.

The home directory shrinks, and backups know what matters.

## Anti-patterns

- **Conflating cache and data** — putting search indexes in `~/.local/share/` means restoring a backup also restores stale indexes; putting your songs in `~/.cache/` means a `rm -rf ~/.cache` deletes irreplaceable content.
- **Hardcoding `~/.config`** — read `$XDG_CONFIG_HOME` first and only fall back to the default. Tests and containers depend on this.
- **One tool, two homes** — some apps drop both `~/.toolname/` and `~/.config/tool/`. Pick one (XDG) and remove the other.
- **Putting secrets under `~/.config/`** — anything with a credential belongs in `~/.local/share/<tool>/` with `chmod 600`, not in a directory you sync via dotfiles git.
- **Tracking `~/.cache/` in dotfiles** — by definition cache is regenerable, so versioning it is churn for no benefit.
- **Symlinking `~/.config/` from a synced cloud drive** — file-watch APIs and atomic-rename behaviour break across many sync layers; link individual subtrees instead.

## Scaling & failure modes

- **Tools that ignore XDG** need env vars, symlinks (use sparingly), or acceptance; don't fight tools that offer no option.
- **State vs data**: logs, history, and last-known-state go in `$XDG_STATE_HOME`; treat it as semi-disposable.
- **Multiple users and containers**: variables may be unset in cron or minimal environments; use defaults in scripts (`${XDG_CONFIG_HOME:-$HOME/.config}`).
- **Portability**: on Windows and macOS the same tools use different native locations.

## Variants

- **Strict XDG** — every tool moved, including legacy holdouts via wrappers (`alias git='git -c …'`, `GNUPGHOME=$XDG_DATA_HOME/gnupg`). Maximal hygiene; highest maintenance.
- **Pragmatic XDG** — move what moves easily, leave `~/.aws/` and `~/.ssh/` alone. Default for most users; matches the Arch Wiki's tracker recommendations.
- **XDG with legacy shims** — keep legacy paths but symlink them into XDG roots so backup policy is unified (`ln -s ~/.aws ~/.local/share/aws`). Useful when a backup tool only walks `~/.local/`.
- **Per-host XDG roots** — set `XDG_CONFIG_HOME=~/.config/$(hostname)` for cross-host config divergence; less common, but powerful for fleet-managed laptops.
- **Container-local XDG** — set all four roots to `/workspace/.xdg/` inside a container so state lives with the project, not the user.

## Adoption checklist

- [ ] Shell profile sets the four variables (or relies on documented defaults).
- [ ] Scripts use `${XDG_...:-default}` fallbacks.
- [ ] `~/.cache` can be deleted without data loss.
- [ ] Backups include config and data, exclude cache.
- [ ] Remaining `$HOME` dotfiles are known exceptions.

## Real-world projects using this

- **freedesktop.org** — the canonical specification; current revision 0.8 (2021), maintained alongside the rest of the freedesktop suite.
- **Neovim** — reads `$XDG_CONFIG_HOME/nvim/init.lua` and writes shada/state under `$XDG_STATE_HOME/nvim/`.
- **Alacritty** — config at `$XDG_CONFIG_HOME/alacritty/alacritty.toml`.
- **ripgrep** and **bat** — both read `$XDG_CONFIG_HOME/<tool>/config`.
- **systemd user units** — `$XDG_CONFIG_HOME/systemd/user/` is the documented user-unit directory.
- **Arch Wiki "XDG Base Directory" page** — community-maintained tracker of which tools support XDG, with workarounds for those that do not.

## Migration & references

To migrate an existing home tree, work tool-by-tool. For each `~/.toolname/`:

```bash
# Example: relocate a hypothetical tool's config under XDG
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/toolname"
mv ~/.toolname/config "${XDG_CONFIG_HOME:-$HOME/.config}/toolname/"
```

Set the four core variables in your shell init so child processes inherit them:

```bash
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_DATA_HOME="$HOME/.local/share"
export XDG_STATE_HOME="$HOME/.local/state"
export XDG_CACHE_HOME="$HOME/.cache"
```

Further reading:

- freedesktop.org "XDG Base Directory Specification" — the formal spec.
- Arch Linux Wiki "XDG Base Directory" — practical compliance tracker per tool.
- `principles/stable-vs-volatile-separation/` — the underlying split that XDG codifies.
- `files/dotfiles-bare-git/` and `files/dotfiles-chezmoi/` — version-control patterns that pair with XDG.
- `files/unix-fhs/` — system-wide layout; XDG is the user-scoped analog.
