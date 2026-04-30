# Hidden-files-policy template

This template is itself an example of the policy it teaches. The visible
file you're reading right now (`README.md`) sits next to three hidden
dotfiles (`.gitignore`, `.editorconfig`, `.env.example`) that demonstrate
the three flavours of "things a leading dot is for."

## What's here

Visible (no leading dot — contributor knowledge):

- `README.md` — this file. Canonical UPPERCASE; explains the template.

Hidden (leading dot — tool plumbing):

- `.gitignore` — tool-mandated dotfile. Git looks up this exact name.
  Contains realistic ignore patterns with explanatory comments.
- `.editorconfig` — tool-mandated dotfile. Editors auto-discover it by
  walking up the directory tree. Sets formatting defaults.
- `.env.example` — convention-mandated dotfile. Hidden because it's in
  the `.env*` family; **committed** because new contributors need to
  discover which variables to set. The populated `.env` itself is
  gitignored (see the patterns in `.gitignore`).

## The three flavours of dotfile

This template covers each of the canonical hidden-file shapes:

1. **Hidden + tracked + tool-defined.** `.gitignore` and `.editorconfig`
   are part of the project; their dotted names are required by the tools
   that read them. Contributors edit them rarely.
2. **Hidden + tracked + as-a-template.** `.env.example` is hidden because
   it's in the env-file family, but committed so contributors know it
   exists. The pattern is "this is your template — copy it before
   editing."
3. **Hidden + gitignored** (illustrated, not present in the template
   itself). `.env`, `.venv/`, `.idea/`, `.vscode/` — local-only state.
   See the `.gitignore` for the actual ignore patterns.

## Why these *aren't* hidden

By policy, the following files in this template are visible (no dot):

- `README.md` — contributors must read it to use the template.
- (When you adopt the template, your `pyproject.toml` / `package.json` /
  `Cargo.toml` / `Makefile` go here visibly too. They're load-bearing
  knowledge, not plumbing.)

The litmus test: would a contributor ever open the file to read or edit
it for project reasons? If yes, visible. If only the tool reads it,
hidden is fine.

## To adopt this template

1. Copy the dotfiles into your project root: `cp -r template/.* <your-project>/`
   (and `cp template/README.md <your-project>/` if you want this README's
   notes — usually you'll replace it with your own project README).
2. Adjust `.gitignore` patterns for your stack. Keep the comment blocks
   so future contributors understand *why* each pattern is there.
3. Tune `.editorconfig` to match your codebase's indentation rules.
4. Edit `.env.example` to list every environment variable your
   application actually reads. Keep placeholder values — never real
   secrets.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this
`template/README.md` to exist. Don't delete it before replacing.
