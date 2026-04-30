# naming-by-purpose-not-type — canonical tree

```
purpose-driven (good)/
├── customer-onboarding/
│   ├── form.tsx
│   ├── api.ts
│   └── types.ts
└── billing/
    ├── invoice.tsx
    ├── api.ts
    └── types.ts

type-driven (bad)/
├── forms/
│   ├── customer-onboarding.tsx
│   └── invoice.tsx
├── api/
│   ├── onboarding.ts
│   └── billing.ts
└── types/
    ├── onboarding.ts
    └── billing.ts
```
