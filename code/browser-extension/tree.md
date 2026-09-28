# browser-extension — canonical tree

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
