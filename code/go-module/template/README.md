# Go single-module — template

A `cp -r`-able starter for a single Go module using the
**`cmd/` + `internal/` + `pkg/`** layout. The module path is
`github.com/example/mymodule`; one binary (`myapp`) is wired in,
`internal/` contains two sample packages, and `pkg/client/`
demonstrates a public package.

## Layout at a glance

```
.
├── go.mod                                  # module github.com/example/mymodule
├── cmd/myapp/main.go                       # the binary
├── internal/                               # compiler-enforced privacy
│   ├── auth/auth.go
│   └── store/store.go
├── pkg/client/client.go                    # public API (delete if not needed)
├── api/                                    # OpenAPI / proto specs go here
└── deployments/                            # Dockerfiles, k8s manifests
```

## What to rename

`github.com/example/mymodule`, `myapp`, and the package contents all
need updating. Pick a real module path matching your repo URL:

- `go.mod` — `module github.com/example/mymodule`.
- `cmd/myapp/main.go` — every `github.com/example/mymodule/...` import.
- `cmd/myapp/` — rename the directory if the binary should be called
  something else.
- This `README.md`.

A repo-wide find/replace handles most of it:

```bash
# Replace the module path in all .go files.
find . -type f -name '*.go' -exec \
  sed -i 's|github.com/example/mymodule|github.com/yourorg/yourmod|g' {} +
# Update go.mod too.
sed -i 's|github.com/example/mymodule|github.com/yourorg/yourmod|' go.mod
```

## What to fill

- `go.mod` — the module path and Go version (`go 1.22` is current).
- `internal/auth/`, `internal/store/`, `pkg/client/` — replace stubs
  with real logic.
- `api/` — drop your OpenAPI / `.proto` files here (delete the
  `.gitkeep` once you do).
- `deployments/` — Dockerfiles, Helm charts, Kustomize overlays.
- `LICENSE` — replace `{{YEAR}}` and `{{NAME}}`.

## What to delete

- This template `README.md`.
- `pkg/` if the module has no external consumers (most apps don't
  need it). If you delete it, also remove its import from `main.go`
  if/when you add one.
- `api/` and `deployments/` if you're shipping a CLI or library that
  doesn't need them.

## First run

```bash
go mod tidy
go vet ./...
go test ./...
go run ./cmd/myapp -user alice
# → "hello, alice"
```

## Building and installing

```bash
go build -o ./dist/myapp ./cmd/myapp           # produces ./dist/myapp
go install ./cmd/...                            # installs every cmd/ binary to $GOBIN
```

For multi-platform release artifacts, consider GoReleaser
(https://goreleaser.com/) — drop a `.goreleaser.yaml` at the repo root
and `goreleaser release --snapshot --clean` produces tarballs for
linux/amd64, darwin/arm64, etc.

## Adding a new binary

```bash
mkdir -p cmd/migrate
# Write cmd/migrate/main.go: package main, func main() { ... }
go build ./cmd/migrate
```

Each `cmd/<name>/` is independent; they can share code via `internal/`.

## Adding a dependency

```bash
go get github.com/spf13/cobra@latest
```

This updates `go.mod` and `go.sum`. Imports in `.go` files just work
once the dep is in `go.mod`.

## Pair this with

- `../GUIDE.md` — full reasoning, including the `pkg/` debate.
- `../../rust-binary/` — analogous Rust binary layout.
- `../../c-cpp-cmake/` — analogous C/C++ layout (with explicit build
  system).
