# Unix Filesystem Hierarchy Standard (FHS)

## TL;DR

For anything that lives outside `$HOME` on a Unix-like system, the FHS dictates which top-level directory it belongs in: `/etc` for host-specific config, `/usr` for read-only programs and data shipped by the OS, `/var` for state that grows during operation (logs, caches, mail spools), `/home` for users, `/opt` for self-contained third-party packages, and `/srv` for content the system serves to the outside world. Distros that comply give administrators a uniform mental model across thousands of packages.

## Principles & why

The FHS is the contract between distributions, package maintainers, and admins. Without it, every project would invent its own install layout — some in `/usr/local/`, some in `/opt/<vendor>/`, some splat across `/etc/` and `/srv/` simultaneously — and `apt`, `dnf`, `pacman`, and Puppet/Ansible/Chef recipes would each need bespoke knowledge of every package.

The split is not arbitrary. It encodes two orthogonal axes:

1. **Mutability** — `/usr` is meant to be read-only and even mountable from a shared NFS export. `/var` exists precisely because some files must be writable. `/etc` is host-local config, written rarely.
2. **Ownership** — `/usr/bin` is owned by the distro's package manager. `/usr/local/` is reserved for the local administrator. `/opt/<vendor>/` is reserved for self-contained third-party software that doesn't fit the package manager's scheme.

Following FHS keeps these axes legible: anyone who reads `/etc/nginx/nginx.conf` knows it's host-local config; anyone who finds a binary in `/usr/local/bin/` knows the admin put it there, not `apt`.

## When to use

- Anything you ship as a system package (`.deb`, `.rpm`, `.apk`) — packagers will reject layouts that violate FHS.
- Software you install from source on a server: `./configure --prefix=/usr/local` is the FHS-correct prefix for admin-installed software.
- Daemons, system services, and anything intended to run before login.
- Multi-user systems where users expect a predictable mental model of where logs, configs, and state live.
- Containers built on FHS-compliant base images (Debian, Ubuntu, Fedora, Alpine) — keep the convention so admins can debug them like any other Unix host.

## When NOT to use

- User-level installs — use the XDG Base Directory layout (`~/.local/`, `~/.config/`) instead. FHS is system-scoped.
- macOS — Apple uses its own hierarchy (`/Applications/`, `~/Library/`, `/Library/`). FHS doesn't apply; trying to bend it onto macOS produces breakage in Spotlight, codesigning, and Time Machine.
- NixOS — the entire point of Nix is that packages live under `/nix/store/<hash>-<name>/` and are symlinked into a per-user profile. NixOS deliberately abandons FHS.
- Container images optimised for size — distroless, scratch-based, or Alpine images often strip `/usr/share/man/`, `/var/log/`, etc. Don't backfill the missing dirs unless something actually needs them.
- Embedded firmware with a tiny squashfs — there's not enough disk to justify the full hierarchy; pick a minimal subset.

## Tree diagram

```
/
├── etc/                ← host-specific config
├── usr/
│   ├── bin/            ← shipped binaries
│   ├── local/          ← admin-installed (your stuff)
│   └── share/          ← arch-independent data
├── var/
│   ├── log/            ← log files
│   ├── lib/            ← persistent state
│   └── cache/
├── home/<user>/
├── opt/<vendor>/       ← third-party self-contained
└── srv/<service>/      ← service-served data
```

## Naming rules

1. Top-level directories are fixed by the spec — do not invent new ones at `/`.
2. Under `/etc/`, each daemon gets a directory named for the daemon: `/etc/nginx/`, `/etc/systemd/`. Avoid stuffing standalone files at `/etc/<daemon>.conf` once the directory form is in use.
3. Under `/var/log/`, each daemon writes to a single subdirectory: `/var/log/nginx/access.log`. Rotate with `logrotate` or `journald`, never let an unbounded file grow at the top of `/var/log/`.
4. Admin-installed software goes under `/usr/local/`, never `/usr/` directly. Distro packages own `/usr/`; admin packages own `/usr/local/`.
5. Self-contained third-party blobs go under `/opt/<vendor>/<product>/` (e.g. `/opt/google/chrome/`). They bundle their own libs and don't depend on `/usr/lib/` layout.
6. Served content (web roots, FTP roots, NFS exports) goes under `/srv/<service>/`. Prefer `/srv/www/` over `/var/www/` on systems that follow FHS strictly.

## Worked example

You built a tool from source and a small internal service, and you need to decide where each part goes.

1. Binaries you built yourself go to `/usr/local/bin/`, libraries to `/usr/local/lib/`, shared data to `/usr/local/share/<tool>/`. Package-manager files stay in `/usr`.
2. A self-contained vendor bundle (its own `bin/`, `lib/`) goes to `/opt/<vendor>/<product>/`.
3. Host config goes to `/etc/<tool>/`; keep defaults out of `/etc` when a program ships them in `/usr/share`.
4. Runtime state goes to `/var/lib/<service>/`, logs to `/var/log/<service>/`, caches to `/var/cache/<service>/`.
5. Content served to others (a website, a git server's repos) goes to `/srv/<service>/`.
6. With systemd, declare these directories in the unit (`StateDirectory=`, `LogsDirectory=`, `ConfigurationDirectory=`) so they're created with the right ownership.
7. Read `man hier` for the reference.

Every file has a predictable home, and package upgrades don't overwrite your files.

## Anti-patterns

- **Installing to `/usr/bin/` from source** — that prefix belongs to the package manager. Use `/usr/local/` so the admin's installs are distinguishable from distro installs.
- **Mixing config and data in `/etc/`** — `/etc/` is config only. A daemon's runtime database belongs in `/var/lib/<daemon>/`, not `/etc/<daemon>/db.sqlite`.
- **Logging to `/tmp/` or `/var/run/`** — `/tmp/` is wiped on reboot and `/var/run/` (now `/run/`) is for runtime sockets and pid files. Logs go to `/var/log/`.
- **Hardcoding `/var/lib/<daemon>/` instead of `/var/lib/<daemon>/<version>/`** — for daemons that change their on-disk format between versions, version the state directory.
- **Putting user data under `/srv/`** — `/srv/` is for content the host *serves* (web pages, FTP files), not for personal files. Personal data lives in `/home/<user>/`.
- **Ignoring `/usr/local/etc/`** — admin-installed software's config goes in `/usr/local/etc/`, not `/etc/`, on strictly FHS-compliant systems.

## Scaling & failure modes

- **Package manager conflicts**: files you put in `/usr` (not `/usr/local`) may be overwritten or removed by upgrades.
- **Containers** ignore most of this; the FHS matters on the host and inside base images, but volumes make the mapping explicit.
- **Per-user installs** belong under `$HOME/.local` (see `xdg-base-directory`), not in system paths.
- **Backups**: the split tells you what to back up (`/etc`, `/var/lib`, `/srv`, `/home`) and what to rebuild (`/usr`).

## Variants

- **Strict FHS** — every directory exactly per spec; common on Debian, Slackware, FreeBSD.
- **FHS with `/usr` merge** — modern Linux (Fedora, Ubuntu, Arch) symlinks `/bin → /usr/bin`, `/sbin → /usr/sbin`, `/lib → /usr/lib`. Same logical layout, simpler to mount `/usr` separately.
- **NixOS layout** — `/nix/store/<hash>-<name>/` plus per-user profile symlinks. Deliberately abandons FHS but provides shims (`/usr/bin/env` works) for portability.
- **Stateless system layout (Fedora Silverblue, openSUSE MicroOS)** — `/etc/` and `/var/` are the only writable trees; the rest is immutable. Same FHS shape, different mount semantics.
- **Container minimalism** — scratch-based or distroless images keep only what runs the binary. The shape is FHS-shaped but missing entire branches (`/var/log/`, `/usr/share/man/`).

## Adoption checklist

- [ ] Locally built software lives in `/usr/local` or `/opt`, never mixed into `/usr`.
- [ ] Each service has separate config, state, log, and cache directories.
- [ ] systemd units declare their directories.
- [ ] Backups cover `/etc`, `/var/lib`, `/srv`, and `/home`.
- [ ] Per-user software is installed under `$HOME`, not system paths.

## Real-world projects using this

- **Filesystem Hierarchy Standard (FHS) 3.0** — the canonical spec, hosted by the Linux Foundation Refspecs project; last revised 2015.
- **Debian Policy Manual** — chapter 9 codifies FHS for Debian packages and adds Debian-specific clarifications.
- **Fedora Packaging Guidelines** — incorporates FHS by reference; documents the `/usr` merge (UsrMove).
- **Linux man-pages `hier(7)`** — per-host description of the standard hierarchy.
- **systemd file-hierarchy(7)** — the systemd project's interpretation, including `/run/`, `/var/lib/private/`, etc.
- **FreeBSD Handbook chapter "Directory Structure"** — BSD's parallel layout, mostly aligned with FHS.

## Migration & references

To audit an existing host for FHS deviations:

```bash
# Find admin-installed binaries that escaped /usr/local/
dpkg -S /usr/bin/* >/dev/null 2>&1 || ls /usr/bin
# Compare paths against the spec; relocate as needed via dpkg-divert
```

When packaging your own software:

- Use `--prefix=/usr` for distro packages, `--prefix=/usr/local` for admin source builds.
- Place config under `/etc/<name>/`; runtime state under `/var/lib/<name>/`; logs under `/var/log/<name>/`.
- For a self-contained tarball install, `/opt/<vendor>/<product>/` is the right prefix.

Further reading:

- FHS 3.0 — https://refspecs.linuxfoundation.org/fhs.shtml
- `man 7 hier` on any Linux system.
- `principles/stable-vs-volatile-separation/` — the underlying split FHS encodes (`/usr` stable vs `/var` volatile).
- `files/xdg-base-directory/` — the user-scoped analog; FHS for system, XDG for home.
- Debian Policy Manual chapter 9 — the most thoroughly enforced FHS interpretation.
