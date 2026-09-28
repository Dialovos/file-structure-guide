## TL;DR

A **browser extension** is a small web application split into isolated pieces, each with its own privileges: a **manifest** that declares everything, a **background service worker** (or event page) that reacts to browser events, **content scripts** injected into web pages, and UI surfaces such as a **popup** and an **options page**. Organize the source by these *execution contexts*, because each runs in a different environment with different APIs and permissions: `src/background/`, `src/content/`, `src/popup/`, `src/options/`, plus `src/shared/` for code that runs in more than one context. Build into a gitignored `dist/` that the browser loads. Keep the manifest minimal: request the fewest **permissions** and **host permissions** you can, because every one is a review hurdle and a user-visible warning. This guide targets Manifest V3, the current format across Chrome, Edge, and Firefox.

## Principles & why

1. **Execution context is the primary boundary.** The service worker, content scripts, and extension pages don't share memory or globals; they communicate by message passing. Directory structure should make it obvious where a piece of code runs.
2. **The manifest is the contract.** It declares permissions, entry points, and matches; anything the extension does beyond it is blocked. Review it like an API surface.
3. **Least privilege.** Request narrow `host_permissions` (specific sites), prefer optional permissions granted at runtime, and avoid `<all_urls>` unless the extension's purpose truly needs it. Broad permissions slow store review and alarm users.
4. **The background is ephemeral.** In Manifest V3 the service worker starts and stops on demand; state must be persisted (`chrome.storage`) or reconstructed, never held in variables.
5. **Content scripts are guests in hostile territory.** Pages can change and can be malicious; treat page data as untrusted, avoid injecting into page scripts, and keep DOM access minimal.
6. **Shared code is explicit.** Types, message names, and storage keys used across contexts live in `shared/` so a change in one place is a compile error in others.

## When to use

- **Extensions that modify or read web pages** (content blockers, page enhancers, clippers).
- **Toolbar utilities** with a popup and background events.
- **Cross-browser extensions** that must work in Chrome, Edge, and Firefox.
- **Internal tools** distributed through an enterprise policy or private store.

## When NOT to use

- **A bookmarklet or userscript is enough.** If the feature is one script on one site, an extension's packaging and review process is overhead.
- **Web apps that only need a website.** A Progressive Web App or a plain site avoids store review entirely.
- **Native integrations** requiring system access; use a native messaging host or a desktop app (see `tauri-desktop-app`).
- **Safari-only projects.** Safari extensions use Xcode projects and a different packaging model, though the web-extension code can be shared.

## Tree diagram

```
my-extension/
├── package.json
├── tsconfig.json
├── README.md
├── src/
│   ├── manifest.json              ← Manifest V3: permissions, entry points, matches
│   ├── background/
│   │   └── service-worker.ts      ← event handlers; no persistent state
│   ├── content/
│   │   └── content-script.ts      ← runs inside matched pages
│   ├── popup/
│   │   ├── popup.html
│   │   └── popup.ts
│   ├── options/
│   │   ├── options.html
│   │   └── options.ts
│   ├── shared/
│   │   ├── messages.ts            ← message types used across contexts
│   │   └── storage.ts             ← typed wrappers over chrome.storage
│   └── icons/
│       ├── icon-16.png
│       ├── icon-48.png
│       └── icon-128.png
├── tests/
├── dist/                          ← generated, gitignored; load this unpacked
└── store/
    ├── description.md             ← listing text
    └── screenshots/
```

## Naming rules

- **Context directories** are lowercase and named for where the code runs: `background/`, `content/`, `popup/`, `options/`; `shared/` for cross-context code.
- **Entry files** name their role (`service-worker.ts`, `content-script.ts`), which makes the manifest readable.
- **Message types** are a small typed set with a clear prefix or namespace (`"page/selection-changed"`), defined once in `shared/messages.ts`.
- **Storage keys** are defined as constants in `shared/storage.ts`, not repeated as string literals.
- **Icons** follow size in the name (`icon-16.png`, `icon-48.png`, `icon-128.png`).
- **Extension ID and version**: `version` in `manifest.json` uses the extension version format (dot-separated integers) and matches release tags.

## Worked example

A userscript that highlights words on any page needs to become an installable extension for Chrome and Firefox.

1. Create `src/manifest.json`: `manifest_version: 3`, name, version, `content_scripts` with narrow `matches`, a `background` entry, and an `action` popup. Start with no permissions beyond what the feature needs (for example `storage`).
2. Move the highlighter into `src/content/content-script.ts`. It reads settings via a message to the background or from `chrome.storage`; don't share variables.
3. Define messages in `src/shared/messages.ts`: `{type: "settings/get"}` and `{type: "settings/changed", ...}`, and use the types on both ends.
4. Put settings persistence in the service worker and `shared/storage.ts`; the worker holds no state in variables because it can be terminated at any time.
5. Build the popup and options pages as separate HTML entry points that use the same storage wrapper.
6. Bundle with a tool that understands extensions (WXT, Vite with a web-extension plugin, or Parcel), outputting to `dist/`.
7. Load `dist/` unpacked (`chrome://extensions` with developer mode; `about:debugging` in Firefox), and test on real pages.
8. For Firefox, the manifest differs slightly (for example `background.scripts` rather than `service_worker`, and a `browser_specific_settings` ID); let the build tool generate per-browser manifests rather than hand-maintaining two.
9. Add unit tests for pure logic in `shared/` and end-to-end tests with Playwright loading the extension.
10. Package `dist/` as a zip and submit to the stores with the `store/` listing text and screenshots.

Each piece of code sits in the directory for the context it runs in, and message types make cross-context contracts checkable.

## Anti-patterns

- **Global state in the service worker.** It is suspended and restarted; variables vanish. Persist or reconstruct.
- **`<all_urls>` host permissions "for flexibility."** It triggers store scrutiny and user warnings; use narrow matches or request optional permissions when needed.
- **Loading remote code.** Manifest V3 forbids remotely hosted executable code; bundle everything.
- **Trusting page data in content scripts** (using page-provided strings as HTML, evaluating page values). Treat pages as untrusted input.
- **Sharing code by copy-paste** between contexts, so message shapes drift.
- **Hand-maintained separate manifests per browser** that diverge. Generate them from one source.
- **Committing `dist/`.** It is build output (see `generated-vs-source-separation`).

## Scaling & failure modes

- **Bundle size and startup**: content scripts run on every matched page; keep them small and lazy-load heavy code from the service worker or on demand.
- **Permissions growth**: each new permission triggers re-consent for existing users and can disable the extension until approved; add them deliberately and document why.
- **Cross-browser differences**: API namespaces (`chrome` versus `browser`), background models, and manifest keys differ; use a polyfill (`webextension-polyfill`) or a framework that abstracts them.
- **Testing surfaces**: unit-test pure logic, and use end-to-end tests with a real browser and the built extension; mock `chrome.*` for logic that touches APIs.
- **Release process**: store reviews take days; automate zips and versioning, and keep a changelog for store listings.
- **Security review**: audit permissions, content security policy, and message handlers periodically; message handlers should validate sender and payload.

## Variants

- **Framework-based** (WXT, Plasmo): opinionated file-based entry points and per-browser builds.
- **Vite plus a web-extension plugin**: a lighter setup with manual manifest control.
- **Plain JavaScript, no build step**: fine for very small extensions; the layout still mirrors contexts.
- **Content-script-only extensions**: no background or popup; the tree collapses to `content/` and the manifest.
- **DevTools extensions and side panels**: add `devtools/` or `sidepanel/` contexts with their own entry points.

## Adoption checklist

- [ ] Directories map to execution contexts, and `shared/` holds cross-context code.
- [ ] The manifest requests only the permissions and host permissions the features need, each justified in the README.
- [ ] The service worker holds no state outside `chrome.storage`.
- [ ] Message types and storage keys are defined once in `shared/`.
- [ ] `dist/` is gitignored, and the extension loads unpacked from it in Chrome and Firefox.
- [ ] Message handlers validate sender and payload.

## Real-world projects using this

- **MDN "Browser extensions"** and **Chrome for Developers "Extensions"** document Manifest V3, execution contexts, permissions, and messaging.
- **WXT** (wxt.dev) and **Plasmo** document file-based extension frameworks with per-browser output.
- **Open-source extensions** such as uBlock Origin, Bitwarden's browser extension, and Dark Reader are public; reading them shows different scales of structure and per-browser handling.
- **`webextension-polyfill`** (Mozilla) documents cross-browser API differences.
- **The Chrome Web Store and Firefox Add-ons developer policies** describe permission and remote-code rules that affect layout decisions.

## Migration & references

- **From a userscript:** move the logic into a content script, add a manifest with narrow matches, and replace `GM_*` APIs with `chrome.storage` and messaging.
- **From Manifest V2 to V3:** replace the persistent background page with a service worker, move remote code into the bundle, and switch to `host_permissions` and `action`.
- **From Chrome-only to cross-browser:** adopt a framework or polyfill that generates per-browser manifests, and test in Firefox early.
- **References:**
  - `principles/generated-vs-source-separation/` for `dist/`.
  - `code/node-library/` for TypeScript build conventions.
  - `code/tauri-desktop-app/` for when you need native capabilities.
  - `principles/config-and-secrets-placement/` for API keys (never bundle secrets in an extension; it is public).
