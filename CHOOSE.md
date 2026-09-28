# Choose

Decision tree. Start at §1 and answer each question to land on a guideline.

## §1. What are you organizing?

- Code → §2
- Notes & knowledge → §3
- General personal files → §4
- Looking for a cross-cutting principle → §5, or browse [`principles/`](principles/)

## §2. CODE — What language/stack?

- Python → §2.1
- Rust → §2.2
- JS/TS → §2.3
- JVM (Java/Kotlin) → §2.4
- Systems (C/C++/Go) → §2.5
- .NET / Mobile → §2.6
- Research / specialized → §2.7
- Architecture pattern (cross-language) → §2.8
- Desktop apps, browser extensions, infrastructure, containers, repo metadata, docs sites → §2.9

### §2.1 Python — what kind of project?

- Library you'll publish to PyPI → [`code/python-src-layout/`](code/python-src-layout/)
- Several related packages in one repository sharing one lockfile → [`code/python-uv-workspace/`](code/python-uv-workspace/)
- Model training with many runs to compare and reproduce → [`code/ml-experiment-project/`](code/ml-experiment-project/)
- App, internal tool, or unpublished project → [`code/python-flat-layout/`](code/python-flat-layout/)
- Django web app → [`code/django-project/`](code/django-project/)
- FastAPI service → [`code/fastapi-project/`](code/fastapi-project/)
- ML / data science (productionizing) → [`code/cookiecutter-data-science/`](code/cookiecutter-data-science/)
- Notebook-first research / paper repo → [`code/jupyter-research/`](code/jupyter-research/)
- Single-binary CLI tool → [`code/cli-tool/`](code/cli-tool/)
- Extensible app with third-party plugins → [`code/plugin-architecture/`](code/plugin-architecture/)

### §2.2 Rust — what kind of crate?

- Single binary (CLI, daemon, service) → [`code/rust-binary/`](code/rust-binary/)
- Library published to crates.io → [`code/rust-library/`](code/rust-library/)
- Multiple crates sharing one repo → [`code/rust-workspace/`](code/rust-workspace/)
- Subcommand-style CLI conventions → [`code/cli-tool/`](code/cli-tool/)

### §2.3 JS/TS — what kind of project?

- Publishable npm package → [`code/node-library/`](code/node-library/)
- Next.js app (App Router) → [`code/nextjs-app/`](code/nextjs-app/)
- Nuxt 3 / Vue app → [`code/vue-nuxt-app/`](code/vue-nuxt-app/)
- Monorepo with task caching (lightweight) → [`code/turborepo-monorepo/`](code/turborepo-monorepo/)
- Monorepo with project graph (heavyweight, polyglot) → [`code/nx-monorepo/`](code/nx-monorepo/)
- Frontend app organized by feature → [`code/feature-based-frontend/`](code/feature-based-frontend/)
- Design-system / component library → [`code/atomic-design/`](code/atomic-design/)

### §2.4 JVM — Java or Kotlin?

- Single-module Maven project → [`code/java-maven/`](code/java-maven/)
- Multi-module Gradle build → [`code/java-gradle-multi/`](code/java-gradle-multi/)
- Android app (multi-module, modern) → [`code/kotlin-android/`](code/kotlin-android/)

### §2.5 Systems — C/C++ or Go?

- C/C++ with CMake → [`code/c-cpp-cmake/`](code/c-cpp-cmake/)
- Single Go module (`cmd/` + `internal/`) → [`code/go-module/`](code/go-module/)
- Multiple Go modules with independent release cadences → [`code/go-multi-module/`](code/go-multi-module/)
- Go subcommand CLI tool → [`code/cli-tool/`](code/cli-tool/)

### §2.6 .NET / Mobile

- .NET solution (`.sln` + `src/` + `tests/`) → [`code/dotnet-solution/`](code/dotnet-solution/)
- Swift Package Manager library or app → [`code/swift-package/`](code/swift-package/)
- Android (Kotlin, multi-module) → [`code/kotlin-android/`](code/kotlin-android/)
- Flutter (Dart, cross-platform) → [`code/flutter-app/`](code/flutter-app/)

### §2.7 Research / specialized

- Productionizable data-science project → [`code/cookiecutter-data-science/`](code/cookiecutter-data-science/)
- Notebook-as-artifact research repo → [`code/jupyter-research/`](code/jupyter-research/)
- Single-binary CLI tool (any language) → [`code/cli-tool/`](code/cli-tool/)
- Extensible app with plugins → [`code/plugin-architecture/`](code/plugin-architecture/)

### §2.8 Architecture pattern (cross-language)

- Domain-rich service with replaceable infrastructure → [`code/ddd-hexagonal/`](code/ddd-hexagonal/)
- Frontend app organized by user-facing capability → [`code/feature-based-frontend/`](code/feature-based-frontend/)
- Component library with composition gradient → [`code/atomic-design/`](code/atomic-design/)
- Stable host + open plugin set → [`code/plugin-architecture/`](code/plugin-architecture/)

### §2.9 Apps, infrastructure, and delivery

- Desktop app with a web UI and a native Rust backend → [`code/tauri-desktop-app/`](code/tauri-desktop-app/)
- Browser extension (Manifest V3) → [`code/browser-extension/`](code/browser-extension/)
- Cloud infrastructure as code (Terraform) → [`code/terraform-infrastructure/`](code/terraform-infrastructure/)
- Multi-service local stack with Docker Compose → [`code/docker-compose-services/`](code/docker-compose-services/)
- GitHub workflows, issue and PR templates, code owners → [`code/github-repository-meta/`](code/github-repository-meta/)
- Documentation site built from Markdown in the repo → [`code/docs-as-code-site/`](code/docs-as-code-site/)

## §3. NOTES — What's your style?

- Project-driven knowledge work → §3.1
- ID-numbered filing → §3.2
- Atomic interlinked notes → §3.3
- Daily/journal-driven → §3.4
- Tool-specific (Obsidian, Logseq, Roam, TiddlyWiki) → §3.5
- Public-facing notes → §3.6
- Work, study, and research records → §3.7

### §3.1 Project-driven knowledge work

- Forte's four-bucket Projects/Areas/Resources/Archive → [`notes/para/`](notes/para/)
- PARA + Capture/Organize/Distill/Express workflow → [`notes/second-brain-code/`](notes/second-brain-code/)
- Six-folder framework when PARA outgrows → [`notes/access-framework/`](notes/access-framework/)
- David Allen's GTD as flat markdown → [`notes/gtd-digital/`](notes/gtd-digital/)
- Map-of-Content driven hub/spoke vault → [`notes/lyt-linking-your-thinking/`](notes/lyt-linking-your-thinking/)
- Academic literature review (papers + summaries + bib) → [`notes/literature-review-structure/`](notes/literature-review-structure/)

### §3.2 ID-numbered filing

- Hard-capped 10×10×100 numeric IDs → [`notes/johnny-decimal/`](notes/johnny-decimal/)
- Luhmann's branching alphanumeric IDs → [`notes/folgezettel/`](notes/folgezettel/)
- Timestamp/ID-addressed slip-box → [`notes/zettelkasten-classic/`](notes/zettelkasten-classic/)

### §3.3 Atomic interlinked notes

- The pure rule (tool-neutral) → [`notes/atomic-notes/`](notes/atomic-notes/)
- Andy Matuschak's evergreen discipline → [`notes/evergreen-notes/`](notes/evergreen-notes/)
- Classic Zettelkasten in markdown → [`notes/zettelkasten-classic/`](notes/zettelkasten-classic/)
- Luhmann's branching ID variant → [`notes/folgezettel/`](notes/folgezettel/)
- First-class hub notes (MOCs) → [`notes/maps-of-content/`](notes/maps-of-content/)

### §3.4 Daily/journal-driven

- Per-day + per-week canonical files → [`notes/daily-weekly-notes/`](notes/daily-weekly-notes/)
- Bullet Journal (tasks + events + notes) → [`notes/bullet-journal-digital/`](notes/bullet-journal-digital/)
- Roam-style flat daily pages with `[[backlinks]]` → [`notes/roam-daily-pages/`](notes/roam-daily-pages/)
- Topic vs date — intentional mix decision → [`notes/topic-vs-date-organization/`](notes/topic-vs-date-organization/)

### §3.5 Tool-specific

- Obsidian (any philosophy underneath) → [`notes/obsidian-vault-structure/`](notes/obsidian-vault-structure/)
- Logseq (outliner-first, daily journals) → [`notes/logseq-outliner/`](notes/logseq-outliner/)
- Roam Research (flat, link-driven) → [`notes/roam-daily-pages/`](notes/roam-daily-pages/)
- TiddlyWiki (single-file or Node.js mode) → [`notes/tiddlywiki-structure/`](notes/tiddlywiki-structure/)

### §3.6 Public-facing notes

- Slowly-tended garden with status-tagged drafts → [`notes/digital-garden/`](notes/digital-garden/)
- MOC-driven public vault → [`notes/lyt-linking-your-thinking/`](notes/lyt-linking-your-thinking/)
- Maps of Content as published indexes → [`notes/maps-of-content/`](notes/maps-of-content/)

### §3.7 Work, study, and research records

- Coursework: notes, homework, quizzes, exams per course → [`notes/course-notes-structure/`](notes/course-notes-structure/)
- Experiments with hypotheses, protocols, and results → [`notes/research-lab-notebook/`](notes/research-lab-notebook/)
- Daily work log, weekly review, wins for performance reviews → [`notes/engineering-work-log/`](notes/engineering-work-log/)

## §4. FILES — What kind of personal files?

- Application config & data → §4.1
- Time-based archives (receipts, scans, journals) → §4.2
- Photos / media → §4.3
- Mail → §4.4
- Dotfiles → §4.5
- Cloud sync / removable / desktop hygiene → §4.6
- Workspaces, business documents, worktrees, backups → §4.7

### §4.1 Application config & data

- XDG Base Directory (`~/.config`, `~/.local/share`, `~/.cache`, `~/.local/state`) → [`files/xdg-base-directory/`](files/xdg-base-directory/)
- System-wide layout (`/etc`, `/usr`, `/var`, `/opt`) → [`files/unix-fhs/`](files/unix-fhs/)

### §4.2 Time-based archives

- Generic append-only date archive → [`files/date-archive/`](files/date-archive/)
- Receipts and financial documents → [`files/receipts-and-finance/`](files/receipts-and-finance/)
- OCR'd scanned paper documents → [`files/scanned-documents/`](files/scanned-documents/)
- Project lifecycle (active vs archived) → [`files/project-archive/`](files/project-archive/)

### §4.3 Photos / media

- Photos (date-bucket + named events) → [`files/photos-by-date-and-event/`](files/photos-by-date-and-event/)
- Music collection (Beets/Picard/Plex shape) → [`files/music-library/`](files/music-library/)
- Movies and TV shows (Plex Personal Media) → [`files/video-library/`](files/video-library/)
- Ebook library managed by Calibre → [`files/ebook-library-calibre/`](files/ebook-library-calibre/)
- Screenshots (capture → triage → archive flow) → [`files/screenshots-auto-flow/`](files/screenshots-auto-flow/)

### §4.4 Mail

- Maildir (per-message-file, lock-free, NFS-safe) → [`files/maildir/`](files/maildir/)

### §4.5 Dotfiles

- Bare git repo with `$HOME` as work-tree → [`files/dotfiles-bare-git/`](files/dotfiles-bare-git/)
- Chezmoi (filename-encoded metadata, templating, secrets) → [`files/dotfiles-chezmoi/`](files/dotfiles-chezmoi/)

### §4.6 Cloud sync / removable / desktop hygiene

- Namespace cloud sync under `~/cloud/<provider>/<purpose>/` → [`files/cloud-sync-structure/`](files/cloud-sync-structure/)
- USB / SD / external-drive imports with provenance → [`files/removable-media-layout/`](files/removable-media-layout/)
- `~/Desktop/` empty-by-policy → [`files/desktop-zero-policy/`](files/desktop-zero-policy/)
- `~/Downloads/` as triaged inbox → [`files/downloads-triage/`](files/downloads-triage/)

### §4.7 Workspaces, business documents, worktrees, backups

- One root folder for all projects, business, school, and an inbox → [`files/workspace-root-layout/`](files/workspace-root-layout/)
- Several branches of one repository checked out at once → [`files/git-worktrees-layout/`](files/git-worktrees-layout/)
- Clients, contracts, invoices, and legal documents for a business → [`files/business-documents-layout/`](files/business-documents-layout/)
- Backups you can actually restore (3-2-1) → [`files/backup-3-2-1-layout/`](files/backup-3-2-1-layout/)

## §5. PRINCIPLES — Which cross-cutting question are you facing?

- One repository or many? → [`principles/monorepo-vs-polyrepo/`](principles/monorepo-vs-polyrepo/)
- Where do config values and secrets go? → [`principles/config-and-secrets-placement/`](principles/config-and-secrets-placement/)
- How do I instruct AI coding assistants consistently? → [`principles/ai-agent-context-files/`](principles/ai-agent-context-files/)
- Big or binary files are bloating git → [`principles/large-files-and-binary-assets/`](principles/large-files-and-binary-assets/)
- How do I record why we chose X? → [`principles/decision-records-adr/`](principles/decision-records-adr/)
- Naming, dates, depth, READMEs, tests, ignores → browse [`principles/`](principles/) for the other sixteen.
