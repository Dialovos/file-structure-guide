# Next.js App Router — template

A `cp -r`-able starter for a Next.js 14+ App Router project with
TypeScript. Server components by default, route groups, an API route,
and the standard four-folder layout (`app/`, `components/`, `lib/`,
`public/`).

## What lives where

- **`app/`** — every URL in the app. Each route is a folder with a
  `page.tsx` (and optionally `layout.tsx`, `loading.tsx`, `error.tsx`).
  API routes live in `app/api/<name>/route.ts`. Route groups are
  parenthesized folders (e.g. `(marketing)`) that organize without
  appearing in the URL.
- **`components/ui/`** — presentational primitives (Button, Input,
  Card). No business logic. Imported by many routes.
- **`components/feature/`** — composed feature components (UserCard,
  PostList) that may import from `lib/`. Still reusable; just bigger.
- **`lib/`** — non-component utilities. Database clients, auth helpers,
  formatters, validators. Server-side only.
- **`public/`** — static files served at the root URL. `favicon.ico`,
  `robots.txt`, `og-image.png`. Don't import from here in code; use
  static imports for images you want optimized by `next/image`.
- **`styles/`** — only if you want non-Tailwind, non-`globals.css`
  stylesheets. Most projects leave this empty and put everything in
  `app/globals.css`.

## What to rename

- `package.json` `"name"`: replace `my-app`.
- `app/layout.tsx` `metadata.title` / `metadata.description`.
- `LICENSE` `{{YEAR}}` and `{{NAME}}`.

## What to fill

- `lib/db.ts` — wire up your real database driver (Prisma, Drizzle, pg).
- `lib/auth.ts` — wire up your real auth library (NextAuth, Clerk).
- Real components in `components/ui/` and `components/feature/`.
- Real `public/favicon.ico` (the file in this template is a zero-byte
  placeholder).

## What to delete

- This template `README.md`.
- `app/(marketing)/about/page.tsx` if you don't want a route group
  example.
- `app/api/hello/route.ts` once you have real API routes.
- `.gitkeep` files in `components/ui/` and `components/feature/` once
  they have real content.

## First run

```bash
npm install
npm run dev      # http://localhost:3000
npm run build    # production build
npm run start    # serve the production build
npm run lint     # eslint via next lint
```

## Server Components vs. Client Components

Files in `app/` are Server Components by default. They run only on the
server and ship zero JS to the browser. To opt a file into client-side
rendering, add `"use client"` at the top:

```tsx
"use client";
import { useState } from "react";
// ...
```

Use Client Components when you need: `useState`/`useEffect`, event
handlers (`onClick`), browser-only APIs (`window`, `localStorage`),
context providers, third-party libraries that depend on the DOM.

Use Server Components for: data fetching with `await`, secrets (DB
connection strings), heavy logic you don't want shipped to the client.

## Pair this with

- `../GUIDE.md` — full reasoning behind this layout.
- `../vue-nuxt-app/` — Vue/Nuxt equivalent.
- `../turborepo-monorepo/` — when you have multiple Next apps that
  share components.
- The Next.js docs — `nextjs.org/docs/app` is the canonical reference.
