# tauri-desktop-app — template

A structure reference for a Tauri 2 app (frontend at the root, native code in `src-tauri/`, capabilities, thin commands). For a runnable scaffold, generate one with `npm create tauri-app@latest` and compare it with this layout.

## What to rename

- `my-app`, `my_app_lib`, and `com.example.my-app` to your real names

## What to fill

- `src-tauri/tauri.conf.json` — identity and bundle settings
- `src-tauri/capabilities/default.json` — only the permissions you need

## What to delete

- The example `greet` command once you have real commands

## First run

```bash
npm create tauri-app@latest  # scaffold, then compare with this tree
npm run tauri dev
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../../rust-workspace/` — moving logic into its own crate
