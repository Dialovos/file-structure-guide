# workspace-root-layout — canonical tree

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
