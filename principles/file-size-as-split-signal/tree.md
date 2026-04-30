# file-size-as-split-signal — canonical tree

```
before/
└── auth.ts                 ← 800 lines, multiple concerns

after/
└── auth/
    ├── index.ts            ← public API, 30 lines
    ├── login.ts            ← 200 lines
    ├── signup.ts           ← 200 lines
    ├── token-refresh.ts    ← 150 lines
    └── types.ts            ← 80 lines
```
