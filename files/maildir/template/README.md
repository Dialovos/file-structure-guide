# Maildir template

An empty-tree skeleton for a Bernstein-style Maildir with two pre-built subfolders (`.Sent/`, `.Drafts/`). Drop it into `$HOME` (typically as `Maildir/`), point your MDA or sync tool at it, and it's ready to receive messages.

## What's here

- `new/`, `cur/`, `tmp/` — the canonical three-directory triple every Maildir must have.
- `.Sent/{new,cur,tmp}/` — pre-stubbed sent-mail subfolder (Maildir++ style).
- `.Drafts/{new,cur,tmp}/` — pre-stubbed drafts subfolder.
- `.gitkeep` files preserve the empty directories under version control. Real mail clients ignore them.

## To adopt this template

1. Copy the tree into place: `cp -r template/ ~/Maildir/` (or `~/mail/`, etc.).
2. Lock down permissions: `chmod 700 ~/Maildir ~/Maildir/{new,cur,tmp}` — Maildir's atomic-rename safety assumes only the owner can write.
3. Configure your MDA:
   - **Postfix**: `home_mailbox = Maildir/` in `main.cf`.
   - **qmail**: `.qmail` files using `./Maildir/`.
   - **mbsync**: set `MaildirStore.Path` and `MaildirStore.Inbox`.
4. Add subfolders as needed: `mkdir -p ~/Maildir/.Archive.2025/{new,cur,tmp}`. Always create all three subdirectories together.
5. (Optional) initialise an indexer: `notmuch new` or `mu init --maildir=~/Maildir`.

## What to rename or remove

- Add or remove subfolders (`.Sent/`, `.Drafts/`, `.Archive.YYYY/`, `.Lists.<list>/`) to match your filing scheme.
- Remove `.gitkeep` placeholders once real mail arrives — the directories will no longer be empty.
- Drop this `README.md` once the template has been adapted (the verifier requires it while it lives in this repo).

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.
