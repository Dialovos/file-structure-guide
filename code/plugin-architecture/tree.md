```
my-host/
├── README.md
├── pyproject.toml          ← or equivalent manifest
├── core/
│   ├── __init__.py
│   ├── plugin_api.py       ← abstract base / interface
│   └── registry.py         ← discovery + loading
├── plugins/
│   ├── audio/
│   │   ├── plugin.toml     ← plugin manifest
│   │   └── audio_plugin.py
│   ├── video/
│   │   ├── plugin.toml
│   │   └── video_plugin.py
│   └── README.md
└── tests/
    └── test_registry.py
```
