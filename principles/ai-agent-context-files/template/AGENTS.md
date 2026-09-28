# Agent instructions

Shared rules for every AI assistant working in this repository. Change shared rules here.

## Commands

- Install: `<install command>`
- Test: `<test command>`
- Lint and format: `<lint command>`

## Conventions

- Follow the naming and layout rules in `README.md`.
- Keep changes small and focused; do not refactor unrelated code.

## Boundaries

- Do not edit generated files (`dist/`, `build/`) or files listed in `.gitignore`.
- Do not commit secrets. Real values belong in a gitignored `.env`; commit only `.env.example`.
- Ask before pushing, opening pull requests, or deleting branches.

## Where things go

- Long-form design notes: `docs/`
- Decisions: `docs/adr/`
