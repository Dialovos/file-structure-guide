## TL;DR

AI coding assistants read plain files in your repository for instructions: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/`, `.github/copilot-instructions.md`. Give them **one shared source of truth** and keep tool-specific files thin. Put the durable rules (how to build, test, name things, what not to touch) in a single `AGENTS.md` at the repository root; make each tool-specific file a short pointer that imports or references it and adds only notes unique to that tool. Add nested `AGENTS.md` files only where a subdirectory really has different rules, and keep every file short and factual. Treat these files as documentation that a reader with no memory of your project must be able to act on: commands that work, conventions that are checkable, and boundaries stated plainly. And treat them as public: never put secrets, personal details, or private paths in them.

## Principles & why

1. **One source of truth.** Rules copied across five files drift apart. The shared rules live in `AGENTS.md`; other files point to it.
2. **Instructions are documentation with a machine reader.** They should be short, concrete, and testable: "run `pytest -q` before committing" beats "write good tests".
3. **Scope by directory.** Rules nearest the code win. A root file states repository-wide rules; a nested file states what differs in that subtree.
4. **State boundaries, not just preferences.** What the assistant must not do (touch generated files, edit migrations, run destructive commands, push without asking) matters more than style notes.
5. **Durable knowledge belongs in project docs, not in a tool's private memory.** If a decision or gotcha matters to the next person or machine, it lives in the README or `docs/`, where every tool and every human sees it.
6. **The files are versioned and reviewed like code.** A wrong instruction misleads every future session; changes go through pull requests.

## When to use

- **Any repository worked on with an AI assistant**, even occasionally.
- **Teams using more than one assistant**, where duplicated instructions would diverge.
- **Workspaces with several projects**, where a root file states shared rules and project files add specifics.
- **Repositories with sharp edges**: generated code, migrations, data files, or security-sensitive directories that should not be edited casually.

## When NOT to use

- **Don't use these files as a knowledge base.** Long architecture essays belong in `docs/`; link to them.
- **Don't put secrets or personal information in them.** They are committed, often public, and read by tools you may not control.
- **Don't try to enforce policy with prose alone.** Rules that must hold (formatting, secret scanning, forbidden files) belong in hooks and CI; the instruction file describes them.
- **Don't duplicate the README.** If setup instructions are in the README, link to them from the agent file.

## Tree diagram

```
repo/
├── AGENTS.md                      ← shared rules; the source of truth
├── CLAUDE.md                      ← pointer: imports AGENTS.md + Claude-specific notes
├── GEMINI.md                      ← pointer to AGENTS.md
├── .github/
│   └── copilot-instructions.md    ← pointer to AGENTS.md
├── .cursor/
│   └── rules/
│       └── project.mdc            ← pointer to AGENTS.md
├── README.md                      ← human-facing; agents link to it for setup
├── docs/
│   └── architecture.md            ← long-form knowledge, linked from AGENTS.md
└── services/
    └── billing/
        └── AGENTS.md              ← only what differs inside billing/
```

## Naming rules

- **`AGENTS.md`** is the shared, tool-neutral file. UPPERCASE is deliberate: it is a canonical meta-file like `README.md` (see `capitalization-policy`).
- **Tool files** use each tool's expected name (`CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursor/rules/*.mdc`). Their names are dictated by the tool, so follow them exactly.
- **Nested files** keep the same name (`AGENTS.md`) at the directory they apply to, so scope is visible from the path.
- **Sections** inside the file use plain headings such as "Commands", "Conventions", "Boundaries", "Where things go".
- **Local overrides** (personal preferences) belong in the tool's gitignored local file, not in the shared one.

## Worked example

A repo has a 400-line `CLAUDE.md`, a slightly different `.cursorrules`, and a Copilot file from a year ago.

1. Read all three and list every distinct rule. Delete rules that are wrong, stale, or obvious.
2. Group the survivors into: commands, conventions, boundaries, layout.
3. Write `AGENTS.md` with those four sections, each rule one line and checkable ("Tests: `pytest -q`", "Never edit `migrations/` by hand; generate with `make migration`").
4. Reduce `CLAUDE.md` to a few lines: an import of `AGENTS.md` and any Claude-only notes (for example, notes about its permissions file).
5. Replace the Cursor and Copilot files with one-paragraph pointers to `AGENTS.md`.
6. Move anything long (architecture, decisions) to `docs/` and link it.
7. Add a CI check that the pointer files still mention `AGENTS.md`, or a periodic review reminder.

New sessions read one short file and act correctly, and there is one place to fix a wrong rule.

## Anti-patterns

- **Copy-pasting the same rules into every tool file.** They drift; the assistant follows whichever it reads.
- **Novel-length instructions.** Long files bury the rules that matter and use up context; keep each file to what changes behavior.
- **Vague aspirations** ("write clean code"). Replace with commands and checks.
- **Instructions that contradict tooling.** A rule that says "never use X" while the linter requires X leaves the assistant stuck.
- **Secrets, tokens, or personal details** in the file, including absolute paths to a home directory.
- **Stale instructions.** A command that no longer works costs more than no instruction; test them like documentation.

## Scaling & failure modes

- **Monorepos and workspaces**: keep the root file for cross-cutting rules and give each project a nested file; be explicit that tools which do not load nested files need the root file to name them (for example, "read the nearest `AGENTS.md` before editing a project").
- **Context budget**: every line is read every session. Prune regularly, and move rarely needed detail to linked docs.
- **Multiple tools with different loading rules** (some load only the root file, some load nested ones): put critical rules at the root.
- **Team review**: treat changes like code review, because a bad rule affects everyone's sessions.
- **Drift from reality**: add the instruction file to your release or quarterly checklist.

## Variants

- **AGENTS.md only**: sufficient when your tools all read it.
- **AGENTS.md plus thin pointers** (this guide): the safest choice for mixed tooling.
- **Per-directory AGENTS.md**: for large repositories where subtrees have different rules.
- **Tool-specific rich files**: only for capabilities unique to one tool (custom commands, hooks, permissions), never for shared rules.
- **Docs-first**: keep the substance in `docs/` and have `AGENTS.md` be an index of links plus the boundaries.

## Adoption checklist

- [ ] One `AGENTS.md` at the root holds the shared rules; other files point to it.
- [ ] Every command in the file was run successfully in the last month.
- [ ] Boundaries (what not to touch, what needs approval) are stated explicitly.
- [ ] No secrets, personal emails, or absolute home paths appear in any instruction file.
- [ ] Long-form knowledge is in `docs/` and linked, not pasted.
- [ ] Tool-specific files are under about 20 lines.

## Real-world projects using this

- **agents.md** (the open `AGENTS.md` convention) documents the shared file and is read by a number of coding agents.
- **Claude Code** reads `CLAUDE.md` (with import syntax to include other files), **Gemini CLI** reads `GEMINI.md`, **GitHub Copilot** reads `.github/copilot-instructions.md`, and **Cursor** reads `.cursor/rules/`. Each tool's documentation states its precise loading rules.
- **Open-source repositories** increasingly include `AGENTS.md` alongside `CONTRIBUTING.md`; reading a few gives concrete examples of command and boundary sections.

## Migration & references

- **From several tool files:** consolidate into `AGENTS.md`, then convert the others into pointers (see the worked example).
- **From tool-private memory:** move durable facts (decisions, gotchas) into the README or `docs/`, so other tools and other machines see them.
- **To nested files:** add a nested `AGENTS.md` only after the root file has a rule that doesn't apply to a subtree.
- **References:**
  - `principles/readme-placement/` for human-facing documentation placement.
  - `principles/config-and-secrets-placement/` for keeping credentials away from files tools can read.
  - `code/github-repository-meta/` for `.github/` conventions.
  - `files/workspace-root-layout/` for a root file shared across projects.
