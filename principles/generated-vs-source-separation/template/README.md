# Generated-vs-source-separation template

This template demonstrates the layout: source under `src/`, generated
output under `dist/`, dependency caches under `node_modules/`, and a
`.gitignore` that captures every regeneratable directory across the
common ecosystems.

## What's here

```
template/
├── README.md
├── .gitignore           ← shows the universal "ignore generated dirs" pattern
├── src/
│   └── main.ts          ← stub source: tracked, hand-written
└── dist/
    └── .gitkeep         ← marker file; in a real project, dist/ is fully ignored
```

## A note on `dist/.gitkeep`

In a real project that follows this policy, **`dist/` is gitignored
and contains no tracked file**. The `.gitkeep` here exists *only* so the
template can ship the layout for you to look at — git would otherwise
not let an empty `dist/` directory exist in version control.

When you adopt this template:

1. Delete `dist/.gitkeep`.
2. Confirm `dist/` is matched by your `.gitignore` (the bundled
   `.gitignore` already covers it).
3. Let your build (`tsc`, `vite build`, `webpack --mode=production`,
   etc.) produce `dist/` locally. Never commit it.

## The bundled `.gitignore`

The `.gitignore` in this template is annotated and covers the canonical
output dirs across ecosystems:

- **JS/TS** — `dist/`, `build/`, `out/`, `.next/`, `.nuxt/`, etc.
- **Dependencies** — `node_modules/`, `.venv/`, `*.egg-info/`
- **Rust** — `target/`
- **Java/Maven (target/)** and **Gradle (build/)** — already covered.
- **Static sites** — `_site/`, `public/` (note: `public/` is sometimes
  *tracked* when source-of-truth, e.g. classic Next.js static assets).
- **Python** — `__pycache__/`, `*.pyc`, `.venv/`, `*.egg-info/`.
- **Tool caches** — `.cache/`, `.pytest_cache/`, `.mypy_cache/`,
  `.ruff_cache/`.

Trim this list to your stack; don't ship a polyglot `.gitignore` that
implies the project produces output it doesn't.

## To adopt this template

1. Copy `src/`, `.gitignore`, and (a tailored version of) `README.md`
   into your project. **Do not copy `dist/.gitkeep`** — it's a layout
   illustration, not a real artefact.
2. Tune `.gitignore` to your stack: remove sections you don't use, add
   any framework-specific output dirs (`.svelte-kit/`, `.astro/`,
   `.docusaurus/`, etc.).
3. Confirm your build pipeline produces output into one of the listed
   gitignored directories (or add the dir to `.gitignore` if not).
4. Run `git status` after a fresh `<your build cmd>`. The build's output
   should not appear; if it does, your `.gitignore` is missing a rule.

## The mental model

Two questions for every directory:

1. **Could a fresh clone reproduce this with `git pull && <build>`?**
   - Yes -> generated, gitignore it.
   - No -> source, track it.
2. **Would deleting it lose information that isn't recoverable from git
   history + the build process?**
   - Yes -> source.
   - No -> generated.

When the answers conflict (rare, e.g. vendored generated code that
downstream consumers can't regenerate themselves), put it in a clearly
marked `generated/` directory with a README explaining the regen
command. Don't pretend it's source.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this
`template/README.md` to exist. Don't delete it before replacing.
