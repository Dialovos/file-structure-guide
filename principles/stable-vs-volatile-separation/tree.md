# stable-vs-volatile-separation — canonical tree

```
project/
├── src/                ← stable (rarely renamed)
├── config/             ← semi-stable
├── data/
│   ├── raw/            ← stable inputs
│   └── processed/      ← regenerable, gitignored
├── logs/               ← volatile, gitignored
└── .cache/             ← ephemeral, gitignored
```
