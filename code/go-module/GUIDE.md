## TL;DR

A **go-module** project is a single Go module: one `go.mod` at the repo root, executable entry points under `cmd/<binary>/`, private code under `internal/`, and (optionally) reusable public code under `pkg/`. The Go compiler **enforces** `internal/` privacy: any package under `internal/` can only be imported by packages whose import path is rooted at the module's own path. That's a real, language-level boundary — not a convention. `cmd/` is also language-recognised: each subdirectory of `cmd/` is conventionally a separate `main` package producing one binary, which lets you `go install ./cmd/...` to build them all. The `pkg/` directory is **controversial**: many projects (the Go standard library itself, kubernetes, hugo) skip it entirely and put public packages at the module root; others (terraform, prometheus) use `pkg/` to flag "this is meant for external consumption." Both are fine; pick a side and be consistent. This guide covers the `cmd/` + `internal/` + `pkg/` layout because it's the most explicit; if you don't need `pkg/`, delete it.

## Principles & why

A Go module's structure is shaped by five principles that interact tightly with the Go toolchain.

1. **`go.mod` defines the module.** The first line, `module github.com/example/mymodule`, is the import path for every package in the repo. Relative imports don't exist in Go; everything imports via fully-qualified module path. Sub-packages follow the directory tree: `internal/auth/auth.go` is imported as `github.com/example/mymodule/internal/auth`.
2. **`internal/` is a compiler-enforced privacy boundary.** A package at `<module>/internal/foo` can only be imported by packages rooted at `<module>/`. If someone forks your code and places it elsewhere, their imports of your `internal/` packages won't compile. This is the *only* access-control mechanism in Go beyond exported/unexported identifiers (capitalised names).
3. **`cmd/<name>/` is the convention for binaries.** Each subdirectory contains a `main` package that becomes one binary. `go build ./cmd/myapp` produces `myapp`. `go install ./cmd/...` builds all of them. Distinct from libraries (which never have a `main` package) and distinct from `internal/`.
4. **One package per directory.** A directory is a Go package; you cannot have two packages in one directory (except `<package>` and `<package>_test` for test-only code). Choose package boundaries by directory.
5. **Module path matches repository URL.** `module github.com/example/mymodule` — and the repo *is* at github.com/example/mymodule. `go get` reads the module path, fetches the repo, and the round-trip works. Putting a different module path than the repo URL almost always breaks consumers.

The Go layout philosophy is intentionally minimal: there's no equivalent of `src/main/java/`. If a directory contains `.go` files, those files are a Go package, period. The `cmd/`, `internal/`, `pkg/` conventions are layered on top to organise *kinds* of packages — entry points, private packages, and (sometimes) public-API packages. Skip them when they don't apply.

## When to use

- **Any single-module Go project.** `cmd/` + `internal/` is canonical and well-understood by every Go developer.
- **CLIs with a single binary.** Even one binary belongs in `cmd/myapp/main.go` once the project is non-trivial.
- **Services with a small number of binaries.** API server, worker, migration tool — all in `cmd/`, sharing types and logic via `internal/`.
- **Libraries with one or two example commands.** Library at the root, example CLIs in `cmd/`.
- **When you want compiler-enforced privacy.** Anything under `internal/` is invisible to importers. Useful for "we don't promise stability for these packages."
- **When you intend to publish to pkg.go.dev.** The public packages (root or `pkg/`) get auto-documented; `internal/` correctly stays out.

## When NOT to use

- **Multi-module repositories** (one repo, multiple `go.mod` files with independent versioning). That's `code/go-multi-module/` (a sibling guide). Examples: gRPC's `grpc-go` repo with separate modules per protocol version.
- **Tiny single-file scripts.** A 50-line tool doesn't need `cmd/`. Just `main.go` at the root and `go run main.go`.
- **Code that's strictly a library, no binaries.** Drop `cmd/`. Library packages live at the module root or a clear named subdirectory.
- **Migration from GOPATH-era projects.** Old projects often have `src/`, `vendor/` baked in patterns that Go modules made obsolete. Update the layout when you move to modules.
- **When you're convinced `pkg/` adds value without using `internal/`.** That's fine — but understand that `pkg/` is convention only, while `internal/` is language-enforced.

## Tree diagram

```
mymodule/
├── go.mod
├── go.sum
├── README.md
├── LICENSE
├── .gitignore
├── cmd/
│   └── myapp/
│       └── main.go
├── internal/                   ← compiler-enforced privacy
│   ├── auth/
│   │   └── auth.go
│   └── store/
│       └── store.go
├── pkg/                        ← public packages (controversial; many projects skip)
│   └── client/
│       └── client.go
├── api/                        ← OpenAPI/proto specs
└── deployments/                ← Dockerfiles, Helm charts
```

## Naming rules

- **Module path**: matches the repo URL (`github.com/example/mymodule`). Lowercase, no underscores, hyphens allowed.
- **Repository directory**: usually the last path segment (`mymodule/`). Doesn't have to match, but easier when it does.
- **Go package names**: short, lowercase, single word, no underscores, no `pkg`/`util`/`common` (too generic). `auth`, `store`, `httputil`, `protoparse`. Match the directory name.
- **`cmd/` subdirectories**: `cmd/<binary-name>/`. The directory name becomes the binary name when you `go install`. `cmd/myapp/`, `cmd/migrate/`, `cmd/healthcheck/`.
- **Test files**: `<source>_test.go` in the same directory. `auth.go` and `auth_test.go` together.
- **Exported vs unexported**: capitalised first letter = exported (`Authenticate`); lowercase = unexported (`hashPassword`). The compiler enforces this; no `public`/`private` keyword.
- **Interface names**: usually end in `-er` for single-method interfaces (`Reader`, `Writer`, `Stringer`). Multi-method interfaces are usually nouns (`Server`, `Client`).
- **Avoid stuttering**: if your package is `auth`, name the type `Service`, not `AuthService`. Consumers write `auth.Service` already; `auth.AuthService` becomes "auth.AuthService" which reads as duplication.

## Worked example

A service keeps everything in `main.go` and other repos import its helper packages by accident.

1. Create `cmd/myapp/main.go` and keep it to flag parsing, wiring, and `run()`.
2. Move business code to `internal/<area>/` (`internal/auth`, `internal/store`). The compiler now prevents outside modules from importing it.
3. Publish only what you intend to support under `pkg/` (or skip `pkg/` entirely and make the module root the public package).
4. Add table-driven tests beside code: `internal/auth/auth_test.go`.
5. Wire `go vet ./... && go test ./...` into CI and add `golangci-lint`.
6. Use `go build -ldflags "-X main.version=..."` to inject the version.

The public surface is explicit, and everything else can be refactored freely.

## Anti-patterns

- **Putting `main.go` at the root** *and* trying to be a library. A module can't easily be both. Pick one: a library (no `main`) or an app (a `main` somewhere, ideally under `cmd/`).
- **`pkg/` everywhere when nothing's actually public.** If you have one binary and no external consumers, `pkg/` is overhead. Keep code under `internal/`.
- **`util/`, `common/`, `helpers/` packages.** These accrete grab-bag code; package names should describe what they do, not what kind of code they are.
- **Importing `internal/` from outside the module.** Won't compile, but newcomers sometimes restructure to "fix" the import error by removing `internal/`. Don't — the privacy enforcement is the feature.
- **Cyclic imports.** Go forbids them at the language level, so they manifest as compile errors. The fix is almost always to extract the shared pieces into a third package that both can import.
- **Vendoring everything by default.** `go mod vendor` is useful for reproducible builds in restrictive environments, but it bloats the repo. Most projects don't vendor; they rely on `go.sum` for integrity.
- **Committing build artifacts.** Compiled binaries (`mymodule`, `mymodule.exe`), `*.test` files, coverage profiles all gitignored.
- **Skipping `go vet` and `staticcheck` in CI.** Both catch real bugs cheaply. They're part of "modern Go CI" the same way `mvn test` is part of Maven CI.
- **Module path with uppercase letters or that doesn't match the repo URL.** `go get` will fail in confusing ways.

## Scaling & failure modes

- **`pkg/` debate**: it only adds a path segment. Use it if you have a clear split between public library and internal app; otherwise omit it.
- **Package granularity**: many tiny packages create import cycles; group by what changes together.
- **Multiple binaries** share `internal/`; keep each `cmd/<name>/main.go` thin.
- **Growth to multiple release cadences** is the trigger to consider `go-multi-module`.

## Variants

- **with-`pkg/`** (this guide) — explicit "this is public" prefix for shared packages.
- **no-`pkg/`** — public packages live at the module root (`mymodule/client/`, `mymodule/types/`). Used by the Go standard library itself, kubernetes/kubernetes (mostly), hugo, terraform-provider-aws. Argument for: less typing in import paths. Argument against: less obvious which packages are stable public API.
- **`cmd/`-and-`internal/`-only** — no `pkg/`, no public packages. Used when the module is "an app, not a library" and you don't intend external consumption. Most apps look like this.
- **flat layout** — for libraries with no binaries: just `mymodule/foo.go`, `mymodule/bar.go` at the root. Trivial small libraries (e.g., `pkg.go.dev/github.com/google/uuid`) use this.
- **with-`api/` and `deployments/`** (this guide) — `api/` for OpenAPI/proto/gRPC schemas, `deployments/` for Dockerfiles, Helm charts, Kustomize overlays. Common in production services.
- **`golang-standards/project-layout` style** — adds `web/`, `assets/`, `scripts/`, `init/`, `configs/`, `test/`, `tools/`, `examples/`, `third_party/`, `githooks/`. Comprehensive but heavy. The repo is widely cited; it's not an official Go recommendation, despite the name.

## Adoption checklist

- [ ] `go vet ./... && go test ./...` pass from a clean clone.
- [ ] `main.go` files contain wiring only.
- [ ] Everything not meant for outside use is under `internal/`.
- [ ] `go.mod` has the correct module path and Go version; `go mod tidy` yields no diff.
- [ ] No package named `util`, `common`, or `helpers`.

## Real-world projects using this

- **kubernetes/kubernetes** — vast Go module; `cmd/`, `pkg/`, `staging/`, `internal/`-style separation. Reference for very large-scale Go.
- **prometheus/prometheus** — observability platform; `cmd/`, `pkg/`, `model/`, `discovery/`. Uses `pkg/`.
- **gohugoio/hugo** — static site generator; flat layout (no `pkg/`), `cmd/` for the CLI.
- **hashicorp/terraform** — infrastructure-as-code; `cmd/terraform/` + many top-level packages. Uses neither `pkg/` nor `internal/` heavily.
- **golang/go** — the Go compiler/standard library itself; `src/cmd/`, `src/runtime/`, no `pkg/`. Reference for "what the language designers think canonical Go looks like."
- **grafana/grafana** — `cmd/grafana-server/`, `pkg/` (heavy use), `public/` (frontend assets).
- **golang-standards/project-layout** — the *most-cited* layout guide; not officially endorsed by the Go team, but widely used as a starting point. Worth reading; don't follow it slavishly.

## Migration & references

- **From GOPATH to modules**: at the repo root, `go mod init github.com/example/mymodule`. This generates `go.mod` from existing imports. `go mod tidy` populates `go.sum`. Delete any `vendor/` unless you specifically need it; modules supersede it.
- **From `pkg/` to no-`pkg/` (or back)**: `git mv pkg/client client && go mod tidy`. The mass-update is `find . -type f -name '*.go' -exec sed -i 's|/pkg/client|/client|g' {} +`. Don't forget docs and READMEs.
- **From single-module to multi-module**: split a big repo into multiple `go.mod` files. Each subdirectory with a `go.mod` becomes its own module. Useful when parts have different release cadences (e.g., `api/v1` vs. `api/v2`). Tooling: `go work` (workspace mode) helps develop multiple modules in one tree without publishing.
- **Adding `internal/` to lock down accidentally-public packages**: identify packages no external consumer should depend on, `git mv pkg/foo internal/foo`, run `go mod tidy`. External consumers who were importing them break loudly; internal callers continue working.
- **References**:
  - The Go Blog — *Organizing a Go module*: https://go.dev/doc/modules/layout
  - Go FAQ — *What's in a name?* (the package-naming section): https://go.dev/doc/effective_go#package-names
  - *Effective Go* — https://go.dev/doc/effective_go
  - `golang-standards/project-layout` (https://github.com/golang-standards/project-layout) — comprehensive but unofficial.
  - Sibling guides: `code/go-multi-module/` (when it exists), `code/rust-binary/`, `code/c-cpp-cmake/`.
