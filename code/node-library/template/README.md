# Node library — template

A `cp -r`-able starter for an npm-publishable TypeScript library.
**tsc-only** build (no bundler), **vitest** for tests, **ESM** by
default, modern `"exports"` field with both `import` and `types`
conditions, and a Node 18/20/22 CI matrix.

## What gets published vs. what stays in git

This template uses the **`"files"` field** in `package.json` to
whitelist what gets uploaded to npm:

```json
"files": ["dist"]
```

`package.json`, `README.md`, and `LICENSE` are auto-included. Everything
else (`src/`, `tests/`, `.github/`, `tsconfig.json`) stays out of the
tarball.

The alternative is a `.npmignore` file that blacklists. We omit it
intentionally — when both exist, `.npmignore` overrides `"files"` in
ways that are easy to get wrong. Pick one; we picked `"files"`.

`dist/` is **gitignored, npm-published**. The `prepublishOnly` script
runs `tsc` before publish, so `dist/` is regenerated fresh from `src/`
on every release. Don't commit `dist/`.

## What to rename

`my-pkg` is the placeholder package name. Replace everywhere:

- `package.json` — `"name"`, `"description"`, `"repository"`,
  `"homepage"`, `"bugs"`, `"author"`.
- This `README.md`.
- The package name has no other code references; no imports use it.

If you publish under a scope (`@myorg/my-pkg`), update only the
`"name"` field. The rest of the layout is unchanged.

## What to fill

- `package.json` — `"keywords"`, real `"description"`, real
  repository URL, real author.
- `LICENSE` — replace `{{YEAR}}` and `{{NAME}}`.
- `src/core.ts` — replace `greet` with the real API.
- `src/index.ts` — re-export your real public surface; this is the
  documented public API.
- `tests/core.test.ts` — write tests for your real API.

## What to delete

- This template `README.md`.
- The `greet`/`GreetOptions` stub once you have real code.
- `.github/workflows/ci.yml` if you don't use GitHub Actions.

## First run

```bash
npm install
npm run typecheck     # tsc --noEmit
npm run build         # tsc → dist/
npm test              # vitest run
```

Once tests pass, dry-run a publish to inspect the tarball contents:

```bash
npm publish --dry-run
```

The output should list `dist/`, `package.json`, `README.md`, and
`LICENSE` — nothing else.

## Adding a CLI entry point

Add `"bin": { "my-pkg": "./dist/cli.js" }` to `package.json`, write
`src/cli.ts` with a `#!/usr/bin/env node` shebang at the top, and
re-export from `src/index.ts` if you want the CLI's API also
importable as a library.

## Pair this with

- `../GUIDE.md` — full reasoning behind this layout.
- `../../rust-library/` — Rust equivalent.
- The Node.js docs on the `"exports"` field — the most important
  package.json concept this template embodies.
