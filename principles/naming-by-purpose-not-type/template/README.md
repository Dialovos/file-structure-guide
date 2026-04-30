# Naming-by-purpose-not-type template

Two trees in one template: a `purpose/` tree showing the good shape, and a
`bad-by-type/` tree showing what type-driven layout looks like at the same
scale.

## What's here

- `purpose/customer-onboarding/{form.tsx,api.ts,types.ts}` — one feature, one directory, three peer files. Each names a *kind* (form, api, types) but the *directory* names the purpose.
- `purpose/billing/invoice.tsx` — the second feature, same shape.
- `bad-by-type/forms/customer-onboarding.tsx` — the same form, but living in a `forms/` bucket. Header comment explains why the layout is wrong.

## To adopt this template

1. Copy the `purpose/` directory contents under your `src/`: `cp -r template/purpose/* src/`.
2. Each top-level dir is one feature. Add files inside named by *type at the leaf* (`form.tsx`, `api.ts`, `types.ts`, `*.test.ts`, etc.).
3. Resist creating top-level `forms/`, `api/`, `types/`, `components/`. The moment one of these appears, you're back in type-driven territory.
4. Delete `bad-by-type/` before shipping. It exists only to demonstrate the anti-pattern.

## When the leaf goes type-shaped

Inside a purpose directory, leaf filenames can absolutely be type-shaped — that's the right level for "what is this file". The rule is at the *directory* level only.

```
customer-onboarding/
├── form.tsx       ← leaf names a type, fine
├── api.ts         ← leaf names a type, fine
├── types.ts       ← leaf names a type, fine
└── form.test.ts   ← test next to subject, fine
```

## Acceptance test

After adopting, ask: *"To delete this feature entirely, how many directories do I touch?"* Purpose-driven answer is one (`rm -rf customer-onboarding/`). Type-driven answer is three or more. If your answer is three, refactor.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this `template/README.md` to exist. Don't delete it before replacing.
