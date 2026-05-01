# Plugins directory

This directory holds plugins shipped *with* the host. The registry
auto-discovers them by scanning for `plugins/<name>/plugin.toml`. You
can also publish plugins as separate distributions; both paths are
handled by `core/registry.py`.

## Adding an in-tree plugin

1. Create `plugins/<your-plugin-name>/`.
2. Add `plugin.toml`:
   ```toml
   [plugin]
   name = "your-plugin-name"
   version = "0.1.0"
   entry_point = "plugins.your_plugin_name.your_plugin_name_plugin:YourPluginNamePlugin"
   capabilities = []
   api_version = "1.0"
   ```
3. Add the Python module (`<snake_name>_plugin.py`) with a class that
   subclasses `core.Plugin` and implements `name()` and `run()`.
4. The registry will discover it automatically; verify with:
   ```python
   from core.registry import discover
   print([p.name for p in discover()])
   ```

## Adding an external plugin (separate distribution)

Ship a Python package with this in its `pyproject.toml`:

```toml
[project.entry-points."myhost.plugins"]
your-plugin-name = "your_pkg.plugin:YourPluginClass"
```

Once installed (`pip install your-plugin-name`), the host registry
picks it up via `importlib.metadata.entry_points`. No host changes
needed.

## Naming

- Folder: kebab-case (`markdown-pre`).
- Python module: snake_case (`markdown_pre_plugin.py`).
- Class: PascalCase ending in `Plugin` (`MarkdownPrePlugin`).
- The redundant `Plugin` suffix is intentional — it makes plugin
  classes greppable across an ecosystem.
