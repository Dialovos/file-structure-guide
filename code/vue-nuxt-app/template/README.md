# Nuxt 3 — template

A `cp -r`-able starter for a Nuxt 3 project. Filesystem routing,
auto-imported components and composables, a sample API endpoint
(`server/api/hello.get.ts`), and a default layout. TypeScript-first.

## What lives where

- **`pages/`** — every URL in the app. `pages/index.vue` is `/`,
  `pages/about.vue` is `/about`, `pages/blog/[slug].vue` is
  `/blog/:slug`. The file tree *is* the route table.
- **`components/`** — Vue components, auto-imported in any template
  by their PascalCase name (`BaseButton.vue` → `<BaseButton />`).
  No `import` statements needed.
- **`composables/`** — shared `useXxx()` hooks (`useAuth`, `useCart`).
  Auto-imported in any `<script setup>`.
- **`layouts/`** — wrappers with a `<slot />` for the page content.
  `default.vue` runs unless a page opts in to a different layout via
  `definePageMeta({ layout: "..." })`.
- **`server/api/`** — backend endpoints. `hello.get.ts` becomes
  `GET /api/hello`. The `defineEventHandler` helper is the universal
  shape.
- **`public/`** — static files served at the root URL, untouched by
  the build (`favicon.ico`, `robots.txt`).
- **`assets/`** — files processed by the build (CSS, fonts, source
  images). Imported via `~/assets/...`.

## What to rename

- `package.json` `"name"`: replace `my-app`.
- `LICENSE` `{{YEAR}}` and `{{NAME}}`.

## What to fill

- Real composables in `composables/` (replace the stub `useAuth`).
- Real components in `components/`.
- Real API endpoints in `server/api/`.
- Real pages in `pages/`.

## What to delete

- This template `README.md`.
- `.gitkeep` files in `public/` and `assets/styles/` once they have
  real content.
- `pages/about.vue` if you don't need an About route.

## First run

```bash
npm install
npm run dev        # http://localhost:3000
npm run build      # production SSR build
npm run preview    # serve the build locally
npm run generate   # static site generation (SSG)
```

The `postinstall` script runs `nuxt prepare`, which generates the
`.nuxt/` typings used by `tsconfig.json`. If TypeScript complains
about missing types after a fresh checkout, run `npm run postinstall`
manually.

## Auto-imports — what's real

The following are auto-imported and need *no* `import` line:

- Anything in `components/` — by its PascalCase file name.
- Anything in `composables/` — by its export name.
- Anything in `utils/` — same.
- Nuxt-provided helpers: `useFetch`, `useAsyncData`, `useState`,
  `useRoute`, `useRouter`, `navigateTo`, `definePageMeta`,
  `defineEventHandler`, etc.

If your editor doesn't see them, run `npm run postinstall` to
regenerate `.nuxt/auto-imports.d.ts`.

## Pair this with

- `../GUIDE.md` — full reasoning behind this layout.
- `../nextjs-app/` — React/Next.js equivalent.
- `../turborepo-monorepo/` — when you scale to multiple Nuxt apps.
- The Nuxt docs at nuxt.com/docs — canonical reference, especially
  the *Directory Structure* and *Auto-imports* pages.
