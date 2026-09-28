# Dotfiles via chezmoi

## TL;DR

Chezmoi manages dotfiles by keeping a *source* tree at `~/.local/share/chezmoi/` whose filenames encode the metadata git can't (file mode, leading dots, secrecy, templating). Files starting with `dot_` render as `.foo` after `chezmoi apply`; `private_*` chmods to 600; `executable_*` chmods to +x; `*.tmpl` files are run through Go's text/template with chezmoi-supplied data and secret references. The result: a *single source* you can sync across many machines, where per-host content (work email vs home email, GUI vs headless) is conditionally rendered, and secrets pull in from 1Password / Bitwarden / age at apply time. Heavier than bare git, but pays for itself the moment you have two machines or one secret.

## Principles & why

Chezmoi exists because plain git plus symlinks can't express three things dotfiles routinely need:

1. **Per-machine variation.** Your work laptop's `~/.gitconfig` needs your work email; your personal desktop needs your personal email. Hand-maintained branches drift. Templates render the right value at apply time based on `chezmoi data`.
2. **Secrets references, not committed secrets.** API keys, SSH keys, and tokens must not live in a public dotfiles repo. Chezmoi templates can call `{{ onepasswordRead "op://Personal/GitHub/api-key" }}` or `{{ bitwarden "github" }}`, fetching the value at apply time without committing the secret.
3. **Mode and visibility encoded in filenames.** Git stores file mode as 644 / 755; it cannot store "this file should be 600". Chezmoi's `private_*` prefix maps to chmod 600 on apply. The `dot_*` prefix lets the source tree itself look like normal directories (no leading dots) for ergonomic editing while still rendering as `.bashrc` on the target.

The trade-off versus bare git: chezmoi is a Go binary you must install, and its naming convention takes a day or two of muscle-memory cost. The gain is that you stop maintaining parallel `gitconfig.work` / `gitconfig.home` files by hand and stop worrying about whether you accidentally committed a token.

## When to use

- Multiple machines (work laptop, personal desktop, home server, VM, container) where the same logical dotfile must produce different content.
- Any dotfile that references a secret you don't want in plain git — SSH config, AWS profile, GitHub tokens.
- Teams or households where one person curates a "house style" dotfile repo that others apply with their own data.
- Bootstrap scenarios where one command — `chezmoi init <repo>` followed by `chezmoi apply` — must turn an empty home directory into a configured one.
- Mixed-platform setups (macOS + Linux, sometimes WSL) where templates discriminate on `{{ .chezmoi.os }}`.
- Cases where you want pre/post-apply hooks (run `mise install`, refresh a Homebrew bundle) tied to dotfile changes.

## When NOT to use

- Single-machine, single-secret-free setups where bare git suffices. The templating and secret system is overhead you don't need.
- You're allergic to Go templates — chezmoi's template syntax is `{{ .name }}`, `{{ if eq .chezmoi.os "darwin" }}...{{ end }}`. If you'd rather not learn it, look at `yadm` (a thinner alternative).
- Restricted environments where you can't install third-party binaries — chezmoi must be present to apply, and bootstrap on a fresh box without it is slightly more work than `git clone`.
- Dotfile repos under heavy collaborative editing — chezmoi's source-tree naming (`dot_`, `private_`, `.tmpl`) is one more thing newcomers must learn.
- You only need *one* feature chezmoi provides (e.g. only secrets) and prefer a focused alternative — `git-crypt` for secrets-only, `stow` for module enablement-only, `dotbot` for hook-only.

## Tree diagram

```
~/.local/share/chezmoi/
├── .chezmoiignore
├── dot_bashrc
├── dot_config/
│   ├── git/
│   │   └── config.tmpl     ← templated, references chezmoi data
│   └── nvim/
│       └── init.lua
└── private_dot_ssh/
    └── config.tmpl
```

## Naming rules

1. **`dot_<name>`** in the source tree maps to `.<name>` in `$HOME` after apply. So `dot_bashrc` becomes `~/.bashrc`. This lets the source tree look like a normal directory for editing.
2. **`private_<name>`** sets the resulting file's mode to 0600 (or directory mode 0700). Applied recursively. Use for `private_dot_ssh/`, AWS profile, etc.
3. **`executable_<name>`** sets mode 0755 — for scripts and helpers like `executable_dot_local/bin/myscript`.
4. **`<name>.tmpl`** is rendered through Go templates with chezmoi data. Strip `.tmpl` from the target name. So `dot_gitconfig.tmpl` → `~/.gitconfig`.
5. **`empty_<name>`** allows the file to be applied even when its template renders to empty (otherwise chezmoi treats empty as "skip").
6. **`encrypted_<name>`** is encrypted at rest using the configured method (gpg, age). Decrypted on apply.
7. **`.chezmoiignore`** at the source root is a Go-template-aware ignore file (`.git/`, `**/*.swp`, OS-specific ignores). Lines can be templated to ignore platform-specific files.
8. **`.chezmoidata.<format>`** holds chezmoi data variables (`name`, `email`, custom keys) accessible inside templates via `{{ .name }}`.
9. The conventional source root is `~/.local/share/chezmoi/`. Override with `--source` or `~/.config/chezmoi/chezmoi.toml`.

## Worked example

Two machines share a git config, but one has a different email and the other needs an extra SSH host.

1. `chezmoi init` creates the source tree at `~/.local/share/chezmoi/`.
2. Add files: `chezmoi add ~/.bashrc ~/.config/nvim/init.lua`. They appear as `dot_bashrc` and `dot_config/nvim/init.lua`.
3. Make the git config a template: `chezmoi add --template ~/.config/git/config`, then use data: `email = {{ .email }}` and a per-machine value in `~/.config/chezmoi/chezmoi.toml` under `[data]`.
4. Handle machine differences inline with `{{ if eq .chezmoi.hostname "workstation" }}...{{ end }}`.
5. Preview before writing: `chezmoi diff`, then `chezmoi apply`.
6. Commit from `chezmoi cd` and push. On the new machine: `chezmoi init --apply <user>/dotfiles`.
7. For secrets, use a password-manager integration (or `age` encryption), never plaintext in the repo.

One repo produces the right config on each machine.

## Anti-patterns

- **Editing files at the target (`~/.bashrc`) instead of the source.** Changes will be reverted on the next `chezmoi apply`. Always edit via `chezmoi edit ~/.bashrc` or directly in the source tree.
- **Committing rendered secrets** — running `chezmoi apply` produces `~/.ssh/config` with the resolved token; that resolved file must never be committed. Source-tree `.tmpl` files reference the secret; only the reference is committed.
- **Forgetting to add `.tmpl` extension** — a file with template syntax but without `.tmpl` is treated as literal content, leaving `{{ .name }}` in the rendered output.
- **Storing host-specific data in branches** — the templating system replaces what you'd otherwise put in branches. Use `{{ if eq .chezmoi.hostname "work-laptop" }}` instead of `git checkout work`.
- **Mixing `dot_` and unprefixed names for the same logical file** — chezmoi reads the source tree literally; `bashrc` and `dot_bashrc` are two different sources.
- **Encrypting everything by default** — encryption adds friction (you need the decryption key on every machine). Encrypt only what's secret; templating with secret-manager calls is often cleaner than committing encrypted blobs.
- **Letting `chezmoi diff` accumulate** — run `chezmoi apply` regularly. A growing diff means your machine has drifted from the source of truth.

## Scaling & failure modes

- **Learning curve**: source names (`dot_`, `private_`, `executable_`, `.tmpl`) are unfamiliar, and editing in the source tree versus the target is a common confusion; use `chezmoi edit`.
- **Drift**: files edited directly in `$HOME` diverge from source; `chezmoi diff` shows it and `chezmoi re-add` accepts it.
- **Large repos**: use `.chezmoiignore` (templated) to skip files on some machines.
- **Bootstrap**: a new machine needs chezmoi installed first; keep a one-line install snippet in the repo README.

## Variants

- **chezmoi-only** — pure templates and chezmoi data, no secret manager. Sufficient if you only need per-host variation.
- **chezmoi-with-1password-secrets** — `{{ onepasswordRead "..." }}` template helpers for SSH keys, API tokens, etc. Most popular variant for individual users with 1Password.
- **chezmoi-with-bitwarden** — same idea via `{{ bitwarden "..." }}`. Requires `bw` CLI authenticated.
- **chezmoi-with-age** — sops-style encrypted blobs decrypted at apply time using the `age` symmetric encryption tool. Good when no remote secret manager is available.
- **chezmoi-with-keepass** — desktop password manager via the `keepassxc-cli` integration.
- **chezmoi-with-pass** — Unix `pass` (gpg-backed) for users already on the GPG path.
- **chezmoi-only-on-managed-machines** — bare git on personal machines, chezmoi on managed/multi-host. Splits the surface area.

## Adoption checklist

- [ ] `chezmoi diff` is empty on every machine after `chezmoi apply`.
- [ ] Machine-specific values live in `chezmoi.toml` data, not in duplicated files.
- [ ] Secrets come from a password manager or encrypted files, not the plain repo.
- [ ] `.chezmoiignore` handles files that shouldn't exist on some machines.
- [ ] A bootstrap command is documented and tested on a fresh account.

## Real-world projects using this

- **chezmoi.io** — official documentation and quick start. https://www.chezmoi.io/
- **chezmoi GitHub repo** — `twpayne/chezmoi`, maintained by Tom Payne. https://github.com/twpayne/chezmoi
- **Many cloud-engineer dotfiles repos** — searching GitHub for the topic `chezmoi` returns thousands; inspect a few for real-world patterns (templates, ignore rules, scripts).
- **chezmoi user gallery** — https://www.chezmoi.io/links/dotfile-repos/ links to several public repos using chezmoi at different scales.
- **chezmoi `init` boot scripts** — many repos ship a one-liner that does `chezmoi init --apply <repo>` to bootstrap a new machine end-to-end.

## Migration & references

To start from scratch:

```bash
# Install chezmoi (https://www.chezmoi.io/install/ has every package manager)
brew install chezmoi      # macOS
sudo pacman -S chezmoi    # Arch
# or: sh -c "$(curl -fsLS get.chezmoi.io)"

# Initialise an empty source directory
chezmoi init

# Add an existing dotfile to the source
chezmoi add ~/.bashrc      # creates ~/.local/share/chezmoi/dot_bashrc
chezmoi add ~/.gitconfig   # creates ~/.local/share/chezmoi/dot_gitconfig

# Convert a file to a template after adding
chezmoi chattr +template ~/.gitconfig
chezmoi edit ~/.gitconfig  # opens dot_gitconfig.tmpl

# Set chezmoi data (rendered into templates)
chezmoi edit-config        # opens ~/.config/chezmoi/chezmoi.toml
# Add: [data] / name = "..." / email = "..."

# Preview and apply
chezmoi diff
chezmoi apply
```

To migrate from bare git:

1. Move tracked files from `$HOME` into `~/.local/share/chezmoi/` with `dot_` prefixes (`~/.bashrc` → `~/.local/share/chezmoi/dot_bashrc`).
2. Convert files with per-host variation to `*.tmpl` and replace literal values with `{{ .name }}` etc.
3. Move secret references — replace literal tokens in `~/.config/aws/credentials` with `{{ onepasswordRead "op://..." }}` and rename to `*.tmpl`.
4. `chezmoi apply` and verify `chezmoi diff` is empty afterwards.
5. Decommission the bare repo only after the chezmoi setup is solid on every machine.

To bootstrap a new machine:

```bash
chezmoi init --apply git@github.com:<you>/dotfiles.git
```

Further reading:

- chezmoi documentation — https://www.chezmoi.io/
- "How To Manage Your Dotfiles With Chezmoi" — chezmoi's own quick-start guide.
- `files/dotfiles-bare-git/` — the simpler alternative when chezmoi's overhead isn't justified.
- `principles/hidden-files-policy/` — the underlying convention chezmoi works around with `dot_*` naming.
- `files/xdg-base-directory/` — chezmoi follows XDG: source tree at `~/.local/share/chezmoi/`, config at `~/.config/chezmoi/`.
