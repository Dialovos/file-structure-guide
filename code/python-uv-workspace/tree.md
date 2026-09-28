# python-uv-workspace — canonical tree

```
acme/
├── pyproject.toml              ← virtual root: [tool.uv.workspace], dev groups, tool config
├── uv.lock                     ← one lockfile for every member
├── README.md
├── .python-version
├── packages/
│   ├── acme-core/
│   │   ├── pyproject.toml
│   │   ├── src/acme_core/
│   │   │   └── __init__.py
│   │   └── tests/
│   ├── acme-cli/
│   │   ├── pyproject.toml      ← depends on acme-core via workspace source
│   │   ├── src/acme_cli/
│   │   └── tests/
│   └── acme-api/
│       ├── pyproject.toml
│       ├── src/acme_api/
│       └── tests/
└── scripts/
```
