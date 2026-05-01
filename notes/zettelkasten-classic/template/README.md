# Zettelkasten-classic template

A bare classic-3-folder slip box: `inbox/` for capture, `permanent/` for atomic evergreen notes, `literature/` for per-source extraction, plus a `references.bib` stub and an example `INDEX.md` of MOCs.

## What's here

- `inbox/.gitkeep` — placeholder; this is where new capture lives until you process it.
- `permanent/.gitkeep` — placeholder; refined atomic notes go here, named with a 12-digit timestamp prefix (`YYYYMMDDhhmm slug.md`).
- `literature/.gitkeep` — placeholder; one note per source, named like `<author>-<short-title>.md` to match its BibTeX cite key.
- `references.bib` — empty BibTeX stub with a commented example entry.
- `INDEX.md` — example top-of-vault note listing your MOCs.
- `README.md` — this file.

## To adopt this template

1. Copy `template/` into your vault root:
   ```bash
   cp -r template/ ~/zettelkasten/
   cd ~/zettelkasten
   ```
2. Delete the three `.gitkeep` files as you start adding real notes.
3. Edit `INDEX.md` to remove the example MOC links and add your own once you've written some.
4. Add BibTeX entries to `references.bib` as you create literature notes.
5. (Optional) Open the folder as a vault in Obsidian, Logseq, Zettlr, or The Archive.

## Daily / weekly routine

- **Daily**: capture freely into `inbox/`. Don't worry about naming or structure.
- **Weekly**: process `inbox/`. Each item becomes a refined `permanent/` note (with timestamp ID and at least two links), an extension of an existing literature note, or trash.
- **Periodically**: when 5-7 permanent notes form a thread, write a MOC and add it to `INDEX.md`.

## What to rename or remove

- The example MOC links inside `INDEX.md` are placeholders; replace them with your own.
- The commented BibTeX example in `references.bib` is for reference only — leave or remove the comment as you like.
- Remove this `README.md` once the template is in use; the verifier needs it only while it lives in this repo.

## Verifier

`docs/superpowers/scripts/verify-guideline.sh notes/zettelkasten-classic` checks that this README, `GUIDE.md`, `tree.md`, and the `template/` directory all exist with the required sections.
