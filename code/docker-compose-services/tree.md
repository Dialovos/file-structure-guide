# docker-compose-services — canonical tree

```
project/
├── compose.yaml                 ← base: services as they run everywhere
├── compose.override.yaml        ← dev overrides: bind mounts, debug ports (auto-loaded)
├── compose.prod.yaml            ← production overrides (use -f)
├── .env                         ← real values, gitignored
├── .env.example                 ← names only, committed
├── services/
│   ├── api/
│   │   ├── Dockerfile
│   │   ├── .dockerignore
│   │   └── src/
│   └── web/
│       ├── Dockerfile
│       └── .dockerignore
├── db/
│   └── init/                    ← SQL run once on first start
└── README.md
```
