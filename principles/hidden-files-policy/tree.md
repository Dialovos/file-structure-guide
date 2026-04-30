# hidden-files-policy — canonical tree

```
project/
├── .editorconfig       ← hidden: tool config, rarely edited
├── .gitignore          ← hidden: tool config
├── .github/            ← hidden: CI config
├── .env.example        ← hidden but committed (a discoverable template)
├── .env                ← hidden, gitignored, secrets
├── README.md           ← visible
├── pyproject.toml      ← visible: meaningful config
└── src/
    └── main.py
```
