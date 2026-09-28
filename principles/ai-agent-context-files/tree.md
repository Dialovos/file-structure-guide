# ai-agent-context-files — canonical tree

```
repo/
├── AGENTS.md                      ← shared rules; the source of truth
├── CLAUDE.md                      ← pointer: imports AGENTS.md + Claude-specific notes
├── GEMINI.md                      ← pointer to AGENTS.md
├── .github/
│   └── copilot-instructions.md    ← pointer to AGENTS.md
├── .cursor/
│   └── rules/
│       └── project.mdc            ← pointer to AGENTS.md
├── README.md                      ← human-facing; agents link to it for setup
├── docs/
│   └── architecture.md            ← long-form knowledge, linked from AGENTS.md
└── services/
    └── billing/
        └── AGENTS.md              ← only what differs inside billing/
```
