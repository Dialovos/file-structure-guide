## TL;DR

The **Nuxt 3** layout is the convention-over-configuration counterpart to Next.js: every top-level directory has a meaning Nuxt knows about, and you almost never write the wiring yourself. `pages/` becomes the file-system router, `components/` is auto-imported (no explicit `import` statements anywhere), `composables/` exposes shared `useFoo()` hooks (also auto-imported), `layouts/` wraps pages, `server/api/` is the API surface (handlers with `defineEventHandler`), and `public/` and `assets/` separate served-as-is files from build-pipeline files. The single most important mental model is **auto-imports**: a `BaseButton.vue` in `components/` is usable as `<BaseButton />` in any template without an `import` line; a `useAuth.ts` in `composables/` is callable as `useAuth()` from any setup script. This is a productivity feature, not magic — Nuxt scans these directories at build time and generates the imports for you. The single most common mistake is fighting the auto-import system by adding manual `import` statements that conflict with Nuxt's generated ones (you'll get duplicate-binding errors). This guide uses **Nuxt 3 with TypeScript**, no `src/` directory (the `src/` variant is documented), and Vue 3 Composition API throughout. Older `nuxt.config.js` (Nuxt 2) is documented as a legacy variant.

## Principles & why

Nuxt's directory layout encodes five conventions, each with a build-step that pays for the convention.

1. **Filesystem routing in `pages/`.** A `.vue` file at `pages/about.vue` becomes the route `/about`. `pages/blog/[slug].vue` is `/blog/:slug`. `pages/index.vue` is `/`. No router config — the file tree *is* the route table. Nuxt auto-generates `vue-router` config from this directory.
2. **Auto-imports.** Files in `components/`, `composables/`, `utils/`, and certain Nuxt-provided helpers (`useFetch`, `useState`, `navigateTo`) are automatically importable in any `.vue` file or `<script setup>` block. The `.nuxt/` build output contains generated `auto-imports.d.ts` so TypeScript and your editor know about them. Write less import boilerplate; let Nuxt wire it up.
3. **Composables for shared logic.** A `composable` is a function that returns reactive state and uses Vue's Composition API. `useAuth()`, `useCart()`, `useTheme()` are typical. They live in `composables/`, are auto-imported, and replace the role of Vuex/Redux for many use cases. (Pinia is the modern store layer if you want explicit global state — it works fine alongside composables.)
4. **`server/` is the backend, in the same repo.** Nuxt 3's `server/` directory turns Nuxt into a full-stack framework. `server/api/hello.get.ts` becomes `GET /api/hello`. `server/middleware/` runs on every request. `server/routes/` for non-API routes (e.g., webhooks). The `defineEventHandler` helper is the universal handler shape; it works on Node, Edge, and serverless deployments without code changes.
5. **`public/` vs. `assets/` is a real distinction.** Files in `public/` are copied verbatim to the build output and served at the root URL — `public/robots.txt` becomes `/robots.txt`. Files in `assets/` go through the build pipeline (Vite) — they get hashed, optimized, tree-shaken, and you import them by path (`~/assets/styles/main.css`). Static-as-is goes in `public/`; build-time-processed goes in `assets/`.

A sixth, softer principle: **layouts are `<slot />`-shaped wrappers.** A layout in `layouts/default.vue` is a Vue component with a `<slot />` that the page renders into. Use layouts for headers/footers/sidebars shared across pages. A page can opt into a non-default layout by setting `definePageMeta({ layout: "admin" })`.

## When to use

- **New full-stack Vue projects.** Nuxt 3 is the default Vue meta-framework; the Vue ecosystem points here for serious apps.
- **SSR / static generation.** Nuxt handles SSR, SSG, ISR, and SPA modes from the same codebase. `nuxt build` for SSR, `nuxt generate` for SSG.
- **Apps that want auto-imports.** If the boilerplate of explicit imports bothers you, Nuxt's auto-import system is the strongest argument for it.
- **Vue + a backend in one repo.** `server/` lets you keep the API and the UI together when they're tightly coupled.
- **TypeScript-first projects.** Nuxt 3's TypeScript support is excellent — `tsconfig.json` extends an auto-generated one that knows about your `pages/`, `components/`, `composables/`, etc.

## When NOT to use

- **Plain Vite + Vue projects.** No auto-imports, no filesystem routing, no `server/`. Lighter, less magic. Use it when you want full control and don't need a meta-framework.
- **Nuxt 2 codebases.** Nuxt 2's layout is similar but not identical (no `composables/`, no `server/`, different config shape). Documented as a legacy variant. Migration to Nuxt 3 is non-trivial; don't mix conventions.
- **React projects.** Use `nextjs-app/` for React. Nuxt is Vue-only.
- **Backend-heavy services with thin UIs.** A dedicated backend (`fastapi-project/`, NestJS) is cleaner; Nuxt's `server/` is great for full-stack but isn't trying to compete with a dedicated backend framework.
- **Deeply customized Vue routing.** If you need programmatic router config (lazy guards, role-based redirects implemented in JS), Nuxt's filesystem routing fights you. Use plain Vue Router.

## Tree diagram

```
my-app/
├── package.json
├── nuxt.config.ts
├── tsconfig.json
├── README.md
├── pages/
│   ├── index.vue
│   └── about.vue
├── components/
│   ├── BaseButton.vue
│   └── FeatureCard.vue
├── composables/
│   └── useAuth.ts
├── layouts/
│   └── default.vue
├── server/
│   └── api/
│       └── hello.get.ts
├── public/
└── assets/
    └── styles/
```

## Naming rules

- **Pages**: `kebab-case.vue` (`about.vue`, `blog-archive.vue`). Route URL matches the filename. Dynamic segments use square brackets: `[slug].vue`, `[...path].vue` for catch-all.
- **Components**: `PascalCase.vue` is conventional and recommended (`BaseButton.vue`, `FeatureCard.vue`). Auto-import name matches the file name. Multi-word names avoid clashing with HTML elements (Vue's style guide rule).
- **Composables**: `useXxx.ts` — leading `use` is the conventional prefix for any function that uses Vue's reactivity (`useAuth`, `useCart`, `useTheme`). Auto-imported as `useAuth`, `useCart`, etc.
- **Layouts**: `kebab-case.vue` (`default.vue`, `admin.vue`, `auth.vue`). The default layout is `default.vue`; pages without `definePageMeta({ layout: "..." })` use it.
- **Server handlers**: `<name>.<method>.ts` — `hello.get.ts` for `GET /api/hello`, `users.post.ts` for `POST /api/users`. Method-less names (`hello.ts`) handle all methods. Catch-all routes via `[...].ts`.
- **Plugins**: in `plugins/`, `kebab-case.ts`. They auto-run on app start.
- **Middleware**: in `middleware/`, `kebab-case.ts`. Apply per-page with `definePageMeta({ middleware: "auth" })`.

## Worked example

A Vue SPA with manual router config and imports at the top of every file moves to Nuxt 3.

1. Move views to `pages/`; the file names produce routes (`pages/users/[id].vue` gives `/users/:id`).
2. Move shared components to `components/` and drop their explicit imports (they are auto-imported by name).
3. Extract logic into `composables/useAuth.ts` and call `useAuth()` anywhere without importing.
4. Add server endpoints under `server/api/` (`hello.get.ts` with `defineEventHandler`), replacing a separate backend proxy.
5. Use `useFetch` or `useAsyncData` for data so it runs on the server and hydrates without a second request.
6. Configure `nuxt.config.ts` runtime config: private values in `runtimeConfig`, browser-exposed values in `runtimeConfig.public`.
7. Verify with `npx nuxi typecheck` and `nuxt build`.

The wiring code disappears and data loads during server rendering.

## Anti-patterns

- **Manual `import` statements for auto-imported things.** `import BaseButton from "~/components/BaseButton.vue"` plus auto-import on the same name will produce a duplicate-binding error or just be redundant. Trust the auto-import system; your editor's IntelliSense will pick it up via the generated `.nuxt/auto-imports.d.ts`.
- **Storing state in plain modules.** A top-level `const cart = ref([])` in a regular `.ts` file is shared across requests in SSR — every user sees every other user's cart. Use `useState()` (Nuxt-provided, request-scoped) or a Pinia store.
- **Putting source files in `public/`.** They won't be processed by Vite (no hashing, no minification, no Tailwind). Use `assets/` for source files; `public/` for opaque blobs.
- **Importing from `assets/` with a leading `/`.** `/assets/styles/main.css` won't resolve (that's the URL convention; `public/` uses `/`). Use `~/assets/styles/main.css` or the `assets:` alias.
- **`pages/` as a generic dump.** Anything not used as a route should not be in `pages/`. A `pages/components/` folder is wrong — every `.vue` in `pages/` becomes a route. Use `components/` for non-route components.
- **Mixing Options API and Composition API in new code.** Pick one. Nuxt 3 strongly favors Composition API + `<script setup>`. Mixing creates inconsistent patterns; new contributors get confused.
- **Using `.nuxt/` files directly.** That's the build output — generated, gitignored, ephemeral. Treat it as opaque.
- **Forgetting `definePageMeta` on a page that needs a non-default layout.** The page silently uses `default.vue` and your custom layout never runs.

## Scaling & failure modes

- **Auto-import ambiguity**: component names derive from paths; nested folders create long names, and duplicates collide. Keep names unique and prefer explicit folders.
- **Hydration mismatches** come from browser-only code (`window`, random values) in render paths; wrap in `onMounted` or `<ClientOnly>`.
- **Module sprawl**: each Nuxt module adds config surface; audit them on upgrade.
- **Large apps** may adopt layers (`extends`) to share code across Nuxt projects.

## Variants

- **Nuxt 3 default (this guide)** — the layout most new projects use; auto-imports, `server/`, Composition API.
- **Nuxt 3 with `srcDir: "src/"`** — set in `nuxt.config.ts`; everything moves under `src/`. Some teams prefer the cleaner repo root. Trade-off is one more level of nesting.
- **Nuxt 2 (legacy)** — different layout: no `composables/`, no `server/api/`, `nuxt.config.js` instead of `.ts`, Options API as the default, `store/` for Vuex. Migration to Nuxt 3 is recommended where feasible.
- **Nuxt + Pinia** — replaces `useState` for global state. Add `@pinia/nuxt` module; create stores in `stores/`. Auto-imported alongside composables.
- **Nuxt + content** — `@nuxt/content` module for Markdown-driven content. Adds a `content/` directory; pages query it with `queryContent()`.
- **Nuxt as static site** — `nuxt generate` for SSG. Same layout; output is a folder of HTML files plus client-side hydration.

## Adoption checklist

- [ ] `nuxi typecheck` and `nuxt build` pass.
- [ ] Private secrets are only in `runtimeConfig`, never `runtimeConfig.public`.
- [ ] Data fetching uses `useFetch`/`useAsyncData`, not raw `fetch` in components.
- [ ] Component names are unique and match their folder path.
- [ ] Browser-only code is guarded against server rendering.

## Real-world projects using this

- **nuxt/nuxt** — Nuxt itself; the repo includes example apps under `examples/` showing every convention.
- **nuxt/starter** — official starter at github.com/nuxt/starter; minimal but canonical.
- **vueuse/vueuse** — Vue composition utilities; their docs site is a Nuxt app and a good reference for `composables/` patterns.
- **Vueform** — form library; their docs are a Nuxt 3 app (`vueform.com`).
- **Volta.net**, **Storyblok demos**, **Vercel's Nuxt examples** — production Nuxt 3 apps; all use the conventions in this guide.
- **The Nuxt docs site** itself (nuxt.com) is a Nuxt app, dogfooding every convention.

## Migration & references

- **From Nuxt 2 to Nuxt 3**: official migration guide at nuxt.com/docs/migration. Major changes: replace Options API with Composition API, move API logic from `~/api/` to `~/server/api/`, replace Vuex with Pinia or `useState`, update `nuxt.config.js` shape (becomes `nuxt.config.ts` with `defineNuxtConfig`), audit modules for Nuxt 3 compatibility. The official `@nuxt/bridge` package eases the transition.
- **From plain Vite + Vue to Nuxt 3**: `npx nuxi init` a fresh project, then move files: routes go to `pages/`, shared logic goes to `composables/`, components stay in `components/` (rename to PascalCase if not already), the API moves into `server/api/`. Remove explicit `import` statements for auto-imported items.
- **Adding `src/` to an existing flat Nuxt 3 app**: set `srcDir: "src/"` in `nuxt.config.ts`, `git mv pages components composables layouts server src/`, update any path aliases. Build will pick up the new layout.
- **Switching from `useState` to Pinia**: install `@pinia/nuxt`, add to `modules` in `nuxt.config.ts`, create `stores/<name>.ts` files with `defineStore`. Migrate piecemeal; both can coexist.
- **References**:
  - Nuxt docs (nuxt.com/docs) — the canonical reference, especially the *Directory Structure* page.
  - Vue 3 docs — *Composition API* and *Reactivity Fundamentals*.
  - Pinia docs (pinia.vuejs.org) — for the state-management upgrade path.
  - Sibling guides: `code/nextjs-app/` (React/Next equivalent), `code/turborepo-monorepo/` (when you scale to multiple Nuxt apps).
