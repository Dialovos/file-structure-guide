# Maildir

## TL;DR

Maildir is Daniel J. Bernstein's per-message-file mail format. Each message is a single file inside one of three subdirectories — `new/` (just delivered, unread), `cur/` (read or otherwise touched, with status flags appended to the filename), and `tmp/` (in-progress delivery, atomically renamed into `new/` once written). Subfolders are sibling directories prefixed with `.` (e.g. `.Sent/`, `.Drafts/`), each with its own `new/cur/tmp/` triple. Because every operation is a directory rename rather than a write into a shared file, Maildir is lock-free, NFS-safe, and resistant to corruption — qualities that make it the de-facto local store for `mbsync`/`offlineimap` plus `mu`/`notmuch`/`mutt` setups.

## Principles & why

The format encodes three deliberate choices.

1. **One message = one file.** Unlike `mbox` (one file holds the entire mailbox, separated by `From ` lines), Maildir avoids the worst-case rewrite when you delete a single 5 KB message in the middle of a 4 GB mbox. Indexing tools like `mu` and `notmuch` can also read the messages in parallel.
2. **Delivery uses three-stage atomic rename.** A delivery agent writes to `tmp/<unique>`, fsyncs, then renames into `new/<unique>`. The rename is atomic on POSIX, so a reader scanning `new/` never sees a partial message. No global lock is required, which is why Maildir works on NFS where flock is unreliable.
3. **Status lives in the filename.** Once a client reads a message, it moves the file from `new/<unique>` to `cur/<unique>:2,<flags>` where flags include `S` (seen), `R` (replied), `T` (trashed), `F` (flagged), `D` (draft). No mailbox-level metadata file exists; the directory listing is the index. This is why `rsync` and `git annex` work on Maildirs out of the box.

The result is a format that survives crashes, scales linearly with message count, and is editable with ordinary Unix tools (`find`, `mv`, `grep`).

## When to use

- Local mail storage with `mbsync` (isync) or `offlineimap` syncing from an IMAP server, then indexed by `mu` or `notmuch` and read with `mutt`/`neomutt`/`alot`/`afew`/`Geary`.
- Server-side delivery with `qmail`, `Postfix` (`mailbox_format = Maildir`), `Dovecot` (default backend), or `Courier`.
- Any system where you want mail to be backed up by a generic file-tree backup tool (`borg`, `restic`, `rsync`).
- Multi-tenant systems where users expect per-folder quotas — Maildir++ extends the format with `maildirsize` files for that purpose.
- Migrations from `mbox`: tools like `mb2md` produce Maildirs that drop straight into the above pipelines.

## When NOT to use

- Single-user, single-mailbox setups that already work with `mbox` and don't index more than a few thousand messages — the format upgrade buys you nothing.
- IMAP-only clients with no local cache (Thunderbird and Apple Mail in their default modes) — they store messages in their own SQLite or `.mbox`-derived caches and don't expose a Maildir.
- Filesystems with poor handling of large directories — ext2 or pre-2008 ext3 without `dir_index` will choke on a `cur/` containing 200k files. Modern ext4, XFS, ZFS, and Btrfs are fine.
- FAT32 and exFAT — the colon (`:`) in `cur/<unique>:2,<flags>` is illegal on those filesystems. Maildir cannot live there without a renaming layer.
- Windows native filesystems where `:` is reserved as the alternate-data-stream separator — same problem as FAT.

## Tree diagram

```
Maildir/
├── new/                ← unread, just delivered
├── cur/                ← read, with status flags in filename
├── tmp/                ← in-progress delivery
├── .Sent/
│   ├── new/
│   ├── cur/
│   └── tmp/
├── .Drafts/
└── .Archive.2025/
```

## Naming rules

1. The top-level directory is conventionally named `Maildir/` in `$HOME`, but any name works — what matters is that it contains exactly the three subdirectories `new/`, `cur/`, and `tmp/`.
2. Subfolders are siblings of `new/cur/tmp/` prefixed with `.` (dot), e.g. `.Sent/`, `.Drafts/`, `.Archive.2025/`. The dot makes them hidden from naive `ls` and signals "subfolder, not message".
3. Subfolder names use `.` as a hierarchy separator under Maildir++: `.Archive.2024.Personal/` is rendered as `Archive/2024/Personal` in IMAP. Avoid spaces; use `.Lists.debian-devel/` style for nested lists.
4. Message filenames in `tmp/` and `new/` follow `<seconds>.<unique>.<hostname>` where `<unique>` includes a process ID and a counter; in `cur/` the suffix `:2,<flags>` is appended (e.g. `1714439822.M123P456.host:2,RS`).
5. Flag letters in `:2,<flags>` are alphabetised: `D` draft, `F` flagged, `P` passed (forwarded), `R` replied, `S` seen, `T` trashed. The flag list is rewritten in alphabetical order on every status change.
6. Never rename `new/cur/tmp/`. Tools rely on those exact lowercase names; case differences break delivery agents.

## Worked example

You want offline, greppable mail with a local client.

1. Choose a sync tool (`mbsync`/isync, offlineimap) and configure a Maildir store: `Path ~/Mail/personal/`, `Inbox ~/Mail/personal/Inbox`, `SubFolders Verbatim` (or `Maildir++`, depending on your client's expectations).
2. Run `mbsync -a`. Each message becomes a file in `new/` or `cur/`; read messages carry flags in the name, such as `:2,S` (seen), `R` (replied), `F` (flagged), `T` (trashed).
3. Point a client at it: `mutt`, `aerc`, or `notmuch` plus an interface.
4. Index for search: `notmuch new`, then `notmuch search from:alice AND date:2026-04..`.
5. Back up with a plain copy or `rsync`; there is no database to snapshot.
6. Don't edit files in `cur/` by hand while a client or sync is running.

Mail is ordinary files: tools can grep, back up, and process it without a server.

## Anti-patterns

- **Copying a Maildir with `cp -r` instead of `cp --reflink` or `rsync -aH`** — `cp` may follow symlinks for shared messages and double-store, plus it loses hardlink-based deduplication used by some sync tools.
- **Letting `tmp/` accumulate** — `tmp/` is for in-progress deliveries that must be cleaned by a cron entry (most Maildir-aware MDAs ship one). A `tmp/` with thousands of stale files indicates a crashed delivery agent.
- **Storing arbitrary non-mail files in `Maildir/`** — clients will try to parse anything in `cur/` as RFC 5322. Never put `notes.txt` or `index.json` directly under the Maildir root.
- **Versioning `Maildir/` with git** — possible but painful: every read changes filenames in `cur/`, producing huge diffs. Use `borg`/`restic` for backups instead.
- **Mixing two clients writing to the same Maildir without a lock** — Maildir's lock-free guarantees apply to delivery, not to two readers both trying to move messages from `new/` to `cur/`. Pick one indexer; let others read-only.
- **Symlinking `new/` to a remote NFS share separate from `cur/`** — atomic rename is only atomic *within a single filesystem*. Splitting `new/` and `cur/` across mounts breaks the format.

## Scaling & failure modes

- **Many small files**: hundreds of thousands of messages slow some file systems and backup tools; archive old years to separate Maildirs or compress them.
- **Flag conflicts**: sync tools resolve flags and moves between server and local; use one master and test with a spare folder before a full sync.
- **Folder naming** differs between Maildir flavors (dot-prefixed `Maildir++` vs plain directories); match your client and sync tool.
- **Encryption at rest**: Maildir is plain text; use disk encryption for the volume.

## Variants

- **Maildir (Bernstein original)** — the three-directory format described above. Specified at https://cr.yp.to/proto/maildir.html.
- **Maildir++** — Courier extension that adds `.subfolder` directories with their own `new/cur/tmp/`, plus a `maildirsize` file in the top-level directory tracking quota usage. The de-facto format Dovecot, Courier, and `mbsync` use today.
- **Maildir+S=size (Dovecot)** — appends `,S=<bytes>` to filenames so directory listing alone reveals size; `maildirsize` becomes redundant. Set via `maildir_extra_file_size` in Dovecot.
- **Maildir+W=lines (Dovecot)** — similar but caches RFC 822 line counts.
- **MH** — older Bernstein-adjacent format with one file per message but flat numbering. Maildir replaced it because MH's locking story was weak.

## Adoption checklist

- [ ] Sync tool and client agree on the Maildir flavor.
- [ ] A full backup copy exists and was restored once.
- [ ] A search index (`notmuch`) is current.
- [ ] Old years are archived to keep active directories small.
- [ ] The volume holding mail is encrypted.

## Real-world projects using this

- **qmail** — Bernstein's MTA, the original implementation; defines the format.
- **Dovecot** — the most-deployed open-source IMAP/POP3 server; Maildir is one of two default backends (alongside mdbox).
- **Postfix** — set `home_mailbox = Maildir/` to deliver in Maildir format.
- **Courier MTA / Courier IMAP** — the project that introduced Maildir++.
- **mbsync (isync)** — mirrors IMAP folders into local Maildirs.
- **OfflineIMAP** — Python alternative to mbsync, Maildir-native.
- **mu** — Maildir indexer; powers `mu4e` (Emacs) and is itself a CLI search tool.
- **notmuch** — tag-based mail indexer over Maildir; backend for `alot`, `astroid`, `notmuch-emacs`.
- **Mutt / NeoMutt** — text-mode mail clients; can read Maildir directly.
- **Geary's `gmi`** — the underlying GNOME mail engine supports Maildir for local stores.

## Migration & references

To migrate from `mbox` to Maildir:

```bash
# Debian/Ubuntu: install perfect_maildir / mb2md
mb2md -s ~/mail/inbox -d ~/Maildir
```

To bootstrap an empty Maildir manually:

```bash
mkdir -p ~/Maildir/{new,cur,tmp}
chmod 700 ~/Maildir ~/Maildir/{new,cur,tmp}
```

To rebuild a notmuch index after restoring a Maildir backup:

```bash
notmuch new
```

Further reading:

- DJB's specification — https://cr.yp.to/proto/maildir.html
- Maildir++ specification — https://www.courier-mta.org/imap/README.maildirquota.html
- Dovecot wiki on Maildir — https://doc.dovecot.org/admin_manual/mailbox_formats/maildir/
- `principles/one-purpose-per-directory/` — Maildir's `new/cur/tmp/` split is the canonical example.
- `principles/hidden-files-policy/` — the leading-dot subfolder convention is hidden-files used as a namespace.
- `files/xdg-base-directory/` — for index databases (notmuch, mu) that should sit alongside but not inside the Maildir.
