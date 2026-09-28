## TL;DR

A **Tauri** desktop app pairs a **web frontend** (any framework that builds to static files) with a small **Rust backend** that runs natively and exposes **commands** the frontend can call. The repository has two halves with a clean boundary: the frontend at the root (`src/`, `package.json`, `index.html`), and everything native in **`src-tauri/`** (`Cargo.toml`, `tauri.conf.json`, `src/`, `capabilities/`, `icons/`). The frontend never touches the operating system directly; it calls Rust commands through IPC, and Tauri's **capabilities** (permission files in `src-tauri/capabilities/`) decide which windows may call which commands or plugins. Keep the Rust side thin: window setup, commands, and native integrations, with domain logic in plain Rust modules or a separate crate that has its own tests. Generated output (`dist/`, `src-tauri/target/`, `src-tauri/gen/`) is gitignored. The result is a small, fast app with a narrow, auditable native surface.

## Principles & why

1. **Two halves, one boundary.** The web frontend and the Rust backend are separate programs joined by a typed IPC contract. Directory structure and code review should treat the commands as an API.
2. **Deny by default, grant explicitly.** Tauri 2 capabilities list, per window, exactly which core APIs, plugins, and commands are allowed. Nothing is available to the frontend unless a capability grants it.
3. **The frontend is untrusted like a website.** Even though you ship it, it can render remote content or be affected by injected scripts; validate every command argument in Rust and keep dangerous operations narrow.
4. **Keep native code thin and testable.** Command handlers should translate between IPC and plain functions; the logic in those functions is unit-tested without launching a window.
5. **Build output is not source.** Frontend bundles, the Rust `target/` directory, and generated schemas are reproducible and stay out of git.
6. **Configuration lives in one place per concern.** App identity, windows, and bundling in `tauri.conf.json`; permissions in `capabilities/`; dependencies in `Cargo.toml` and `package.json`.

## When to use

- **Desktop applications** that want web-technology UIs with small binaries and native performance for the backend.
- **Tools that need file system, notifications, tray, or OS integration** but ship as a single installable app.
- **Teams with web frontend skills** who also want Rust for performance-sensitive or security-sensitive parts.
- **Apps where auditing native capabilities matters**, since the capability model makes them explicit.

## When NOT to use

- **Pure websites.** If it doesn't need native access, a web app or PWA avoids installation and updates.
- **Apps needing a bundled full browser engine with identical rendering everywhere.** Tauri uses the system webview (WebView2, WKWebView, WebKitGTK), so rendering can differ across platforms; consider Electron if uniformity is critical.
- **Heavy native UI.** For platform-native widgets, use the platform toolkits or a native cross-platform UI framework.
- **Browser add-ons.** See `browser-extension` for that model.

## Tree diagram

```
my-app/
├── package.json                    ← frontend deps and scripts (tauri dev/build)
├── index.html
├── src/                            ← frontend source (any framework)
│   ├── main.ts
│   ├── lib/
│   │   └── commands.ts             ← typed wrappers around invoke()
│   └── components/
├── dist/                           ← frontend build output, gitignored
└── src-tauri/
    ├── Cargo.toml
    ├── build.rs
    ├── tauri.conf.json             ← app identity, windows, bundle settings
    ├── capabilities/
    │   └── default.json            ← permissions granted to windows
    ├── icons/
    ├── src/
    │   ├── main.rs                 ← thin entry point
    │   ├── lib.rs                  ← builder setup, command registration
    │   └── commands/               ← #[tauri::command] handlers, thin
    ├── gen/                        ← generated schemas, gitignored
    └── target/                     ← Rust build output, gitignored
```

## Naming rules

- **Frontend** follows its framework's conventions (see `feature-based-frontend`, `vue-nuxt-app`, or `nextjs-app` for a static export).
- **Rust modules and crates** use `snake_case`; the crate name in `Cargo.toml` is kebab or snake case, and the library name is `snake_case` (`my_app_lib`).
- **Commands** are `snake_case` Rust functions (`read_settings`), invoked from the frontend by the same name; wrap each in a typed function in `src/lib/commands.ts`.
- **Capabilities** are JSON files named by scope (`default.json`, `settings-window.json`), each with an `identifier` and the windows it applies to.
- **App identifier** in `tauri.conf.json` is reverse-DNS (`com.example.my-app`) and stable once released, because it determines data directories and updates.
- **Events** exchanged between frontend and backend are namespaced strings (`"settings:changed"`).

## Worked example

A web app running in the browser needs to read and write local files and ship as an installable desktop app.

1. Scaffold with `npm create tauri-app@latest` (choose your frontend), which creates `src-tauri/` beside the existing frontend. Check that `npm run tauri dev` opens a window.
2. Move domain logic that touches files into plain Rust functions in `src-tauri/src/storage.rs` with unit tests (`cargo test`), independent of Tauri.
3. Expose a thin command in `src-tauri/src/commands/settings.rs`:
```
#[tauri::command]
fn read_settings(app: tauri::AppHandle) -> Result<Settings, String> {
    storage::read(&app.path().app_config_dir().map_err(|e| e.to_string())?)
        .map_err(|e| e.to_string())
}
```
and register it in `lib.rs` with `invoke_handler(tauri::generate_handler![read_settings])`.
4. Wrap it once in `src/lib/commands.ts`: `export const readSettings = () => invoke<Settings>("read_settings")`, so components never use raw string names.
5. Grant only what is needed in `src-tauri/capabilities/default.json`: `core:default` and any plugins (for example the dialog plugin), scoped to the main window.
6. Validate inputs in Rust (paths, sizes, formats), and restrict file access to the app's directories unless the user picks a file through a dialog.
7. Set `identifier`, `productName`, and `version` in `tauri.conf.json`, and generate icons (`npm run tauri icon path/to/logo.png`).
8. Build installers: `npm run tauri build`, and test them on each target OS.
9. Gitignore `dist/`, `src-tauri/target/`, and `src-tauri/gen/`.

The frontend stays a normal web app, and the native surface is a short list of typed commands and explicit permissions.

## Anti-patterns

- **Business logic inside command handlers.** It can't be unit-tested without the runtime; keep handlers thin and logic in plain functions.
- **Granting broad capabilities "to make it work."** Wide filesystem or shell permissions defeat the model; scope to specific paths and commands.
- **Trusting frontend input in Rust.** Validate every argument as if it came from the network.
- **Raw `invoke("name", ...)` strings scattered through components.** Wrap them in typed functions.
- **Changing the app identifier after release.** Data directories and updater identity change with it.
- **Committing build output** (`dist/`, `target/`, `gen/`).
- **Loading remote content in a window that has powerful capabilities.** Use separate windows with minimal capabilities for remote content.

## Scaling & failure modes

- **Command surface growth**: group commands by module, keep a documented list, and review capabilities whenever one is added.
- **Large Rust logic**: move it into a separate crate in a Cargo workspace (see `rust-workspace`) with its own tests, and depend on it from `src-tauri`.
- **Multiple windows**: give each window its own capability file and label, and restrict remote-content windows.
- **Build times**: Rust compilation dominates; use a shared `target/` in CI cache, and `cargo check` during development.
- **Cross-platform testing**: system webviews differ (WebView2, WKWebView, WebKitGTK); test on each OS, and set minimum versions in documentation.
- **Updates and signing**: adopt the updater plugin with signing keys stored as CI secrets (see `config-and-secrets-placement`), and plan certificate handling per platform.

## Variants

- **Single-crate app** (this guide): logic and commands in `src-tauri`.
- **Workspace with a core crate**: domain logic in `crates/core`, Tauri app depending on it, and possibly a CLI sharing the same core.
- **Mobile targets**: Tauri 2 can target iOS and Android; `src-tauri/gen/` then includes platform projects, and layout adds per-platform configuration.
- **Frontend in Rust** (Leptos, Yew, Dioxus): the frontend is also Rust; the split remains but tooling differs.
- **Electron alternative**: a bundled Chromium plus Node backend; different layout (`main/`, `renderer/`, `preload/`).

## Adoption checklist

- [ ] Frontend and native code are separated (`src/` versus `src-tauri/`), joined only through typed commands.
- [ ] `capabilities/*.json` grant the minimum permissions per window.
- [ ] Command handlers are thin and validate every argument.
- [ ] Business logic has Rust unit tests that run without launching the app.
- [ ] `dist/`, `src-tauri/target/`, and `src-tauri/gen/` are gitignored.
- [ ] The app identifier is final before the first release, and installers were tested on each target OS.

## Real-world projects using this

- **Tauri's documentation** (tauri.app) describes the project structure, `tauri.conf.json`, the capabilities and permissions system, and the command and event model.
- **Open-source Tauri apps**, including many listed in the "awesome-tauri" collection, show a range of layouts; browse a few with different frontends.
- **The Tauri repository itself** contains example apps under `examples/` that follow the recommended structure.
- **Cargo workspaces documentation** (see `rust-workspace`) applies when the native logic moves into its own crate.

## Migration & references

- **From a web app:** add `src-tauri/` with the scaffolder, point `frontendDist` at your build output, and move file, OS, or network operations behind commands.
- **From Electron:** replace `main`/`preload` code with Rust commands and capabilities, keep the renderer code mostly as is, and re-check any Node-only APIs.
- **From Tauri 1 to 2:** follow the official migration guide; the allowlist is replaced by capabilities and plugins.
- **References:**
  - `code/rust-workspace/` and `code/rust-binary/` for the Rust side.
  - `code/feature-based-frontend/` for organizing the frontend.
  - `principles/config-and-secrets-placement/` for signing keys and API secrets.
  - `code/browser-extension/` for the other web-tech-plus-privileges model.
