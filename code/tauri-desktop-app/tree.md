# tauri-desktop-app — canonical tree

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
