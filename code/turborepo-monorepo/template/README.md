# Turborepo monorepo — template

A `cp -r`-able starter for a Turborepo + pnpm monorepo. Two
deployable apps in `apps/` (web, docs), a shared UI package in
`packages/ui`, and shared `eslint-config` and `typescript-config`
packages. Pipeline declared in `turbo.json`; remote-cache-ready.

## What lives where

- **`apps/web/`** — a Next.js app. Imports `@my-monorepo/ui`.
- **`apps/docs/`** — a Next.js docs app (placeholder). Same shape.
- **`packages/ui/`** — shared React component library. JIT (no build);
  consumers' bundlers compile the TypeScript.
- **`packages/typescript-config/`** — shared `tsconfig` files. Apps
  and packages `extend` `@my-monorepo/typescript-config/base.json`.
- **`packages/eslint-config/`** — shared ESLint config. Apps and
  packages `extends: ["@my-monorepo/eslint-config"]`.

## What to rename

- `package.json` `"name"`: replace `my-monorepo`.
- `packages/*/package.json` `"name"`: replace the `@my-monorepo/*`
  scope with your scope.
- `apps/web/package.json` workspace deps (`@my-monorepo/...`).
- `LICENSE` `{{YEAR}}` and `{{NAME}}`.

A find-replace of `@my-monorepo` across the repo is the fastest path.

## What to fill

- `apps/web/` — scaffold a real Next.js app inside it (`pnpm create
  next-app@latest apps/web`). The `package.json` in this template
  is a stub showing the expected dependency shape.
- `apps/docs/` — similar; `.gitkeep` is just there to track the dir.
- `packages/ui/src/` — real components beyond the sample `Button`.

## What to delete

- This template `README.md`.
- `.gitkeep` files inside `apps/web/` and `apps/docs/` once the apps
  exist.

## First run

```bash
pnpm install            # installs across all workspaces
pnpm dev                # `turbo run dev` — starts web and docs in parallel
pnpm build              # `turbo run build`
pnpm lint               # `turbo run lint`
pnpm typecheck          # `turbo run typecheck`
```

`pnpm <task>` at the root delegates to `turbo run <task>`, which
handles topological ordering and caching. Run a task in just one
workspace with `pnpm --filter <name> <task>`.

## Adding a workspace

```bash
# A new app:
mkdir apps/admin
cd apps/admin && pnpm create next-app@latest .
# Add @my-monorepo/ui to its dependencies, then:
pnpm install        # from the root

# A new package:
mkdir packages/utils
# Create packages/utils/package.json with name "@my-monorepo/utils"
# Source in packages/utils/src/
pnpm install        # from the root
```

## Remote caching

```bash
npx turbo login
npx turbo link
```

In CI, set `TURBO_TOKEN` and `TURBO_TEAM` (already in the sample
`.github/workflows/ci.yml`). Builds across machines now share cache.

## Pair this with

- `../GUIDE.md` — full reasoning behind this layout.
- `../nx-monorepo/` — the more opinionated alternative.
- `../nextjs-app/` — the typical contents of `apps/web/`.
- The Turborepo docs at turbo.build/repo/docs — canonical reference.
