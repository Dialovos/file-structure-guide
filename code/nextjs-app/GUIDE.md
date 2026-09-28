## TL;DR

The **Next.js App Router** layout (Next 13+, default for new apps in 14/15) is built around four top-level directories: `app/` for routes (file-system-based, server components by default), `components/` for shared React UI, `lib/` for non-component utilities (DB clients, auth helpers, validators), and `public/` for static assets served at the root URL. Routes are folders containing special files: `page.tsx` (rendered route), `layout.tsx` (wrapper), `loading.tsx`, `error.tsx`, `route.ts` (API endpoint). The single most important mental shift from the legacy Pages Router is that **components in `app/` are React Server Components by default** — they render on the server, can `await` data directly, and ship zero JS to the client unless marked `"use client"`. The `app/` directory is the source of truth for the URL tree; `components/` and `lib/` are flat, framework-agnostic helpers that `app/` imports from. This template uses the **App Router with TypeScript**, no `src/` directory (the `src/` variant is documented below), Tailwind-ready `globals.css`, and the modern `next.config.js` shape. The single most common mistake is dropping `"use client"` everywhere out of habit and losing the server-component benefits — only mark a file client when it actually needs hooks, browser APIs, or event handlers.

## Principles & why

The App Router layout encodes five principles, each with a specific cost if violated.

1. **`app/` is the URL.** Folder names map directly to URL segments. `app/about/page.tsx` is `/about`. `app/blog/[slug]/page.tsx` is `/blog/:slug`. `app/(marketing)/about/page.tsx` is *also* `/about` — parentheses are *route groups*, organizational folders that don't appear in the URL. This means moving a folder moves the URL; renaming a folder renames the URL. Predictability is the whole point.
2. **Server Components by default.** A `page.tsx` or `layout.tsx` without `"use client"` runs only on the server. It can `async function Page()` and `await` data inline. It ships zero JavaScript to the browser for that component. Marking a component `"use client"` opts into the legacy React model (state, effects, event handlers) and ships its JS to the client. Use server components for anything that doesn't need interactivity; use client components for forms, modals, anything with `useState`/`useEffect`.
3. **Co-location inside `app/`.** Tests, styles, sub-components, types — anything *only* used by one route — lives next to that route's `page.tsx`. Files in `app/` whose name isn't a recognized special name (`page`, `layout`, `loading`, `error`, `not-found`, `route`, `template`, `default`) are *not* routable; they're just regular files. So `app/blog/[slug]/post-header.tsx` and `app/blog/[slug]/page.test.tsx` are private to that route.
4. **`components/` is flat and reusable.** Anything imported by 2+ routes belongs in `components/`. This template splits it into `components/ui/` (presentational primitives — Button, Input, Card; no business logic) and `components/feature/` (composed feature components — UserCard, PostList; may import from `lib/`). The split mirrors atomic-design vocabulary without enforcing the full hierarchy.
5. **`lib/` is the non-React kitchen.** Database clients, auth helpers, fetch wrappers, schema validators (Zod), formatters — anything that isn't a React component. If a file exports a function and not a component, it lives in `lib/`. This separation means you can swap UI frameworks without touching `lib/`, and you can unit-test `lib/` without rendering.

A sixth, softer principle: **`public/` is the root URL.** Anything in `public/foo.png` is served at `/foo.png`. No build step, no import. Use it for `favicon.ico`, `robots.txt`, `og-image.png`, and any third-party verification files. Imports from inside `app/` should *not* go through `public/` — use static imports for images you actually want optimized.

## When to use

- **New Next.js projects.** App Router is the default since Next 13.4 (May 2023) and the strong recommendation in the Next.js docs.
- **Apps that benefit from server components.** Content-heavy sites, dashboards with server-side data fetching, anything where shipping less JS matters.
- **Apps using Server Actions.** Server actions (form submissions handled server-side without an API route) are an App-Router-only feature.
- **Streaming UI / Suspense at the page level.** `loading.tsx` and `<Suspense>` boundaries are first-class in the App Router; awkward in Pages Router.
- **Edge runtime deployments.** Cleaner ergonomics than Pages Router's `getServerSideProps`.

## When NOT to use

- **Legacy Next.js projects on Pages Router.** Migrating is incremental but non-trivial; if your project is large and stable, the Pages Router (documented as a variant below) is still supported and not deprecated.
- **Frameworks other than Next.js.** Use `vue-nuxt-app/` for Nuxt; use the Astro/Remix/SvelteKit-specific guides if/when those exist. App Router conventions are Next-specific.
- **Static-export-only sites with no dynamic routes.** Astro or plain Vite is lighter; Next is overkill for a brochure site.
- **Backend-heavy services.** If your app is 90% API and 10% UI, a dedicated backend framework (`fastapi-project/`, NestJS) plus a small frontend is cleaner. Next API routes work, but they're not the strongest tool for that job.

## Tree diagram

```
my-app/
├── package.json
├── next.config.js
├── tsconfig.json
├── README.md
├── .gitignore
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── globals.css
│   ├── api/
│   │   └── hello/route.ts
│   └── (marketing)/
│       └── about/page.tsx
├── components/
│   ├── ui/                       ← presentational, reusable
│   └── feature/                  ← feature-specific, composed
├── lib/                          ← non-component utilities
│   ├── db.ts
│   └── auth.ts
├── public/                       ← static, served as-is
│   └── favicon.ico
└── styles/                       ← if not all in app/globals.css
```

## Naming rules

- **Special files in `app/`** are reserved names: `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`, `route.ts` (API), `template.tsx`, `default.tsx`. These are the *only* files Next routes through. Any other filename in `app/` is a private file (good for co-located helpers).
- **Dynamic routes**: `[slug]` for one segment, `[...slug]` for catch-all, `[[...slug]]` for optional catch-all. Brackets are literal directory names.
- **Route groups**: `(marketing)`, `(auth)`, `(dashboard)` — parenthesized names that organize routes without affecting the URL.
- **Private folders**: `_components/`, `_lib/` — leading underscore; Next ignores them for routing. Useful for co-located helpers shared across a subtree.
- **Component files**: `PascalCase.tsx` (`Button.tsx`, `UserCard.tsx`). Matches the React component name. One default export per file.
- **Utility files in `lib/`**: `kebab-case.ts` or `camelCase.ts` — pick one. `db.ts`, `auth.ts`, `format-date.ts`. Multiple named exports are fine.
- **API routes**: `app/api/foo/route.ts` (the file is *named* `route.ts`; the URL segment is the parent folder). Export `GET`, `POST`, etc. as named functions.

## Worked example

A Pages Router app mixes API routes and UI logic; the team wants server components and cleaner data loading.

1. Create `app/` with a root `layout.tsx` and `page.tsx`; migrate route by route (both routers can coexist during migration).
2. Turn each page into a server component that fetches data directly, and mark only interactive leaves with `"use client"`.
3. Move endpoints from `pages/api/*` to `app/api/<name>/route.ts`.
4. Put data access and auth helpers in `lib/`, and import them only from server code (`import "server-only"`).
5. Group routes without changing URLs using route groups: `app/(marketing)/about/page.tsx`.
6. Add `loading.tsx` and `error.tsx` beside routes that fetch.
7. Check the client bundle with `next build` output and remove any accidental server imports.

Most components ship no client JavaScript and data loading sits next to the route that uses it.

## Anti-patterns

- **Sprinkling `"use client"` everywhere.** Defeats the App Router's main benefit. Default to server; opt into client only when you need hooks or browser APIs.
- **Putting non-route components in `app/` outside their route's folder.** If a component is shared across routes, move it to `components/`. `app/` should contain routes and their private helpers, nothing else.
- **Importing from `app/` into `components/`.** Direction-of-dependency violation. `app/` imports from `components/` and `lib/`, never the reverse.
- **Mixing App Router and Pages Router on the same routes.** `pages/about.tsx` and `app/about/page.tsx` will conflict. Pick one router per route. (You *can* coexist them on different routes during a migration.)
- **Storing large media in `public/`.** `public/` ships unchanged; large images don't get Next's image optimization. Import images from inside `app/` or `components/` so `next/image` can process them.
- **Putting database connection logic in a Client Component.** Anything in a `"use client"` file gets bundled to the browser. Keep DB code in `lib/` and only call it from server components or route handlers.
- **Using `next.config.js` `experimental.appDir`.** That flag was for Next 13's beta period; on Next 14+, App Router is on by default and the flag is gone. Old tutorials may still mention it.
- **Forgetting `export const dynamic = "force-dynamic"`** when a route reads cookies/headers and needs to opt out of static rendering. Next will sometimes silently statically render and your page goes stale.

## Scaling & failure modes

- **`"use client"` creep**: one client boundary too high pulls a whole subtree into the bundle. Push it down to the smallest interactive component.
- **`components/` sprawl**: split `ui/` primitives from feature components, or use `feature-based-frontend` colocation inside `app/`.
- **Caching semantics** change between Next releases; pin the version and read the release notes when upgrading.
- **Environment variables**: only `NEXT_PUBLIC_*` reach the browser; review any variable you add for secrets.

## Variants

- **App Router (this guide)** — Next 13+, default for new projects. Server components, server actions, file-system routing.
- **App Router with `src/`** — same layout, but everything lives under `src/` (`src/app/`, `src/components/`, `src/lib/`). Some teams prefer this for a cleaner repo root. Next supports it natively; just create the `src/` directory.
- **Pages Router** — legacy (still supported, not deprecated). `pages/` instead of `app/`. `pages/api/` for API routes. `getServerSideProps`/`getStaticProps` for data fetching. Older docs assume this layout.
- **Turbopack-built** — Next's new bundler (vs. webpack). Same file layout; difference is build performance. Enable with `next dev --turbo`. Stable for dev; experimental for prod builds as of Next 14.
- **Hybrid** — Pages Router and App Router coexisting on different routes during migration. Common during transition periods. Eventually consolidate to App Router.

## Adoption checklist

- [ ] Only components that need interactivity have `"use client"`.
- [ ] Server-only modules import `server-only`.
- [ ] Each data-fetching route has `loading.tsx` and `error.tsx`.
- [ ] No secret is exposed via `NEXT_PUBLIC_` variables.
- [ ] `next build` output has been checked for unexpected large client bundles.

## Real-world projects using this

- **vercel/commerce** — Next.js commerce starter; canonical App Router layout with route groups for marketing vs. shop.
- **vercel/next.js** — the Next.js repo itself; the `examples/` directory has dozens of App Router examples (`with-tailwindcss`, `with-prisma`, `with-stripe-typescript`, etc.).
- **shadcn-ui/taxonomy** — instructive App Router project; full-stack with auth, MDX, route groups, server actions. Reads like a tutorial.
- **vercel/nextjs-postgres-nextauth-tailwindcss-template** — small, focused App Router starter that combines NextAuth, Postgres, and Tailwind.
- **Next.js Learn** — the official tutorial at nextjs.org/learn; builds an App Router dashboard from scratch with the conventions this guide describes.
- **t3-oss/create-t3-app** — opinionated starter combining Next App Router, tRPC, Prisma, NextAuth, Tailwind. Wider stack than this guide but the file layout is App-Router-canonical.

## Migration & references

- **From Pages Router to App Router**: Next's docs include an incremental migration guide. The short version: `app/` and `pages/` can coexist on different routes, so move one route at a time. Start with leaf pages (no shared layout); leave routes with complex `getServerSideProps` for last. Update data-fetching to `async` server components. Replace `useRouter` (next/router) with `useRouter`/`usePathname`/`useSearchParams` from `next/navigation`.
- **From Webpack to Turbopack**: change `"dev": "next dev"` to `"dev": "next dev --turbo"`. No code changes; if a third-party plugin breaks, fall back to webpack.
- **From flat `app/` to `src/app/`**: create `src/`, `git mv app components lib styles src/`. Update `tsconfig.json` `paths` if you used aliases. Next picks up `src/app/` automatically.
- **From `next.config.js` to `next.config.mjs`**: rename, switch `module.exports` to `export default`. Required if you want to `import` ESM modules in your config. Next supports both; ESM is the modern default.
- **References**:
  - Next.js docs — *App Router* (the canonical reference for everything in this guide).
  - React docs — *Server Components* (background reading; explains why the App Router is shaped this way).
  - Vercel blog — *Why we built the App Router* (architectural rationale).
  - Sibling guides: `code/vue-nuxt-app/` (Vue equivalent), `code/turborepo-monorepo/` (when you outgrow one app).
