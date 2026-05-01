# TiddlyWiki — Node.js mode template

A working skeleton of a TiddlyWiki run in **Node.js mode**: per-tiddler
`.tid` files in `tiddlers/`, a `tiddlywiki.info` config at the root,
and a build target that produces a single-file `output/index.html`.
See `../GUIDE.md` for the full reasoning.

## Layout

```
wiki/
├── tiddlers/
│   ├── HelloThere.tid       ← welcome tiddler
│   ├── 2026-04-30.tid       ← sample journal tiddler
│   └── $__StoryList.tid     ← system-tiddler override (encoded $:/StoryList)
├── tiddlywiki.info          ← wiki config (JSON)
└── output/                  ← build artifacts (gitignored)
    └── index.html           ← produced by `tiddlywiki . --build index`
```

## The two storage modes

TiddlyWiki has two physical layouts. This template demonstrates the
**Node.js mode** because it composes well with git, code review, and
many-tiddler workflows.

- **Single-file mode**: one `wiki.html` containing the engine, styles,
  and every tiddler embedded as JSON. You open the HTML in a browser
  and use a "saver" to write changes back to disk. Maximally portable;
  worst for git because every change rewrites a multi-MB blob.
- **Node.js mode** (this template): per-tiddler `.tid` files at rest,
  compiled to a single HTML on demand. Best for version control and
  any workflow where you want diffs to be readable.

## The `.tid` file format

Every tiddler file has two parts separated by a blank line:

```
title: HelloThere
tags: Welcome Index
created: 20260430120000000
modified: 20260430120000000

! Heading
Body content in WikiText
```

The header is line-oriented `key: value` pairs. The body is WikiText
(or Markdown if the markdown plugin is enabled). Don't omit the blank
line between header and body — the parser uses it as the separator.

## System tiddler filename encoding

TiddlyWiki's system tiddlers have titles like `$:/StoryList`. On disk,
the prohibited filename character `/` is encoded to `_`, and the
leading `$:/` becomes `$__`. So `$:/StoryList` lives at
`tiddlers/$__StoryList.tid`. Don't fight this — TiddlyWiki round-trips
between the title and the filename automatically.

## Day-one workflow

1. Install TiddlyWiki: `npm install -g tiddlywiki`
2. From this template's directory, run `tiddlywiki . --listen`.
3. Open `http://localhost:8080` in a browser — you'll see the wiki
   with the sample tiddlers loaded.
4. Edit tiddlers in the browser; saves go back to `tiddlers/` as
   per-tiddler `.tid` files.
5. To produce a portable single-file build:
   `tiddlywiki . --build index` writes `output/index.html`.

## What this template includes

- **`tiddlers/HelloThere.tid`** — a sample welcome tiddler with a
  WikiText quick reference inline.
- **`tiddlers/2026-04-30.tid`** — a sample journal tiddler showing
  the `Journal` tag convention.
- **`tiddlywiki.info`** — minimal config: `tiddlyweb`, `filesystem`,
  and `markdown` plugins; `vanilla` + `snowwhite` themes; an `index`
  build target that produces `output/index.html`.
- **`README.md`** — this file.

You'll typically also want a `.gitignore` containing `output/` so the
build artifact doesn't bloat history.

## Pair this with

- `../../atomic-notes/` — the tiddler is the canonical atomic note.
- `../../zettelkasten-classic/` — TiddlyWiki ships an official
  Zettelkasten edition.
- `../../daily-weekly-notes/` — the journal-tiddler convention.

## Sync recommendations

- **Git** is the cleanest sync for Node.js mode — `.tid` files are
  text and diff well.
- For single-file mode, **TiddlyHost** (managed cloud) handles the
  save endpoint without browser-saver gymnastics.
- Avoid mixing modes mid-stream: do not build to `output/index.html`,
  edit it in a browser, then expect changes to flow back into
  `tiddlers/` — they don't, and you'll desync.
