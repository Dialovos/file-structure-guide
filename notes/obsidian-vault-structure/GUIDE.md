## TL;DR

Obsidian-specific conventions sit *underneath* whatever knowledge philosophy you pick (PARA, LYT, ACCESS, Zettelkasten, evergreen). The philosophies dictate how your *content* folders look; this guide dictates the **Obsidian-specific scaffolding** that should accompany them: a `.obsidian/` config dir (partially gitignored), a `00-meta/` folder for templates and snippets, an `attachments/` folder configured in Obsidian's settings, and a `daily/` folder for daily notes. The numeric prefix `00-` keeps the meta folder above content folders alphabetically. Critical Obsidian-specific decisions: (1) where attachments go (recommended: a single `attachments/` folder), (2) what to gitignore inside `.obsidian/` (workspace.json and plugin caches yes; theme/snippets no), (3) where templates live (recommended: `00-meta/templates/`), and (4) how to align with whatever organizational scheme you've chosen for content. This guide answers all four.

## Principles & why

Obsidian is a *Markdown editor* layered over a folder of `.md` files. It adds three things on top of plain folders: a `.obsidian/` config dir, plugin support, and a graph database of `[[wikilinks]]`. None of the three changes the on-disk structure of your *content*, but each adds files you have to decide about.

1. **`.obsidian/` is the per-vault settings folder.** It contains `workspace.json` (UI state — pane layout, last-open tab), `appearance.json` (theme), `community-plugins.json` (which plugins are installed), per-plugin settings, `themes/`, `snippets/`, and plugin caches. The split: keep theme settings, snippets, and plugin *settings* in git (you want them on every machine); gitignore plugin *caches* and `workspace.json` (machine-specific UI state churns constantly).
2. **Attachments need a single home.** Obsidian's default is "next to the note" which scatters images everywhere and makes vault portability painful. Configure `Settings → Files & Links → Default location for new attachments` to a single `attachments/` folder. Per-note subfolders (`attachments/<note-name>/`) is a valid variant if you have many image-heavy notes.
3. **Templates and snippets are vault assets, not user assets.** Each Obsidian vault has its own templates (daily-note template, MOC template, project template). Put them in `00-meta/templates/`. Configure the Templates core plugin (or Templater) to point at that folder. CSS snippets go in `00-meta/snippets/` symlinked or copied into `.obsidian/snippets/` — keep the source of truth in `00-meta/` so they're version-controlled with the rest of the vault.
4. **The numeric prefix `00-` is intentional.** It sorts above any letter-prefixed folder. Combined with PARA's `1-projects/`–`4-archive/` (or any other content scheme), `00-meta/` is always at the top of the file list — meta should be visually distinct from content.

## When to use

- **Any Obsidian vault.** If you use Obsidian, you need this scaffolding regardless of philosophy.
- **First-time vault setup** — start with the structure here, add a content philosophy on top.
- **Migrating a flat vault** — when you've accumulated 500 unsorted notes and want to clean up: introduce `00-meta/`, `attachments/`, `daily/` first; sort content second.
- **Multi-machine vaults synced via git** — the gitignore choices in this guide are designed for git-synced vaults (Obsidian Sync handles this differently and obviates some of it).
- **Vaults shared across team members** — shared vaults need shared templates/snippets and personal-machine state ignored. Same gitignore split applies.

## When NOT to use

- N/A in the literal sense — if you use Obsidian, you need this scaffolding. The "when not" is just: **don't apply this if you're not using Obsidian.** Logseq, Bear, Notion, plain folders, etc., have their own conventions.
- **Don't use `00-meta/` if your philosophy already specifies a meta location.** Some PARA implementations put templates in `0-inbox/templates/`; some LYT setups use `_meta/`. Pick one; don't double-up.
- **Don't gitignore `.obsidian/` entirely.** Some guides recommend this for simplicity, but you lose theme + snippet + plugin settings — meaning every machine has to be reconfigured. The selective gitignore in this guide is the better default.

## Tree diagram

```
vault/
├── .obsidian/                  ← Obsidian config (selectively gitignored)
│   ├── workspace.json          ← gitignored: UI state churns constantly
│   ├── plugins/                ← gitignored: plugin caches
│   ├── themes/                 ← keep in git: vault theme of record
│   └── snippets/               ← keep in git: CSS customizations
├── 00-meta/                    ← templates, snippets, vault meta
│   ├── templates/
│   │   ├── daily.md            ← `{{date}}` Templater placeholders
│   │   └── moc.md              ← Map of Content template
│   └── snippets/               ← source of truth for CSS snippets
├── attachments/                ← all images, PDFs (configured in Settings)
├── daily/                      ← daily notes — `YYYY-MM-DD.md`
└── notes/                      ← content layer — pick a philosophy
```

The content layer (`notes/`) is intentionally placeholder — replace it with whatever organization you adopt: PARA's `1-projects/`–`4-archive/`, LYT's `+ Maps/`, ACCESS's six folders, etc. The Obsidian scaffolding (`00-meta/`, `attachments/`, `daily/`, `.obsidian/`) sits alongside.

## Naming rules

- **`.obsidian/`** — leave the directory name as Obsidian created it. Don't rename or move.
- **`00-meta/`** — kebab-case. The `00-` prefix sorts it above content. If you prefer `_meta/`, that also sorts first in most filesystems but breaks under some sort orders; `00-` is more reliable.
- **`00-meta/templates/`** — one file per template, kebab-case: `daily.md`, `moc.md`, `project.md`, `meeting.md`. Templates use `{{date}}`, `{{title}}`, `{{time}}` placeholders if using core Templates plugin, or `<% tp.date.now() %>` if using Templater.
- **`attachments/`** — flat by default. Filenames as Obsidian generates them: `Pasted image 20260430120000.png` is fine; rename only if you'll reuse the image. For per-note variant: `attachments/<note-slug>/`.
- **`daily/`** — `daily/YYYY-MM-DD.md` (ISO 8601). Configure Daily Notes core plugin: `Settings → Core plugins → Daily notes → Date format: YYYY-MM-DD`, `Folder: daily/`, `Template: 00-meta/templates/daily.md`.
- **Snippets** — `00-meta/snippets/<descriptor>.css`. Once edited, copy to `.obsidian/snippets/<descriptor>.css` (Obsidian only reads from there). A small post-pull script can sync; some users symlink the directory.

## Anti-patterns

- **Gitignoring all of `.obsidian/`.** You lose theme + snippet + plugin settings. Every fresh clone needs reconfiguration. Use the selective gitignore in this guide.
- **Committing `workspace.json`.** Causes constant merge conflicts as different machines write different UI state. Always gitignore.
- **Default attachment location ("Same folder as current file").** Scatters images across every folder. Almost always wrong; configure a single `attachments/` folder on day one.
- **Mixing meta and content in one tree.** Putting your daily-note template inside `daily/` (next to actual daily notes) means your template file gets picked up in template-name searches. Keep templates in `00-meta/templates/` only.
- **Renaming `.obsidian/`.** Obsidian will recreate it. You'll have two config dirs, neither working as expected.
- **Storing snippets only in `.obsidian/snippets/` without a copy in `00-meta/`.** If `.obsidian/` is gitignored you lose your snippets on a fresh clone. Source of truth lives in `00-meta/snippets/`.

## Variants

- **Flat-attachments** (this guide) — single `attachments/` folder. Simple; fine for most.
- **Per-note attachments** — `attachments/<note-slug>/<image>`. Better for image-heavy notes; configure Obsidian: `Default location for new attachments → In subfolder under current folder` and use Templater to set the subfolder name.
- **Mixed content + meta (no `00-meta/`)** — keep templates in PARA's `1-projects/_template/` or similar. Less separation; smaller folder count.
- **Underscore-prefixed meta** — `_meta/` instead of `00-meta/`. Sorts first on most filesystems; visually distinct. Equivalent in practice.
- **Separate snippets repo** — keep CSS snippets in a separate dotfiles repo and symlink `.obsidian/snippets/` to it. Best if you reuse snippets across multiple vaults.

## Real-world projects using this

- **Obsidian official documentation** (help.obsidian.md) — the source-of-truth for config dir contents, daily notes, templates, attachment settings.
- **Obsidian Hub** (publish.obsidian.md/hub) — community-maintained directory of vaults, plugins, and template patterns.
- **Obsidian forum** (forum.obsidian.md) — many vault-structure threads, especially in #share-showcase and #knowledge-management.
- **Public starter vaults on GitHub** — search "Obsidian starter vault" or "Obsidian template vault"; dozens exist with varying conventions, including Nick Milo's LYT Kit and various PARA starter kits.
- **Linking Your Thinking (LYT) Kit** by Nick Milo — well-known public Obsidian starter vault built around LYT philosophy; demonstrates many of the conventions in this guide.

## Migration & references

- **From a flat vault** (no structure): create `00-meta/templates/`, `00-meta/snippets/`, `attachments/`, `daily/`. In Obsidian Settings → Files & Links, set default attachment location to `attachments/`. Move existing images into `attachments/` (Obsidian updates inline image links automatically). Move daily-style notes to `daily/`. Leave content notes wherever they are until you adopt a philosophy.
- **From a non-Obsidian Markdown vault**: Obsidian creates `.obsidian/` automatically on first open. Add the gitignore entries from this guide. Configure Daily Notes and Templates plugins. Then layer your content philosophy.
- **Adding to an existing PARA / LYT vault**: introduce `00-meta/` alongside the philosophy's content folders. Templates move from wherever they were to `00-meta/templates/`. Update plugin settings (Templates, Daily Notes, Templater) to point at the new paths.
- **References**:
  - help.obsidian.md — official docs.
  - Sibling guides: `notes/para/`, `notes/lyt-linking-your-thinking/`, `notes/access-framework/`, `notes/zettelkasten-classic/` — pair this scaffolding with one of those for the content layer.
  - Anti-pattern reference: `ANTIPATTERNS.md` for "gitignored entire `.obsidian/`" and "default attachment scatter".
