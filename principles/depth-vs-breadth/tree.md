# depth-vs-breadth — canonical tree

```
shallow-good/
├── auth/
│   ├── login.ts
│   └── signup.ts
├── billing/
│   ├── invoices.ts
│   └── payments.ts
└── reports/
    └── monthly.ts

deep-bad/
└── src/
    └── main/
        └── app/
            └── modules/
                └── auth/
                    └── components/
                        └── forms/
                            └── login.ts   ← 8 levels
```
