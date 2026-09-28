## TL;DR

The **feature-based frontend layout** organises a React/Vue/Svelte app by *what it does*, not by *what kind of file each thing is*. Each user-facing capability lives in `src/features/<feature-name>/{components,api,types,hooks,index.ts}` as a self-contained slice. Cross-feature shared code lives in `src/components/ui/` (generic UI primitives), `src/lib/` (utilities), and `src/types/` (global types). The `index.ts` of a feature is its public API: it re-exports the few components, hooks, or types that other features may consume; everything else is internal. The discipline is the boundary: features are deletable as a unit, never reach into a sibling feature's `components/` directly, and never live half-in-features-half-in-`/components/`. The shape was popularised by Alan Alickovic's *Bulletproof React* and is now the default in T3, Vercel "best practice" examples, and most React shops past the prototype stage. Adopt it once you have ≥5 features. Skip it for 1-page apps and component libraries (those want `code/atomic-design/`).

## Principles & why

The feature layout enforces three separations that fight the natural drift of frontend codebases.

1. **Features are vertical, technical types are horizontal.** A "type-driven" tree (`/components/`, `/hooks/`, `/api/`, `/utils/` at the root) groups together unrelated work that happens to share a file extension. The cost shows up at scale: a billing change touches 4–5 sibling directories and the same code review must scan all of them. Feature-based grouping inverts the choice — one folder per capability — so a PR for "billing" is contained, and the file list of a feature is its TOC. The horizontal split (UI primitives vs. business code) still exists, but at the *feature* boundary, not at every file.
2. **`index.ts` is the public API of a feature.** Other features and the app shell import only from `@/features/<feature>` (the barrel). They do not reach into `@/features/<feature>/components/Internal.tsx`. This restriction makes refactors cheap (move things inside a feature freely; only the `index.ts` is the contract) and makes deletion safe (delete the folder, fix the imports, done). ESLint rules (e.g., `eslint-plugin-boundaries` or `eslint-plugin-import` `no-restricted-paths`) are how you enforce this in CI.
3. **Shared is the exception, not the default.** When two features need the same `<Button>`, it goes to `src/components/ui/`. When two features need the same `formatCurrency`, it goes to `src/lib/`. But "shared by default" is a trap — `/components/` and `/utils/` become catch-alls and the feature folders thin out to almost nothing. The right rule: code starts inside a feature and is *promoted* to shared only when a second consumer appears. One real consumer beats ten anticipated ones.

The layout works best in apps with 5+ features and team members who don't all touch every feature. Tiny apps (1–2 features) pay the indirection cost without getting the benefit; component libraries are inherently horizontal (atoms/molecules/organisms) and should use `code/atomic-design/` instead.

## When to use

- **React, Vue, or Svelte apps with ≥5 user-facing features.** The break-even point is around the moment the first developer says "I can never find anything."
- **Teams with feature-ownership boundaries.** Each squad owns one or more features; the layout matches the team layout.
- **Apps shipping to production with non-trivial business logic.** The feature isolation pays off the first time you delete a feature flag or sunset a feature.
- **Migration target from a "type-driven" sprawl** (`forms/`, `api/`, `types/`, `views/` at root). Feature folders are how you escape the catch-all.
- **Combinations with monorepo tools** (Turborepo, Nx). Each feature can graduate to its own package once the boundaries harden — see `code/turborepo-monorepo/`.

## When NOT to use

- **Tiny apps with 1–2 features.** A flat `src/` with `App.tsx`, a few components, and a `lib/` is honest. You can always restructure later; the cost is low for small apps.
- **Component libraries.** Atoms / molecules / organisms is the right vocabulary; use `code/atomic-design/`. Component libraries are horizontal by construction.
- **Pure design-system repos.** Same as above — Storybook-driven libraries are organised by component, not by feature.
- **Frameworks with mandated layout.** If you're shipping a Remix or Next.js app where the framework drives the file tree, follow the framework first; layer features inside its conventions (Next.js: features still live in `src/features/`, while `src/app/` holds routes).
- **Throwaway prototypes and demos.** Keep them flat; restructure when they survive past the spike.

## Tree diagram

```
my-app/
├── package.json
├── README.md
├── src/
│   ├── app/                                ← Next.js routes / Vite entry
│   ├── features/
│   │   ├── customer-onboarding/
│   │   │   ├── components/
│   │   │   │   ├── OnboardingForm.tsx
│   │   │   │   └── ProgressIndicator.tsx
│   │   │   ├── api/
│   │   │   │   └── onboarding-client.ts
│   │   │   ├── hooks/
│   │   │   │   └── useOnboardingState.ts
│   │   │   ├── types.ts
│   │   │   └── index.ts                    ← public API
│   │   └── billing/
│   ├── components/                         ← cross-feature shared UI
│   │   └── ui/
│   ├── lib/                                ← cross-feature utilities
│   └── types/                              ← global types
└── tests/
```

## Naming rules

- **Feature folder**: kebab-case (`customer-onboarding/`, `account-settings/`). The name is a domain noun, not a UI label.
- **Component file**: PascalCase (`OnboardingForm.tsx`). Matches React's component-naming convention; the file name and the default export name are the same.
- **Hook file**: camelCase, prefix `use` (`useOnboardingState.ts`). The file exports the hook as a named export with the same name.
- **API file**: kebab-case, suffix `-client` or `-api` (`onboarding-client.ts`). Files contain network/data-access functions, not React code.
- **Types file**: lowercase `types.ts` for the feature's own types; `src/types/` for app-global types.
- **Barrel**: every feature has an `index.ts`. It re-exports *only* the public API of the feature — components, hooks, types other features may need. It deliberately does not re-export internals.
- **Path alias**: configure `@/*` → `src/*` in `tsconfig.json`. Imports become `import { X } from "@/features/billing"`. Avoid relative imports across feature boundaries (`../../features/...` is a code smell).
- **Cross-feature shared UI**: `src/components/ui/<ComponentName>/<ComponentName>.tsx`. Components in here are presentational and should not import from `src/features/`.
- **Cross-feature lib**: `src/lib/<concern>.ts` (`http.ts`, `dates.ts`, `currency.ts`).

## Worked example

A React app's `components/` and `hooks/` folders each contain code for every feature, and a checkout change touches five directories.

1. List features from the product's point of view: `customer-onboarding`, `billing`, `search`.
2. For one feature, create `src/features/billing/{components,api,hooks}/`, plus `types.ts` and `index.ts`.
3. Move all billing-only files there; leave truly shared UI in `src/components/ui/`.
4. Export only what other features need from `billing/index.ts`; make everything else internal by convention.
5. Enforce with `eslint-plugin-import` `no-restricted-paths` or `eslint-plugin-boundaries`: features may import `lib/`, `components/ui/`, and other features' `index.ts` only.
6. Repeat per feature in small PRs.

Deleting a feature is deleting one folder, plus its route entry.

## Anti-patterns

- **Importing from another feature's internals.** `import { Foo } from "@/features/billing/components/Internal"` couples you to billing's implementation. Either Foo is part of billing's public API (re-export from `index.ts`) or it doesn't belong outside billing.
- **A `shared/` directory that becomes everything.** `shared/components/`, `shared/utils/`, `shared/hooks/`, `shared/types/`, `shared/api/` — when more than half of `src/` lives under `shared/`, the feature split has failed. Audit the imports; promote things back into features.
- **A feature with no `index.ts`.** Without a barrel, every other feature reaches into your internals; refactors break unrelated code. The barrel is cheap and you should add one when you create the folder.
- **Features that are really views/pages.** A "feature" called `dashboard-page` is a page, not a feature. Pages compose features. Move the actual capabilities (`reporting`, `team-management`) into their own features.
- **Files-by-type *inside* a feature.** `features/billing/components/billing-button.tsx`, `features/billing/components/billing-modal.tsx` — fine. `features/billing/components/buttons/` and `features/billing/components/modals/` — over-engineered; flatten until a feature has ≥10 components.
- **Co-locating tests poorly.** Either co-locate (`OnboardingForm.test.tsx` next to `OnboardingForm.tsx`) consistently, or use a parallel `tests/` tree consistently. Pick one; alternating breaks the muscle-memory.
- **Reaching into the framework's reserved paths from features.** `src/app/` is Next.js routing or Vite's entry; features should not import from it. Routes import from features, not the other way around.

## Scaling & failure modes

- **Cross-feature dependencies** show up as import cycles. Extract the shared part into a lower feature or into `lib/`, rather than allowing deep imports.
- **Shared folder growth**: `components/ui/` should hold primitives only; move anything with domain meaning into a feature.
- **Route layer**: keep routes (`app/` in Next, router config in Vite) as thin wiring over feature exports.
- **Large features** may need internal subfolders; apply the same rule recursively but keep total depth within budget.

## Variants

- **features-with-shared** (this guide) — `src/features/` plus `src/components/ui/`, `src/lib/`, `src/types/`. The default; works for the vast majority of React apps.
- **strict-features-only** — no shared directory; features duplicate small things by design. Used in some monorepos where each feature is a published package and accidental coupling is the worst sin. Combine with `code/turborepo-monorepo/`.
- **monorepo-features-as-packages** — each feature graduates to its own package (`packages/feature-billing/`); the app composes packages. The natural endpoint for large feature trees. See `code/turborepo-monorepo/` and `code/nx-monorepo/`.
- **Bulletproof React variant** — adds `src/providers/`, `src/stores/`, `src/config/`, `src/test/` at the same level as `features/`. Slightly heavier but proven at scale; the *Bulletproof React* repo is the reference.
- **Feature-vertical with co-located routes** — Next.js App Router lets routes live next to features; `src/features/billing/` exports the page component and `src/app/billing/page.tsx` re-exports it. Keeps related code together at the cost of one indirection.

## Adoption checklist

- [ ] Each feature exposes a single `index.ts` and nothing imports from its internals.
- [ ] A lint rule enforces the boundary.
- [ ] `components/ui/` holds only domain-free primitives.
- [ ] Routes only import from feature public APIs.
- [ ] Removing a feature touches its folder and one registry line.

## Real-world projects using this

- **Bulletproof React** (`alan2207/bulletproof-react`) — the canonical reference; every section of this guide tracks it.
- **T3 stack** (`create-t3-app`) — the official starter for Next.js + tRPC + Prisma adopts feature-based folders out of the box.
- **theodorusclarence/ts-nextjs-tailwind-starter** — popular Next.js TypeScript starter with the feature-based layout baked in.
- **Vercel "best practice" examples** — many `examples/` in the `vercel/next.js` repo have moved to feature folders for non-trivial apps.
- **Cal.com** (`calcom/cal.com`) — open-source scheduling app organised around `apps/`, `packages/features/<feature>/`, with each feature exporting a public API.
- **Mattermost web client** — large React codebase with feature-based modules under `webapp/`.

## Migration & references

- **From a type-driven sprawl** (`/components/`, `/api/`, `/hooks/` at root): pick the worst-coupled feature; create `src/features/<that-feature>/`. Move every file that *only* this feature uses into that folder, preserving subfolders (`components/`, `api/`, `hooks/`). Add `index.ts` re-exporting the parts other code currently imports. Update imports across the codebase. Repeat per feature; what remains in the global folders is the genuinely shared code.
- **From a single-file `App.tsx` with everything**: identify the ≥5 user flows that live there. Each becomes a feature. Move components, state, and API calls per flow. Stop when `App.tsx` is a router that mounts feature components.
- **From `@/components/Header.tsx` for everything**: Header is global UI; it stays. But `@/components/BillingHeader.tsx` is a feature header that snuck out — move it back to `features/billing/components/`.
- **From relative `../../` imports**: configure `@/*` path alias in `tsconfig.json` and the bundler. Use codemods (jscodeshift, ts-morph) to rewrite. The alias makes feature boundaries grep-able (`grep "from \"@/features/"`).
- **References**:
  - **Bulletproof React** (`github.com/alan2207/bulletproof-react`) — the reference that defines this layout for React.
  - **T3 docs** (`create.t3.gg`) — the layout adopted by the T3 community.
  - Kent C. Dodds' "Co-locate" essays (`kentcdodds.com/blog/colocation`) — the principle behind the feature folder.
  - Brad Frost's *Atomic Design* — the contrasting horizontal model; useful to read for what feature-based is *not*.
  - Sibling guides: `code/nextjs-app/` (the routing layer this guide composes with), `code/atomic-design/` (when you're building a component library, not an app), `code/turborepo-monorepo/` (graduating features into packages), `principles/colocation/`.
