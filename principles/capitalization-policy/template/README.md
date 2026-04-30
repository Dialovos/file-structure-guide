# Capitalization-policy template

This template is itself an example of the policy it teaches: the only
UPPERCASE files are the canonical set (`README.md`, `LICENSE`,
`CONTRIBUTING.md`); everything else (`lowercase-feature.md`) is lowercase
kebab-case.

## What's here

- `README.md` — this file. Canonical UPPERCASE. Doubles as both the template's usage notes (below) and the full policy explanation. There is exactly one `README*.md` in this template by design — adding a second would split the policy across files and mute the signal.
- `LICENSE` — canonical UPPERCASE, no extension. Stub MIT-flavoured placeholder; not a real license assignment. See the file itself.
- `CONTRIBUTING.md` — canonical UPPERCASE. Stub explaining the capitalization policy from a contributor's angle.
- `lowercase-feature.md` — a non-canonical document. Demonstrates the lowercase kebab-case convention applied to ordinary docs.

## To adopt this template

1. Copy the template into your project root: `cp -r template/* <your-project>/`.
2. Replace `LICENSE` with a real license file. Keep the canonical UPPERCASE filename.
3. Replace `CONTRIBUTING.md` with your project's actual contribution guidelines (or delete if the project is private and the file isn't needed). Keep the canonical UPPERCASE filename.
4. Rename or delete `lowercase-feature.md`. New non-canonical docs should follow the same lowercase-kebab-case convention. Most non-canonical docs go in `docs/`.
5. Replace this README's contents with your project's actual README, but keep the file at canonical UPPERCASE `README.md`.

## The capitalization policy (full)

UPPERCASE is reserved for the closed canonical set:

```
README.md          CONTRIBUTING.md    CHANGELOG.md
LICENSE            CODE_OF_CONDUCT.md SECURITY.md
GUIDE.md           INDEX.md           CHOOSE.md
PHILOSOPHY.md      ANTIPATTERNS.md    GLOSSARY.md
```

Everything else is lowercase, with kebab-case for multi-word names
(`getting-started.md`, not `gettingStarted.md` or `getting_started.md` —
unless your language is Python or similar, where `snake_case.py` is the
ecosystem norm).

Two motivations:

1. **Visual signal.** UPPERCASE only works if it's rare. Reserving it for
   the canonical set keeps the signal sharp.
2. **Tooling contract.** GitHub (and most other forges) render
   `README.md`, `LICENSE`, `CONTRIBUTING.md`, etc. specially. Inventing
   new UPPERCASE filenames doesn't extend that contract; it just makes
   readers and tools wonder which UPPERCASE files are special.

## Why a single README in this template

The original template plan suggested a second README-style notes file
(`README-template-notes.md`). We deliberately fold that content into this
single `README.md` for two reasons:

1. **One canonical README per directory.** A second `README*.md` muddies
   the rule the template is trying to teach.
2. **Verifier expectation.** `docs/superpowers/scripts/verify-guideline.sh`
   checks for exactly one `template/README.md`; a parallel
   `README-template-notes.md` would either be redundant or fight the
   verifier's contract.

If you need separate sections of guidance, structure them as headings
within this file (as done above), not as parallel files.

## Acceptance test

Run this command from your project root after adopting:

```bash
find . -type f -name "*.md" \
  | grep -v node_modules \
  | grep -E '/[A-Z][A-Z0-9_-]+\.md$' \
  | grep -vE '/(README|LICENSE|CONTRIBUTING|CHANGELOG|CODE_OF_CONDUCT|SECURITY|GUIDE|INDEX|CHOOSE|PHILOSOPHY|ANTIPATTERNS|GLOSSARY)\.md$'
```

Empty output means full compliance: every UPPERCASE markdown file is in
the canonical set.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this
`template/README.md` to exist. Don't delete it before replacing.
