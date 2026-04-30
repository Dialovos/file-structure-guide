# Unix FHS template

An empty-tree skeleton showing the four most-edited branches of a Filesystem Hierarchy Standard layout. Real systems have many more directories under `/`; this template focuses on the ones a packager or admin actually touches.

## What's here

- `etc/` — drop host-specific configuration (one subdirectory per daemon).
- `usr/local/` — admin-installed binaries, libraries, and configs (`bin/`, `lib/`, `etc/`, `share/`).
- `var/log/` — log files, one subdirectory per daemon.
- `srv/` — content served to the outside world (web roots, FTP roots, NFS exports).

`.gitkeep` files preserve the empty shape; replace them as you populate real content.

## To adopt this template

1. This template is meant for a **packaging skeleton**, not a literal `/`-rooted overlay. Use it as the layout reference when you build a `.deb`, `.rpm`, or container image, or when you organise an `/opt/<vendor>/<product>/` install tree.
2. For each daemon you ship, create:
   - `etc/<daemon>/` — config files only.
   - `var/log/<daemon>/` — log destination (set in the daemon's config).
   - Optionally `usr/local/<daemon>/` if you ship out-of-band of the system package manager.
3. Keep `srv/` only if your software serves user-visible content (web pages, files); otherwise delete it.
4. When packaging, set `./configure --prefix=/usr` (distro package) or `--prefix=/usr/local` (admin install) and let the build system place files at FHS paths.

## What to rename or remove

- Rename `etc/`, `var/log/`, etc. with daemon-specific subdirectories — for example, `etc/nginx/` instead of just `etc/`.
- Delete `srv/` if your project doesn't serve content.
- Remove `.gitkeep` placeholders once real files exist.
- Drop this `README.md` once the template has been adapted to your project (verifier requires it while it lives in this repo).

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.
