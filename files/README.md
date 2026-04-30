# Personal-files layouts

18 conventions for the everyday content that lives outside any project — config, photos, music, mail, scanned documents, downloads, and so on.

## OS-level baselines

- [`xdg-base-directory/`](xdg-base-directory/) — `$XDG_CONFIG_HOME`, `$XDG_DATA_HOME`, etc.
- [`unix-fhs/`](unix-fhs/) — Filesystem Hierarchy Standard for system-wide layout

## Time-based archives

- [`date-archive/`](date-archive/) — `YYYY/YYYY-MM/` for receipts, journals, scans
- [`project-archive/`](project-archive/) — completed projects under `archive/<year>/`
- [`scanned-documents/`](scanned-documents/) — OCR'd PDFs, dated filenames
- [`receipts-and-finance/`](receipts-and-finance/) — `YYYY/YYYY-MM/<vendor>-<amount>.pdf`

## Media libraries

- [`photos-by-date-and-event/`](photos-by-date-and-event/) — `2026/2026-04-spring-trip/`
- [`music-library/`](music-library/) — `Artist/Year - Album/01 Track.flac` (Beets-compatible)
- [`video-library/`](video-library/) — Plex/Jellyfin layouts
- [`ebook-library-calibre/`](ebook-library-calibre/) — Calibre's `Author/Title/`

## Mail

- [`maildir/`](maildir/) — Bernstein's per-message-file format

## Dotfiles

- [`dotfiles-bare-git/`](dotfiles-bare-git/) — bare-repo home-as-worktree pattern
- [`dotfiles-chezmoi/`](dotfiles-chezmoi/) — chezmoi-managed templated dotfiles

## Daily-flow hygiene

- [`downloads-triage/`](downloads-triage/) — `inbox/` + weekly cleanup ritual
- [`screenshots-auto-flow/`](screenshots-auto-flow/) — auto-saved → triaged
- [`desktop-zero-policy/`](desktop-zero-policy/) — desktop must stay empty
- [`cloud-sync-structure/`](cloud-sync-structure/) — `~/cloud/<sync-name>/` namespacing
- [`removable-media-layout/`](removable-media-layout/) — labels + `IMPORT-<date>/`

## How to pick

Most users want `xdg-base-directory` + `date-archive` + one media-library guide as their baseline; pile on dotfiles and dailies as needed. [`CHOOSE.md`](../CHOOSE.md) sketches the decision.
