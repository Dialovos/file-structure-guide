# gitignore-and-keep-files — canonical tree

```
project/
├── .gitignore           ← excludes node_modules, dist, .env*
├── data/
│   ├── raw/
│   │   └── .gitkeep     ← preserves empty dir
│   └── processed/
│       └── .gitkeep
└── src/
    └── main.ts
```
