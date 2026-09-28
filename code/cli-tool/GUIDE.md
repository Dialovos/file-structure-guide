## TL;DR

This guideline is about the **structure of a single-binary CLI tool** — independent of programming language. The shape every modern git/kubectl/docker-style CLI converges on: a thin `main` entrypoint that parses argv and dispatches to a *root command*; a hierarchy of subcommands (`mytool foo`, `mytool foo bar`, `mytool baz --flag value`); a shell-completion file per shell (bash, zsh, fish, sometimes PowerShell); a man page (groff `*.1` or markdown that pandoc converts); a `Makefile` or `goreleaser.yml` for release packaging; and CI that produces signed binaries / homebrew formulas / apt packages. The directory layout follows whatever the host language conventions dictate (`cmd/<binary>/main.go` for Go, `src/main.rs` for Rust, `<package>/cli.py` for Python with click/typer, `bin/mytool` + `lib/` for Node), but the *user-facing* layout — completions, manpage, subcommand help — is constant. This guide's template is **Go + cobra** because Go has the strongest CLI-tool ecosystem (cobra, viper, the kubectl/cobra-cli generator, goreleaser), but the structure transfers cleanly. The single most important principle: subcommands are *modular* — each subcommand lives in its own file under `internal/commands/`, gets registered with the root command, and can be added/removed without touching anything else. The single most common mistake: putting all subcommands in `main.go`. By the time you have five subcommands, the file is 1500 lines and unmergeable.

## Principles & why

A polished CLI tool is shaped by six principles, each enforced by a directory or convention.

1. **Thin `main`, fat root command.** `main.go` (or its language equivalent) does one thing: call `commands.Execute()`. All argv parsing, flag registration, help formatting, and dispatch happens in `internal/commands/root.go`. This is what lets you swap CLI frameworks (cobra → urfave/cli) by editing one file.
2. **One subcommand per file.** `internal/commands/foo.go` defines `mytool foo`. `internal/commands/bar.go` defines `mytool bar`. Each file is self-contained: flag definitions, business logic stub, registration with root. Files of the same shape compose well — adding a new subcommand is "copy `foo.go` to `baz.go`, edit, register."
3. **Shell completions are first-class.** A real CLI ships `_mytool` (zsh), `mytool.bash` (bash), `mytool.fish` (fish), and increasingly a PowerShell completion. Cobra (Go), clap_complete (Rust), and click (Python) all have completion-generation built in — call `mytool completion zsh > _mytool` at release time.
4. **A man page is part of distribution.** `mytool(1)` is what users get from `man mytool` after `brew install mytool`. Generate it from markdown with pandoc, or use cobra's `doc.GenManTree`. Skip this and your tool is "less professional" by exactly one signal.
5. **Subcommands are *nouns* or *verbs*, consistently.** Git is verbs (`git commit`, `git push`). kubectl is verb-noun (`kubectl get pods`, `kubectl apply -f`). Pick one mental model and stick to it. Mixing (`mytool deploy` + `mytool status`) is fine; mixing (`mytool deployment` + `mytool deploy`) is confusing.
6. **CI builds release artifacts, not just runs tests.** A `cli-tool` repo's CI does *more* than `go test` — it builds binaries for darwin/linux/windows × amd64/arm64, produces tarballs, generates SHA256 sums, optionally pushes to Homebrew tap, GitHub Releases, snap, deb, rpm. Tools like `goreleaser` (Go), `cargo-dist` (Rust), `pyoxidizer`/`shiv` (Python) handle this. The release pipeline is part of the project structure.

A seventh, softer principle: **subcommand naming is its own design problem.** `mytool sync` vs. `mytool refresh` vs. `mytool pull` — these aren't equivalent to your users. Look at how git, docker, and kubectl name things and copy patterns where they fit. Don't invent novel verbs when an existing one is clear.

## When to use

- **CLI tools intended for distribution** to other developers / users. Anything that ships to a `brew install` audience.
- **Multi-subcommand tools** following the git/kubectl/docker pattern. The structure scales to 50+ subcommands.
- **Tools with shell-completion expectations.** Users on zsh / fish expect `<tab>` to work; the structure makes it trivial.
- **Tools that pair with a host language layout.** Pair this guide with `code/go-module/`, `code/rust-binary/`, or a Python src-layout for the language-specific structure.
- **Tools that will eventually have manpages, packaging, and proper releases.** The structure makes the path obvious.

## When NOT to use

- **Internal scripts / one-off tools.** No need for completion files, manpages, or subcommand frameworks. A single `script.py` or `script.sh` is the right tool.
- **Single-purpose CLI** that takes flags and does one thing (`grep`-style). Don't add a subcommand layer for one operation. Skip the `internal/commands/` hierarchy; just put the logic in `main`.
- **TUI-driven tools** where the CLI is a launcher for a Bubble Tea / Textual interface. Different shape — see "Variants" below.
- **CLIs that wrap a library.** If the *library* is the canonical artifact and the CLI is a thin wrapper, structure as the library's layout (e.g., `python-src-layout`) with one `bin/cli.py` rather than this layout.

## Tree diagram

```
mytool/
├── README.md
├── LICENSE
├── go.mod                  ← or pyproject.toml / Cargo.toml / package.json
├── cmd/
│   └── mytool/
│       ├── main.go         ← thin entry: parse, route to subcommand
│       └── completion.go   ← shell completion generation
├── internal/
│   └── commands/
│       ├── root.go
│       ├── foo.go          ← `mytool foo`
│       └── bar.go          ← `mytool bar`
├── docs/
│   └── manpage.md
└── completions/
    ├── _mytool             ← zsh
    ├── mytool.bash
    └── mytool.fish
```

## Naming rules

- **Binary name**: short, lowercase, no dashes if possible. `gh`, `kubectl`, `docker`, `terraform`. Two-to-eight characters is the sweet spot. Match the repo name where reasonable.
- **Subcommand names**: single words, lowercase, no dashes. `commit`, `push`, `apply`, `inspect`. Two-word subcommands use a space (`mytool image build`, not `mytool image-build`); under the hood they nest as a sub-subcommand.
- **Flags**: short flag is one letter (`-v`); long flag is kebab-case (`--verbose`, `--output-format`). Match conventions: `-h` is help, `-v` is verbose (or version, depending on community), `-o` is output. Don't surprise users.
- **Files in `internal/commands/`**: lowercase Go convention. `root.go`, `foo.go`, `version.go`. One file per top-level subcommand.
- **Completion files**: `_<binary>` for zsh (no extension; the `_` prefix is mandatory for zsh's `compdef` system). `<binary>.bash` for bash. `<binary>.fish` for fish. `<binary>.ps1` for PowerShell.
- **Man pages**: `<binary>.1` for the main page, `<binary>-<subcommand>.1` for subcommand pages (e.g. `git-commit.1`). Section 1 = user commands.
- **Module paths**: Go uses `github.com/<owner>/<repo>` as the module path; this guide's template uses `github.com/example/mytool` as a placeholder.

## Worked example

A 600-line script has grown three modes chosen by `--mode`. Users complain about help output and missing completions.

1. Model modes as subcommands: `mytool sync`, `mytool export`, `mytool config get|set`.
2. Keep `main` thin: parse argv, build the root command, call it. Put each subcommand in its own file under `internal/commands/`.
3. Make every command return an exit code and write results to stdout, diagnostics to stderr, so pipes work.
4. Generate shell completions from the command tree (cobra, clap, click, or argparse-completion) into `completions/`.
5. Add a manpage under `docs/` and a `--version` that prints a build-injected version.
6. Add a golden-file test per command that runs the binary and compares stdout and exit code.

Users get `mytool --help`, tab completion, and stable machine-readable output.

## Anti-patterns

- **Putting all subcommand logic in `main.go`** or `cmd/main.go`. Once you have more than two subcommands, the file becomes unreviewable. One file per subcommand under `internal/commands/`.
- **Shipping without shell completion.** Users on zsh / fish notice immediately. Cobra / clap / click generate it for free; ship it.
- **Hand-writing completion files.** They drift. Generate at release time with `mytool completion zsh > completions/_mytool` (committed for distribution, but regenerable from CI).
- **Hand-writing the man page.** Same drift problem. Use cobra's `doc.GenManTree` (Go) or pandoc to convert markdown.
- **No `--help` for subcommands.** Every subcommand should respond to `--help` with a synopsis, flags, and an example. Cobra/clap give this for free; don't override it badly.
- **Inconsistent flag handling.** `-o file` in one subcommand, `--output=file` in another. Pick one style (POSIX-strict, GNU-style, both) and apply uniformly.
- **Subcommands that print to `stdout` what should be on `stderr`.** Diagnostic / status messages → stderr. Actual program output → stdout. So `mytool list | grep foo` works; `mytool list 2>/dev/null` suppresses the spinner.
- **Returning exit code 1 for every error.** Use distinct codes: 0 success, 1 generic failure, 2 usage error, 64-78 standard codes from sysexits.h. Tools that compose with `&&` / `||` care about this.
- **Logging to a file by default.** A CLI tool isn't a daemon. Log to stderr; let users redirect.
- **Bundling secrets / config in the binary.** Use the platform's standard config dir (`~/.config/mytool/config.yaml` on Linux per XDG, `~/Library/Application Support/mytool/` on macOS, `%APPDATA%\mytool\` on Windows).
- **No version subcommand.** `mytool version` (or `mytool --version`) should print the version, the commit SHA, and the build date. Bug reports always start with "what version?"

## Scaling & failure modes

- **Command sprawl**: past about 15 subcommands, group with nested commands (`mytool config get`) and keep `--help` output short.
- **Stable interfaces**: flags and output formats become an API. Deprecate with a warning for at least one release before removing.
- **Config precedence** (flag over env over file over default) must be documented and tested; it's where most bug reports come from.
- **Distribution** (Homebrew, apt, winget, static binaries) each need a release artifact; automate with the ecosystem's release tool.

## Variants

- **Subcommand-style (this guide)** — `mytool foo bar`, git-pattern. The dominant modern convention.
- **Flag-only style** — `mytool --command=foo --arg=bar`. Older Unix tools (`tar`, `find`). Compose well with shell pipelines, harder to discover.
- **POSIX-strict** — only short flags (`-v`), no GNU long flags. Common in BSD utilities. Less friendly to newcomers.
- **GNU-style (default)** — both `-v` and `--verbose`. Most modern CLIs.
- **TUI-driven** — the CLI is a launcher; the real UI is a terminal app (Bubble Tea / Textual / ink). Layout adds a `tui/` directory with components. See: `gh dash`, `lazygit`, `htop`.
- **Hybrid CLI + REPL** — `mytool` with no args opens a REPL; with a subcommand runs it once. See: `psql`, `python`, `node`.
- **Plugin-driven** — `mytool` discovers `mytool-<plugin>` binaries on `$PATH` and runs them as subcommands. The pattern git, gh, and kubectl all use. Layout adds a `plugins/` directory and a discovery protocol.
- **Bun / single-file** — Bun + TypeScript can produce a single-binary CLI from one file. Smaller scale, fewer moving parts; structure is simpler.

## Adoption checklist

- [ ] `--help` works at every command level and `--version` prints the real version.
- [ ] Data goes to stdout, logs and errors to stderr, and exit codes are meaningful and documented.
- [ ] Completions for at least bash and zsh are generated from the command tree.
- [ ] Config precedence is written in the README and covered by a test.
- [ ] Each command has at least one end-to-end test that runs the built binary.

## Real-world projects using this

- **GitHub CLI `gh`** (`cli/cli`) — the canonical modern Go-CLI structure. `cmd/gh/main.go` + `pkg/cmd/<subcommand>/`. Manpages, completions, plugin support.
- **kubectl** (`kubernetes/kubernetes`, in `cmd/kubectl` and `staging/src/k8s.io/cli-runtime`) — verb-noun subcommand model.
- **Docker CLI** (`docker/cli`) — large-scale subcommand structure with plugins.
- **hub** (`mislav/hub` / `github/hub`) — older but influential git-wrapper.
- **ripgrep `rg`** (`BurntSushi/ripgrep`) — exemplary single-purpose CLI; flag-style rather than subcommand-style. Used as a reference for *not* over-structuring small tools.
- **fd** (`sharkdp/fd`) — Rust CLI, similar shape to ripgrep.
- **cobra-cli** (`spf13/cobra-cli`) — generator for new cobra CLIs. The output of `cobra-cli init` is the canonical starter for this pattern.
- **git itself** — the archetype. Its plugin model (executables on `$PATH` matching `git-*`) is the inspiration for gh and kubectl plugins.
- **Terraform** (`hashicorp/terraform`) — large CLI, subcommand-heavy.
- **Hugo** (`gohugoio/hugo`) — Go + cobra; clean structure of `commands/`.

## Migration & references

- **From "everything in `main.go`" to this structure**: create `internal/commands/`. Move the root setup to `root.go`. For each subcommand, create `<name>.go` with `var <name>Cmd = &cobra.Command{...}` and `func init() { rootCmd.AddCommand(<name>Cmd) }`. Delete the dispatch logic from `main.go`.
- **Adding a subcommand**: `cobra-cli add <name>` (Go) or copy an existing subcommand file. Implement, register in `init()`, regenerate completions.
- **Adding a sub-subcommand**: define both as cobra commands; `parentCmd.AddCommand(childCmd)` instead of registering the child with root. The result: `mytool parent child`.
- **Setting up release**: install `goreleaser` (or `cargo-dist`, etc.). Add `.goreleaser.yml` defining build matrix, archive formats, optional Homebrew formula. CI on tag push runs `goreleaser release`; binaries land in GitHub Releases.
- **Adding a Homebrew tap**: in `goreleaser.yml`, add a `brews:` block with `tap: { owner, name: homebrew-tap }`. After release, `brew install <owner>/<tap>/mytool` works.
- **Generating man pages and completions** at build time: hook into `make build` or the release script. `mytool completion zsh > completions/_mytool && pandoc -s -t man docs/manpage.md -o docs/mytool.1`.
- **References**:
  - Cobra docs (cobra.dev) — Go CLI framework, the de facto standard.
  - clap docs (docs.rs/clap) — Rust equivalent.
  - click docs (click.palletsprojects.com), typer (typer.tiangolo.com) — Python equivalents.
  - The *Command Line Interface Guidelines* (clig.dev) — opinionated style guide for CLI design.
  - sysexits.h — standard exit-code constants.
  - Sibling guides: `code/go-module/` (Go-language layout), `code/rust-binary/` (Rust-language layout), `code/python-src-layout/` (Python equivalent if you build a Python CLI).
