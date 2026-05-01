# Maps of Content template

A starter MOC layout: a `MOCs/` folder with one example MOC, a `notes/` folder with two example atomic notes that the MOC links to. Demonstrates the dedicated-folder variant.

## What's here

- `MOCs/+ example-topic.md` — example MOC showing the orientation paragraph and section structure.
- `notes/example-note-1.md` — example atomic note linked from the MOC.
- `notes/example-note-2.md` — second example atomic note, mutually linked with note 1.
- `README.md` — this file.

## To adopt this template

1. Copy `template/` into your vault root, or just take the `MOCs/` folder if you already have notes:
   ```bash
   cp -r template/ ~/vault/
   cd ~/vault
   ```
2. Open in Obsidian (or any wikilink-capable editor).
3. Rename `+ example-topic.md` to your real topic — keep the `+ ` prefix.
4. Replace the example notes with your own. The MOC should link to them by their actual titles.
5. Once you have 5-15 MOCs, write `+ Home.md` at vault root linking to all of them.

## Conventions

- **MOC filenames:** `+ Title Case.md` (LYT-style). Keep the marker rigid — mixing prefixes defeats the sort/visual function.
- **Atomic notes:** `lowercase-hyphenated.md` in `notes/`.
- **One MOC per topic cluster.** Don't make sub-MOCs of sub-MOCs.
- **MOC body:** orientation paragraph, then 3-7 sections of grouped links. Not a flat list.

## What to rename or remove

- `+ example-topic.md` and the two example notes are placeholders — replace with your real first MOC and notes.
- Remove this `README.md` once the template is in use; the verifier needs it only while it lives in this repo.

## Verifier

`docs/superpowers/scripts/verify-guideline.sh notes/maps-of-content` checks that this README, `GUIDE.md`, `tree.md`, and the `template/` directory all exist with the required sections.
