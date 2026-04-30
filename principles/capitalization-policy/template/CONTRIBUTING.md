# Contributing

This file is one of the canonical UPPERCASE meta-files (`README.md`,
`LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`,
`SECURITY.md`). GitHub renders it specially in the PR-creation flow, which
is the contract that gives the UPPERCASE convention its meaning.

## Capitalization policy in this template

- **UPPERCASE** is reserved for the canonical closed set defined in
  `template/README.md`. Don't invent new UPPERCASE filenames.
- **lowercase kebab-case** for everything else: source files, config files,
  ordinary docs, asset files. See `lowercase-feature.md` next to this file
  for an example of a non-canonical doc that lives lowercase.

## How to file a contribution

This is a stub. In a real project:

1. Open an issue describing the change.
2. Fork, branch, and submit a PR referencing the issue.
3. Follow the project's coding and naming conventions — including the
   capitalization policy above.

## When to add a new UPPERCASE file

Almost never. The canonical set is intentionally closed. If you find
yourself wanting to add `INSTALL.md` UPPERCASE, the right move is one of:

- A new section inside `README.md`.
- A lowercase file under `docs/` (e.g. `docs/installing.md`).
- A canonical addition (`CHANGELOG.md`, `CODE_OF_CONDUCT.md`) if it fits
  the existing closed set.
