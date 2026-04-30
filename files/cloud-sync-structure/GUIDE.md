# Cloud-sync structure

## TL;DR

Don't let Dropbox, iCloud, OneDrive, Google Drive, or Box scatter their sync roots wherever the installer drops them — namespace them all under a single `~/cloud/<provider>/<purpose>/` parent. The provider sits at the second level, the purpose at the third. The benefits compound: you avoid drag-and-drop accidents into the wrong sync root; you make provider boundaries visible in `cd ~/cloud`; backup tools can target the entire cloud-synced surface (or skip it entirely) with one path; and "what's in Dropbox vs what's in OneDrive" stops being a guessing game. Doesn't apply to providers with mandated paths (notably iCloud Drive on macOS) — for those, leave them in place and link from `~/cloud/icloud/` if symbolic visibility matters.

## Principles & why

The default behavior of every consumer cloud-sync provider is to plant a flagged folder at `$HOME` — `~/Dropbox/`, `~/OneDrive/`, `~/Google Drive/`, `~/Box/`. If you use only one, fine; the moment you use two or three, your home directory hosts three top-level cloud roots that look identical to ordinary directories, and you spend mental cycles remembering which one syncs where.

Three problems follow:

1. **Drag-and-drop accidents.** A 2 GB video file dropped into `~/Dropbox/` instead of `~/OneDrive/` syncs to the wrong place and either burns quota or leaks to the wrong audience.
2. **Backup tools can't tell.** A `borg`/`restic`/`rsync` run against `$HOME` happily backs up your already-cloud-synced files, doubling storage and making restore-from-backup ambiguous when both copies disagree.
3. **Path semantics get lost.** "I have it in Dropbox" doesn't tell you whether it's the personal Dropbox, the family-shared folder, or the work-handoff bucket — three very different audiences.

Namespacing under `~/cloud/<provider>/<purpose>/` makes all three visible:

- `cd ~/cloud` and you see exactly which providers you use.
- `cd ~/cloud/dropbox` and you see how Dropbox is partitioned (shared-with-spouse, work-handoff, archive).
- Backup excludes are one-line: `--exclude '/home/*/cloud/'` skips the whole synced surface; `--include '/home/*/cloud/dropbox/work-handoff'` selectively re-includes specific buckets.
- Drag-and-drop targets are explicit: you drop into `cloud/dropbox/shared-with-spouse/`, not just "somewhere in Dropbox".

The provider-first hierarchy (`<provider>/<purpose>/`) is intentional. Provider is the *bigger* boundary — it determines who has access, what the quota is, what the privacy model is. Purpose is finer-grained inside that. Reversing it (`~/sync/<purpose>/<provider>/`) is a valid variant but tends to make the provider feel incidental, which is exactly what causes the "is this Dropbox or OneDrive?" confusion in the first place.

## When to use

- You use **two or more cloud-sync providers** on the same machine.
- You use **one provider** but with **two or more distinct purposes** (personal-archive vs work-handoff vs shared-with-family) and want the partition reflected in paths.
- You back up `$HOME` with a tool whose excludes you'd rather express by path than by provider-specific markers.
- You sometimes drag-and-drop large files and have been bitten by syncing the wrong one.
- You configure new machines often and want the sync layout to look identical on every box.

## When NOT to use

- **Provider-mandated paths.** iCloud Drive on macOS lives at `~/Library/Mobile Documents/com~apple~CloudDocs/` — Apple does not support relocating it. Box Drive on macOS likewise has restrictions. For these, leave the real path in place and (optionally) put a symlink at `~/cloud/icloud/` for visibility.
- **Single-provider, single-purpose users.** If you only use Dropbox and only for one thing, the namespace is overhead.
- **Corporate-managed laptops.** IT departments often configure OneDrive/Dropbox at fixed paths for DLP and conditional-access reasons. Don't fight the policy; document the actual paths.
- **Providers that require their root to be at a specific name.** Some legacy syncs (older Google Drive desktop with backup-and-sync features, certain enterprise OneDrive configurations) bind to `~/Google Drive/` or `~/OneDrive - <Tenant>/`; relocating breaks the binding.
- **You're already happy with your layout.** If `~/Dropbox/` works for you, don't refactor for the sake of it.

## Tree diagram

```
~/cloud/
├── dropbox/
│   ├── shared-with-spouse/
│   └── work-handoff/
├── icloud/
│   └── notes-mirror/
└── google-drive/
    └── reference-pdfs/
```

## Naming rules

1. The top-level parent is `~/cloud/` (lowercase, no hyphens). Avoid `~/Cloud/` — case differences cause friction on case-insensitive filesystems vs case-sensitive ones.
2. Provider directories use the canonical lowercase name: `dropbox/`, `onedrive/`, `google-drive/`, `box/`, `icloud/`, `proton-drive/`. Use a hyphen for two-word providers; do not abbreviate ("gdrive/" is too cryptic at a glance).
3. Purpose subdirectories use kebab-case and start with a verb-y noun describing audience or use: `shared-with-spouse/`, `work-handoff/`, `archive/`, `family-photos/`, `team-deliverables/`.
4. Avoid date-based purposes at this level — purposes are durable; dates belong inside (`work-handoff/2025-Q3/`).
5. If a provider's actual sync root cannot be relocated (iCloud on macOS), put a real symlink at `~/cloud/icloud/` pointing to the mandated path so commands like `ls ~/cloud/` still show every provider you use.
6. Don't nest providers (`~/cloud/google-drive/work/dropbox/`) — providers must be at exactly the second level, never deeper.

## Anti-patterns

- **Letting installers default to `~/<Provider>/`** — accept their default, then move and reconfigure their root once. Every installer supports a custom location; finding the option is a 30-second cost.
- **Mixing providers under a single purpose-folder** — `~/cloud/work-handoff/` containing a Dropbox subfolder *and* an OneDrive subfolder defeats the visibility goal. Keep providers as the top split.
- **Backing up `~/cloud/` to another cloud** — sync of a sync amplifies conflicts. Either back up cloud-synced files to *local* storage, or trust the provider's own version history.
- **Storing project source code under `~/cloud/`** — git repos sync poorly through Dropbox; merge conflicts on `.git/` directories are a known nightmare. Use a real git remote.
- **Symlinking individual files into a sync root** — many sync clients refuse to follow symlinks or follow them inconsistently across platforms. Move the file, don't symlink it.
- **Putting secrets in cloud-synced folders unencrypted** — `.env` files, SSH keys, AWS credentials. If you must, encrypt with `age`, `sops`, or a vault first.
- **Leaving conflict files (`Conflicted copy.docx`, `(Hoang's MacBook)`) untouched** — they accumulate. Resolve and delete on each weekly triage.

## Variants

- **by-provider (this guide)** — `~/cloud/<provider>/<purpose>/`. Provider visibility is paramount. Best when audiences/quotas matter most.
- **by-purpose-then-provider** — `~/sync/<purpose>/<provider>/`. Purpose visibility is paramount. Better when the same logical bucket (e.g. "work handoff") might be backed by Dropbox today and OneDrive tomorrow.
- **single-flat** — keep one sync provider at its default, no namespacing. Lowest overhead, but doesn't scale to multi-provider.
- **flat-with-symlinks** — providers stay at their installed paths, with `~/cloud/<provider>/` symlinks for visibility. Useful when relocation is impossible (iCloud).
- **per-tenant subdirectories** — for OneDrive at companies with multiple tenants: `~/cloud/onedrive/<tenant>/`. Adds a fourth level only when needed.

## Real-world projects using this

- **Many opinionated dotfile setups** publish their `~/cloud/` (or `~/sync/`) layout in their dotfiles' README, often as part of an "installation profile" section. Search GitHub for "cloud sync structure" or "sync folder layout".
- **Corporate IT laptop layouts** (financial services, healthcare) often pre-create per-provider folders matched to DLP rules — the namespace acts as a policy boundary.
- **Hazel rule libraries (macOS)** — published rule sets often assume a `~/cloud/<provider>/` namespace so rules can target a single provider's tree.
- **Personal wiki/note workflows** (e.g. Obsidian + iCloud, Logseq + Dropbox) document the sync-root location prominently because the choice ripples into the tool's identity.
- **Restic / Borg backup configurations** in personal sysadmin repos often use `~/cloud/` exclusion patterns directly. The pattern is widespread enough to be a de-facto convention even without a single canonical source.

## Migration & references

To migrate from default-named sync roots:

1. **Quit the sync client** for the provider you're moving (Dropbox, OneDrive, etc.). Mid-flight relocation corrupts state.
2. Create the target: `mkdir -p ~/cloud/dropbox`.
3. Move the existing root: `mv ~/Dropbox ~/cloud/dropbox/main` (or split into purposes as you go: `~/cloud/dropbox/shared-with-spouse`, `~/cloud/dropbox/work-handoff`).
4. Re-launch the sync client. Use its preferences pane to point the sync root at the new location. Some clients require you to re-link the account; the local files are recognised and not re-downloaded.
5. Verify the file count matches and no "files removed" notification fires from the provider — if it does, undo and consult the provider's "move sync folder" docs.
6. Update any path references in scripts, backup configs, editor "recent files" lists.

For provider-mandated paths (iCloud Drive):

```bash
# Don't relocate iCloud — link it instead
mkdir -p ~/cloud
ln -s "$HOME/Library/Mobile Documents/com~apple~CloudDocs" ~/cloud/icloud
```

Backup-tool integration example (`restic`):

```
# ~/.config/restic/excludes
/home/*/cloud/dropbox/
/home/*/cloud/onedrive/
# Selectively re-include critical hand-off buckets:
!/home/*/cloud/dropbox/work-handoff/
```

Further reading:

- Each provider's own "change sync folder location" documentation — Dropbox Help, OneDrive Help, Google Drive for Desktop docs, Box Help.
- Apple's iCloud Drive documentation explaining why the path is fixed on macOS.
- `principles/one-purpose-per-directory/` — the broader rule this layout instantiates.
- `principles/stable-vs-volatile-separation/` — cloud-sync content sits on the volatile side; namespace it deliberately.
- `files/downloads-triage/` — the inbox-style sibling pattern; avoid letting `Downloads/` become a de-facto cloud sync target.
