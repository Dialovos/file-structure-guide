## TL;DR

A **go-multi-module** repository contains **multiple `go.mod` files**, each rooting an independent Go module. Each subtree is published, tagged, and versioned on its own — `core/v1.4.2` and `client/v0.9.0` can ship in the same repo without dragging each other along. The Go tooling treats each `go.mod` as a hard module boundary: a module *cannot* see code in a sibling module's `internal/` (because they have different module paths), and dependencies between siblings must go through normal `require` directives in `go.mod`. This is heavier than a single-module repo (`code/go-module/`) — `go test ./...` doesn't recurse across module boundaries, every module needs its own `go.mod`/`go.sum`/`go mod tidy`, and version bumps propagate manually. Use it only when **components have genuinely independent release cadences**, when **tools shouldn't pull in production deps**, or when **you're publishing several distinct Go libraries from one repo**. Otherwise, single-module is dramatically simpler. The `replace` directive (covered below) is the bridge for local development across sibling modules; remove it before tagging.

## Principles & why

The multi-module layout exists because Go's module system makes the *module*, not the *repository*, the unit of versioning and publishing.

1. **One `go.mod` = one module = one independent version stream.** A repo with three `go.mod` files publishes three modules. Each can be tagged `<module-path>/vX.Y.Z` separately. `go get github.com/example/myrepo/client@v0.9.0` resolves to `client/go.mod` at that tag; `core` is unaffected.
2. **`internal/` privacy is per-module, not per-repo.** A package at `core/internal/foo` is private to `core`; `client` is a *different* module, so it cannot import `core/internal/foo` even though they share a repo. This is enforced by the Go compiler. If you want code shared across siblings, it must live in a module's exported (non-`internal`) packages.
3. **Sibling modules use `require` + (optionally) `replace`.** `client/go.mod` declares `require github.com/example/myrepo/core v1.4.2` to depend on `core` at a tagged version. For local development before tags exist, a `replace github.com/example/myrepo/core => ../core` directive points the require at the working copy on disk. **Remove `replace` before publishing**, or downstream consumers can't resolve the module. (Alternative: Go workspaces — `go.work` files — replace this pattern in modern setups; see Variants.)
4. **`tools/` as a separate module isolates dev-time deps.** A common pattern: keep static-analysis tools (staticcheck, mockgen, golangci-lint) in `tools/go.mod` so they're not pulled into every consumer's transitive dep graph. The `//go:build tools` build tag plus blank-imports keeps the tools versioned without compiling them into binaries.
5. **`go test ./...` and `go build ./...` stop at module boundaries.** Tooling has to iterate modules explicitly: `for d in core client server tools; do (cd "$d" && go test ./...); done`. Most multi-module repos ship a `Makefile` or a `tools/` build script for this.
6. **Module path = repo URL + subdirectory.** `github.com/example/myrepo/core` means "the module rooted at the `core/` directory of github.com/example/myrepo." Tag prefix matches the subdirectory: `core/v1.4.2` for the `core` module, *not* `v1.4.2` (which would be ambiguous).

The principles together justify the cost: you accept extra ceremony (separate `go.mod`s, `replace` directives, multi-module test loops) in exchange for **independent versioning** and **dep-tree isolation**. Single-module is the default; only reach for multi-module once the cost of versioning components together exceeds the cost of running multiple modules.

## When to use

- **Components with genuinely independent release cadences.** A stable `core` library at `v1.x.x` paired with an experimental `client` at `v0.x.x` that breaks frequently — single-module would force you to bump them in lockstep.
- **Multiple libraries published from one repo.** gRPC's `grpc-go` repo is the canonical case: separate modules per protocol implementation, each with its own version stream.
- **`tools/` isolation.** Even projects that are otherwise single-module sometimes split out a `tools/` module to keep linters, codegen, mock generators, and benchmarking deps out of the production module's `go.sum`.
- **Vendor of multiple SDKs.** A monorepo publishing `aws-sdk-go-v2/service/<service>/` style modules — one per service — uses multi-module so each service SDK can ship independently.
- **API versioning at the module level.** `api/v1` and `api/v2` as separate modules let consumers pin to one major version while you iterate on the other.
- **When you have a reference implementation plus a few satellite modules** (a server core, plus optional adapters for different storage backends, each as its own module).

## When NOT to use

- **Components versioned together.** If all binaries in your repo cut a release at the same time, single-module is dramatically simpler — one `go.mod`, one `go.sum`, one `go mod tidy`, one tag. Don't pre-emptively split.
- **New projects.** Start single-module. Splitting later is straightforward (`go mod init` in a subdirectory); merging multi-module back to single-module is more painful.
- **Small repos with one binary.** The `cmd/<binary>/` + `internal/` layout from `code/go-module/` covers this far better.
- **When you don't have a release cadence problem.** Multi-module exists to solve "we have to ship core and client at different times." If your team ships them together every sprint, multi-module is pure overhead.
- **Teams unfamiliar with Go modules.** The `replace` directive, tag-prefix convention (`core/v1.4.2`), and `go.work` interactions trip up newcomers. Don't introduce multi-module until at least one team member is comfortable with single-module workflows.

## Tree diagram

```
my-repo/
├── README.md
├── core/
│   ├── go.mod
│   └── core.go
├── client/
│   ├── go.mod                  ← depends on core via replace or version
│   └── client.go
├── server/
│   ├── go.mod
│   └── server.go
└── tools/
    └── go.mod                  ← independent from main modules
```

## Naming rules

- **Module paths**: each `go.mod` declares a distinct module path, conventionally `<repo-url>/<subdir>`. For `github.com/example/myrepo` the children are `github.com/example/myrepo/core`, `.../client`, `.../server`, `.../tools`.
- **Subdirectory names**: lowercase, single word where possible, no underscores. `core/`, `client/`, `server/`, `tools/`. Match the trailing component of the module path.
- **Tags**: prefix with the subdirectory + `/`. `core/v1.4.2`, `client/v0.9.0`, `tools/v0.0.5`. **Never** plain `v1.4.2` in a multi-module repo — Go can't tell which module the tag belongs to.
- **Internal packages**: still `<module>/internal/<pkg>`. Each module has its own `internal/`; they're invisible to siblings.
- **`tools/` module**: by convention `<repo>/tools` with a `tools.go` file using `//go:build tools` to satisfy `go mod` while keeping the imports out of binaries.
- **`go.work` (workspaces)**: when present, lives at the repo root and lists each module path: `use ./core`, `use ./client`, etc. Don't commit `go.work.sum` if you intend `go.work` to be local-only — but in practice committing both is common and sane.
- **Avoid**: nested modules (a `go.mod` *inside* another module's directory tree). Technically valid, but confuses every Go tool and most humans. Prefer flat sibling layout.

## Worked example

A repo holds a library and a server; the library needs v1 stability while the server changes weekly.

1. Give each subtree its own `go.mod`: `core/`, `client/`, `server/`.
2. In `server/go.mod`, require the library at a released version, and use a `go.work` file locally so edits are seen across modules without `replace` directives: `go work init ./core ./client ./server`.
3. Tag releases by subdirectory: `git tag core/v1.4.2`.
4. Run tests per module in CI: `for m in core client server; do (cd $m && go test ./...); done`.
5. Don't commit `go.work` unless the team agrees; release builds should resolve real versions.

Each module releases on its own and consumers of `core` don't download server dependencies.

## Anti-patterns

- **Pre-emptive multi-module split** before you have an actual release-cadence problem. Adds ceremony with no payoff.
- **Forgetting to remove the `replace` directive before tagging.** A published module with `replace github.com/example/myrepo/core => ../core` is broken for any consumer who isn't sitting at `../core` themselves. Strip `replace` (or better, gate it behind `go.work`) before `git tag` + push.
- **Mismatched tag prefixes.** Tagging `v1.4.2` instead of `core/v1.4.2` in a multi-module repo. `go get github.com/example/myrepo/core@v1.4.2` won't resolve it; consumers see "unknown revision" errors.
- **Cross-module `internal/` access attempts.** `client` trying to `import "github.com/example/myrepo/core/internal/foo"` won't compile — they're different modules. The fix is to export the package from `core` (move it out of `internal/`) or duplicate it in `client`. Don't try to "trick" the compiler.
- **Committing `vendor/` per module without need.** Multiplies repo size; rarely worthwhile. Reserve vendoring for environments that demand it (air-gapped CI, regulated builds).
- **One CI job for the whole repo.** Multi-module repos almost always need a per-module job (or matrix) so a failure in `tools` doesn't block `core`.
- **Importing the parent module path as if it were a single module.** `import github.com/example/myrepo` (no subdirectory) only resolves if you have a `go.mod` at the repo root. In a sibling-modules layout, the root has *no* `go.mod` — there is no "myrepo" module, only its children.
- **Skipping `go mod tidy` per module.** Each module's `go.mod`/`go.sum` is independent; running tidy in `core` doesn't update `client`. Add a `make tidy` target that loops.
- **Mixing single-module and multi-module conventions.** A single root `go.mod` plus child `go.mod`s is the "nested" anti-pattern. Pick one style.

## Scaling & failure modes

- **Coordination cost** rises with the number of modules: each cross-module change needs release then bump. Keep the count small.
- **`replace` directives** left in committed `go.mod` files break downstream consumers.
- **Major versions** need a `/v2` path suffix in module and directory; plan for it before the first breaking change.
- **Tooling** (linters, CI) must iterate over modules; a `Makefile` target or a small script is essential.

## Variants

- **sibling-modules** (this guide) — flat layout, each top-level subdirectory is one module. The most common multi-module shape.
- **tools-only-split** — single primary module + `tools/` module to isolate dev deps. Used by many otherwise-single-module Go projects (Kubernetes ecosystem subprojects, Caddy plugins). Useful when only the tools-isolation principle applies.
- **nested-modules** — a `go.mod` *inside* another module's directory (e.g., `core/experimental/go.mod`). Rare; mostly seen in `examples/` subdirectories that depend on the parent during local dev. Confusing; prefer siblings.
- **`go.work` workspace mode** — a `go.work` file at the repo root replaces per-module `replace` directives during local development. Modules see each other through the workspace; downstream consumers see them through tags. Modern recommendation as of Go 1.18+. Combine with sibling-modules.
- **API-version split** — modules organised by API version (`api/v1/go.mod`, `api/v2/go.mod`) so consumers pin to one major while you iterate on another. Used by some gRPC and protobuf libraries.
- **Per-service SDK modules** — each external service gets its own module under `service/<name>/go.mod`. AWS SDK for Go v2 follows this pattern.

## Adoption checklist

- [ ] Each module builds and tests independently: `cd <module> && go test ./...`.
- [ ] No committed `replace` pointing at a local path.
- [ ] Release tags follow `<dir>/vX.Y.Z`.
- [ ] CI loops over all modules and fails on any.
- [ ] A short document lists which module depends on which.

## Real-world projects using this

- **caddyserver/caddy** — modular HTTP server; the core is one module and many official plugins live as separate Go modules in adjacent repos / submodules. The plugin model leans heavily on multi-module discipline so plugins ship independently.
- **google/wire** — DI codegen; uses a `tools/`-as-separate-module split so the generator's deps don't infect consumers.
- **aws/aws-sdk-go-v2** — service-per-module monorepo; each AWS service is its own Go module under `service/<name>/`. Independent versioning per service is the explicit goal.
- **kubernetes/kubernetes** & **sigs.k8s.io/** subprojects — many of the staging modules and `sigs.k8s.io/...` libraries live as separate modules within larger umbrellas. `sigs.k8s.io/controller-runtime` and `sigs.k8s.io/kind` are separate modules with independent release streams.
- **grpc/grpc-go ecosystem** — protocol implementations, examples, and generated code split across modules that version independently.
- **etcd-io/etcd** — historically split into multiple modules (`api/`, `client/v3/`, `server/`, `pkg/`) precisely because the API surface and the server implementation evolve at different speeds.

## Migration & references

- **From single-module to multi-module** (splitting): in the subdirectory you want to extract, run `go mod init github.com/example/myrepo/<subdir>`. Update imports in *that* subtree to point at the new module path. In siblings that depend on it, add `require github.com/example/myrepo/<subdir> v0.0.0` plus `replace github.com/example/myrepo/<subdir> => ../<subdir>` for local dev. Tag the new module as `<subdir>/v0.0.1` once it's stable.
- **From multi-module back to single-module** (consolidating): `git mv <subdir>/* .` (carefully), delete the subdir's `go.mod`, run `go mod tidy` at the root. Imports collapse from `github.com/example/myrepo/<subdir>/foo` to `github.com/example/myrepo/foo`. Mass find-replace handles the import update.
- **Adopting `go.work`** for local dev: at the repo root, `go work init ./core ./client ./server ./tools`. Now `go build`, `go test`, etc. see all modules as one workspace; the `replace` directives in individual `go.mod`s become unnecessary for local work. Don't tag with `replace` directives still active.
- **Tagging discipline**: `git tag core/v1.4.2`, `git push origin core/v1.4.2`. Repeat per module. Most projects use a `make release MODULE=core VERSION=v1.4.2` target.
- **References**:
  - Go Blog — *Go modules: v2 and beyond* (covers multi-module versioning): https://go.dev/blog/v2-go-modules
  - Go Blog — *Multi-module workspaces in Go 1.18*: https://go.dev/blog/get-familiar-with-workspaces
  - Go documentation — *Tutorial: Getting started with multi-module workspaces*: https://go.dev/doc/tutorial/workspaces
  - Go reference — `go mod` command and `replace` directive: https://go.dev/ref/mod
  - Sibling guide: `code/go-module/` (single-module Go layout) — start there if you don't yet have a release-cadence problem.
