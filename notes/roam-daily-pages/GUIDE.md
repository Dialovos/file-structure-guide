## TL;DR

Roam Research's organizing model is radically simple in shape but deep in implication: **every day is a page** (`2026-04-30.md`), and **topical pages emerge from inline `[[bracket links]]`** typed inside daily-page bullets. There are no folders. The filesystem is essentially flat — a directory of pages, where most pages happen to have ISO-date filenames and a few have human-readable titles like `deep work.md`. Structure isn't imposed up front; it accretes from the act of writing. Two further ideas make Roam different from a flat folder of markdown: (1) **block references** (`((block-uuid))`) make any individual bullet citable and live-transcludable, and (2) **bidirectional backlinks** are first-class — opening a topical page shows every block elsewhere that linked to it. Roam itself is cloud-only (you can't run it on your local files), so this guide is primarily about the *conventions* you'd find in an exported Roam graph and what to mirror if you want a Roam-style workflow in tools like Logseq or a plain-markdown setup. The trade is: extreme simplicity in directory shape vs. heavy reliance on the runtime to surface structure (links, backlinks, queries). When you don't have the runtime, the directory looks underwhelming.

## Principles & why

Three Roam design choices shape what a Roam graph (or its export) looks like.

1. **Every day is a page.** Roam opens to today's daily page; that's the canonical entry point for capture. The filename is the ISO date (`2026-04-30.md`), and the page title in the UI is rendered as "April 30th, 2026". This collapses *journaling* and *thinking* into the same surface — you don't decide whether something is "a thought" or "a journal entry"; both go on today's page.
2. **Topical pages auto-create from `[[bracket links]]`.** Type `[[deep work]]` anywhere and Roam either links to the existing `deep work` page or creates it on the spot. The implication for filesystem shape: topical pages emerge spontaneously and live next to dailies in the same flat directory. There is no "topics folder" — Roam's graph is mostly flat and the structure lives in the link graph, not in directories.
3. **Block references make bullets citable.** Every bullet (block) has a UUID. You can transclude a block from yesterday's daily into today's daily, into a topical page, into anywhere — and edits propagate. The unit of thought drops from "page" to "bullet". This is why Roam-style notes look like deeply-nested outlines rather than paragraph prose: outliners give you addressable atoms.

The structural consequence: Roam graphs in export look like a flat folder of mostly date-named markdown files, plus a smattering of topically-named markdown files, plus heavy use of `[[brackets]]` and `((block refs))` inline. Without Roam's runtime, the markdown is readable but uninspiring — the value lives in queries, backlinks, and the graph view.

A frequent misconception: Roam isn't *anti*-organization. It's *post*-organization: the structure exists, but it lives in the link graph and surfaces through tools (filtered references, queries, daily review), not in directory hierarchy.

## When to use

- **You think in branching outlines.** Bulleted, indented, nested-as-deep-as-needed thinking is your default mode.
- **Bidirectional links are your primary structuring tool.** You want to write `[[X]]` and have a topic page exist with all its references attached, without explicit filing.
- **Block transclusion matters.** Quoting a single bullet from elsewhere — and having that quote update if the source updates — is part of how you write.
- **Daily-page-first capture suits you.** You're happy starting at "today" and letting topics emerge from there, rather than starting at a topic.
- **You're willing to live in the cloud.** Roam itself is hosted; you accept that constraint for the runtime experience.

## When NOT to use

- **You want offline-first / local-first ownership.** Roam is cloud-only. **Compare Logseq** — explicitly a local-first Roam-alike, same daily-page model on your filesystem. If local ownership is non-negotiable, use Logseq instead.
- **You want long-form prose.** Outliners constrain paragraphs. If your notes are essays, Roam will fight you.
- **You want strict folder hierarchy.** Roam doesn't do folders. If you want ACCESS / Johnny Decimal / PARA discipline, Roam won't enforce them.
- **Cost sensitivity.** Roam is one of the more expensive notes products (no free tier beyond a trial in most pricing eras). Logseq is free; Obsidian is free for personal use.
- **Privacy-sensitive content.** Cloud-hosted, third-party. If your notes contain client data with strict residency requirements, Roam may be excluded by policy.

## Tree diagram

```
graph/
├── 2026-04-30.md            ← daily page; mostly outlined bullets
├── 2026-05-01.md
├── deep work.md             ← topical page; auto-created on first link
└── attention.md
```

The filesystem stays flat — Roam doesn't introduce subfolders. All structure lives in the link graph (bidirectional links and block references) and surfaces at runtime through queries and backlinks.

## Naming rules

- **Daily pages**: ISO date as filename — `2026-04-30.md`. The Roam UI renders this as "April 30th, 2026" with ordinal suffixes; the on-disk form is the ISO date in markdown export.
- **Topical pages**: human-readable title with spaces preserved — `deep work.md`. Roam treats `[[Deep Work]]`, `[[deep work]]`, and `[[deep_work]]` as different titles unless you alias them, so be deliberate about capitalization the first time you create a page.
- **Block references**: not a filename concern; appear inline as `((some-uuid))`. The UUID is generated by Roam. In an export, references are usually expanded to embedded text rather than preserving the UUID syntax (depends on export options).
- **Tags vs page-links**: Roam's `#tag` and `[[link]]` are equivalent (`#deep-work` ≡ `[[deep-work]]`). The convention is hashtag for ad-hoc taxonomies, brackets for navigation-worthy topics. Both end up creating or linking to the same page.
- **Aliases**: pages can have multiple titles via aliases in the page properties block. The on-disk filename is the canonical title; aliases are metadata.

## Anti-patterns

- **Replicating folder hierarchy in titles.** Writing `[[productivity/deep work]]` to mimic folders works but loses the wiki-link affordance — Roam doesn't treat the `/` as a hierarchy. Use either flat titles or pure tagging; don't fake folders.
- **Manual "MOC-of-MOCs".** Heavy index-page maintenance defeats Roam's emergent-structure model. The unread/unfiled-references panel on every page is the dynamic MOC.
- **Long paragraphs inside a single block.** Roam's outliner shape is non-negotiable; a 500-word block is technically possible but defeats block-reference granularity. Break paragraphs into bullets.
- **Forking pages by capitalization.** `[[Deep Work]]` and `[[deep work]]` are different pages by default. The fix is either be consistent at first reference or use page aliases. Don't accumulate near-duplicates.
- **Treating Roam exports as the source of truth.** Roam's value is the runtime. Markdown export is for archival / portability; round-tripping back into Roam can be lossy (especially for queries, embeds, attribute pairs).
- **Using `((block-ref))` for what should be a permanent reference.** A block ref tracks the source; if the source is deleted, the ref breaks. For things you want to *quote permanently*, copy the text or convert the ref to text.

## Variants

- **Roam-classic** (this guide). Daily-page-first, flat directory, links and block refs as the primary structuring tools.
- **Roam-with-strict-templates.** A daily template enforces a fixed outline ("Did / Doing / Read / Linked"), giving emergent structure a scaffold. Popularized by Roam-power-user communities.
- **Roam-with-MOC-pages.** Hand-curated index pages (e.g., `[[MOC: Productivity]]`) sit alongside dailies, providing reading paths into the graph. Useful when sharing a graph or onboarding.
- **Logseq** — local-first Roam-alike. Same daily-page model, same block refs, your data on your filesystem. See `notes/logseq-outliner/`.
- **Athens / RemNote / Capacities.** Other Roam-influenced products with their own takes on the model.

## Real-world projects using this

- **Roam Research** (roamresearch.com) — the source-of-truth product. The product website, blog, and onboarding define the canonical conventions.
- **Conor White-Sullivan's writeups** (CEO/co-founder) — Twitter threads and the early Roam blog posts capture the "every day is a page" philosophy in his own words.
- **Roam Brain podcast and community** — episodes with power users; the Roam community Slack/Discord and the public r/RoamResearch subreddit document working graphs.
- **Nat Eliason's "Effortless Output with Roam"** — a paid course that became a widely-cited reference for Roam workflow conventions.
- **Public Roam graphs** — several practitioners have published their working graphs (sometimes via the Roam-Sharing feature, sometimes as plain-text exports on GitHub). Search "Roam graph site:github.com" for examples.

## Migration & references

- **From Roam to Logseq**: Roam → JSON export → Logseq import (`Settings → Import → Roam EDN/JSON`). Pages and block refs survive; some plugins / queries don't. The daily-page model maps directly.
- **From Roam to Obsidian**: Roam → markdown export → drop into an Obsidian vault. Works at the page level. Block references degrade to plain text quotes; queries don't survive.
- **From Roam to plain markdown**: same export path. The directory becomes a flat folder of markdown files. Backlinks and queries are gone unless you bring your own indexer.
- **Adopting the Roam style without Roam**: Logseq is the closest match. Obsidian + Daily Notes + Strict Folder Discipline gives a similar feel with more file-system freedom.
- **References**:
  - `roamresearch.com` — official site and docs.
  - `nateliason.com/effortless` — Effortless Output with Roam.
  - Sibling guides: `notes/logseq-outliner/` (the local-first equivalent), `notes/daily-weekly-notes/` (the daily-page concept generally), `notes/atomic-notes/` (block-as-atom maps to Roam's block model), `notes/topic-vs-date-organization/` (Roam is the canonical "intentional mix").
