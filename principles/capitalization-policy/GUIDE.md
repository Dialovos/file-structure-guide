# Capitalization policy

## TL;DR

UPPERCASE is reserved for *canonical* meta-files: `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, plus a small set this repo recognises (`GUIDE.md`, `INDEX.md`, `CHOOSE.md`, `PHILOSOPHY.md`, `ANTIPATTERNS.md`, `GLOSSARY.md`). Everything else — source files, config files, ordinary docs, asset files — is lowercase, and prefer kebab-case for multi-word names. Treat the canonical UPPERCASE list as a *closed set*: don't invent new UPPERCASE names.

## Principles & why

UPPERCASE on a file is a visual signal: "this is special, look here first." That signal only works when it's used sparingly. If `MY-NOTES.md`, `INSTALL.md`, `CONFIG.MD`, and `OVERVIEW.md` all SHOUT, none of them stand out, and the canonical files (the ones GitHub actually renders specially) drown in the noise.

The closed-set discipline matters because the well-known UPPERCASE filenames are a contract with tooling: GitHub renders `README.md` at the top of any directory listing, links `LICENSE` from the repo header, surfaces `CONTRIBUTING.md` in the PR template flow, and so on. Adding new UPPERCASE filenames doesn't extend this contract; it just makes the list of "specially rendered" files unpredictable.

Lowercase kebab-case for everything else is portable. Windows is case-insensitive but case-preserving; macOS HFS+ defaults the same way; Linux is case-sensitive. A file called `My-Notes.md` on macOS becomes `my-notes.md` on Linux when round-tripped through certain tools, breaking imports. Keeping non-canonical files all-lowercase removes the entire failure class.

## When to use

Apply this rule everywhere — it's a single-line policy that scales infinitely:

- Every project, every directory: UPPERCASE only for the closed canonical set; everything else lowercase kebab-case.
- New repo: add `README.md`, `LICENSE`, and one or two others as needed. Resist the urge to UPPERCASE `INSTALL.md` or `USAGE.md` — those go in `docs/` lowercase or are sections inside `README.md`.
- Code files: lowercase kebab-case (`http-client.ts`) or lowercase snake_case (`http_client.py`) per ecosystem norm. Never UPPERCASE.
- Asset files: lowercase. `logo.svg`, not `LOGO.SVG`.

## When NOT to use

A few ecosystems mandate different capitalization and you should follow them:

- **.NET / C# / Java** — file names often mirror class names, which are PascalCase by convention. `OrderService.cs` is correct in C#; renaming to `order-service.cs` would break the convention.
- **Go exported identifiers** — capitalization rule applies to *identifiers*, not files. Go files are lowercase (`http.go`); the exported `HttpClient` symbol inside is unrelated to file casing.
- **Make / GNU build files** — `Makefile`, `Dockerfile`, `Containerfile`, `Vagrantfile` are PascalCase by tooling convention. They're effectively a closed set too.
- **Filesystem-mandated** — `Info.plist` on macOS, `Manifest.toml` in some Julia tools, etc.

When you take an exception, do it because the tool requires it, not because the file feels important.

## Tree diagram

```
project/
├── README.md          ← UPPERCASE canonical
├── LICENSE            ← UPPERCASE canonical
├── CONTRIBUTING.md    ← UPPERCASE canonical
├── CHANGELOG.md       ← UPPERCASE canonical
├── pyproject.toml     ← lowercase (config)
├── src/
│   └── main.py        ← lowercase
└── docs/
    └── architecture.md  ← lowercase

bad/
├── readme.md          ← canonical should be UPPERCASE
├── My-Notes/          ← non-canonical should be lowercase
└── License            ← inconsistent (no extension, mixed case)
```

## Naming rules

1. The canonical UPPERCASE set in this repo: `README.md`, `LICENSE` (with or without extension), `CONTRIBUTING.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `GUIDE.md`, `INDEX.md`, `CHOOSE.md`, `PHILOSOPHY.md`, `ANTIPATTERNS.md`, `GLOSSARY.md`. Treat additions to this list as a deliberate repo-wide policy decision.
2. All other files: lowercase, kebab-case for word separation (`getting-started.md`, not `getting_started.md` or `gettingStarted.md`), unless the language norm differs (Python: `snake_case.py`).
3. Directories: always lowercase, kebab-case (`customer-onboarding/`, not `CustomerOnboarding/` or `customer_onboarding/`). Exception: ecosystem-mandated PascalCase folders in .NET / Java toolchains.
4. Don't capitalise *parts* of a filename (`api-V2.md`, `Auth-tokens.md`). Either it's a canonical UPPERCASE file or it's all-lowercase.
5. The `LICENSE` file is canonical with or without `.md` / `.txt` — both are recognised by GitHub. Pick one and be consistent within a project.
6. Markdown files outside the canonical set go in `docs/` (or a topical subdir) lowercase, or are sections inside `README.md`.

## Worked example

A repo has grown three spellings of the same idea: `Readme.md`, `docs/Architecture.MD`, and `Assets/Logo.PNG`. On a case-insensitive laptop this all works; on the Linux CI runner a link to `docs/architecture.md` returns 404.

1. List the offenders: `git ls-files | grep '[A-Z]'`.
2. Keep only the closed canonical set in UPPERCASE (`README.md`, `LICENSE`, `CHANGELOG.md`, ...). Everything else becomes lowercase kebab-case.
3. Rename in two steps so git records the change on case-insensitive filesystems: `git mv Assets assets-tmp && git mv assets-tmp assets`.
4. Grep for links to the old names (`grep -rn "Architecture.md" .`) and fix them in the same commit.
5. Add a CI step that fails on new uppercase names outside the allow-list.

The rename commit touches many paths but changes no content, which keeps `git blame` usable with `--follow`.

## Anti-patterns

- **`readme.md` in lowercase** — GitHub still renders it, but readers used to scanning for the SHOUTING `README.md` miss it. Use the canonical case.
- **`MY-NOTES.md` UPPERCASE** — non-canonical SHOUTING. Move to `docs/my-notes.md` or rename `notes.md` lowercase at root.
- **Mixed-case directories** (`Docs/`, `Source/`, `Tests/`) — only justified when an ecosystem mandates it. Otherwise pure lowercase.
- **`License` without extension and mixed case** — file is canonical but the casing is inconsistent. GitHub's special handling of `LICENSE` is forgiving but readers shouldn't have to wonder.
- **`Readme.md`** (Title Case) — looks like a typo of either canonical UPPERCASE or pragmatic lowercase. Pick one.
- **`Config.toml`** for `pyproject.toml` — config files are tool-defined; don't impose UPPERCASE on them.

## Scaling & failure modes

- **Case-insensitive filesystems (macOS, Windows) hide the bug.** Two files that differ only by case can't coexist on those systems, so a checkout of a repo that contains both silently loses one. This is the main practical reason to keep the rule strict.
- **Ecosystem-mandated uppercase** (`Dockerfile`, `Makefile`, `Cargo.toml`, `Gemfile`, `CMakeLists.txt`) is a fixed exception list per tool; add to it deliberately, never by habit.
- **Growth of the canonical set.** Every new UPPERCASE name dilutes the signal that UPPERCASE means "read me first". If the set passes roughly a dozen names, fold some into `docs/`.

## Variants

- **Strict** (this repo's choice) — only the closed canonical set is UPPERCASE; every other file is lowercase. Easiest to enforce, easiest to read.
- **Permissive** — any "doc-like" markdown file can be UPPERCASE if the author thinks it deserves attention. Drifts toward visual clutter; not recommended.
- **All-lowercase** — even `readme.md` is lowercase. Common in some Go projects. Loses the GitHub-special-rendering contract for nothing in return; only sensible if you genuinely don't render on GitHub.
- **PascalCase ecosystem variant** — .NET, Java: file names mirror exported class names. Different rule set entirely; don't mix it with the canonical UPPERCASE policy.
- **GNU/Make convention** — PascalCase filenames where tooling expects them (`Makefile`, `Dockerfile`); treat as a separate closed set distinct from the meta-doc set.

## Adoption checklist

- [ ] `git ls-files | grep '[A-Z]'` shows only the allow-listed names and tool-mandated files.
- [ ] No two tracked paths differ only by case (`git ls-files | tr A-Z a-z | sort | uniq -d` is empty).
- [ ] The allow-list is written down (in `CONTRIBUTING.md` or the CI script), not implied.
- [ ] Ecosystem exceptions are listed next to the rule that grants them.

## Real-world projects using this

- **GitHub** — recognises `README*`, `LICENSE*`, `CONTRIBUTING*`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`, `FUNDING.yml`, `ISSUE_TEMPLATE/`, `PULL_REQUEST_TEMPLATE.md` with special rendering. The canonical UPPERCASE set comes from this contract.
- **Apache Software Foundation** — virtually every project has `README`, `LICENSE`, `NOTICE`, `CHANGES` UPPERCASE at the project root.
- **Linux kernel** — `README`, `COPYING`, `MAINTAINERS`, `CREDITS`, `Documentation/` (capital D for the directory by historical exception, lowercase content inside).
- **rust-lang/rust** — `README.md`, `LICENSE-MIT`, `LICENSE-APACHE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` follow the canonical pattern; everything else is lowercase.
- **golang/go** — same pattern: UPPERCASE meta files, lowercase source and docs (`doc/`, `src/`, `lib/`).
- **kubernetes/kubernetes** — UPPERCASE `README.md`, `LICENSE`, `OWNERS` (k8s-specific canonical), and lowercase everything else.

## Migration & references

To bring an existing repo into compliance:

```bash
# 1. Find non-canonical UPPERCASE files
find . -type f \( -name "*.md" -o -name "*.MD" \) \
  | grep -v node_modules \
  | grep -E '/[A-Z][A-Z0-9_-]*\.[Mm][Dd]$' \
  | grep -vE '/(README|LICENSE|CONTRIBUTING|CHANGELOG|CODE_OF_CONDUCT|SECURITY|GUIDE|INDEX|CHOOSE|PHILOSOPHY|ANTIPATTERNS|GLOSSARY)\.md$'

# 2. Rename them to lowercase, one commit per batch
git mv MY-NOTES.md docs/my-notes.md
git commit -m "rename: lowercase non-canonical doc per capitalization-policy"

# 3. Find canonical files in wrong case and fix
[ -f readme.md ] && git mv readme.md README.md && \
  git commit -m "rename: canonical README.md UPPERCASE"
```

On case-insensitive filesystems (macOS default, Windows), git rename to a different case requires an intermediate step:

```bash
git mv readme.md _README.md
git mv _README.md README.md
git commit -m "rename: canonical README.md UPPERCASE"
```

Further reading:

- GitHub Docs, "About READMEs" / "Adding a license to a repository" / "Setting up your project for healthy contributions" — the source of the canonical-rendering contract.
- *POSIX filename portability* (POSIX.1-2017, §3.281) — defines the portable filename character set, which informs lowercase-kebab-case as a safe default.
- `principles/naming-conventions/` — sibling rule covering broader filename mechanics (separators, extensions, length).
- `PHILOSOPHY.md` (this repo) — UPPERCASE files at the root are the live demonstration of this policy.
