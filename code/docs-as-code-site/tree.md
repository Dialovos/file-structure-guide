# docs-as-code-site — canonical tree

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
