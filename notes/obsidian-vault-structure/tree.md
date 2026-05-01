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
