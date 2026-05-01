```
my-app/
├── package.json
├── next.config.js
├── tsconfig.json
├── README.md
├── .gitignore
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── globals.css
│   ├── api/
│   │   └── hello/route.ts
│   └── (marketing)/
│       └── about/page.tsx
├── components/
│   ├── ui/                       ← presentational, reusable
│   └── feature/                  ← feature-specific, composed
├── lib/                          ← non-component utilities
│   ├── db.ts
│   └── auth.ts
├── public/                       ← static, served as-is
│   └── favicon.ico
└── styles/                       ← if not all in app/globals.css
```
