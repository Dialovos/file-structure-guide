## TL;DR

The **Turborepo** monorepo layout splits a workspace into two top-level directories: `apps/` for deployable units (a Next.js web app, a docs site, a CLI, a backend service) and `packages/` for shared libraries (a UI component library, ESLint config, TypeScript config, business-logic SDK). The split is the whole idea: anything you `npm install`-style depend on lives in `packages/`; anything you `git push` and deploy lives in `apps/`. The two load-bearing config files are `turbo.json` (declarative pipeline: which tasks depend on which, what to cache) and `pnpm-workspace.yaml` (which subdirectories are workspaces). Turborepo itself is a *task runner with a remote cache* — it doesn't bundle, doesn't compile, doesn't enforce conventions on what's inside `apps/web/`. It just runs `pnpm build` (or whatever you tell it) across the workspace, in topological order, with caching. The single most important mental shift from a single-package repo is **internal packages** (`@my-monorepo/ui`) — these are listed in dependents' `package.json` like any npm package, but they resolve to `../packages/ui` via the workspace protocol. The single most common mistake is putting too much in `packages/` (only put it there if 2+ apps actually use it). This guide uses **pnpm + Turborepo + TypeScript**; npm/yarn/bun variants are documented below.

## Principles & why

A Turborepo is shaped by five principles, each enforced by a specific config file or convention.

1. **`apps/` deploys, `packages/` ships internally.** An `app` has a `Dockerfile`/Vercel config/whatever; it's a deployable artifact. A `package` has a `package.json` with `main`/`exports`; it's consumed by other workspaces. Putting a shared component library in `apps/` because "it has UI" is wrong — if it's reused, it belongs in `packages/`.
2. **`turbo.json` is a DAG of tasks, not a build script.** You don't write `pnpm --filter web build && pnpm --filter docs build` anywhere. You declare in `turbo.json` that `build` in any package depends on `^build` (its dependencies' build) and outputs `dist/**`. Then `turbo build` figures out the order, parallelizes the independent ones, and caches everything. The pipeline is *declarative*.
3. **Workspace dependencies use the workspace protocol.** In `apps/web/package.json`: `"@my-monorepo/ui": "workspace:*"`. pnpm resolves `workspace:*` to the local `packages/ui` directory (a symlink); npm/yarn use the `workspaces` field at the root for the same effect. This is what makes `apps/web` import `@my-monorepo/ui` and have it just work.
4. **Caching is keyed by inputs, restored to outputs.** Turborepo hashes the source files, dependency manifests, and env vars listed as inputs to a task; if the hash matches a cached result, it skips the task and restores the outputs (`dist/`, `.next/`, etc.). Configure this per-task in `turbo.json`. The remote cache (Vercel-hosted or self-hosted) shares the cache across CI runs and team members — this is the productivity story.
5. **Internal packages can be unbuilt or built.** *Just-in-time* (JIT) packages are pure TypeScript that consumers compile (e.g., a Next.js app's bundler reads `packages/ui/src/index.ts` directly). *Compiled* packages have a `build` step that produces `dist/` and are consumed via `dist/index.js`. JIT is simpler; compiled is necessary if non-bundler consumers (a Node CLI) use the package. The Turborepo docs lay out the trade-offs explicitly.

A sixth, softer principle: **shared config is its own package.** `packages/eslint-config`, `packages/typescript-config`, `packages/prettier-config` are package-shaped (have a `package.json`, exposed via the workspace) so that downstream apps `extends` from them. This avoids copy-pasting `.eslintrc` across every app.

## When to use

- **Two or more apps share a UI component library, design system, or business-logic SDK.** The classic motivating case.
- **Frontend monorepos with multiple deployable surfaces** — marketing site, dashboard, admin, mobile web. Sharing components across them.
- **Sub-second incremental builds at scale.** Turborepo's caching is the strongest selling point on a CI that's run many times a day.
- **Vercel-deployed apps.** Vercel's Turborepo support is first-class — remote caching is one click in the dashboard.
- **Mixed runtime apps.** A Next.js web app + a Node CLI + a Cloudflare Worker can all sit in `apps/` and share `packages/`.

## When NOT to use

- **Single-app projects.** A monorepo for one app is overhead with zero payoff. Use `nextjs-app/` directly.
- **Heavy build-tool customization, code generation, or polyglot backends.** `nx-monorepo/` is more opinionated and includes generators, project graph viz, and language-aware tooling for backends. For pure-frontend with shared UI, Turborepo wins on simplicity; for enterprise polyglot, Nx wins on power.
- **Large numbers of independently versioned packages published to npm.** Lerna or changesets-only setups handle versioning more deeply. Turborepo can integrate with changesets, but the focus is task running, not versioning.
- **No shared code at all.** If `apps/web` and `apps/docs` don't share *any* code, you don't need a monorepo — separate repos are simpler.

## Tree diagram

```
my-monorepo/
├── package.json                ← workspace root
├── pnpm-workspace.yaml
├── turbo.json
├── tsconfig.json               ← base, extended by apps/packages
├── README.md
├── apps/
│   ├── web/                    ← Next.js app
│   │   └── package.json
│   └── docs/                   ← Next.js docs site
├── packages/
│   ├── ui/                     ← shared component library
│   │   ├── package.json
│   │   └── src/
│   ├── eslint-config/
│   └── typescript-config/
└── .github/workflows/ci.yml
```

## Naming rules

- **Workspace root**: project name in `package.json` (`my-monorepo`); `"private": true` is mandatory (the root is never published).
- **Apps**: `apps/<name>/` — short, kebab-case names (`web`, `docs`, `api`, `admin`). Match Vercel project names if deploying there.
- **Packages**: `packages/<name>/` — kebab-case directory; the `name` in `package.json` is scoped (`@my-monorepo/<name>`). The scope marks them as internal to this monorepo.
- **Config packages**: `packages/eslint-config`, `packages/typescript-config`, `packages/tailwind-config`, `packages/prettier-config`. Conventional names; downstream `extends` from them.
- **Pipeline tasks** in `turbo.json`: short, lowercase verbs (`build`, `dev`, `lint`, `test`, `typecheck`). Multiple-word tasks use `:` (`db:migrate`, `test:e2e`).
- **Cache outputs**: relative paths from each package (`dist/**`, `.next/**`, but never `.next/cache/**` — that's already cached by Turborepo's input layer).

## Worked example

Two apps and a shared UI library live in one repo; CI rebuilds everything and the UI package is copied via relative imports.

1. Declare workspaces in `pnpm-workspace.yaml` (`apps/*`, `packages/*`).
2. Create `packages/ui` with its own `package.json` (`"name": "@acme/ui"`) and consume it with `"@acme/ui": "workspace:*"` from the apps.
3. Define the pipeline in `turbo.json`, for example `build` with `dependsOn: ["^build"]` and `outputs: ["dist/**"]`.
4. Share configs as packages (`packages/eslint-config`, `packages/typescript-config`).
5. Run `turbo run build test lint`; a second run should show `FULL TURBO` cache hits.
6. Enable remote caching for CI so branches reuse each other's results.

Changing one package only rebuilds that package and its dependents.

## Anti-patterns

- **Putting one-off scripts in `packages/`.** A package is meant to be `import`ed by 2+ consumers. A throwaway script for one app belongs in that app's `scripts/` directory. Don't pollute `packages/` with single-use code.
- **Cross-importing between apps.** `apps/web` should never `import` from `apps/docs`. If they share code, factor it into a `packages/<shared>/`.
- **Forgetting to set `outputs` in `turbo.json`.** A task without `outputs` declared can't be cache-restored — Turborepo runs it every time. Set `"outputs": ["dist/**"]` (or `.next/**`, etc.) explicitly per task.
- **Using `"main": "src/index.ts"` in an internal package without bundler awareness.** This works for JIT packages consumed by Next.js (which understands TS source), but breaks for non-bundler consumers (a Node CLI). Either commit to JIT and document it, or build to `dist/`.
- **Editing the root `package.json` to add app dependencies.** App dependencies go in `apps/<name>/package.json`. The root `package.json` should only have devDependencies that operate on the whole repo (turbo, prettier, typescript at the root level if shared).
- **Gitignoring `pnpm-lock.yaml`.** The lockfile is the deterministic install record across the whole workspace. Commit it.
- **Running tasks with `pnpm <task>` instead of `turbo run <task>`.** You lose caching and topological ordering. Always go through Turbo for monorepo-wide tasks.
- **Putting `node_modules` in the repo.** Each workspace gets its own `node_modules` (managed by pnpm); they're all gitignored at the root.

## Scaling & failure modes

- **Undeclared outputs or inputs** create wrong cache hits; declare `outputs` and `inputs` and watch for stale results.
- **Dependency hoisting** issues appear with pnpm strictness; fix phantom dependencies by declaring what you import.
- **Package proliferation**: a package needs an owner and a reason (shared by two consumers).
- **Versioning** of internal packages is usually unnecessary (`workspace:*`); use changesets only for published ones.

## Variants

- **Turborepo + pnpm (this guide)** — pnpm is the most efficient; uses `pnpm-workspace.yaml`. Default for new projects.
- **Turborepo + npm workspaces** — `"workspaces": ["apps/*", "packages/*"]` in root `package.json`. Slower installs, larger `node_modules`. Works fine.
- **Turborepo + yarn berry (v3+)** — yarn's plug'n'play resolution can speed installs. Slightly different config; some Turbo features need yarn berry's `nodeLinker` set to `node_modules` to work cleanly.
- **Turborepo + bun** — bun-as-package-manager works; bun-as-runtime works for some apps. Newer, less battle-tested for monorepos as of 2025-2026.
- **Turborepo + changesets** — for monorepos that publish packages to npm. Adds `.changeset/` directory and a release workflow. Common for component libraries with public packages.
- **Turborepo with remote caching** — same layout; enable in the Turbo dashboard or self-host. The killer feature for large CI; same code locally.

## Adoption checklist

- [ ] `turbo run build` twice shows cache hits on the second run.
- [ ] Every task declares `dependsOn` and `outputs` accurately.
- [ ] Shared lint and TypeScript configs live in packages.
- [ ] Each internal package declares all its imports.
- [ ] CI uses caching and runs only affected tasks (`--filter=...[origin/main]`).

## Real-world projects using this

- **vercel/turborepo** — Turborepo itself; the repo is dogfood. The `examples/` directory contains canonical starters (basic, pnpm, with-tailwind, design-system, kitchen-sink).
- **vercel/commerce** — Vercel's commerce starter; the larger versions are Turborepo monorepos with `apps/` and `packages/`.
- **shadcn-ui/taxonomy** — Next.js + Turborepo; smaller, instructive.
- **t3-oss/create-t3-turbo** — t3-stack (Next.js, Prisma, tRPC) inside a Turborepo. Common starting point for full-stack apps.
- **Vercel's official pnpm/turbo starter templates** — `npx create-turbo@latest` scaffolds a fresh repo following the conventions in this guide.
- **Cal.com** — a real production Turborepo (apps/web, packages/lib, packages/ui, etc.).

## Migration & references

- **From a single-app repo to a Turborepo**: create `apps/web/`, `git mv` the existing app's contents into it. Add `packages/`. Add `pnpm-workspace.yaml`, `turbo.json`. Move shared logic into `packages/<name>` one piece at a time. Update CI to run `turbo run build test lint` from the root.
- **From npm workspaces to pnpm**: install pnpm (`npm install -g pnpm`), `rm -rf node_modules package-lock.json`, add `pnpm-workspace.yaml`, run `pnpm install`. Lockfile changes from `package-lock.json` to `pnpm-lock.yaml`. Most workspaces migrate cleanly; check for any dependencies that depend on hoisted node_modules (rare but possible).
- **Adding a new app**: `mkdir apps/admin`, scaffold inside it (`pnpm create next-app@latest apps/admin`), add `"@my-monorepo/ui": "workspace:*"` to its `package.json`, run `pnpm install` from the root. Turborepo picks up the new workspace automatically.
- **Adding a shared package**: `mkdir packages/utils`, create `package.json` with `"name": "@my-monorepo/utils"`, source in `src/`, declare `"exports"`. Add to consumers' dependencies as `"@my-monorepo/utils": "workspace:*"`. Run `pnpm install`.
- **Enabling remote cache**: `npx turbo login`, then `npx turbo link`. CI gets `TURBO_TOKEN` and `TURBO_TEAM` env vars. Builds across machines now share cache.
- **References**:
  - Turborepo docs (turbo.build/repo/docs) — canonical reference, especially *Pipelines* and *Caching*.
  - pnpm docs — *Workspace* page covers the workspace protocol.
  - Vercel blog — *Why Turborepo* (architectural rationale and case studies).
  - Sibling guides: `code/nx-monorepo/` (the more opinionated alternative), `code/nextjs-app/` (the typical contents of `apps/web/`).
