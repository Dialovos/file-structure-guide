## TL;DR

The **3-2-1 rule** says keep **three copies** of data that matters (the original plus two backups), on **two different kinds of media** (for example an internal disk and an external drive), with **one copy off-site** (another location or an encrypted cloud store). This guide is about the *layout that makes the rule practical*: decide **what is worth backing up** (a short, written list of paths), keep the **backup tool's repository** apart from the data it protects, and keep a **manifest** and a **restore-test log** in a known place. Use a deduplicating, encrypting tool (restic, Borg, Kopia) rather than hand-rolled copies, exclude what can be regenerated, and, most importantly, **test restores on a schedule**, because a backup you have never restored is a hope, not a backup. Encrypt everything that leaves the machine, and store the encryption key separately from the backups it unlocks.

## Principles & why

1. **Redundancy needs independence.** Two copies on the same disk, in the same room, or in the same account fail together. Different media, locations, and credentials make failures uncorrelated.
2. **Back up by list, not by hope.** A written list of included paths and exclusions is reviewable. "Everything" backs up caches and skips the one folder you forgot to mount.
3. **Regenerable is not precious.** Package caches, build outputs, virtual environments, and downloaded installers can be rebuilt; excluding them keeps backups small and fast (see `generated-vs-source-separation`).
4. **Backups are for restoring.** The only test is a restore. Schedule one, write down the result, and fix what fails.
5. **Encryption and key custody.** Off-site copies must be encrypted; the key or passphrase must be stored where you can find it after losing the machine, but not next to the data.
6. **Versions beat mirrors.** A mirror copies deletions and corruption too; snapshots with retention let you go back to before the mistake.

## When to use

- **Anyone with data they'd be upset to lose**: documents, photos, code not pushed anywhere, personal records.
- **Workstations and servers** that hold state outside Git remotes.
- **Small teams and individuals** who need a simple, testable routine rather than enterprise backup software.
- **Families and small businesses** keeping records with legal retention needs (see `receipts-and-finance`).

## When NOT to use

- **As a substitute for version control.** Git tracks intentional history of text; backups protect against loss. Use both.
- **For syncing between devices.** Sync clients propagate deletions and corruption (see `cloud-sync-structure`); a sync folder is not a backup.
- **For data you can regenerate cheaply.** Backing up a container image cache is waste.
- **For regulated data** with specific retention and audit requirements. Follow the applicable regulation; this layout is a personal and small-team baseline.

## Tree diagram

```
backup-plan/                          ← lives in version control and a printed copy
├── README.md                         ← the 3-2-1 plan in one page: what, where, how often
├── backup-paths.txt                  ← paths to include, relative to the home directory
├── backup-excludes.txt               ← patterns to exclude (caches, build outputs)
├── backup.sh                         ← runs the tool, prunes, checks
├── manifest.md                       ← copies: location, media, tool, retention, last verified
└── restore-tests/
    ├── 2026-04-30.md                 ← date, what was restored, result, time taken
    └── 2026-01-31.md

Copies (outside the repository):
  1. original data                    ← internal disk
  2. local backup repository          ← external drive (different media)
  3. off-site backup repository       ← another location or encrypted cloud storage
```

## Naming rules

- **The plan directory** is `backup-plan/` (or a folder in your tools directory); it's plain text and belongs in Git, since it contains no secrets.
- **Repositories** are named by location and role in the manifest (`local-external`, `offsite-cloud`), not by date; the tool handles snapshots.
- **Snapshot tags** describe the trigger (`scheduled`, `pre-upgrade`), and the tool records the timestamp.
- **Restore-test logs** are `YYYY-MM-DD.md`, one per test (see `iso-date-formats`).
- **Path lists** use one path per line, comments starting with `#`, and stay short enough to review at a glance.
- **Secrets** (repository passphrase, cloud credentials) are never in the plan directory; reference where they are kept (`keyring`, `password manager`), not their values.

## Worked example

A laptop holds photos, documents, and unpushed code, backed up occasionally by dragging folders to a USB drive.

1. List what matters in `backup-paths.txt` (relative to your home directory): `documents`, `photos`, `projects`, `.config`, `.ssh` (encrypted backup only). Everything not on the list is deliberately not backed up.
2. List exclusions in `backup-excludes.txt`: `**/node_modules`, `**/.venv`, `**/target`, `.cache`, `**/__pycache__`.
3. Create a local repository on an external drive with restic: `restic -r /path/to/external/repo init` (choose a strong passphrase and store it in a password manager, plus a sealed paper copy elsewhere).
4. Create an off-site repository, for example in encrypted cloud object storage or on a friend's or relative's machine: `restic -r <offsite-repo> init`.
5. Export the repository locations and password file path in the environment for the script (never in the repository), and run `backup.sh` against each repository on a schedule (systemd timer or cron).
6. Prune with a retention policy: `restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune`.
7. Verify integrity regularly: `restic check --read-data-subset=5%`.
8. Every quarter, do a **restore test**: `restic restore latest --target /tmp/restore-test --include "$HOME/documents/some-file"`, open the files, compare a checksum against the original, and write the result to `restore-tests/YYYY-MM-DD.md`.
9. Update `manifest.md` with each copy's location, media, and last verified date.

Three copies on two media types, one off-site, with proof that a restore works.

## Anti-patterns

- **Never testing a restore.** Untested backups regularly turn out to be empty, corrupt, or unrecoverable without a lost key.
- **Backup to the same disk or account** as the data. One failure, theft, or ransomware event takes both.
- **Sync folders as backups.** Deletion and encryption by malware propagate to every copy.
- **Backing up everything, including caches.** Slow, expensive, and hides the important files in noise.
- **Passphrase stored only on the backed-up machine.** Lose the machine, lose the ability to decrypt.
- **Always-attached backup drives.** Ransomware and power surges reach them; use offline or append-only copies for at least one.
- **No monitoring.** Scheduled jobs fail silently; alert on failure or on "no new snapshot in N days".

## Scaling & failure modes

- **Larger data** (terabytes of media): use tools that deduplicate and chunk well (restic, Borg, Kopia), and consider hardware with an offsite replica rather than a cloud copy for cost.
- **Multiple machines**: one repository per machine or a shared deduplicating repository with distinct host tags; manage credentials per machine.
- **Retention growth**: define retention by policy (daily, weekly, monthly, yearly) instead of keeping everything; storage cost then stays predictable.
- **Ransomware resilience**: keep at least one copy that the source machine cannot modify (offline drive, object-lock or append-only storage).
- **Databases and running services**: file-level backups of live databases are unreliable; use the database's dump or snapshot tools, and back up the dump.
- **Legal and business records**: add retention periods to the manifest and consider a longer-term archive tier with periodic integrity checks.

## Variants

- **Deduplicating repository tools** (this guide): restic, Borg, Kopia; encrypted, versioned, efficient.
- **Snapshot filesystems** (ZFS, Btrfs) with `send/receive` replication: fast local snapshots and remote replicas, needing matching filesystems.
- **`rsync` with hard-link snapshots** (`--link-dest`, rsnapshot): simple, transparent on disk, no encryption on its own.
- **Cloud backup services**: turnkey off-site copy; check encryption, restore time, and lock-in.
- **Machine images** for whole-system recovery, in addition to file-level backups of data.

## Adoption checklist

- [ ] `backup-paths.txt` and `backup-excludes.txt` exist, are reviewed, and match what you actually care about.
- [ ] There are three copies on two media types, with at least one off-site.
- [ ] Backups are encrypted, and the passphrase is stored separately from the backups.
- [ ] Jobs run on a schedule and alert on failure.
- [ ] A restore test was performed this quarter and logged in `restore-tests/`.
- [ ] At least one copy cannot be modified by the source machine.

## Real-world projects using this

- **The 3-2-1 rule** was popularized by photographer Peter Krogh in *The DAM Book* and is now standard advice in backup guidance.
- **restic**, **BorgBackup**, and **Kopia** document deduplicated, encrypted, versioned backup repositories, including `check` and restore commands.
- **rsnapshot** and `rsync --link-dest` document the hard-link snapshot technique.
- **Backblaze, and other providers'** engineering blogs publish drive-failure statistics that motivate redundancy.
- **Debian and Arch wikis** have practical pages on backup tools and strategies.

## Migration & references

- **From manual copies:** create the path and exclude lists first; then initialize a repository, take one full snapshot, and retire the manual routine after a successful restore test.
- **Between tools:** keep the old repository read-only while the new one builds history; restore-test the new one before deleting the old.
- **To add the off-site copy:** initialize a second repository at the new location and run the same script against it (or replicate the first with the tool's copy command).
- **References:**
  - `files/cloud-sync-structure/` for why sync is not backup.
  - `files/receipts-and-finance/` and `files/scanned-documents/` for records worth backing up.
  - `principles/generated-vs-source-separation/` for exclusions.
  - `principles/stable-vs-volatile-separation/` for deciding what needs backup.
