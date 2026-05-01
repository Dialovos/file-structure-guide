```
my-app/
├── package.json
├── README.md
├── src/
│   ├── app/                                ← Next.js routes / Vite entry
│   ├── features/
│   │   ├── customer-onboarding/
│   │   │   ├── components/
│   │   │   │   ├── OnboardingForm.tsx
│   │   │   │   └── ProgressIndicator.tsx
│   │   │   ├── api/
│   │   │   │   └── onboarding-client.ts
│   │   │   ├── hooks/
│   │   │   │   └── useOnboardingState.ts
│   │   │   ├── types.ts
│   │   │   └── index.ts                    ← public API
│   │   └── billing/
│   ├── components/                         ← cross-feature shared UI
│   │   └── ui/
│   ├── lib/                                ← cross-feature utilities
│   └── types/                              ← global types
└── tests/
```
