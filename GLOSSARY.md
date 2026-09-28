# Glossary

Terms used across guidelines. Each links to the canonical guideline that defines or uses it.

## A

- **adapter** (DDD/hexagonal) — a concrete implementation of a port that wraps a vendor library or transport (e.g. `SqlAlchemyOrderRepository` adapting to PostgreSQL). Adapters live in `infrastructure/`. See [`code/ddd-hexagonal/`](code/ddd-hexagonal/).
- **ADR** (Architecture Decision Record) — a short, dated, numbered, append-only document capturing one significant decision with its context, options, and consequences. See [`principles/decision-records-adr/`](principles/decision-records-adr/).
- **AGENTS.md** — a repository-root file holding the shared rules for AI coding assistants; tool-specific files (`CLAUDE.md`, Copilot and Cursor rules) point to it. See [`principles/ai-agent-context-files/`](principles/ai-agent-context-files/).
- **atomic note** — a note small enough to capture exactly one idea, embeddable inline elsewhere without losing context. Underpins Zettelkasten and evergreen-notes systems. See [`notes/atomic-notes/`](notes/atomic-notes/).

## B

- **3-2-1 rule** (backups) — keep three copies of important data, on two kinds of media, with one copy off-site. See [`files/backup-3-2-1-layout/`](files/backup-3-2-1-layout/).
- **blast radius** — how much can break when one change or one state goes wrong; splitting Terraform state by environment shrinks it. See [`code/terraform-infrastructure/`](code/terraform-infrastructure/).
- **bounded context** (DDD) — an explicit boundary inside which a domain model has a single, consistent meaning. Two contexts can use the same word (`Order`) for different concepts without conflict. See [`code/ddd-hexagonal/`](code/ddd-hexagonal/).

## C

- **capability** (Tauri) — a permission file in `src-tauri/capabilities/` that states which windows may call which core APIs, plugins, and commands. See [`code/tauri-desktop-app/`](code/tauri-desktop-app/).
- **CCDS** — Cookiecutter Data Science, Drivendata's de-facto layout convention for ML/DS projects (data tiers, numbered notebooks, installable `src/`). See [`code/cookiecutter-data-science/`](code/cookiecutter-data-science/).
- **CODE method** — Tiago Forte's *Capture / Organize / Distill / Express* workflow for personal knowledge management. The verb layer paired with PARA's noun layer. See [`notes/second-brain-code/`](notes/second-brain-code/).
- **convention plugin** (Gradle) — a custom Gradle plugin under `build-logic/` that captures repeated build configuration (Android library setup, Kotlin compilation, test wiring) so each module just `apply`s a single plugin. See [`code/kotlin-android/`](code/kotlin-android/) and [`code/java-gradle-multi/`](code/java-gradle-multi/).

## D

- **Diátaxis** — a documentation framework that separates tutorials, how-to guides, reference, and explanation by reader intent. See [`code/docs-as-code-site/`](code/docs-as-code-site/).
- **digital garden** — a public-facing collection of notes published as a slowly-tended garden, with works-in-progress visible alongside polished writing. See [`notes/digital-garden/`](notes/digital-garden/).
- **dotfile** — a file or directory whose name begins with `.`, hidden by default in Unix listings. Used for plumbing (tool config, CI infrastructure) — never for knowledge contributors must discover. See [`principles/hidden-files-policy/`](principles/hidden-files-policy/).

## E

- **entry points** (Python) — a packaging metadata mechanism (`[project.entry-points]` in `pyproject.toml`) by which a host application discovers plugins shipped in separate distributions, via `importlib.metadata.entry_points(group="...")`. See [`code/plugin-architecture/`](code/plugin-architecture/).
- **evergreen note** — a note refined over time toward stable, reusable knowledge. Andy Matuschak's discipline: atomic, concept-oriented, declarative-titled, densely linked. See [`notes/evergreen-notes/`](notes/evergreen-notes/).

- **execution context** (browser extensions) — an isolated environment (service worker, content script, popup, options page) with its own APIs and privileges; extension source is organized by context. See [`code/browser-extension/`](code/browser-extension/).

## F

- **FHS** — Filesystem Hierarchy Standard, the Linux conventional layout for `/usr`, `/var`, `/etc`, `/home`, `/opt`, `/srv`. See [`files/unix-fhs/`](files/unix-fhs/).
- **flat layout** — a Python project layout where the import package sits at the repo root rather than under `src/`. Right default for apps and unpublished projects. See [`code/python-flat-layout/`](code/python-flat-layout/).
- **fleeting note** — a brief, transient capture (a thought scribbled mid-day) destined for the inbox until processed into something atomic and permanent. See [`notes/zettelkasten-classic/`](notes/zettelkasten-classic/).
- **Folgezettel** — Luhmann-style alphanumeric IDs (`1a`, `1a1`, `1b`) encoding parent/child branching in flat-file Zettelkasten — the IDs themselves are the navigation. See [`notes/folgezettel/`](notes/folgezettel/).

## G

- **git worktree** — an additional working directory attached to the same repository, so several branches can be checked out at once. See [`files/git-worktrees-layout/`](files/git-worktrees-layout/).

## H

- **hexagonal architecture** — Alistair Cockburn's "ports and adapters" pattern; a domain core surrounded by ports (interfaces), with adapters connecting to external systems. Often paired with DDD. See [`code/ddd-hexagonal/`](code/ddd-hexagonal/).

## I

- **inbox** (note system) — a holding area for unprocessed capture; items move out to permanent locations during the review ritual. Core to GTD, Zettelkasten, and digital-garden flows. See [`notes/zettelkasten-classic/`](notes/zettelkasten-classic/) and [`notes/gtd-digital/`](notes/gtd-digital/).

## J

- **Johnny.Decimal** — a numeric ID system organizing notes/files into ≤10 areas × ≤10 categories × ≤100 items, with every file getting a unique two-part ID. See [`notes/johnny-decimal/`](notes/johnny-decimal/).

## L

- **literature note** — a one-per-source extraction note (one per book, paper, or article) summarising the source in your own words. Sits between raw highlights and atomic permanent notes. See [`notes/zettelkasten-classic/`](notes/zettelkasten-classic/) and [`notes/literature-review-structure/`](notes/literature-review-structure/).

## M

- **Maildir** — Bernstein's per-message-file mail storage layout (`new/`, `cur/`, `tmp/` triple) — lock-free and NFS-safe. See [`files/maildir/`](files/maildir/).
- **manifest** — the file at a project's root that declares its identity, dependencies, and metadata: `pyproject.toml` (Python), `Cargo.toml` (Rust), `package.json` (JS), `pubspec.yaml` (Dart), `Package.swift` (Swift), `pom.xml` (Maven), `*.csproj` (.NET).
- **MOC** (Map of Content) — an index note linking related atomic notes; the navigable entry point that distinguishes a knowledge graph from a junk drawer. See [`notes/maps-of-content/`](notes/maps-of-content/).
- **monorepo** — a single repository containing multiple independently buildable projects sharing tooling and history. See [`code/turborepo-monorepo/`](code/turborepo-monorepo/) and [`code/nx-monorepo/`](code/nx-monorepo/).

## P

- **PARA** — Projects/Areas/Resources/Archive, Tiago Forte's four-bucket note-organization framework. See [`notes/para/`](notes/para/).
- **pointer file** — a small tracked file (Git LFS pointer, `.dvc` file, manifest with checksums) that identifies a large file stored elsewhere. See [`principles/large-files-and-binary-assets/`](principles/large-files-and-binary-assets/).
- **port** (DDD/hexagonal) — an abstract interface declared in the domain layer (e.g. `OrderRepository`) that the application calls and adapters implement. Ports invert the dependency from infrastructure to domain. See [`code/ddd-hexagonal/`](code/ddd-hexagonal/).

## R

- **rapid logging** (BuJo) — Ryder Carroll's notation for capturing tasks, events, and notes via short signified entries (`•` task, `○` event, `–` note, `*` priority). See [`notes/bullet-journal-digital/`](notes/bullet-journal-digital/).
- **run ID** (ML experiments) — the unique, dated name of one training run, such as `2026-04-30-wider-model-s0`; its directory holds the resolved config, metadata, metrics, and checkpoints. See [`code/ml-experiment-project/`](code/ml-experiment-project/).

## S

- **scaffold** — a starter directory tree, copyable as a project's initial layout. Every `template/` in this repo is a scaffold.
- **seedling** — in a digital garden, a rough early-stage note (a captured idea or first draft) before it has matured into `budding/` or `evergreen/` content. See [`notes/digital-garden/`](notes/digital-garden/).
- **src layout** — a Python project layout where source lives under `src/<package>/`, isolating it from the repo root so tests can only import from the installed distribution. See [`code/python-src-layout/`](code/python-src-layout/).
- **state file** (Terraform) — the record of which real resources a configuration manages; it can contain sensitive values, so it lives in a remote, locked, encrypted backend and never in git. See [`code/terraform-infrastructure/`](code/terraform-infrastructure/).

## T

- **target** (Swift Package) — a build unit declared in `Package.swift` mapping to a directory under `Sources/` or `Tests/`. Each target produces a module, a library, an executable, or a test bundle. See [`code/swift-package/`](code/swift-package/).

## U

- **uv workspace** (Python) — several packages in one repository sharing one `uv.lock` and one environment, declared with `[tool.uv.workspace]`. See [`code/python-uv-workspace/`](code/python-uv-workspace/).

## V

- **vault** (Obsidian) — the root directory Obsidian opens as a workspace, identified by its `.obsidian/` config dir. The vault's content layout is independent of philosophy (PARA, LYT, ACCESS, evergreen, etc.). See [`notes/obsidian-vault-structure/`](notes/obsidian-vault-structure/).
- **version catalog** (Gradle) — a TOML file at `gradle/libs.versions.toml` declaring all dependency coordinates and versions in one place so they can't drift across modules. See [`code/kotlin-android/`](code/kotlin-android/) and [`code/java-gradle-multi/`](code/java-gradle-multi/).

## W

- **wins document** — a running, dated list of accomplishments with impact and evidence, kept for reviews and promotions (also called a brag document). See [`notes/engineering-work-log/`](notes/engineering-work-log/).
- **workspace** (npm/pnpm/yarn) — a multi-package layout where one repository's `package.json` lists subdirectories (typically `apps/*`, `packages/*`) as members; internal packages resolve to local paths via the workspace protocol. See [`code/turborepo-monorepo/`](code/turborepo-monorepo/).
- **workspace root** — one folder holding all project work, with top-level folders named by kind of work and each project its own Git repository. See [`files/workspace-root-layout/`](files/workspace-root-layout/).

## X

- **XDG** — XDG Base Directory Specification, freedesktop.org's standard for `$XDG_CONFIG_HOME`, `$XDG_DATA_HOME`, `$XDG_CACHE_HOME`, `$XDG_STATE_HOME`, `$XDG_RUNTIME_DIR`. See [`files/xdg-base-directory/`](files/xdg-base-directory/).

## Z

- **Zettelkasten** — Niklas Luhmann's slip-box note system; one idea per note, dense linking, capture → process → permanent flow. See [`notes/zettelkasten-classic/`](notes/zettelkasten-classic/).
