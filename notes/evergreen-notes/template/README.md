# Evergreen notes template

A bare evergreen vault: a flat directory with two example claim-titled notes, an optional `INDEX.md` Map of Content, and this README. Demonstrates Andy Matuschak's declarative-title style without prescribing topic content.

## What's here

- `example-claim-as-title.md` — short example showing declarative-title form.
- `another-declarative-title.md` — second example, mutually linked.
- `INDEX.md` — optional top-level MOC listing entry-point notes.
- `README.md` — this file.

The directory is flat by design. All structure lives in the links and in MOCs.

## To adopt this template

1. Copy `template/` into your vault root:
   ```bash
   cp -r template/ ~/evergreen/
   cd ~/evergreen
   ```
2. Replace the example notes with real claims of your own. Each filename should be a *complete claim*, lowercase-hyphenated, e.g. `attention-residue-tax-from-task-switching.md`.
3. Maintain at least 2-3 links from every new note to existing ones. Isolated notes are signal that the topic isn't yet integrated into your thinking.
4. Edit `INDEX.md` to point at your real entry-point notes once you've written some.
5. (Optional) Open the folder as a vault in Obsidian, Logseq, or any tool with first-class backlinks.

## Rules quick reference

- **Atomic** — one idea per note.
- **Concept-oriented** — claims, not projects or sources.
- **Declarative title** — `attention-residue-tax-from-task-switching.md`, not `attention-residue.md`.
- **Densely linked** — every note links to and is linked from others.

## What to rename or remove

- The two example notes are placeholders; replace their content (you may keep them as a starter pair if you wish, but the filenames should ultimately be your own claims).
- The example link in `INDEX.md` is illustrative; rewrite once you have real entry points.
- Remove this `README.md` once the template is in use; the verifier needs it only while it lives in this repo.

## Verifier

`docs/superpowers/scripts/verify-guideline.sh notes/evergreen-notes` checks that this README, `GUIDE.md`, `tree.md`, and the `template/` directory all exist with the required sections.
