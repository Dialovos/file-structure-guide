```
my-monorepo/
├── package.json                ← workspace root
├── pnpm-workspace.yaml
├── turbo.json
├── tsconfig.json               ← base, extended by apps/packages
├── README.md
├── apps/
│   ├── web/                    ← Next.js app
│   │   └── package.json
│   └── docs/                   ← Next.js docs site
├── packages/
│   ├── ui/                     ← shared component library
│   │   ├── package.json
│   │   └── src/
│   ├── eslint-config/
│   └── typescript-config/
└── .github/workflows/ci.yml
```
