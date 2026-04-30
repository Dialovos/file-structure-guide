# test-colocation-vs-separation — canonical tree

```
separated (Python-style)/
├── src/
│   └── myapp/
│       ├── auth.py
│       └── billing.py
└── tests/
    ├── test_auth.py
    └── test_billing.py

co-located (JS/Go-style)/
└── src/
    ├── auth.ts
    ├── auth.test.ts
    ├── billing.ts
    └── billing.test.ts
```
