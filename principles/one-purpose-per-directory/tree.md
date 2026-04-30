# one-purpose-per-directory — canonical tree

```
good/
├── string-formatting/
├── date-parsing/
├── http-retry/
└── auth-tokens/

bad/
└── utils/
    ├── format_string.ts
    ├── parse_date.ts
    ├── retry_http.ts
    └── token_helpers.ts
```
