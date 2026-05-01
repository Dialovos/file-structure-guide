## TL;DR

The **Nx** monorepo layout splits a workspace into `apps/` (deployable units — a Next.js web frontend, a NestJS API, a React Native mobile app) and `libs/` (shared libraries — UI, data-access, feature modules, utilities). The split mirrors Turborepo's `apps/`/`packages/` distinction, but Nx is **far more opinionated**: it ships generators (`nx g @nx/react:lib ui`), enforces module boundaries via tags and ESLint rules (e.g., `feature` libs cannot import from each other), computes a project graph that powers `nx affected` (only test/build what changed), and natively understands polyglot stacks (TypeScript apps next to Java/Go/Rust/Python via plugins). The two load-bearing config files are `nx.json` (workspace-wide caching, target defaults, named inputs, plugin registry) and per-project `project.json` (build/serve/test target definitions). `tsconfig.base.json` declares path aliases (`@my-workspace/ui` → `libs/ui/src/index.ts`) so that `libs/` are importable by name. Nx's killer feature versus Turborepo is **the project graph**: Nx parses imports, builds a real dependency DAG, and `nx affected --target=test` runs only what actually depends on changed files — no manual configuration of which app uses which lib. The cost is ceremony: more configuration up front, more conventions to learn, an Nx Cloud account if you want shared remote caching at scale.

## Principles & why

A Nx workspace is shaped by six principles, each backed by a config file or generator convention.

1. **`apps/` is deployed; `libs/` is composed.** An app has an entry point and produces a deployable artifact (a Next.js bundle, a Docker image, an Electron binary). A lib is a chunk of code consumed by apps and other libs via TypeScript path aliases. Apps should be **thin** — most of the logic lives in `libs/`, and apps wire libs together.
2. **Libs have categories: feature, ui, data-access, util.** Nx's recommended taxonomy: `ui` libs are presentational, `feature` libs are smart components with state, `data-access` libs talk to APIs, `util` libs are pure helpers. Tag each lib (`"tags": ["scope:web", "type:feature"]` in `project.json`) and enforce import rules with `@nx/enforce-module-boundaries` so that `util` cannot import `feature`, etc. This keeps the dependency graph acyclic and intentional.
3. **Path aliases make libs importable by name.** `tsconfig.base.json` declares `"@my-workspace/ui": ["libs/ui/src/index.ts"]`. Apps and libs `import { Button } from "@my-workspace/ui"` — never relative paths across project boundaries. The barrel file (`libs/ui/src/index.ts`) is the public API; nothing outside the lib should import from `libs/ui/src/lib/internal.ts`.
4. **`project.json` declares targets; `nx.json` declares defaults.** Per-project: `targets.build.executor`, `targets.test.options`, etc. Workspace: `targetDefaults.build.cache: true`, `targetDefaults.build.dependsOn: ["^build"]`, `namedInputs` (which files invalidate a cache hash). Inheritance is one-way: project-level overrides workspace-level.
5. **The project graph is automatic.** Nx parses every TS/JS file's imports, plus `package.json` deps, and builds the graph. `nx graph` opens an interactive viz; `nx affected -t test --base=main` runs tests only on projects whose code (or whose dependencies' code) changed since `main`. CI gets dramatically faster on large repos because PR-only changes touch only a slice.
6. **Generators (`nx g`) are first-class.** `nx g @nx/react:lib feature-auth --directory=libs/web/auth` scaffolds the lib, updates `tsconfig.base.json` paths, registers the project, adds tags. Custom generators live in `tools/generators/`. The generator approach trades flexibility for consistency — every lib in the repo looks the same.

A seventh principle: **Nx is incrementally adoptable.** You can add Nx to an existing repo (`npx nx@latest init`) without restructuring; you can use Nx purely as a task runner without generators. The full power (generators + module boundaries + project graph) shows up when the repo gets large.

## When to use

- **Large enterprise monorepos** with dozens of apps and hundreds of libs. Nx's tooling scales to thousands of projects.
- **Polyglot stacks** — TypeScript frontend + NestJS backend + Python ML + Go service. Nx has plugins for all of these and computes a unified project graph across languages.
- **Heavy module-boundary enforcement.** Teams want guarantees that `apps/admin` can't reach into `apps/web`'s code, that `util` libs can't import `feature` libs, etc. Nx's ESLint plugin enforces this at lint time.
- **CI pipelines that need `affected` builds.** PRs that touch one lib should not retest 200 unrelated apps. Nx's project graph + `affected` make this automatic.
- **Teams that want generators, schematics, and a CLI-driven workflow.** `nx g`, `nx run`, `nx graph` are part of daily development.
- **Existing Angular shops.** Nx grew out of Angular; its Angular tooling is unmatched.

## When NOT to use

- **Small repos with one or two apps.** The ceremony of `project.json`, `nx.json`, generators, and tags is overhead. Use `nextjs-app/` or `turborepo-monorepo/`.
- **Pure frontend-only with shared UI.** Turborepo is simpler, ships less config, and covers the common case (Next.js apps + shared component lib) with one fifth the docs surface.
- **Teams allergic to opinionation.** Nx imposes conventions: where libs live, how to scaffold them, how imports flow. Teams that want maximum flexibility chafe at this.
- **Hostile to plugin-driven tooling.** Nx's plugins are powerful but introduce a layer of abstraction over your build tools (webpack, Vite, etc.). If you want raw access to bundler config without going through `@nx/webpack:webpack`, Nx will feel heavy.
- **Single-language projects with no need for cross-cutting CI.** If you don't need `affected`, the project graph, or generators, you don't need Nx.

## Tree diagram

```
my-workspace/
├── nx.json
├── package.json
├── tsconfig.base.json
├── README.md
├── apps/
│   ├── web/
│   │   ├── project.json
│   │   └── src/
│   └── api/
│       ├── project.json
│       └── src/
├── libs/
│   ├── ui/
│   │   └── project.json
│   ├── data/
│   └── shared/
│       └── utils/
└── tools/
    └── generators/
```

## Naming rules

- **Workspace name**: in `package.json` (`"name": "my-workspace"`); also referenced by path-alias scope (`@my-workspace/...`).
- **Apps**: `apps/<name>/`, kebab-case. Match deployment-target names if useful (`web`, `api`, `admin`, `mobile`). The Nx project name in `project.json` matches the directory name.
- **Libs**: `libs/<scope>/<name>/` for grouped libs (e.g., `libs/web/feature-auth`, `libs/api/data-access-users`) — Nx calls this **directory grouping**. Scope tags follow (`scope:web`, `scope:api`, `scope:shared`).
- **Lib type prefixes**: convention is `feature-`, `ui-`, `data-access-`, `util-` (`libs/web/ui-button`, `libs/api/data-access-users`). Communicates intent at a glance.
- **Path aliases** in `tsconfig.base.json`: `@<workspace>/<scope>-<name>` or `@<workspace>/<scope>/<name>`. Pick one convention and apply it everywhere.
- **Targets** (in `project.json`): conventional names — `build`, `serve`, `test`, `lint`, `e2e`, `typecheck`. Custom targets are fine but match the `dash-case` convention.
- **Tags**: `<dimension>:<value>` (`scope:web`, `type:feature`, `platform:browser`). Documented in `nx.json` or per-project; consumed by `@nx/enforce-module-boundaries`.

## Anti-patterns

- **Putting business logic in `apps/`.** Apps should be thin shells that compose libs. If `apps/web/src/services/users.ts` exists, it almost certainly belongs in `libs/web/data-access-users` (or shared, if reused).
- **Importing into a lib via a relative deep path.** `import { Foo } from "../../../libs/ui/src/lib/Foo"` defeats the lib boundary. Always go through the path alias and the barrel: `import { Foo } from "@my-workspace/ui"`.
- **Skipping tags and module-boundary enforcement.** Without tags, the dependency graph is unconstrained and quickly tangles. Configure `@nx/enforce-module-boundaries` from day one.
- **Manually editing `tsconfig.base.json` paths instead of using generators.** `nx g lib` updates paths automatically. Manual edits forget steps; the generator doesn't.
- **Putting one-off scripts in `tools/generators/`.** That directory is for Nx generators (workspace generators that scaffold projects). Throwaway scripts go in `tools/scripts/` or a project-level `scripts/`.
- **Running `npm test` instead of `nx test <project>` or `nx run-many -t test`.** You lose caching, parallelization, and the `affected` filter.
- **Committing the `.nx/` cache directory.** It's machine-local cache; it must be gitignored. The cache key portability comes from Nx Cloud, not from committing the cache.
- **Mixing `apps/` and `libs/` content.** A lib that mounts to a port is an app; an app that's importable as a TypeScript module is a lib. The `project.json` `targets` make the distinction concrete (an app has `serve`/`build`; a lib has `build`/`lint`/`test`).

## Variants

- **Nx-classic (apps/libs, this guide)** — the integrated workspace; everything is Nx-aware. Default for new workspaces.
- **Nx with package-based config** — newer (Nx 16+); each project's tooling lives in standard `package.json` scripts; Nx layers task running and caching on top. Easier incremental adoption in existing repos.
- **Nx + Lerna (legacy hybrid)** — older Angular/JS monorepos that combined Nx (task runner) with Lerna (versioning + publish). Lerna v7 was reborn under Nx, so this hybrid is converging into pure Nx.
- **Nx + standalone apps** — `npx create-nx-workspace --preset=react-standalone` skips the `apps/`/`libs/` split for a single-app project. Useful as an on-ramp; promote to a full workspace later by `nx g lib` and `nx g app`.
- **Nx Cloud (remote cache + distributed task execution)** — same layout; activate via `nx connect-to-nx-cloud`. Distributed task execution splits the test suite across CI runners and shares cache hits. The premium feature on top of OSS Nx.
- **Nx + non-JS plugins** — `@nx/expo`, `@nx/react-native`, `@nrwl/nx-go`, third-party Python/Java plugins. Same `apps/`/`libs/` shape, plugin-specific executors.

## Real-world projects using this

- **nrwl/nx** — Nx itself is an Nx workspace. The canonical example; reading the source teaches you the conventions.
- **storybook/storybook** — Storybook moved its monorepo to Nx; large polyglot codebase with many libs.
- **angular/components** — Angular Material's component library workspace structure mirrors Nx conventions (Angular and Nx share roots).
- **Capital One open-source repos** — several use Nx for enterprise-style polyglot monorepos.
- **Hasura's frontend monorepo** — Hasura Console is an Nx workspace with multiple apps and many libs.
- **`nx-examples`-style starter repos in the nrwl org** — official starters demonstrating Next.js, NestJS, Storybook, React Native within one workspace.
- **Many Fortune 500 internal monorepos** — Nx is widely adopted in enterprise; Nrwl publishes case studies.

## Migration & references

- **From a single-app repo to Nx**: `npx nx@latest init` adds Nx to an existing repo without restructuring. Tasks gain caching immediately; you can incrementally extract libs.
- **From Turborepo to Nx**: similar mental model (`apps/` + `packages/`/`libs/`). The migration is mostly mechanical: rename `packages/` to `libs/`, add a `project.json` per project, port `turbo.json` pipelines to `nx.json` `targetDefaults`, replace `workspace:*` with `tsconfig.base.json` paths. Module-boundary enforcement is new and worth turning on after migration.
- **From Lerna to Nx**: Lerna v7+ uses Nx under the hood; `lerna run` becomes `nx run-many`. Versioning + publish stays with Lerna's commands.
- **Adding a new lib**: `nx g @nx/js:lib utils --directory=libs/shared/utils` (or `@nx/react:lib` etc.). Generator updates `tsconfig.base.json`, scaffolds the lib, registers the project. Add tags afterwards in `project.json`.
- **Adding a new app**: `nx g @nx/next:app web` (or `@nx/nest:app api`, `@nx/expo:app mobile`). Generator scaffolds inside `apps/<name>/`.
- **Connecting Nx Cloud**: `nx connect-to-nx-cloud`. CI gets `NX_CLOUD_ACCESS_TOKEN`. Builds across machines share cache and (with DTE) split work.
- **References**:
  - Nx docs (nx.dev) — comprehensive; especially the *Concepts* and *Recipes* sections.
  - "Mental Models" section of Nx docs — explains apps/libs, types of libs, tags.
  - Sibling guides: `code/turborepo-monorepo/` (simpler alternative), `code/nextjs-app/` and `code/vue-nuxt-app/` (typical contents of `apps/web/`), `code/node-library/` (the shape of a published library if you also publish from libs).
  - Nrwl blog and YouTube channel — patterns and case studies for large workspaces.
