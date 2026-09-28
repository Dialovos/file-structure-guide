# browser-extension — template

A no-build Manifest V3 extension with a content script, service worker, popup, and shared message definitions. Load `src/` directly as an unpacked extension to try it.

## What to rename

- `name` and `version` in `src/manifest.json`
- `matches` patterns to the sites you really need

## What to fill

- `src/content/content-script.js` — your page logic
- `src/background/service-worker.js` — your event handling

## What to delete

- The example message handler and popup text

## First run

```bash
# Chrome: chrome://extensions -> Developer mode -> Load unpacked -> select the src/ directory
# Firefox: about:debugging -> This Firefox -> Load Temporary Add-on -> select src/manifest.json
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../../node-library/` — TypeScript build conventions
