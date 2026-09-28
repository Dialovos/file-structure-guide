# ml-experiment-project — canonical tree

```
project/
├── pyproject.toml
├── README.md
├── Makefile                          ← train, eval, lint, test entry points
├── configs/
│   ├── base.toml                     ← defaults shared by all runs
│   ├── experiment/
│   │   ├── baseline.toml
│   │   └── wider-model.toml          ← overrides only
│   └── data/
│       └── splits-v1.toml
├── src/
│   └── project/
│       ├── data.py                   ← loading, splits, transforms
│       ├── model.py
│       ├── train.py                  ← reads config, writes runs/<run-id>/
│       ├── evaluate.py
│       └── config.py                 ← loading and merging configs
├── tests/
│   ├── test_data.py
│   └── test_train_smoke.py           ← tiny run on fake data
├── data/
│   ├── raw.dvc                       ← pointer to immutable raw data
│   └── .gitignore                    ← real data paths, added by the tool
├── runs/                             ← gitignored: one directory per run
│   └── 2026-04-30-baseline-s0/
│       ├── config.resolved.toml
│       ├── metrics.jsonl
│       └── checkpoints/
├── reports/                          ← tracked summaries and figures
└── notebooks/                        ← exploration only, no pipeline logic
```
