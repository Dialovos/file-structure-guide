# Nx monorepo — template

A `cp -r`-able starter for an Nx integrated workspace. Two apps in
`apps/` (a `web` frontend, an `api` backend), shared libs in `libs/`
(`ui`, `data`, `shared/utils`), workspace generators in
`tools/generators/`, and load-bearing config in `nx.json`,
`tsconfig.base.json`, and per-project `project.json` files.

## What lives where

- **`apps/web/`** — frontend application (Vite + React assumed in the
  sample `project.json`; swap the executor for the framework you use:
  `@nx/next:*` for Next.js, `@nx/expo:*` for React Native, etc.).
- **`apps/api/`** — backend application (webpack + Node sample;
  `@nx/nest:*` for NestJS).
- **`libs/ui/`** — shared presentational components. Importable as
  `@my-workspace/ui` via `tsconfig.base.json` paths.
- **`libs/data/`** — data-access layer (REST/GraphQL clients, query
  hooks).
- **`libs/shared/utils/`** — pure utilities, no framework dependencies.
- **`tools/generators/`** — workspace generators (`nx g
  ./tools/generators/<name>`). Empty here; populate as conventions
  emerge.

## What to rename

- `package.json` `"name"`: replace `my-workspace`.
- `tsconfig.base.json` `paths`: replace `@my-workspace/...` with your
  scope.
- `LICENSE` `{{YEAR}}` and `{{NAME}}`.

A find-replace of `@my-workspace` across the repo is the fastest path.

## What to fill

- `apps/web/src/` — real application source (the Nx generator will
  scaffold this when you run `nx g @nx/react:app web` against an empty
  workspace, but here we ship the directory structure so you can
  `git mv` an existing app in).
- `apps/api/src/` — backend source.
- `libs/ui/src/` — `index.ts` (the public barrel) plus components.
- `libs/data/src/`, `libs/shared/utils/src/` — same shape (`index.ts`
  + sources).
- `apps/*/tsconfig.app.json`, `libs/*/tsconfig.lib.json`,
  `*/jest.config.ts`, `*/.eslintrc.json` — produced by Nx generators.
  Run `nx g @nx/js:lib utils --directory=libs/shared/utils` (etc.) on
  a fresh checkout to scaffold.

## What to delete

- This template `README.md`.
- `.gitkeep` files inside lib/app source directories once real source
  exists.

## First run

```bash
pnpm install
pnpm exec nx graph                     # interactive project graph
pnpm exec nx serve web                 # serve the web app
pnpm exec nx run-many -t build         # build everything
pnpm exec nx affected -t test          # test only what changed vs. main
```

`pnpm <task>` at the root delegates to `nx run-many` (see
`package.json` `scripts`).

## Adding a project

```bash
# A new lib (recommended path; the generator wires up paths):
nx g @nx/js:lib feature-checkout --directory=libs/web/feature-checkout

# A new app:
nx g @nx/next:app admin                # for Next.js
nx g @nx/nest:app worker               # for a NestJS service
```

The generator updates `tsconfig.base.json`, scaffolds `project.json`,
and registers the project. Add module-boundary `tags` in the new
`project.json` (`scope:web`, `type:feature`, etc.) and turn on
`@nx/enforce-module-boundaries` in your ESLint config.

## Module boundaries (recommended)

In your root ESLint config:

```json
{
  "rules": {
    "@nx/enforce-module-boundaries": [
      "error",
      {
        "allow": [],
        "depConstraints": [
          { "sourceTag": "scope:web", "onlyDependOnLibsWithTags": ["scope:web", "scope:shared"] },
          { "sourceTag": "scope:api", "onlyDependOnLibsWithTags": ["scope:api", "scope:shared"] },
          { "sourceTag": "type:feature", "onlyDependOnLibsWithTags": ["type:feature", "type:ui", "type:data-access", "type:util"] },
          { "sourceTag": "type:ui", "onlyDependOnLibsWithTags": ["type:ui", "type:util"] },
          { "sourceTag": "type:util", "onlyDependOnLibsWithTags": ["type:util"] }
        ]
      }
    ]
  }
}
```

This stops `apps/web` from reaching into `apps/api`, stops `util`
libs from importing `feature` libs, etc.

## Nx Cloud (remote cache + DTE)

```bash
pnpm exec nx connect-to-nx-cloud
```

CI gets `NX_CLOUD_ACCESS_TOKEN`; builds across machines share cache
hits. With DTE enabled, the test suite splits across CI runners
automatically.

## Pair this with

- `../GUIDE.md` — full reasoning behind this layout.
- `../turborepo-monorepo/` — the simpler alternative.
- `../nextjs-app/`, `../vue-nuxt-app/` — typical contents of an app
  inside `apps/`.
- The Nx docs at nx.dev — canonical reference (especially
  *Concepts* and *Recipes*).
