# Index

Alphabetical catalog of all 82 guidelines. Use Ctrl+F.

| Guideline | Category | One-liner |
|---|---|---|
| `access-framework` | notes | Six-folder vault for outgrown PARA: Action / Categories / Concepts / Entries / Search / Sources. [Read](notes/access-framework/) |
| `atomic-design` | code | Component hierarchy: atoms / molecules / organisms / templates / pages — for design systems. [Read](code/atomic-design/) |
| `atomic-notes` | notes | One note = one idea, small enough to embed inline elsewhere — tool-neutral discipline. [Read](notes/atomic-notes/) |
| `bullet-journal-digital` | notes | Ryder Carroll's BuJo in markdown: Future / Monthly / Daily logs + Index, rapid logging. [Read](notes/bullet-journal-digital/) |
| `c-cpp-cmake` | code | Modern CMake (3.20+) with `src/`, `include/<project>/`, `tests/`, target-centric config. [Read](code/c-cpp-cmake/) |
| `capitalization-policy` | principles | UPPERCASE is a closed set of canonical meta-files; everything else lowercase kebab-case. [Read](principles/capitalization-policy/) |
| `cli-tool` | code | Subcommand CLI shape (cobra-style) with completions, manpage, modular `internal/commands/`. [Read](code/cli-tool/) |
| `cloud-sync-structure` | files | Namespace cloud sync under `~/cloud/<provider>/<purpose>/` so providers stop scattering. [Read](files/cloud-sync-structure/) |
| `cookiecutter-data-science` | code | Drivendata's CCDS: `data/{raw,interim,processed}/`, numbered notebooks, installable `src/`. [Read](code/cookiecutter-data-science/) |
| `daily-weekly-notes` | notes | Canonical files per day (`daily/2026-04-30.md`) and ISO week (`weekly/2026-W18.md`). [Read](notes/daily-weekly-notes/) |
| `date-archive` | files | Two-level `archive/YYYY/YYYY-MM/<YYYY-MM-DD>-<slug>.<ext>` for any append-only stream. [Read](files/date-archive/) |
| `ddd-hexagonal` | code | Concentric domain / application / infrastructure layers; ports in domain, adapters outside. [Read](code/ddd-hexagonal/) |
| `depth-vs-breadth` | principles | Aim for ≤3 levels root-to-leaf; 4 is warning, 5+ almost always wrong. [Read](principles/depth-vs-breadth/) |
| `desktop-zero-policy` | files | `~/Desktop/` is empty wallpaper, not a workspace — 24h move-or-delete rule. [Read](files/desktop-zero-policy/) |
| `digital-garden` | notes | Public notes by status: `seedlings/` then `budding/` then `evergreen/`, work-in-progress visible. [Read](notes/digital-garden/) |
| `django-project` | code | Two Scoops layout: `apps/<feature>/`, split `settings/`, split `requirements/`. [Read](code/django-project/) |
| `dotfiles-bare-git` | files | Manage `$HOME` as a git work-tree with bare `.git` at `~/.dotfiles/`, no symlinks. [Read](files/dotfiles-bare-git/) |
| `dotfiles-chezmoi` | files | Source tree at `~/.local/share/chezmoi/` with `dot_`/`private_`/`*.tmpl` filename encoding. [Read](files/dotfiles-chezmoi/) |
| `dotnet-solution` | code | `.sln` + `src/<Project>/` + `tests/<Project>.Tests/`, PascalCase, central package management. [Read](code/dotnet-solution/) |
| `downloads-triage` | files | `~/Downloads/` is an inbox: `inbox/`, `archive/`, `_to-process/`, weekly triage. [Read](files/downloads-triage/) |
| `ebook-library-calibre` | files | Calibre's `Author/Title (Series N)/Title - Author.{epub,jpg,opf}` triple, auto-managed. [Read](files/ebook-library-calibre/) |
| `evergreen-notes` | notes | Andy Matuschak's atomic + concept-oriented + declarative-title + densely-linked rule. [Read](notes/evergreen-notes/) |
| `fastapi-project` | code | Layered `app/{api,schemas,models,services,db,core}/` + Alembic — thin routers, fat services. [Read](code/fastapi-project/) |
| `feature-based-frontend` | code | `src/features/<name>/{components,api,types,hooks,index.ts}` — deletable feature slices. [Read](code/feature-based-frontend/) |
| `file-size-as-split-signal` | principles | ~500 lines is a *signal* (not rule) that a file wants to become a directory of modules. [Read](principles/file-size-as-split-signal/) |
| `flutter-app` | code | Standard `lib/`, `test/`, `pubspec.yaml`; inside `lib/` use feature folders not screen dump. [Read](code/flutter-app/) |
| `folgezettel` | notes | Luhmann's branching alphanumeric IDs (`1a`, `1a1`, `1b`) — IDs *are* the navigation. [Read](notes/folgezettel/) |
| `generated-vs-source-separation` | principles | Build outputs (`dist/`, `target/`, `build/`) live in dedicated gitignored dirs, never mixed. [Read](principles/generated-vs-source-separation/) |
| `gitignore-and-keep-files` | principles | `.gitignore` excludes; `.gitkeep` preserves empty dirs — both mandatory past toy size. [Read](principles/gitignore-and-keep-files/) |
| `go-module` | code | Single `go.mod` + `cmd/<binary>/` + language-enforced `internal/` + optional `pkg/`. [Read](code/go-module/) |
| `go-multi-module` | code | Multiple `go.mod` per subtree for independent release cadences and dep isolation. [Read](code/go-multi-module/) |
| `gtd-digital` | notes | David Allen's GTD as flat markdown: `inbox.md`, `next-actions.md` (by `@context`), `projects/`. [Read](notes/gtd-digital/) |
| `hidden-files-policy` | principles | Leading dot is a "plumbing, not surface" marker — hide tool config, not knowledge. [Read](principles/hidden-files-policy/) |
| `indexes-and-mocs` | principles | When a dir exceeds ~7 immediate children, add an `INDEX.md` or Map of Content. [Read](principles/indexes-and-mocs/) |
| `iso-date-formats` | principles | Every date in a filename or title is `YYYY-MM-DD` — only format that sorts as plain text. [Read](principles/iso-date-formats/) |
| `java-gradle-multi` | code | Multi-module Gradle Kotlin DSL with version catalog (`gradle/libs.versions.toml`). [Read](code/java-gradle-multi/) |
| `java-maven` | code | Maven Standard Directory Layout (`src/main/java/`, `src/test/java/`) + `pom.xml`. [Read](code/java-maven/) |
| `johnny-decimal` | notes | Hard-capped IDs: 10 areas × 10 categories × 100 items, every file has a unique `AC.NN`. [Read](notes/johnny-decimal/) |
| `jupyter-research` | code | Notebooks-first repo: numbered `notebooks/`, light `data/{raw,processed}/`, optional paper. [Read](code/jupyter-research/) |
| `kotlin-android` | code | Now-in-Android: `app/` + `feature/` + `core/`, version catalog, build-logic convention plugins. [Read](code/kotlin-android/) |
| `literature-review-structure` | notes | `papers/` + `summaries/` + `bib/` + `themes/` with `<year>-<author>-<title>` filenames. [Read](notes/literature-review-structure/) |
| `logseq-outliner` | notes | Outliner-first: `journals/YYYY_MM_DD.md` (note the underscores) + emergent `pages/`. [Read](notes/logseq-outliner/) |
| `lyt-linking-your-thinking` | notes | Nick Milo's MOC-driven vault: `+ Spaces/` (MOCs) / `Calendar/` / `Notes/` / `Resources/`. [Read](notes/lyt-linking-your-thinking/) |
| `maildir` | files | Bernstein's per-message-file format: `new/` / `cur/` / `tmp/`, lock-free and NFS-safe. [Read](files/maildir/) |
| `maps-of-content` | notes | First-class hub notes (`MOCs/`) — self-curated indexes that turn a graph into navigation. [Read](notes/maps-of-content/) |
| `music-library` | files | `Artist/Year - Album/NN Track Name.flac` — Beets/Picard/Plex/Jellyfin de-facto standard. [Read](files/music-library/) |
| `naming-by-purpose-not-type` | principles | Group by what files *do*, not what they *are* — `customer-onboarding/` beats `forms/`+`api/`. [Read](principles/naming-by-purpose-not-type/) |
| `naming-conventions` | principles | Use `kebab-case` everywhere except where ecosystems mandate otherwise (Python, Java, .NET). [Read](principles/naming-conventions/) |
| `nextjs-app` | code | App Router default: `app/` (RSC by default) + `components/` + `lib/` + `public/`. [Read](code/nextjs-app/) |
| `node-library` | code | Publishable npm package: `src/` + `dist/`, `"exports"` field, `tsc`-only (no bundler). [Read](code/node-library/) |
| `nx-monorepo` | code | `apps/` + `libs/` with project graph, `nx affected`, tag-based module-boundary lint rules. [Read](code/nx-monorepo/) |
| `obsidian-vault-structure` | notes | Obsidian scaffolding under any philosophy: `.obsidian/`, `00-meta/`, `attachments/`, `daily/`. [Read](notes/obsidian-vault-structure/) |
| `one-purpose-per-directory` | principles | A directory answers one question — replace `utils/`/`misc/`/`helpers/` with purpose names. [Read](principles/one-purpose-per-directory/) |
| `para` | notes | Tiago Forte's four-bucket: `1-projects/` / `2-areas/` / `3-resources/` / `4-archive/`. [Read](notes/para/) |
| `photos-by-date-and-event` | files | `YYYY/YYYY-MM/` for daily-life + `YYYY/YYYY-MM-DD-event-name/` for retrievable events. [Read](files/photos-by-date-and-event/) |
| `plugin-architecture` | code | Stable host + open plugin set via entry-points group + `plugins/<name>/plugin.toml`. [Read](code/plugin-architecture/) |
| `project-archive` | files | Split projects into `active/<project>/` and `archive/<YYYY>/<project>/` — moving is a ritual. [Read](files/project-archive/) |
| `python-flat-layout` | code | `<package>/` at repo root — for apps/services not published to PyPI. [Read](code/python-flat-layout/) |
| `python-src-layout` | code | `src/<package>/` — PyPA-recommended for libraries; tests can't accidentally import working tree. [Read](code/python-src-layout/) |
| `readme-placement` | principles | A `README.md` at every navigational junction — five lines beat zero. [Read](principles/readme-placement/) |
| `receipts-and-finance` | files | `finance/YYYY/YYYY-MM/YYYY-MM-DD <vendor> $<amount> <description>.pdf` — grep-tally-able. [Read](files/receipts-and-finance/) |
| `removable-media-layout` | files | Physical-label every USB/SD; import to `~/imports/<label>-<YYYY-MM-DD>/` to preserve provenance. [Read](files/removable-media-layout/) |
| `roam-daily-pages` | notes | Flat: every day a page, topical pages emerge from inline `[[bracket links]]`, no folders. [Read](notes/roam-daily-pages/) |
| `rust-binary` | code | `cargo new --bin` + main-with-lib split; `Cargo.lock` committed for reproducible builds. [Read](code/rust-binary/) |
| `rust-library` | code | `src/lib.rs` + dual MIT/Apache-2.0; `Cargo.lock` gitignored; publishing metadata in `Cargo.toml`. [Read](code/rust-library/) |
| `rust-workspace` | code | Multi-crate workspace with shared `target/`, `[workspace.package]`, `[workspace.dependencies]`. [Read](code/rust-workspace/) |
| `scanned-documents` | files | `scans/YYYY/YYYY-MM/YYYY-MM-DD - source - description.pdf` paired with OCR for full-text search. [Read](files/scanned-documents/) |
| `screenshots-auto-flow` | files | `~/Pictures/Screenshots/inbox/` with ISO timestamps + weekly triage to `reference/` or trash. [Read](files/screenshots-auto-flow/) |
| `second-brain-code` | notes | Tiago Forte's CODE workflow (Capture/Organize/Distill/Express) layered onto PARA. [Read](notes/second-brain-code/) |
| `stable-vs-volatile-separation` | principles | Don't mix daily-changing volatile content with stable source — separate dirs, different backup. [Read](principles/stable-vs-volatile-separation/) |
| `status-based-organization` | principles | Top-level `active/` / `archive/` / `someday/` — directory *is* status, not a `_done` suffix. [Read](principles/status-based-organization/) |
| `swift-package` | code | SwiftPM: `Package.swift` + `Sources/<Target>/` + `Tests/<Target>Tests/`, PascalCase modules. [Read](code/swift-package/) |
| `test-colocation-vs-separation` | principles | Pick one: separated `tests/` mirror or `*.test.ts` co-location — never both in one repo. [Read](principles/test-colocation-vs-separation/) |
| `tiddlywiki-structure` | notes | Single-file `wiki.html` or Node.js `tiddlers/*.tid` with text-header metadata. [Read](notes/tiddlywiki-structure/) |
| `topic-vs-date-organization` | notes | Intentional split: `daily/` for time-driven capture + `topics/` for subject-driven knowledge. [Read](notes/topic-vs-date-organization/) |
| `turborepo-monorepo` | code | `apps/` + `packages/` workspace with `turbo.json` pipeline + remote cache (pnpm + Turborepo). [Read](code/turborepo-monorepo/) |
| `unix-fhs` | files | Filesystem Hierarchy Standard: `/etc` config, `/usr` programs, `/var` state, `/home` users. [Read](files/unix-fhs/) |
| `versioning-in-paths` | principles | No `_v2`/`-old`/`-final` in paths — git tags carry version; filesystem is a bad VCS. [Read](principles/versioning-in-paths/) |
| `video-library` | files | Plex's `Movies/Title (Year)/` and `TV Shows/Show/Season XX/Show - sXXeYY.ext` standard. [Read](files/video-library/) |
| `vue-nuxt-app` | code | Nuxt 3 convention: `pages/` router + auto-imported `components/` + `composables/` + `server/api/`. [Read](code/vue-nuxt-app/) |
| `xdg-base-directory` | files | XDG Base Directory: `$XDG_CONFIG_HOME` / `$XDG_DATA_HOME` / `$XDG_CACHE_HOME` / `$XDG_STATE_HOME`. [Read](files/xdg-base-directory/) |
| `zettelkasten-classic` | notes | Luhmann's slip-box in markdown: `inbox/` / `permanent/` / `literature/` + `references.bib`. [Read](notes/zettelkasten-classic/) |
