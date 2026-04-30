# Code project layouts

25 starter layouts for software projects, grouped by ecosystem. Each layout is opinionated — pick the one whose "When to use" section best describes you.

## Python (4)

- [`python-src-layout/`](python-src-layout/) — `src/<pkg>/` for libraries you publish
- [`python-flat-layout/`](python-flat-layout/) — `<pkg>/` at root for apps and small projects
- [`django-project/`](django-project/) — Django apps, settings split, URLs
- [`fastapi-project/`](fastapi-project/) — routers, models, schemas, services

## Rust (3)

- [`rust-binary/`](rust-binary/) — single binary crate
- [`rust-library/`](rust-library/) — library crate with `examples/` and `benches/`
- [`rust-workspace/`](rust-workspace/) — multi-crate workspace

## JS/TS (5)

- [`node-library/`](node-library/) — publishable npm package
- [`nextjs-app/`](nextjs-app/) — App Router or Pages Router layout
- [`vue-nuxt-app/`](vue-nuxt-app/) — Nuxt 3 conventions
- [`turborepo-monorepo/`](turborepo-monorepo/) — Turbo's `apps/` + `packages/`
- [`nx-monorepo/`](nx-monorepo/) — Nx's `apps/` + `libs/`

## JVM (2)

- [`java-maven/`](java-maven/) — Maven standard directory layout
- [`java-gradle-multi/`](java-gradle-multi/) — Gradle multi-module

## Systems (3)

- [`c-cpp-cmake/`](c-cpp-cmake/) — CMake project with `src/`, `include/`, `tests/`
- [`go-module/`](go-module/) — single Go module with `cmd/`, `internal/`, `pkg/`
- [`go-multi-module/`](go-multi-module/) — multiple `go.mod` per subtree

## .NET / Mobile (4)

- [`dotnet-solution/`](dotnet-solution/) — `.sln` + `src/` + `tests/`
- [`swift-package/`](swift-package/) — Swift Package Manager
- [`kotlin-android/`](kotlin-android/) — multi-module Android (Now-in-Android-style)
- [`flutter-app/`](flutter-app/) — `lib/`, `test/`, `pubspec.yaml`

## Research / specialized (4)

- [`cookiecutter-data-science/`](cookiecutter-data-science/) — Drivendata's CCDS template
- [`jupyter-research/`](jupyter-research/) — notebooks-first research repo
- [`cli-tool/`](cli-tool/) — single-binary CLI conventions
- [`plugin-architecture/`](plugin-architecture/) — `core/` + `plugins/<name>/`

## Architecture patterns (3)

- [`ddd-hexagonal/`](ddd-hexagonal/) — domain / application / infrastructure / ports&adapters
- [`feature-based-frontend/`](feature-based-frontend/) — `features/<feature>/{components,api,types}`
- [`atomic-design/`](atomic-design/) — atoms / molecules / organisms / templates / pages

## How to pick

Start with [`CHOOSE.md`](../CHOOSE.md) at the repo root if you're undecided. If you already know your stack, the sub-grouping above is the fastest path.
