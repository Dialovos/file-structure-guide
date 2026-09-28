# backup-3-2-1-layout — canonical tree

```
backup-plan/                          ← lives in version control and a printed copy
├── README.md                         ← the 3-2-1 plan in one page: what, where, how often
├── backup-paths.txt                  ← paths to include, relative to the home directory
├── backup-excludes.txt               ← patterns to exclude (caches, build outputs)
├── backup.sh                         ← runs the tool, prunes, checks
├── manifest.md                       ← copies: location, media, tool, retention, last verified
└── restore-tests/
    ├── 2026-04-30.md                 ← date, what was restored, result, time taken
    └── 2026-01-31.md

Copies (outside the repository):
  1. original data                    ← internal disk
  2. local backup repository          ← external drive (different media)
  3. off-site backup repository       ← another location or encrypted cloud storage
```
