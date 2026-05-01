# Feature-based frontend — template

A `cp -r`-able starter for a React app organised by feature. Each
feature lives under `src/features/<name>/` as a self-contained slice
(`components/`, `api/`, `hooks/`, `types.ts`, `index.ts`). Cross-feature
shared code lives in `src/components/ui/`, `src/lib/`, `src/types/`.
The shape tracks `alan2207/bulletproof-react`.

## What to rename

- `my-app` → your app name in `package.json`.
- The `customer-onboarding` and `billing` features are placeholders.
  Rename or replace them with your real first features once they
  exist.

## What to fill

- **`src/app/`** — your framework's entry. For Vite this is
  `main.tsx` + `App.tsx`; for Next.js App Router this is the
  `app/` directory with `layout.tsx`, `page.tsx`, route folders.
- **`src/features/<name>/index.ts`** — the public API of the
  feature. Add exports as new components/hooks become consumable
  by other features.
- **`src/components/ui/`** — generic, presentational UI primitives
  shared across features (Button, Input, Modal). No business logic.
- **`src/lib/`** — utilities that are not React (date formatting,
  HTTP wrappers, validation helpers).
- **`LICENSE`** — replace `{{YEAR}}` and `{{NAME}}`.

## What to delete

- This `README.md` once you have a real one.
- The placeholder `customer-onboarding` feature once your real
  first feature lands.

## First run

```bash
npm install            # or pnpm / yarn / bun
npm run dev
```

Open `http://localhost:5173`. Run tests with `npm test`.

## Layout cheat-sheet

| You're looking for…                | Path                                                    |
|------------------------------------|---------------------------------------------------------|
| App entry / routes                 | `src/app/`                                              |
| Feature folder                     | `src/features/<feature>/`                               |
| Feature public API                 | `src/features/<feature>/index.ts`                       |
| Feature components                 | `src/features/<feature>/components/<Component>.tsx`     |
| Feature hooks                      | `src/features/<feature>/hooks/use<X>.ts`                |
| Feature network code               | `src/features/<feature>/api/<x>-client.ts`              |
| Cross-feature shared UI primitives | `src/components/ui/`                                    |
| Cross-feature utilities            | `src/lib/`                                              |
| App-global types                   | `src/types/`                                            |

## Boundary rules (enforce in CI)

- A feature imports only from `@/features/<self>/...`,
  `@/components/...`, `@/lib/...`, `@/types/...`.
- A feature **does not** import from `@/features/<other>/components/...`
  — only from `@/features/<other>` (the barrel).
- `src/components/ui/` and `src/lib/` **do not** import from
  `src/features/`.

Tooling: `eslint-plugin-import` `no-restricted-paths` or
`eslint-plugin-boundaries` makes this enforceable on every PR.

## Pair this with

- `../GUIDE.md` — full reasoning behind the layout.
- `../nextjs-app/` — the routing layer this layout composes with.
- `../atomic-design/` — when you're building a component library
  rather than an app.
- `../turborepo-monorepo/` — when features should graduate into
  packages.
