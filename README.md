# file-structure-guide

A reference of **102 in-depth guidelines** for organizing files and folders cleanly.

## What this is

Three domains, plus cross-cutting principles:

- **[principles/](principles/)** — 21 cross-cutting principles (naming, ISO dates, secrets, decision records, monorepo-vs-polyrepo, ...)
- **[code/](code/)** — 36 software project layouts (Python, Rust, JS/TS, JVM, systems, mobile, infrastructure, research, architecture patterns)
- **[notes/](notes/)** — 23 knowledge & note-taking systems (PARA, Johnny.Decimal, Zettelkasten, Evergreen, LYT, coursework, lab notebooks, ...)
- **[files/](files/)** — 22 general personal-files layouts (XDG, FHS, photos, dotfiles, backups, workspaces, media libraries, ...)

## How to use it

Three access paths:

| Path | Entry point | Use it when |
|---|---|---|
| **Browse by domain** | the four category READMEs above | "What are my options for X?" |
| **Search by name** | [INDEX.md](INDEX.md) | "Where is the `johnny-decimal` guide?" |
| **Decide by question** | [CHOOSE.md](CHOOSE.md) | "I'm starting a new Rust library — which layout?" |

## Repo conventions

- Every guideline lives in its own dir with `GUIDE.md`, `tree.md`, and a `template/` you can `cp -r`.
- Every `GUIDE.md` has the same 13 sections, from TL;DR through a worked example, scaling and failure modes, and an adoption checklist (checked by `scripts/check_guide.py`).
- Directory names use kebab-case. UPPERCASE is reserved for canonical files (`README`, `GUIDE`, `INDEX`, `CHOOSE`, `PHILOSOPHY`, `ANTIPATTERNS`, `GLOSSARY`) — see [`principles/capitalization-policy/`](principles/capitalization-policy/).
- Maximum 3 levels deep (`category/guideline/template/`) — see [`principles/depth-vs-breadth/`](principles/depth-vs-breadth/).

## Pointers

- [PHILOSOPHY.md](PHILOSOPHY.md) — the 7 values that thread every guideline
- [ANTIPATTERNS.md](ANTIPATTERNS.md) — cross-cutting bad habits with examples
- [GLOSSARY.md](GLOSSARY.md) — terms used across guides
- [INDEX.md](INDEX.md) — alphabetical catalog
- [CHOOSE.md](CHOOSE.md) — decision tree

## Dogfooding

This guide eats its own dogfood: its layout demonstrates `principles/depth-vs-breadth/`, `principles/naming-conventions/`, and `principles/readme-placement/`. Read [the principles category](principles/) for the rules in action.
