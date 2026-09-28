## TL;DR

A **workspace root** is a single folder that holds all of your project work, so your home directory doesn't fill with repositories and half-finished experiments. Give it a small, fixed set of top-level folders named by *kind of work*: `projects/` for code (split into `public/` and `private/` by repository visibility), `business/`, `personal/`, `school/`, `references/` for notes reused across projects, `tools/` for shared utilities, an `inbox/` where incoming files wait to be placed, an `archive/` for recovery material, and a `.scratch/` for temporary files. Each project inside `projects/` is its **own Git repository**: the workspace itself is a folder of independent repositories, not a monorepo. Add one shared instruction file (`AGENTS.md`) and a short `README.md` map at the root, so any person or AI assistant can find where things go. The rule for growth is: new work goes into an existing folder; a new top-level folder needs a reason and a README line.

## Principles & why

1. **Top level is a table of contents.** A handful of folders named by kind of work lets you answer "where does this go?" without thinking. Extra top-level folders (`output/`, `misc/`, `final/`) are the start of a junk drawer (see `one-purpose-per-directory`).
2. **A project is a repository.** Each project has its own history, remote, visibility, and lifecycle. Nesting repositories or copying one project into another creates divergent copies; a folder of independent repositories keeps each one clean.
3. **Visibility is structural.** Splitting `projects/` into `public/` and `private/` makes it obvious what may be pushed to a public remote, and lets tooling apply stricter checks to public repositories.
4. **Separate inbox, scratch, and archive.** Incoming files, temporary work, and recovery material each have a home, so the rest stays uncluttered. The inbox is emptied by placing files; scratch is emptied at the end of each task; the archive is written only when something that might be needed later is removed.
5. **One shared rulebook.** Conventions (naming, where things go, safety rules) are written once at the root, and every tool and assistant reads that file instead of guessing (see `ai-agent-context-files`).
6. **Sync through remotes, not copies.** If the workspace exists on more than one machine, share code through each project's Git remote, never by copying folders between machines.

## When to use

- **Developers who work on several projects**, and want one predictable place for them.
- **People who mix code, business, school, and personal work** on one machine and need boundaries between them.
- **Workspaces shared with AI coding assistants**, where a clear map and rules reduce mistakes.
- **Anyone maintaining the same workspace on more than one computer**, using Git remotes as the sync mechanism.

## When NOT to use

- **A single project.** Its own repository layout is enough (see the `code/` guides).
- **A monorepo.** If all the code is released together and shares tooling, one repository with `apps/` and `packages/` fits better (see `monorepo-vs-polyrepo`).
- **Cloud-synced document folders.** Don't put Git working trees inside sync folders (see `cloud-sync-structure`).
- **Backups.** The workspace layout says nothing about redundancy; see `backup-3-2-1-layout`.

## Tree diagram

```
workspace/
├── README.md                     ← the map: what each folder is for
├── AGENTS.md                     ← shared rules for every person and assistant
├── projects/
│   ├── public/                   ← repositories whose remote is public
│   │   └── some-library/         ← its own Git repository
│   └── private/                  ← private or local-only repositories
│       └── some-service/
├── business/
│   └── my-company/               ← see business-documents-layout
├── personal/                     ← personal files and planning
├── school/
│   └── cs-101/                   ← see course-notes-structure
├── references/
│   └── topic-name/               ← notes and research reused across projects
├── tools/
│   └── repo-scanner/             ← reusable utilities and shared environments
├── inbox/                        ← files handed over; place each one, then delete
├── archive/
│   └── 2026-04-30-topic/         ← recovery material only
└── .scratch/                     ← temporary files; empty before finishing a task
```

## Naming rules

- **Top-level folders** are lowercase kebab-case nouns for the kind of work (`projects`, `business`, `school`), and the set stays fixed.
- **Projects** use lowercase kebab-case names that say what the project is (`tokenscope`, `file-structure-guide`); the folder, repository, and package share one name (a Python import module uses its `snake_case` form).
- **Archive entries** are `YYYY-MM-DD-topic/`, so the date of removal is visible (see `iso-date-formats`).
- **Instruction files** at the root are the canonical uppercase names (`README.md`, `AGENTS.md`), and each tool-specific file only points to `AGENTS.md`.
- **No suffixes for versions or status**: never `project-copy`, `project-final`, or `-v2` (see `versioning-in-paths`); reuse the project's folder and its Git history.
- **Environment folders** stay inside their projects (`.venv/` in the project root), not shared at the workspace root.

## Worked example

A home directory holds `code/`, `Documents/projects-2/`, `new-project-final/`, and a dozen cloned repositories, and files downloaded for a task have piled up on the Desktop.

1. Create the workspace root and its top-level folders: `projects/public`, `projects/private`, `business`, `personal`, `school`, `references`, `tools`, `inbox`, `archive`, `.scratch`.
2. Make a list of every repository: `find ~ -name .git -maxdepth 4 -type d 2>/dev/null` (adjust the depth). For each, check its remote visibility (`git remote -v`, then the hosting site) and move the folder to `projects/public/` or `projects/private/`.
3. Move non-code work to `business/`, `school/`, `personal/`, and reusable notes to `references/`.
4. Move loose downloads into `inbox/`, then place each file properly as you use it.
5. Resolve duplicates by comparing content and Git history before deleting; never delete something that only exists in one place. If something might be needed later, move it into `archive/YYYY-MM-DD-topic/` instead.
6. Write `README.md` (the map) and `AGENTS.md` (the rules) at the root.
7. Register each project in a small catalog or in the README, and set up the same checks for each repository (for example, shared Git hooks).
8. On a second machine, clone each project from its remote into the same layout; don't copy folders across.

Everything has a predictable place, and public and private work are never confused.

## Anti-patterns

- **Extra top-level folders** (`output`, `misc`, `final`) created on the spot. Each one dilutes the map.
- **Nested repositories and submodules as a filing system.** They complicate every Git operation; keep repositories side by side.
- **Copying a project into another project** to reuse it. Extract a library or use a dependency instead.
- **Duplicated folders across machines** (`project`, `project (1)`, `project-copy`). Use Git remotes; delete stale copies after verifying content.
- **Leaving the inbox and scratch full.** They're queues, not storage; empty them.
- **Putting the workspace in a sync folder** with automatic conflict copies. Git and sync clients corrupt each other.
- **Keeping secrets in the workspace root** (`.env` at the top level). Secrets belong in a keyring or a project-level ignored file (see `config-and-secrets-placement`).

## Scaling & failure modes

- **Dozens of projects**: keep `projects/` flat within `public/` and `private/`, and use a catalog (a table in the README or a small JSON file) with owners, status, and purpose.
- **Active versus dormant**: move finished projects out of `projects/` into an archive (see `project-archive`), rather than piling them up.
- **Multiple machines**: mirror the same tree; keep a documented bootstrap script that clones each project from its remote.
- **Shared tooling**: git hooks, security scanners, and scripts live in `tools/`, and each project is configured to use them, so every repository gets the same checks.
- **Different privacy levels**: keep `business/` and `personal/` out of any tooling that uploads or indexes files to the network.
- **Large binaries**: keep data and media out of repositories (see `large-files-and-binary-assets`) and in a location backed up separately.

## Variants

- **Language-first**: `~/code/python/`, `~/code/rust/`, an older layout that groups by tool; poor when projects mix languages.
- **Domain-first**: `~/work/`, `~/oss/`, `~/personal/`; good when work and open source have different rules.
- **Visibility split** (this guide): `projects/public` and `projects/private`, with the rest of life alongside.
- **Go-style import path layout**: `~/src/<host>/<owner>/<repo>`; mirrors remotes and suits people who clone many third-party repositories.
- **Monorepo instead**: one repository with `apps/` and `packages/` for tightly coupled work.

## Adoption checklist

- [ ] The root README lists every top-level folder and its purpose, and `AGENTS.md` states the shared rules.
- [ ] Every project is its own repository, with no nested repositories or copies.
- [ ] Each project's visibility matches its folder (`public/` or `private/`).
- [ ] `inbox/` and `.scratch/` are empty between tasks.
- [ ] Nothing was deleted without checking its content and history; recoverable material is in `archive/`.
- [ ] Code is shared across machines only through Git remotes.

## Real-world projects using this

- **Go's original `GOPATH` layout** (`src/<host>/<owner>/<repo>`) is a well-known example of a workspace organized by remote.
- **`ghq`** (a repository manager) and **`myrepos`** manage many repositories side by side under a single root, and Google's **`repo`** tool does the same for large multi-repository projects such as Android.
- **Johnny.Decimal** and **PARA** (see `johnny-decimal`, `para`) are alternative organization systems for the non-code parts of a workspace.
- **Dotfiles managers** (see `dotfiles-chezmoi`) show the related idea of syncing configuration through Git rather than by copying.

## Migration & references

- **From a scattered home directory:** follow the worked example, moving repositories first (they're self-describing), then documents.
- **From a monorepo of unrelated projects:** split each project out with `git filter-repo --subdirectory-filter` into its own repository under `projects/`.
- **From a language-first layout:** move each project into `public/` or `private/`; the language is no longer a folder.
- **References:**
  - `principles/one-purpose-per-directory/` for keeping top-level folders honest.
  - `principles/monorepo-vs-polyrepo/` for why each project is a repository.
  - `principles/ai-agent-context-files/` for the shared rulebook.
  - `files/project-archive/` for moving finished projects out.
  - `files/git-worktrees-layout/` for parallel branches of one project.
