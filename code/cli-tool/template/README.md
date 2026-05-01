# cli-tool — template

A `cp -r`-able starter for a single-binary CLI tool. Defaults to
**Go + cobra** because Go has the strongest CLI ecosystem
(cobra, viper, goreleaser); the *layout* (subcommands, completions,
manpage, CI) transfers cleanly to Rust + clap or Python + click.

## What lives where

- **`cmd/mytool/main.go`** — thin entry point. Calls
  `commands.Execute()` and exits.
- **`cmd/mytool/completion.go`** — documentation for the
  cobra-supplied `completion` subcommand. Cobra registers it
  automatically.
- **`internal/commands/root.go`** — root cobra command and
  `Execute()`.
- **`internal/commands/foo.go`** — sample subcommand
  (`mytool foo [name]`). Copy to make new subcommands.
- **`internal/commands/bar.go`** — sample subcommand with a flag
  (`mytool bar --count N`).
- **`docs/manpage.md`** — pandoc-friendly markdown source for
  `mytool(1)`. Generate the real `.1` with
  `pandoc -s -t man docs/manpage.md -o docs/mytool.1`.
- **`completions/`** — placeholder shell-completion scripts. CI /
  release regenerates with `mytool completion <shell> > ...`.
- **`.github/workflows/ci.yml`** — test + lint on every push;
  goreleaser release job runs only on tag pushes (`v*`).

## What to rename

- `go.mod` `module` line — `github.com/example/mytool` → your repo.
- Imports of `github.com/example/mytool/internal/commands` in
  `cmd/mytool/main.go` need to match.
- Binary name everywhere — `mytool` → your name. Files to update:
  `cmd/mytool/`, `completions/_mytool`, `completions/mytool.bash`,
  `completions/mytool.fish`, `docs/manpage.md`, `.gitignore`,
  `.github/workflows/ci.yml`.
- `LICENSE` `{{YEAR}}` and `{{NAME}}`.

A find-replace of `mytool` (case-sensitive) across the template is
the fastest path; rename `cmd/mytool/` and `completions/_mytool`
afterwards.

## First run

```bash
go mod tidy
go run ./cmd/mytool foo
go run ./cmd/mytool foo Alice
go run ./cmd/mytool bar --count 3
go run ./cmd/mytool --help
go test ./...
```

To build a binary:

```bash
go build -o mytool ./cmd/mytool
./mytool foo
```

## Adding a subcommand

```bash
cp internal/commands/foo.go internal/commands/baz.go
# Edit baz.go: rename fooCmd -> bazCmd, change Use/Short/RunE.
# init() already registers with rootCmd.
go run ./cmd/mytool baz
```

For a sub-subcommand (`mytool foo nested`), use
`fooCmd.AddCommand(nestedCmd)` instead of registering with
`rootCmd`.

## Regenerating completions and the man page

```bash
go build -o mytool ./cmd/mytool
./mytool completion bash > completions/mytool.bash
./mytool completion zsh  > completions/_mytool
./mytool completion fish > completions/mytool.fish

pandoc -s -t man docs/manpage.md -o docs/mytool.1
```

CI runs this at release time so committed completions never drift
from the binary.

## Releasing

1. Tag: `git tag v0.1.0 && git push origin v0.1.0`.
2. CI's `release` job runs `goreleaser release --clean`.
3. Binaries land in GitHub Releases as
   `mytool_<os>_<arch>.tar.gz`.

Add a `.goreleaser.yml` at the repo root to configure the build
matrix (darwin / linux / windows × amd64 / arm64), Homebrew tap,
deb/rpm packages, etc.

## Pair this with

- `../GUIDE.md` — full reasoning, including non-Go variants.
- `../go-module/` — the underlying Go-language layout this template
  follows.
- `../rust-binary/` — Rust equivalent if you'd rather build the CLI
  in Rust + clap.
- The Cobra docs at cobra.dev — canonical reference.
- *Command Line Interface Guidelines* at clig.dev — opinionated
  style guide that complements this layout.
