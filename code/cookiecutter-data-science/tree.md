```
project/
├── pyproject.toml          ← or requirements.txt + setup.py (CCDS v2 vs v1)
├── README.md
├── LICENSE
├── .gitignore
├── Makefile                ← `make data`, `make features`, `make train`
├── data/
│   ├── raw/                ← immutable, never committed; .gitkeep only
│   ├── interim/
│   ├── processed/
│   └── external/
├── docs/
├── models/                 ← trained model artifacts (often gitignored)
├── notebooks/              ← exploration; named `0.1-initials-purpose.ipynb`
│   └── 0.1-jh-eda.ipynb
├── references/
├── reports/
│   └── figures/
├── src/                    ← installable package
│   └── project/
│       ├── __init__.py
│       ├── data/
│       │   └── make_dataset.py
│       ├── features/
│       │   └── build_features.py
│       ├── models/
│       │   ├── train_model.py
│       │   └── predict_model.py
│       └── visualization/
└── tests/
```
