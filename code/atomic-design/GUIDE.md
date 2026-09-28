## TL;DR

The **atomic-design layout** organises a UI codebase by *level of composition*, not by feature. Brad Frost's vocabulary maps to folders: `src/atoms/` for the smallest reusable elements (Button, Input, Icon), `src/molecules/` for combinations of atoms (LabeledInput, SearchBar), `src/organisms/` for full UI sections (LoginForm, NavigationBar), `src/templates/` for page-level layouts independent of content, and `src/pages/` for templates filled with real content. Each component lives in its own folder (`Button/Button.tsx`, `Button/Button.stories.tsx`, `Button/index.ts`) so the component, its stories, its tests, and any styles travel together. The discipline is the gradient: atoms know nothing of molecules, molecules compose atoms only, organisms compose atoms and molecules. Storybook is the natural runner — every component has a `.stories.tsx` that documents and demos it. This is the right layout for **design-system codebases and component libraries**, not for application code (use `code/feature-based-frontend/` for apps). Adopt atomic design when designers and engineers need a shared vocabulary; skip it when you're building features rather than primitives.

## Principles & why

Atomic design is a way of thinking that gets cashed out as a folder structure. The structure exists because the thinking exists.

1. **Composition is the axis of organisation.** A `<Button>` is the same Button regardless of which feature uses it. Grouping by composition level — atoms, molecules, organisms — separates "stuff that's reusable" from "stuff that's a destination." This is the inverse of feature-based: feature folders capture *what the app does*; atomic folders capture *what the app is made of*. Component libraries should be the latter, not the former.
2. **A shared vocabulary across designers and engineers.** Designers use "atom / molecule / organism" already (Frost's book is a design book); engineers borrowing the same words eliminates a translation layer. When the design spec says "the molecule LabeledInput uses the Input atom and the Label atom," the engineer opens `src/molecules/LabeledInput/`. The vocabulary is load-bearing — you do not get the benefit of atomic design without using its words.
3. **One component per folder, with siblings co-located.** `atoms/Button/Button.tsx` plus `Button.stories.tsx` plus `Button.test.tsx` plus `index.ts` plus optional `Button.module.css`. The folder is the unit of refactoring: rename the folder and you rename the component everywhere; delete the folder and the component is gone everywhere. The `index.ts` re-exports the component as the public face; consumers never reach into `Button.module.css` from outside.

The trade is a flat hierarchy with many short folders and a discipline about *where* a new component goes (atom or molecule?). When it's genuinely ambiguous, pick atom and promote it later — atoms are cheaper to migrate up than organisms are to migrate down. The other trade is that atomic design is *not* application architecture: a real app needs both a component library (atomic) and a feature layer (feature-based). Most mature codebases have both, in separate packages.

## When to use

- **Design-system codebases.** IBM Carbon, Shopify Polaris, Atlassian Design System — all organise components by composition level, not by feature.
- **Storybook-driven component libraries.** Atomic design and Storybook are a natural pair: each `.stories.tsx` is the canonical demo and doc of its component.
- **Teams where designers and engineers collaborate closely.** The shared vocabulary pays back when a design review discusses "the SearchBar molecule" and everyone knows where the code lives.
- **Apps with a UI component count in the hundreds.** Once you have 50+ atoms and 30+ molecules, the structure is the only way to keep the inventory manageable.
- **Cross-product UI sharing.** When multiple apps consume the same component library, atomic design is the canonical organisation. Combine with `code/turborepo-monorepo/` for the packaging.

## When NOT to use

- **Application code.** Atomic design is horizontal (organised by composition level). Application code is vertical (organised by feature). Use `code/feature-based-frontend/` for the app and reserve atomic design for a library it consumes.
- **Tiny apps and prototypes.** A 5-component prototype does not need the atom/molecule/organism distinction. Flat `components/` is fine; restructure later.
- **Server-rendered apps with mostly-bespoke pages.** If most pages have unique components (newsletters, marketing sites), the reuse atomic-design optimises for isn't there.
- **Teams without a designer.** Atomic-design vocabulary needs design discipline. Engineers picking the level alone tends to drift; without a partner enforcing the boundaries, structure becomes file-naming theatre.
- **Frameworks with strong opinions on layout.** Next.js App Router, Remix, SvelteKit have routing-driven file layouts. Atomic design lives *inside* `src/components/` or as a separate `packages/ui/` — not at the route level.

## Tree diagram

```
component-library/
├── package.json
├── README.md
├── src/
│   ├── atoms/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.stories.tsx
│   │   │   └── index.ts
│   │   ├── Input/
│   │   └── Icon/
│   ├── molecules/
│   │   ├── LabeledInput/
│   │   └── SearchBar/
│   ├── organisms/
│   │   ├── LoginForm/
│   │   └── NavigationBar/
│   ├── templates/
│   │   └── DashboardLayout/
│   └── pages/                              ← rare in pure component libs
└── .storybook/
```

## Naming rules

- **Top-level layer folders**: lowercase, plural — `atoms/`, `molecules/`, `organisms/`, `templates/`, `pages/`. The plurals are the canonical Frost names; do not rename without reason.
- **Component folder**: PascalCase, singular — `Button/`, `LoginForm/`, `DashboardLayout/`. The folder name is the component name.
- **Component file**: PascalCase, same name as the folder — `Button/Button.tsx`. The file's default export (or single named export) is `Button`.
- **Stories file**: `<Component>.stories.tsx` — Storybook 8 CSF3 conventions. One story file per component; multiple stories inside.
- **Tests**: `<Component>.test.tsx` co-located in the component folder. Same convention as `code/feature-based-frontend/` — tests travel with the code they test.
- **Styles**: `<Component>.module.css` (CSS modules) or `<Component>.styles.ts` (CSS-in-JS). Co-located, not at a global `styles/` directory.
- **Barrel**: `index.ts` re-exports the component (and its public types). Consumers always import from the folder, never from the inner `Button.tsx`. This keeps the import path stable across refactors.
- **Public package entry**: `src/index.ts` re-exports the components other apps consume (typically only atoms, molecules, and organisms; templates and pages stay private).

## Worked example

A team has a flat `components/` folder with 120 files and can't tell which are safe to change.

1. Sort components by what they contain, not by what they do: no other component inside means atom (`Button`, `Icon`); a few atoms means molecule (`LabeledInput`); a self-sufficient section means organism (`NavigationBar`).
2. Move one folder per component: `src/atoms/Button/{Button.tsx,Button.stories.tsx,index.ts}`. Keep the `index.ts` as the only import surface.
3. Enforce direction with a lint rule (for example `eslint-plugin-boundaries` or `import/no-restricted-paths`): atoms import nothing above them, molecules import atoms, organisms import molecules and atoms.
4. Give every atom a story so `.storybook/` doubles as living documentation.
5. Hold the line on `templates/` and `pages/`: they hold layout and content wiring, no business logic.

After the migration a reviewer can answer "what breaks if I change Button?" by looking at who imports `atoms/Button`.

## Anti-patterns

- **An `<atom>` that is actually an organism.** A "Button" that includes a dropdown, a popover, and three icons is not an atom — it's an organism with `Button` in its name. Move it. The vocabulary only works when the levels are honest.
- **Atoms that import from molecules.** The arrow points up: atoms ← molecules ← organisms. An atom importing from a molecule means the level is wrong; either the molecule is actually an atom or the atom is actually a molecule.
- **No clear layer for a component.** "It uses three atoms but it's not really an organism" — that's a molecule. The hesitation usually means you don't have enough molecules yet; trust the gradient.
- **Templates filled with content.** A template should accept content via props or slots. The moment a template hard-codes "Welcome to MyApp," it's a page. Move it.
- **Pages in a pure component library.** Component libraries rarely need `pages/` at all; they ship up to organisms or templates. `pages/` is for products that consume the library and add their own pages on top — and those products usually want `code/feature-based-frontend/` instead.
- **A `components/` folder alongside the atomic levels.** When `components/` and `atoms/` coexist at the same level, contributors stop knowing which one to use. Pick one model.
- **Storybook stories in a separate `stories/` directory at root.** Co-locate. The story belongs with the component; a parallel `stories/` tree is the same trap as a parallel `tests/` tree at root, and worse because it breaks Storybook's auto-discovery defaults.

## Scaling & failure modes

- **Classification arguments** ("is this a molecule or an organism?") are the main cost. Time-box them: pick the lower level when unsure and promote when the component gains its own state or data fetching.
- **Feature code doesn't fit the ladder.** Product features that fetch data and hold state belong in feature folders; keep atomic design for the presentational library underneath (see `feature-based-frontend`).
- **Story and test files multiply** with the component count; the one-folder-per-component rule keeps them adjacent.
- **Design tokens** (colors, spacing) live outside the ladder, in a `tokens/` or `theme/` module every level may import.

## Variants

- **Strict Atomic** (this guide) — five layers (atoms, molecules, organisms, templates, pages); pure adherence to Frost's book.
- **Atoms-Molecules-Organisms only** — drop `templates/` and `pages/` for libraries that don't ship higher-level constructs. Common in pure UI kits (e.g., shadcn/ui-style libraries).
- **Modified naming** — substitutions like `atoms/components/blocks/layouts/`. Same intent, different vocabulary; pick this if your designers use different words. Document the mapping in the README.
- **Atomic + tokens** — add `src/tokens/` for design tokens (colors, spacing, typography). Tokens are the substrate atoms consume; treat them as a separate concern below the atomic gradient.
- **Atomic + theming** — add `src/themes/` for theme definitions consumed by components. Common in libraries that ship light/dark or branded variants.

## Adoption checklist

- [ ] Each component has its own folder with an `index.ts` public export.
- [ ] A lint rule enforces the import direction (atoms up to pages).
- [ ] Every atom and molecule has a story or visual test.
- [ ] Data fetching happens no lower than organisms, and ideally in a feature layer.
- [ ] Design tokens are shared and not duplicated per level.

## Real-world projects using this

- **Brad Frost's own *Atomic Design* (book + site)** — `atomicdesign.bradfrost.com` is the canonical reference; the layout originated here.
- **IBM Carbon Design System** — explicit atomic decomposition; `carbon-react` packages atoms (Button, Input), molecules (FormItem), organisms (DataTable).
- **Shopify Polaris** — loose adherence to atomic design; the `polaris-react` repo organises around composition level even where the names differ.
- **Storybook's own design-system examples** — the official "design system" template ships with atomic-design layout out of the box.
- **shadcn/ui** — atoms-and-molecules-only variant; no strict naming, but the composition gradient is identical (a `<Dialog>` is built from atoms like `<Button>` and `<X>` icon).
- **Atlassian Design System** — `atlassian-frontend`'s `packages/design-system/` mirrors the gradient even though they call levels by different names.

## Migration & references

- **From a flat `components/` directory**: list every component; sort by "how many other components does it use?" Components using zero others are atoms; components using only atoms are molecules; the rest are organisms or templates. Move them in waves; update imports per wave. Avoid one giant move-everything PR.
- **From a feature-based app to a feature-based app + atomic library**: extract the components currently duplicated across features. Promote them into a new `packages/ui/` (or `src/ui/`) that is itself organised atomically. Apps consume `@your-org/ui`.
- **From mixed `<button>` styles inline**: identify the visual variants (primary, secondary, danger). Build a single `Button` atom with a `variant` prop; codemod existing buttons to use it. Repeat per atom; the atomic library emerges as you remove duplication.
- **Adding Storybook to an existing tree**: install Storybook 8, point it at `src/**/*.stories.tsx`, and add one story per component progressively. Storybook will auto-discover; you do not need a manifest file.
- **References**:
  - **Brad Frost, *Atomic Design*** (`atomicdesign.bradfrost.com`) — the book; free online.
  - **Storybook docs** (`storybook.js.org`) — official guides for design-system style libraries.
  - **IBM Carbon** (`carbon-design-system.github.io`) — reference component library at scale.
  - **Shopify Polaris** (`polaris.shopify.com`) — public design system with atomic-design influence.
  - Sibling guides: `code/feature-based-frontend/` (the contrasting vertical model for *applications*), `code/node-library/` (the publishing layer when the atomic library ships as a package), `code/turborepo-monorepo/` (when atomic library + apps live in one repo), `principles/depth-vs-breadth/` (why one folder per component beats one file per component).
