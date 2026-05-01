# Obsidian vault — scaffolding template

The Obsidian-specific scaffolding to layer underneath whatever
knowledge philosophy you choose (PARA, LYT, ACCESS, Zettelkasten,
evergreen, ...). See `../GUIDE.md` for the full reasoning.

## Layout

```
vault/
├── .obsidian/                  ← Obsidian config (selectively gitignored)
├── 00-meta/
│   ├── templates/
│   │   ├── daily.md
│   │   └── moc.md
│   └── snippets/
├── attachments/                ← all images, PDFs
├── daily/                      ← daily notes (YYYY-MM-DD.md)
└── notes/                      ← content (replace with your philosophy)
```

## Day-one configuration in Obsidian

After cloning this template, open it as a vault and set:

1. **Settings → Files & Links → Default location for new attachments**:
   `attachments/` (the "In the folder specified below" option).
2. **Settings → Core plugins → Daily notes → Enable**, then set:
   - **Date format**: `YYYY-MM-DD`
   - **New file location**: `daily/`
   - **Template file location**: `00-meta/templates/daily.md`
3. **Settings → Core plugins → Templates → Enable**, then set:
   - **Template folder location**: `00-meta/templates/`
4. *(Optional)* Install **Templater** community plugin for richer
   placeholders. Point its template folder at `00-meta/templates/`.
5. *(Optional)* Install **Dataview** if you want queries over your vault.

## Recommended `.gitignore` for the vault

```gitignore
# Obsidian — gitignore plugin caches and machine-local UI state,
# but keep theme + snippets + plugin settings.
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
.obsidian/plugins/*/data.json
# Optionally also ignore the entire plugins/ dir if you prefer to
# install plugins fresh on each machine:
#   .obsidian/plugins/

# Trash
.trash/
```

The split: theme, snippets, plugin presence, and plugin *configuration*
stay in git so any clone of the vault opens with the same look and the
same plugin set. UI state and per-plugin caches are machine-local.

## Snippets workflow

CSS snippets are the source of truth in `00-meta/snippets/<name>.css`,
copied into `.obsidian/snippets/<name>.css` for Obsidian to load.
Some users symlink the directory; either is fine. Don't *only* keep
snippets in `.obsidian/` — they'll be lost if you clean reinstall.

## What this template includes

- **`00-meta/templates/daily.md`** — daily-note template using
  `{{date}}` placeholders (with a Templater fallback comment).
- **`00-meta/templates/moc.md`** — Map of Content template with
  anchor notes, sub-topics, open questions, and related MOCs.
- **`.obsidian/.gitkeep`** — placeholder so the directory exists.
  Obsidian will populate this on first open.
- **`attachments/`**, **`daily/`**, **`notes/`** — empty content
  scaffolding.

## Pair this with one of

- `../../para/` — PARA folders inside `notes/`
- `../../lyt-linking-your-thinking/` — LYT MOCs
- `../../access-framework/` — ACCESS six-folder layout
- `../../zettelkasten-classic/` or `../../folgezettel/` — Zettelkasten
- `../../evergreen-notes/` — evergreen + atomic
