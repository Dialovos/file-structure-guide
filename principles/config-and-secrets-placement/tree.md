# config-and-secrets-placement — canonical tree

```
project/
├── .env                  ← real values, gitignored
├── .env.example          ← names only, committed
├── .gitignore            ← lists .env and *.local
├── config/
│   ├── default.yaml      ← non-secret defaults, committed
│   ├── development.yaml
│   └── production.yaml   ← non-secret overrides, committed
├── src/
│   └── settings.py       ← reads config + environment, validates
└── deploy/
    └── secrets.README.md ← says where production secrets live (never the values)
```
