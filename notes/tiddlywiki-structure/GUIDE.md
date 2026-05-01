## TL;DR

TiddlyWiki is a **non-linear personal web notebook** with two physical storage layouts depending on which mode you run. In **single-file mode** (the classic one), the entire wiki is one self-contained `wiki.html` file that ships HTML, CSS, JavaScript, and every tiddler embedded inline — that one file is the whole product, opened directly in a browser. In **Node.js mode**, each tiddler becomes a separate `.tid` file in `tiddlers/`, with a small text-based metadata header (`title:`, `tags:`, `created:`, `modified:`) followed by a blank line and then the body; the Node.js server compiles them on demand into `output/index.html`. The directory shape therefore differs sharply from any markdown-based system: the unit is a *tiddler* (small, atomic, addressable note), and the on-disk representation is either an embedded blob or per-tiddler `.tid` text files. TiddlyWiki shines when you need a portable wiki that runs anywhere a browser does (USB stick, email attachment, offline laptop), and when transclusion / macros / templating is part of how you think. It is a poor fit when you want plain markdown with broad ecosystem tooling, or when you need real-time multi-device sync.

## Principles & why

Three TiddlyWiki design choices drive the directory shape.

1. **The tiddler is the atom.** A tiddler is a small named unit (often a paragraph or two), with a title that doubles as its unique ID and any number of tags. Tiddlers transclude, link, and template-render each other. The smallest meaningful operation in TiddlyWiki is *create a tiddler*, not *open a page*. This is why per-tiddler files in Node.js mode are so granular — every captured idea is a separate `.tid` file.
2. **Self-contained portability.** TiddlyWiki was originally designed so the whole wiki could live in a single HTML file you carry on a USB stick, email to yourself, or save to Dropbox. The single-file mode bakes the JavaScript engine, the styles, and all your content into one file. The `.html` is both the *application* and the *database*. This is why directory layout barely exists in single-file mode — there is just `wiki.html`.
3. **System tiddlers and shadow tiddlers.** TiddlyWiki ships hundreds of internal tiddlers (`$:/core/...`, `$:/themes/...`, `$:/plugins/...`) that define the UI, the macros, the translations, the templates. In Node.js mode these are loaded from plugin directories rather than living in `tiddlers/`. User-edited overrides land in `tiddlers/` with the `$__` filename prefix (e.g., `$__StoryList.tid`) — the on-disk encoding of the system-tiddler title `$:/StoryList`.

The structural consequence: if you adopt Node.js mode, you live with a flat or very lightly organized `tiddlers/` directory containing many small files. The TiddlyWiki engine indexes them by *title and tags*, not by directory; you can group tiddlers into subfolders for human convenience without changing addressing. The `tiddlywiki.info` file at the wiki root declares the wiki name, the plugins to include, and the theme — that file is what binds a `tiddlers/` folder into a buildable wiki.

## When to use

- **Self-contained portable wiki.** USB-stick reference manual, offline-first field notes, a "wiki I email to myself" — TiddlyWiki's single-file form is unmatched for this.
- **Strong macro / transclusion / templating needs.** TiddlyWiki's WikiText macros and filter expressions let you compose pages from many tiddlers, build dashboards, and template repeatable layouts. If you want a notes system that doubles as a small content engine, this is the one.
- **You like the Node.js mode workflow.** Per-tiddler `.tid` files in version control, server-side build, output to a static HTML deliverable. It composes well with git.
- **You want plugin-driven extensibility.** TiddlyWiki has a mature plugin ecosystem (TiddlyMap, Projectify, Streams, Bob multi-user) that swaps the UI behavior dramatically without leaving the platform.
- **Long-term durability matters.** TiddlyWiki has been actively maintained since 2004; the single-file format is intentionally future-proof (an HTML file with embedded JSON of tiddlers — readable by any browser indefinitely).

## When NOT to use

- **You want plain markdown files.** TiddlyWiki tiddlers use WikiText (its own markup) by default; you can switch to Markdown via a plugin, but the surrounding tooling (macros, templates, filters) still expects WikiText conventions in places. If markdown ecosystem compatibility is the goal, choose Obsidian/Logseq.
- **You need real-time multi-device sync.** TiddlyWiki's sync story (TiddlySpot, TiddlyHost, Bob, Dropbox via savers) is harder than Obsidian Sync or Logseq Sync. Concurrent edits across devices are not the strength here.
- **You want a familiar block-editor or outliner UI.** TiddlyWiki's UI is its own; users from Notion / Roam / Logseq find it idiosyncratic.
- **Team collaboration.** The single-user assumption runs deep; multi-user requires Bob/TiddlyHost/etc., and conflict handling is limited.
- **Mobile-first usage.** Mobile editors for TiddlyWiki exist but lag dedicated note-app mobile experiences.

## Tree diagram

```
wiki/
├── tiddlers/                       ← per-tiddler files (Node.js mode)
│   ├── HelloThere.tid
│   ├── 2026-04-30.tid
│   └── $__StoryList.tid
├── tiddlywiki.info                 ← config
└── output/
    └── index.html                  ← built single-file wiki
```

Single-file mode collapses to a single `wiki.html` containing everything. Node.js mode is the layout shown — `tiddlers/` is the source of truth, `output/` is build output and is typically gitignored.

## Naming rules

- **Tiddler files** (`.tid`): the on-disk filename matches the tiddler title with characters TiddlyWiki encodes (`/` → `_`, `:` → `_`, etc.). A tiddler titled `HelloThere` becomes `HelloThere.tid`. A system tiddler titled `$:/StoryList` becomes `$__StoryList.tid` — the `$:/` prefix encodes to `$__`.
- **Journal tiddlers**: there is no enforced convention, but the common pattern is ISO date as title (`2026-04-30.tid`). The default `NewJournal` macro uses this.
- **Tags**: tiddlers carry tags in the metadata header (`tags: Journal Daily`). Tag names with spaces wrap in `[[brackets]]`. Tags drive navigation; they are not paths.
- **`tiddlywiki.info`**: must sit at the wiki root. JSON file declaring `description`, `plugins`, `themes`, `languages`, and `build` targets. Don't rename — the CLI looks for this exact filename.
- **Plugin / theme / language directories**: when used, plugins, themes, and languages live in well-known directories (`plugins/`, `themes/`, `languages/`) at the wiki root or are referenced from a system path. The convention is `category/author/plugin-name/`.
- **`output/`**: build artifact directory. Conventional but configurable in `tiddlywiki.info`'s `build` section. Always gitignore.

## Anti-patterns

- **Editing a single-file wiki while it's open in two tabs.** The "save" operation rewrites the whole HTML; two tabs racing each other will lose tiddlers silently. Always edit in one tab.
- **Treating `.tid` files as pure markdown.** They're TiddlyWiki's own format with a metadata header followed by WikiText body. Stripping the header or assuming Markdown rendering breaks tiddler import.
- **Committing `output/` to git.** `output/index.html` is generated and large (megabytes); committing it bloats history. Always gitignore.
- **Renaming `tiddlywiki.info`.** The CLI hardcodes the filename. Rename and `tiddlywiki .` stops working.
- **Editing system tiddlers in place without overrides.** Modify `$:/themes/...` directly and the next plugin update overwrites your changes. Use shadow-tiddler overrides (a `tiddlers/$__themes_...tid` file) so your edits live in your wiki, not in the plugin.
- **Mixing Node.js mode and single-file editing.** If you build `output/index.html`, edit it in a browser, and save — your in-browser edits go to the saved HTML, not back into `tiddlers/`. The two halves desync. Pick a workflow.

## Variants

- **Single-file (classic).** One `wiki.html` with everything embedded. Simplest, most portable, hardest to version-control granularly (one big file diff).
- **Node.js per-tiddler** (this guide). `tiddlers/*.tid` plus `tiddlywiki.info`; build to `output/index.html`. Best for git, best for many-author workflows.
- **TiddlyDesktop.** A small Electron-based wrapper that lets a single-file TiddlyWiki save to disk reliably without browser-saver gymnastics. Same single-file storage shape.
- **TiddlyHost.** Managed-cloud TiddlyWiki — they host your single-file wiki and provide a save endpoint. Storage is still a single HTML file from your perspective.
- **TiddlyWiki Classic.** The pre-5.x version (TiddlyWikiClassic). Mostly historical; not recommended for new wikis.
- **Bob (multi-user).** A Node.js server that exposes a TiddlyWiki to many users with conflict handling. Storage is per-tiddler files like Node.js mode plus a Bob-specific layer.

## Real-world projects using this

- **TiddlyWiki.com** (tiddlywiki.com) — the project's own site is itself a TiddlyWiki, edited in TiddlyWiki, served as TiddlyWiki. Best reference for the canonical structure.
- **Jeremy Ruston's project lead repository** (github.com/Jermolene/TiddlyWiki5) — the official source code; the README and `editions/` directory show canonical Node.js mode layouts.
- **TiddlyHost** (tiddlyhost.com) — managed-cloud TiddlyWiki by Simon Baird; demonstrates the single-file deploy model end-to-end.
- **Grok TiddlyWiki** (groktiddlywiki.com) — Soren Bjornstad's working tutorial wiki; itself an example of a real, published TiddlyWiki.
- **TiddlyMap** and **Projectify** plugins (github.com) — large open-source plugins that demonstrate the directory shape for a TiddlyWiki plugin distributed as a plugin folder.

## Migration & references

- **From Obsidian / Logseq Markdown**: write a small importer that converts each `.md` file into a `.tid` file with a metadata header. The body usually transfers as-is if you enable the Markdown plugin in TiddlyWiki; otherwise you'll convert link syntax (`[[link]]` is the same) and headings (TiddlyWiki uses `! Heading`, not `# Heading`, in WikiText).
- **From Roam / Workflowy outlines**: these don't map cleanly — TiddlyWiki has lists but isn't outliner-first. Plan a flatten step where each top-level outline node becomes a tiddler.
- **From single-file to Node.js mode**: `tiddlywiki --load wiki.html --savewikifolder /path/to/new/wiki` extracts every embedded tiddler into a `tiddlers/` folder and writes a starter `tiddlywiki.info`.
- **From Node.js mode to single-file**: `tiddlywiki /path/to/wiki --build index` uses the `index` build target in `tiddlywiki.info` to produce a single-file `output/index.html`.
- **References**:
  - `tiddlywiki.com` — official docs, especially the WikiText reference and the Node.js mode setup pages.
  - `github.com/Jermolene/TiddlyWiki5` — source, issues, and the `editions/` directory.
  - `groktiddlywiki.com` — Soren Bjornstad's full-length introduction.
  - Sibling guides: `notes/atomic-notes/` (the tiddler is the canonical atomic note); `notes/zettelkasten-classic/` (TiddlyWiki ships a zettelkasten edition); `notes/daily-weekly-notes/` (journal tiddlers map directly).
