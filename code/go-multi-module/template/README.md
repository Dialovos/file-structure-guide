# Go multi-module — template

A `cp -r`-able starter for a **multi-module Go repository**: four
sibling Go modules (`core`, `client`, `server`, `tools`) sharing one
git repo, each with its own `go.mod`, version stream, and tag prefix.

```
.
├── core/                       # github.com/example/myrepo/core
│   ├── go.mod
│   └── core.go
├── client/                     # github.com/example/myrepo/client
│   ├── go.mod                  # require core; replace -> ../core (local dev)
│   └── client.go
├── server/                     # github.com/example/myrepo/server
│   ├── go.mod                  # same shape as client
│   └── server.go
└── tools/                      # github.com/example/myrepo/tools
    ├── go.mod                  # dev-time tools (staticcheck, mockgen)
    └── tools.go                # //go:build tools
```

## Why multi-module

Each subtree publishes and versions on its own. `core/v1.4.2` and
`client/v0.9.0` can ship in the same repo without forcing each other
to bump. Use multi-module when you actually have an independent-cadence
problem; if every binary releases together, prefer the single-module
layout in `../../go-module/`.

## What to rename

`github.com/example/myrepo` is the placeholder root. Replace it with
your real repo URL across every `go.mod` and every `.go` file:

```bash
# At the template root:
find . -type f \( -name 'go.mod' -o -name '*.go' \) -exec \
  sed -i 's|github.com/example/myrepo|github.com/yourorg/yourrepo|g' {} +
```

Then in each module:

```bash
for d in core client server tools; do (cd "$d" && go mod tidy); done
```

## The `replace` directive

`client/go.mod` and `server/go.mod` ship with:

```
replace github.com/example/myrepo/core => ../core
```

This makes local development across modules work before any `core` tag
exists. It must be removed (or guarded by a `go.work` file) before you
publish — a downstream consumer can't satisfy a `replace` pointing at
`../core` on your machine.

Two ways to handle it:

1. **Strip `replace` before tagging.** Edit the two `go.mod`s, run
   `go mod tidy`, then `git tag client/v0.9.0 && git push --tags`.
2. **Use `go.work` instead.** From the repo root:
   ```bash
   go work init ./core ./client ./server ./tools
   ```
   The workspace overrides require directives during local builds; the
   committed `go.mod`s no longer need `replace`. This is the modern
   recommendation as of Go 1.18+.

## What to fill

- `core/core.go` — replace `Greet` with your real public API.
- `client/client.go`, `server/server.go` — flesh out the callers.
- `tools/go.mod` — pin the dev tools you actually use; the template
  starts with `staticcheck` and `mockgen` as examples.
- `tools/tools.go` — keep the `//go:build tools` tag and add blank
  imports for any new tool you add to `tools/go.mod`.
- `LICENSE` — replace `{{YEAR}}` and `{{NAME}}`.

## What to delete

- This template `README.md`.
- Any module you don't need (e.g., `server/` if you only ship a
  library + CLI).

## First run

```bash
# Each module is independent; tidy each one.
for d in core client server tools; do (cd "$d" && go mod tidy); done

# Test each module.
for d in core client server; do (cd "$d" && go test ./...); done

# Install dev tools.
(cd tools && go install honnef.co/go/tools/cmd/staticcheck)
(cd tools && go install go.uber.org/mock/mockgen)
```

## Tagging discipline

Every tag in a multi-module repo **must** be prefixed with the module
subdirectory:

```bash
git tag core/v1.4.2     # tags the core module
git tag client/v0.9.0   # tags the client module
git push origin --tags
```

A bare `v1.4.2` tag is ambiguous and `go get` will not resolve it.
A `make release MODULE=core VERSION=v1.4.2` target is a common
convenience.

## Adding a new module

```bash
mkdir adapters
cd adapters
go mod init github.com/example/myrepo/adapters
echo "package adapters" > adapters.go
# Add a sibling-replace if other modules will depend on it locally:
#   replace github.com/example/myrepo/adapters => ../adapters
# Or, preferably, add it to go.work:
cd .. && go work use ./adapters
```

## CI

Run jobs per module so a failure in `tools` doesn't block `core`. A
GitHub Actions matrix:

```yaml
strategy:
  matrix:
    module: [core, client, server, tools]
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-go@v5
    with: { go-version: '1.22' }
  - run: go test ./...
    working-directory: ${{ matrix.module }}
```

## Pair this with

- `../GUIDE.md` — full reasoning, including the `replace`-vs-`go.work`
  discussion.
- `../../go-module/` — single-module Go layout. Start there unless you
  truly need multi-module.
- `../../rust-workspace/` — the analogous "many crates in one repo"
  pattern in Rust (with Cargo workspaces handling what `go.work` does
  for Go).
