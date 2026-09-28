## TL;DR

**Docs as code** means documentation lives in the repository as plain text (Markdown), is reviewed in pull requests, is built by a static-site generator in CI, and is versioned with the software it describes. Organize the `docs/` tree by **what the reader is trying to do**, using the Diátaxis framework: **tutorials** (learn by doing), **how-to guides** (solve a specific problem), **reference** (look up facts), and **explanation** (understand why). Put one generator configuration (`mkdocs.yml`, or the equivalent for Docusaurus, Sphinx, or Hugo) at the repository root, store images beside the pages that use them, and add a **strict build** and **link check** to CI so broken links and missing pages fail the build. The site is generated output: never committed, always rebuilt.

## Principles & why

1. **Organize by reader intent, not by product structure.** A tutorial and a reference page answer different needs; mixing them satisfies neither. Diátaxis names the four needs and keeps them apart.
2. **Docs change with the code.** Documentation in the same repository can be updated in the same pull request as the behavior it describes, and reviewers can require it.
3. **The site is a build artifact.** Sources are Markdown; HTML is generated, gitignored, and rebuilt in CI (see `generated-vs-source-separation`).
4. **Failing builds keep docs honest.** A strict build (warnings as errors) and a link checker catch broken links, orphan pages, and invalid configuration before readers do.
5. **Assets live beside the pages.** Images and diagrams used by one page sit next to it, so moving or deleting a page moves its assets.
6. **One page, one purpose, one URL.** Stable paths and descriptive filenames mean links from issues, chats, and code comments keep working.

## When to use

- **Libraries, services, and tools** whose users need documentation that tracks releases.
- **Internal platforms and runbooks** owned by engineering teams.
- **Projects with several contributors**, where review and CI improve quality.
- **Any documentation that outgrew a single README** (see `readme-placement`).

## When NOT to use

- **Small projects where the README is enough.** A `docs/` site for a 200-line tool is upkeep without readers.
- **Documents that non-technical collaborators must edit** in a visual editor; a wiki or a document tool serves them better.
- **Private notes and journals.** See the `notes/` guides instead.
- **Marketing sites.** They have design and content workflows that differ from documentation.

## Tree diagram

```
project/
├── mkdocs.yml                        ← site config and navigation
├── requirements-docs.txt             ← pinned docs toolchain
├── docs/
│   ├── index.md                      ← landing page: who this is for, where to start
│   ├── tutorials/
│   │   └── getting-started.md        ← learning by doing, one guided path
│   ├── how-to/
│   │   ├── configure-logging.md      ← task-oriented, assumes basics
│   │   └── deploy-to-production.md
│   ├── reference/
│   │   ├── cli.md                    ← facts, complete, structured
│   │   └── configuration.md
│   ├── explanation/
│   │   └── architecture.md           ← concepts, trade-offs, history
│   ├── adr/                          ← decision records (see decision-records-adr)
│   └── assets/
│       └── architecture.svg
├── site/                             ← generated, gitignored
└── .github/workflows/docs.yml        ← build --strict, link check
```

## Naming rules

- **Files and directories** are lowercase kebab-case, matching the URL (`how-to/configure-logging.md` becomes `/how-to/configure-logging/`).
- **Page titles** name the task or concept; how-to titles start with a verb ("Configure logging"); tutorials say what you will build ("Build your first pipeline").
- **The four section directories** are named for their type: `tutorials/`, `how-to/`, `reference/`, `explanation/`.
- **Landing pages** are `index.md` in each section, with a short orientation and links.
- **Assets** are kebab-case, descriptive (`architecture-overview.svg`), and stored in `docs/assets/` or beside the page in a folder of the same name.
- **Never rename published pages** without a redirect; URLs are part of the interface.

## Worked example

A project has a 900-line README covering install, usage, configuration, API, and design rationale; readers can't find anything and it's often out of date.

1. Sort every paragraph into one of four piles: learn (tutorial), do (how-to), look up (reference), understand (explanation).
2. Create `docs/` with `index.md` and the four directories, and move content into pages, one purpose per page.
3. Cut the README down to summary, install, a five-line example, and a link to the docs.
4. Add `mkdocs.yml` with `site_name`, `nav`, and a theme; add `requirements-docs.txt` pinning `mkdocs` and the theme.
5. Build locally: `mkdocs serve`, and fix what looks wrong.
6. Add CI: `mkdocs build --strict` (fails on warnings such as broken internal links), plus an external link checker such as `lychee` run on the source.
7. Add a pull request template line: "Docs updated or not needed."
8. Publish the built site from CI (for example GitHub Pages), and add the URL to the repository description and README.

Each reader lands on a page matched to what they came to do, and CI stops broken links and orphan pages.

## Anti-patterns

- **Organizing by code structure** (`docs/module-a/`, `docs/module-b/`). Readers don't think in modules; they think in tasks.
- **Tutorials that explain everything.** A tutorial gets the learner to a result; explanation belongs elsewhere with a link.
- **Reference written as prose** without structure. Reference should be scannable and complete.
- **Committing the built site** to the source branch. It creates noisy diffs and stale copies.
- **Screenshots of text and configuration.** They can't be searched, copied, or diffed; use text and code blocks.
- **Unpinned docs toolchain.** A theme update can break the build the day before a release.
- **Docs in a separate repository** that nobody updates with code changes, unless docs and code have different owners by design.

## Scaling & failure modes

- **Versioned docs**: when releases diverge, publish per-version documentation (mike for MkDocs, Docusaurus versioning, or branches); avoid copying the tree into `docs/v1/`.
- **Navigation size**: past about 50 pages, the sidebar needs grouping, search tuning, and section landing pages; make sure each section has an `index.md`.
- **Multiple products or languages**: use one docs tree per product, and translation tooling rather than copies of the pages.
- **Freshness**: add "last reviewed" metadata or a quarterly review; assign owners to sections in `CODEOWNERS`.
- **API reference**: generate from source (OpenAPI, docstrings, `cargo doc`) into `reference/`, and don't hand-maintain it.
- **Build time**: cache dependencies in CI, and build only when `docs/**` or code that feeds the reference changes.

## Variants

- **MkDocs (Material)**: Markdown, simple config, large plugin ecosystem; a common Python-project choice.
- **Docusaurus**: React-based, strong versioning, good for JavaScript ecosystems.
- **Sphinx**: reStructuredText or MyST Markdown, rich cross-referencing and autodoc; standard in scientific Python.
- **Hugo, Astro Starlight, VitePress**: fast static generators with docs themes.
- **mdBook**: the Rust ecosystem's book-style docs.
- **Docs inside the README plus `docs/` folder with no site**: enough for small projects; browse on the forge.

## Adoption checklist

- [ ] `docs/` has the four Diátaxis sections, each page with one purpose.
- [ ] The README is short and links to the docs.
- [ ] CI runs a strict build and a link check on every pull request.
- [ ] The built site is gitignored and published from CI.
- [ ] Toolchain versions are pinned.
- [ ] Renamed or moved pages have redirects.

## Real-world projects using this

- **Diátaxis** (diataxis.fr, by Daniele Procida) defines the tutorial / how-to / reference / explanation framework.
- **Read the Docs, Django, and Python documentation** follow versioned, structured docs; Django's docs are a well-known example of the four kinds in practice.
- **Write the Docs** (writethedocs.org) publishes "docs as code" guidance and community resources.
- **Kubernetes, Stripe, and GitLab** publish documentation sources or handbooks in public repositories; browse them for large-scale structure.
- **MkDocs Material, Docusaurus, and Sphinx** documentation sites are themselves built with their own tools.

## Migration & references

- **From a giant README:** split by reader intent (see the worked example), keep the README as an entry point.
- **From a wiki:** export pages to Markdown, sort into the four sections, fix links, and archive the wiki with a pointer.
- **Between generators:** keep Markdown content and front matter as portable as possible; migrate configuration and navigation last.
- **References:**
  - `principles/readme-placement/` for README versus docs.
  - `principles/indexes-and-mocs/` for section landing pages.
  - `principles/decision-records-adr/` for the `docs/adr/` section.
  - `code/github-repository-meta/` for the CI and repository metadata around the docs.
