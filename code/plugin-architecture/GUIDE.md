## TL;DR

The **plugin-architecture layout** splits an extensible application into a small, stable **host** that defines the plugin contract and an open set of **plugins** that implement it. The shape: `core/plugin_api.py` defines an abstract base class (the contract — `name()`, `run()`, lifecycle hooks). `core/registry.py` discovers and loads plugins via two mechanisms: an entry-points group (`importlib.metadata.entry_points(group="myhost.plugins")`) for plugins shipped as separate distributions, plus an in-tree fallback that scans `plugins/<plugin-name>/` siblings for development. Each in-tree plugin lives in its own folder with a `plugin.toml` manifest (name, version, capabilities) and one Python module that subclasses the API. The host never imports a specific plugin; the registry returns whatever it finds at runtime. The discipline is the inversion: the host owns the *interface*, plugins own the *implementations*, and the runtime owns the *binding*. This is the layout that makes VS Code, OBS, Pelican, tox, and Mozilla products extensible. Build it on day one if you suspect anyone outside your team will extend the system.

## Principles & why

The plugin-architecture layout enforces three separations that protect both the host and the ecosystem.

1. **Interface vs implementation.** `core/plugin_api.py` is the contract: an abstract base class (or `Protocol`) that every plugin satisfies. The host code only ever depends on the abstract type. A plugin can be added, removed, replaced, or swapped without touching the host. This is dependency-inversion at the system level — the host depends on its own interface, not on any concrete plugin.
2. **Discovery vs loading.** `core/registry.py` is responsible for *finding* plugins (entry-points scan, directory scan) and *materialising* them (importing the module, instantiating the class, validating the manifest). Splitting discovery from loading means you can list available plugins without instantiating them, and you can fail one plugin without crashing the host. Registries also let you order, filter, and sandbox plugins as a separate concern.
3. **In-tree development vs external distribution.** Plugins should be loadable from the same repo for development and from a separately-published package in production. The `entry_points` mechanism (Python's `pyproject.toml` `[project.entry-points."myhost.plugins"]`, or Node's `package.json#contributes`) is the industry-standard way to do this. The in-tree `plugins/` directory is a development convenience; the entry-points contract is the production interface.

The layout makes the *open–closed principle* concrete: the host is closed for modification, open for extension. Every new feature that fits the plugin contract is a new folder, not a new branch in the host. The trade is upfront cost: you must commit to a plugin API early, document it as a public interface, and version it like one. Get it right and the ecosystem outgrows your team; get it wrong and every plugin breaks on every minor host release.

## When to use

- **Any extensible system.** Editors (VS Code, Sublime, Vim, Emacs), browsers (Firefox WebExtensions), IDEs (JetBrains, Eclipse), build tools (webpack, esbuild, Vite), test runners (pytest, tox), static-site generators (Pelican, Hugo), CMSs (WordPress).
- **Server apps with documented extension points.** Datadog Agent integrations, Home Assistant integrations, Discord bot frameworks, Mastodon/ActivityPub server extensions.
- **Products with a third-party developer story.** If you want anyone outside your team to add features, you need a plugin contract; ad-hoc forking does not scale.
- **Internal platforms with multiple teams.** Each team owns one plugin; the platform team owns the host. The plugin API is the inter-team contract.
- **Anything where the *kind* of work to be added is open-ended.** New file format readers, new export targets, new cloud providers, new check rules — all natural plugin shapes.

## When NOT to use

- **Closed apps with no extension intent.** A four-screen mobile app with a fixed feature list does not need a plugin system; you'd be paying the cost (interface design, registry, manifest format, versioning policy) for an option you'll never exercise.
- **Apps where the variability is data, not behaviour.** If your "plugins" would all do the same thing with different config, that is configuration, not a plugin system.
- **Tightly-coupled subsystems.** If your would-be plugins all need access to private host internals, you don't have plugins — you have modules. Use module boundaries (`code/python-src-layout/`, `code/feature-based-frontend/`) instead.
- **Hot performance paths.** Indirection through an abstract class plus a registry lookup costs nanoseconds, but plugins also resist inlining and optimisation. If you're building a tight rendering loop, keep it monolithic.
- **Solo prototypes.** Build the feature concretely first; extract the plugin API after the second or third concrete instance teaches you what the abstraction should be.

## Tree diagram

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

## Naming rules

- **Host package**: short, generic — `core/` here. In real codebases pick a project-specific name (`obs/`, `pelican/`, `tox/`). Keep it singular.
- **Plugin API module**: `core/plugin_api.py`. The class inside is `Plugin` (or `<HostName>Plugin` if `Plugin` is too generic). Use a `Protocol` for duck-typed plugins; use `ABC` when you want enforced inheritance.
- **Registry module**: `core/registry.py`. Public API is one or two functions: `discover() -> list[PluginInfo]`, `load(name: str) -> Plugin`. Keep the registry stateless or use a single module-level cache with explicit `clear_cache()` in tests.
- **In-tree plugin folders**: `plugins/<plugin-name>/`, kebab-case for the folder when surfaced to users (`plugins/markdown-pre/`), snake_case for the Python package itself if you want to import it (`plugins/markdown_pre/`). Most ecosystems pick one convention — match yours.
- **Plugin manifest**: `plugin.toml` with `name`, `version`, `entry_point`, `capabilities`. Keep manifest fields machine-readable; descriptions go in the plugin's own README.
- **Plugin module**: `<plugin_name>_plugin.py` exporting one class — `AudioPlugin`, `VideoPlugin`. The redundant `_plugin` suffix is intentional: it makes grepping for plugin classes trivial across an ecosystem.
- **Entry-points group**: `myhost.plugins` (dotted, lowercase). One group per extension point — if you have multiple kinds of extensions (codecs vs filters), use `myhost.codecs` and `myhost.filters`.

## Anti-patterns

- **Host imports specific plugins.** `from plugins.audio import AudioPlugin` defeats the entire pattern; the host now hard-depends on the plugin. The registry returns `Plugin` instances; the host calls methods on those instances and never asks what concrete class they are.
- **Plugins imports private host internals.** A plugin reaches into `core._internals` to do its job — now your "private" internal is the API, but undocumented. Either expose it on the plugin API explicitly or refactor the host until the plugin doesn't need it.
- **No version on the plugin API.** When the host changes a method signature, every plugin breaks at runtime with cryptic errors. Version the plugin API (`API_VERSION = "1.0"`) and have plugins declare which version they target. Reject mismatches at load time with a clear error.
- **Discovery that imports everything eagerly.** Importing every plugin at startup is slow and turns one bad plugin into a startup failure for the whole host. Discover lazily (read manifests first), import only what's actually used, and isolate import failures.
- **Manifest in code instead of a data file.** A plugin's `setup()` function returns a dict — now you must execute the plugin to know what it is. Use a static manifest file (`plugin.toml`, `package.json#contributes`) so the host can introspect plugins without trusting them.
- **Two discovery mechanisms with different semantics.** If `entry_points` and the in-tree scan return different fields or prioritise differently, plugins that work in dev break in production. Make the in-tree scan a *fallback* that produces the exact same `PluginInfo` shape as the entry-points loader.
- **No sandbox for untrusted plugins.** If you'll accept plugins from arbitrary authors, run them under reduced privileges (subprocess, Wasm, restricted import). Native Python plugins have full access to the host process; treat that as a trust decision, not an oversight.

## Variants

- **entry-points-discovered** (this guide) — plugins are separate distributions registering via `pyproject.toml` `[project.entry-points."<group>"]` (Python) or `package.json#contributes`/`activationEvents` (Node/VS Code). Production-grade.
- **in-tree-only** — every plugin is a folder inside the host repo; no external publication. Right for small, closed ecosystems (a corporate platform team's plugins).
- **in-tree-plus-external** (this guide accommodates both) — `plugins/` for development and bundled defaults; entry-points for the community ecosystem. The two paths produce identical `PluginInfo` records.
- **capability-based / sandboxed** — plugins are Wasm modules or subprocesses with a narrow IPC surface. Used by Figma plugins, Envoy filters (Wasm), Pony actor systems. Higher cost, much stronger isolation.
- **declarative-only** — the plugin is the manifest; the host does the work (e.g., GitHub Actions composite actions). Right when "extension" means configuration plus a few well-known scripts.
- **hot-reloadable** — the registry watches the plugin directory and reloads on change. Useful for editor-style hosts; harder to get right because you must invalidate held references safely.

## Real-world projects using this

- **VS Code extensions** — `package.json#contributes` is the manifest, `activationEvents` controls lazy loading; the registry is the Extensions view; the API surface is the `vscode` namespace.
- **OBS Studio plugins** — C++ ABI plugin contract loaded from a shared library directory at startup; manifests via `obs_register_*` calls.
- **Vim and Neovim plugin model** — `runtimepath` is the discovery directory; each plugin folder mirrors the host's directory layout (`plugin/`, `autoload/`, `doc/`).
- **Pelican plugins** — Python entry-points group `pelican.plugins`; this guide's structure is essentially Pelican's plugin layout in miniature.
- **tox plugins** — `pyproject.toml` `[project.entry-points.tox]` registers plugins; `tox-uv`, `tox-gh` are the canonical examples.
- **pytest plugins** — `pyproject.toml` `[project.entry-points.pytest11]`; one of the largest Python plugin ecosystems.
- **Home Assistant integrations** — `custom_components/<integration>/manifest.json`; same shape as this guide, scaled to thousands of integrations.

## Migration & references

- **From a monolith with `if/elif` branches per feature**: identify the feature dimension that was being switched over (file format, provider, target). Extract the common method calls into an abstract base class; move each branch into its own plugin module. The first plugin you extract teaches you what the API really needs to expose; expect to revise the contract once before stabilising.
- **From a registry-by-string-id with no contract**: pick the worst plugin (the one with the most subtle bugs); write its API explicitly as an ABC; refactor it to inherit from the ABC. Repeat for the next worst. Stop when you have an honest abstract base; that base is now the contract.
- **From shared-library plugins to entry-points**: ship the existing plugin folder as a separate Python distribution (`pyproject.toml` with one entry in `[project.entry-points."<group>"]`). Keep the in-tree fallback so existing dev workflows keep working. Migrate one plugin per release.
- **From eagerly-imported plugins**: introduce a `PluginInfo` dataclass that the registry can return *without* importing the plugin module. The actual import happens only on `load(name)`. Migrate the host to call `discover()` for listings and `load()` for use; failures isolate to the plugin that actually fails.
- **References**:
  - Brad Frost-style ecosystems aside, the canonical reference for Python is the *packaging* user guide — *Creating and discovering plugins* (entry-points based).
  - VS Code Extension API docs (`code.visualstudio.com/api`) — best worked example of `contributes` plus `activationEvents`.
  - Pelican plugin docs and the `pelican-plugins` GitHub organization — minimal, readable.
  - tox plugin docs (`tox-dev/tox`) — concise; shows manifest, hookspec, hookimpl.
  - pytest plugin docs — `pytest11` group; the `_pytest.config` registry is worth reading once.
  - Sibling guides: `code/python-src-layout/` (publish your host as a real package so others can install plugins against it), `code/cli-tool/` (for plugin-driven CLIs), `principles/depth-vs-breadth/` (why `plugins/<name>/` per plugin beats one giant `plugins.py`).
