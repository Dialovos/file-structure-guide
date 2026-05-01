```
my-pkg/
├── package.json
├── tsconfig.json
├── README.md
├── LICENSE
├── .gitignore
├── .npmignore               ← or `files` field in package.json
├── src/
│   ├── index.ts             ← public API
│   └── core.ts
├── tests/
│   └── core.test.ts
├── dist/                    ← built output, gitignored, npm-published
└── .github/workflows/ci.yml
```
