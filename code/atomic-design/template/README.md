# Atomic design — template

A `cp -r`-able starter for a component library organised around Brad
Frost's atomic-design vocabulary: atoms, molecules, organisms,
templates, pages. Each component lives in its own folder
(`Component/Component.tsx`, `Component.stories.tsx`, `index.ts`) so
component, stories, tests, and styles travel together.

## What to rename

- `component-library` → your library's name in `package.json`.
- The placeholder `Button` atom is the only fully populated example;
  the other folders contain `.gitkeep` markers showing the layout.
  Replace them with your real atoms / molecules / organisms.
- `LICENSE` — replace `{{YEAR}}` and `{{NAME}}`.

## What to fill

- **`src/atoms/`** — your smallest reusable elements (Button, Input,
  Icon). One folder per component.
- **`src/molecules/`** — combinations of atoms (LabeledInput,
  SearchBar). Composes only atoms.
- **`src/organisms/`** — full UI sections (LoginForm, NavigationBar).
  Composes atoms and molecules.
- **`src/templates/`** — page-level layouts independent of content.
  Templates accept content via slots/props.
- **`src/pages/`** — rare in pure component libraries; templates
  filled with real content.
- **Stories** — every component gets a `<Component>.stories.tsx`
  next to its `.tsx`. Storybook 8 CSF3 auto-discovery picks them up.

## What to delete

- This `README.md` once you have a real one.
- The `Button` placeholder once your real first atom lands.

## First run

```bash
npm install
npm run storybook
```

Storybook opens at `http://localhost:6006`. Run tests with `npm test`,
build the library with `npm run build`.

## Layout cheat-sheet

| Composition level | Use it for                                     | Example                |
|-------------------|------------------------------------------------|------------------------|
| Atoms             | Smallest reusable elements                     | `Button/`, `Input/`    |
| Molecules         | Combinations of atoms                          | `LabeledInput/`        |
| Organisms         | Full sections; compose atoms and molecules     | `LoginForm/`           |
| Templates         | Page layouts independent of content            | `DashboardLayout/`     |
| Pages             | Templates filled with real content (rare here) | `LandingPage/`         |

## Composition rule

```
atoms <- molecules <- organisms <- templates <- pages
```

Atoms must not import from molecules. Molecules must not import from
organisms. The arrow only points up. If you find an inversion, the
component is at the wrong level — move it.

## Pair this with

- `../GUIDE.md` — full reasoning behind the layout.
- `../node-library/` — the publishing layer for shipping this as a
  package.
- `../feature-based-frontend/` — the contrasting vertical model
  for *applications* that consume this library.
- `../turborepo-monorepo/` — when the library + apps live in one
  repo.
