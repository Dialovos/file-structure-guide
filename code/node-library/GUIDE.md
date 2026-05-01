## TL;DR

The **node-library** layout is for npm-published packages: TypeScript source in `src/`, compiled output in `dist/` (gitignored, npm-published), tests in `tests/`. The repo's three load-bearing pieces are `package.json` (declares the public API surface via `"exports"`), `tsconfig.json` (controls what `tsc` produces in `dist/`), and the choice of *what gets published vs. what stays in git*. This guide uses **`tsc` only** (no bundler) — the simplest configuration that produces both ESM JavaScript and `.d.ts` declarations. The single most important field is `"exports"` in `package.json`, which superseded `"main"` in Node 12+ and is the modern way to declare entry points; this template wires it up correctly with both `import` and `types` conditions. The single most common mistake is publishing your `src/` and `tests/` to npm — the `"files"` field (or `.npmignore`) controls this. This template uses `"files"` (the modern preference) and explains why `.npmignore` is the alternative.

## Principles & why

A Node library is shaped by four principles, each enforced by a specific package.json field.

1. **`"exports"` is the public API.** Modern Node (12+) resolves imports through the `"exports"` field, not `"main"`. `"exports"` lets you declare both ESM and CJS entry points, types, subpath exports (`mylib/utils`), and conditional exports per environment. If you only set `"main"`, you're publishing using a deprecated path that doesn't carry type info correctly. Use `"exports"`; keep `"main"` as a fallback for pre-Node-12 consumers if you care about them.
2. **`"files"` controls what ships to npm.** When you `npm publish`, by default *everything* in your repo (minus `.gitignore`'d files and a small built-in deny list) is uploaded. That's almost always wrong — you want to publish `dist/`, `README.md`, `LICENSE`, and `package.json` only. The `"files"` field whitelists exactly that. The alternative is `.npmignore` which blacklists; whitelisting is safer.
3. **`dist/` is gitignored, npm-published.** This is the inverse of normal source-control intuition. Build artifacts don't go in git (they bloat the repo, cause merge conflicts, and reflect a specific compile environment). They *do* go to npm because that's what consumers run. The `prepublishOnly` script (`"build": "tsc"`) runs before `npm publish` and ensures `dist/` is fresh.
4. **TypeScript with `"strict": true`.** The strict family of compiler flags catches a class of bugs at build time. There is no good reason to disable it for a new library. Use `"strict": true`, target a modern ES version (`ES2022`+), emit `.d.ts` files (`"declaration": true`), and emit source maps (`"sourceMap": true`).

A fifth, softer principle: **vitest for tests.** Vitest is the modern default — it's faster than jest, works natively with TS and ESM, and has a near-identical API. Jest still works; it's just no longer the obvious default for new projects.

## When to use

- **TypeScript or JavaScript libraries published to npm.** The whole point.
- **Internal libraries** consumed across multiple Node apps in your org (private npm registry, GitHub Packages, internal git deps).
- **Reusable utilities, SDK clients, framework adapters.** Anything where the API is the product.
- **CLI tools written in Node.** Add a `"bin"` field in `package.json` and a shebang on the entry file. The layout is otherwise identical.
- **TypeScript-first projects.** This template assumes TypeScript, but plain-JavaScript libs use the same shape minus `tsconfig.json`.

## When NOT to use

- **Frontend apps.** Use `nextjs-app/`, `vite-app/`, or whichever framework template applies. A frontend app's `dist/` ships to a CDN, not to npm.
- **Monorepos.** If you have multiple libraries that share deps and tooling, use `turborepo-monorepo/` or `pnpm-workspace/`. A single library is overkill for that case (and a monorepo is overkill for one library).
- **Truly throwaway scripts.** A `package.json` + `index.js` at the repo root is fine for one-off automation. The full library structure is overhead you don't need.
- **Native modules with C++ bindings.** Those need `node-gyp`, `binding.gyp`, and prebuilt binaries. Use the napi-rs or N-API templates instead; the shape is meaningfully different.

## Tree diagram

```
my-pkg/
├── package.json
├── tsconfig.json
├── README.md
├── LICENSE
├── .gitignore
├── .npmignore               ← or `files` field in package.json
├── src/
│   ├── index.ts             ← public API
│   └── core.ts
├── tests/
│   └── core.test.ts
├── dist/                    ← built output, gitignored, npm-published
└── .github/workflows/ci.yml
```

## Naming rules

- **Package name** in `package.json`: `kebab-case`, optionally scoped (`@myorg/my-pkg`). Lowercase only; npm rejects uppercase. Cannot start with `.` or `_`. Maximum 214 characters.
- **Repo directory**: matches the package name (`my-pkg/`) by convention. Scoped packages drop the scope from the directory (`my-pkg/`, not `@myorg/my-pkg/`).
- **Source filenames**: `kebab-case.ts` is the most common Node convention (`http-client.ts`, `parse-args.ts`). `camelCase.ts` is also fine (some projects prefer it). Pick one and stay consistent.
- **Index files**: `index.ts` is the conventional entry point. `package.json`'s `"exports": { ".": "./dist/index.js" }` maps it to the default import.
- **Test files**: `<thing>.test.ts` (or `<thing>.spec.ts`). Vitest auto-discovers both.
- **Type-only files**: `<thing>.types.ts` if you want to separate type definitions, but most libraries inline types in the file that uses them.

## Anti-patterns

- **Using `"main": "src/index.ts"`.** Pointing `"main"` at TypeScript source means consumers must transpile your code themselves. Always point `"main"`/`"exports"` at compiled output (`dist/index.js`) and ship the `.d.ts` files alongside.
- **Forgetting to set `"files"` (or `.npmignore`).** Result: `npm publish` uploads your `node_modules`, `tests/`, `.github/`, `src/`, `coverage/` — a 200MB tarball when consumers expected 50KB. Always set `"files": ["dist"]` (and ensure `package.json`, `README.md`, `LICENSE` are included automatically).
- **Setting both `"files"` and `.npmignore`.** They interact in confusing ways (`.npmignore` overrides `"files"` in some cases). Pick one. Modern preference: `"files"`.
- **Committing `dist/`.** Bloats history, causes merge conflicts, and reflects whatever happened to be the build output of whoever's machine ran `tsc` last. Gitignore it; let `prepublishOnly` rebuild.
- **`"private": true` on a package you intend to publish.** A safety footgun reversed. Set `"private": false` (or omit it) on libraries you publish; `"private": true` on apps and internal-only packages to prevent accidental publishing.
- **Skipping `"types"` field.** TypeScript consumers will get `"could not find a declaration file"`. Always set `"types": "dist/index.d.ts"` (or use the `"types"` condition inside `"exports"`).
- **Targeting `ES5` or `CommonJS` for new libraries.** Modern Node and modern bundlers handle ESM and `ES2022`+ natively. Targeting `ES5` for a library shipped today is needless bloat.
- **`engines` field absent.** Without `"engines": { "node": ">=18" }` (or whatever you actually support), npm has no way to warn users on incompatible Node versions. Set it; pick honestly.

## Variants

- **tsc-only** (this guide) — TypeScript compiler is the only build tool. Simplest setup, slowest builds at scale, perfectly fine for libraries up to ~50 source files.
- **tsup-built** — `tsup` is a zero-config bundler that produces ESM + CJS + `.d.ts` in one shot. Faster than `tsc`, supports tree-shaking. Drop-in replacement for `tsc` in the build script.
- **rollup-built** — `rollup` for libraries that need fine control over output (multiple entry points, custom plugins, code-splitting). More setup; more power.
- **unbuild** — preset rollup configuration from the unjs ecosystem. Less config than rollup, more flexibility than tsup.
- **pkgroll** — minimalist library bundler from the `tsx` author; growing in popularity for small libraries.
- **esbuild + tsc** — esbuild for the JS, tsc only for `.d.ts` emission. Fast; common in larger libraries.

## Real-world projects using this

- **axios** (axios/axios) — HTTP client; classic node-library shape, dual ESM/CJS, well-organized `src/`.
- **zod** (colinhacks/zod) — schema validation; tsc-only, single-package, exemplary `package.json` exports field.
- **yargs** (yargs/yargs) — CLI argument parsing; mature library structure, hand-rolled types.
- **commander** (tj/commander.js) — CLI framework; tiny library, instructive `package.json`.
- **lodash** — utility library; CJS-era reference. Modern equivalents have moved to ESM.
- **chalk** (chalk/chalk) — ESM-only since v5; reference for modern pure-ESM library.
- **The Node.js docs** — *Modules: Packages* explains the `"exports"` field with examples; the canonical reference.

## Migration & references

- **From `"main"` only to `"exports"`**: add `"exports": { ".": { "import": "./dist/index.js", "types": "./dist/index.d.ts" } }`. Keep `"main"` and `"types"` for backward compatibility with old tooling. Test with `node --experimental-resolve` or just publish a minor version and watch for issues.
- **From CJS to ESM**: add `"type": "module"` to `package.json`. Update imports to use `.js` extensions (yes, even in `.ts` files — TypeScript's module resolution requires this for ESM). Update `tsconfig.json`'s `"module": "ESNext"`. Major version bump; consumers' configs may break.
- **From committed `dist/` to gitignored**: add `dist/` to `.gitignore`, `git rm -rf --cached dist`, commit. Add `"prepublishOnly": "npm run build"` to `package.json` so `dist/` is regenerated before publish. Update CI to run `npm run build` before any consumer-facing step.
- **From `.npmignore` to `"files"` field**: list the include-paths in `"files"` (`["dist"]` is usually right), delete `.npmignore`, run `npm publish --dry-run` to verify the tarball contents are what you expect.
- **References**:
  - Node.js docs — *Modules: Packages* (the `"exports"` field).
  - npm docs — *package.json* (`"files"`, `"private"`, `"engines"`, `"bin"`).
  - TypeScript docs — *Publishing* (how to set up a TS library for npm).
  - Vitest docs — *Getting Started*.
  - Sibling guides: `code/rust-binary/`, `code/rust-library/`.
