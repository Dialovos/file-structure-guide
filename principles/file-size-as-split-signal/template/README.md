# File-size-as-split-signal template

This template ships a *before* and *after* of one module: a single
oversized file with section-comment markers, then the same module split
into a directory of focused files.

## What's here

```
template/
├── README.md
├── before/
│   └── single-large-file.ts        ← stub showing the smell
└── after/
    └── single-large-file/
        ├── index.ts                ← re-export surface
        ├── concern-a.ts            ← extracted "// === Login ===" section
        └── concern-b.ts            ← extracted "// === Signup ===" section
```

## The "before" file

`before/single-large-file.ts` is intentionally short (~50 lines) but
illustrates the *structural* problem the policy targets. It contains
three section markers (`// === Login ===`, `// === Signup ===`, `// ===
Token refresh ===`) — and those markers are the smell. When a file
needs section comments to be navigable, the file is asking to become
a directory.

In a real codebase, the same shape commonly shows up at 500-1000 lines.
The line count is the secondary signal; the section-comment pattern is
the primary one.

## The "after" directory

`after/single-large-file/` shows the same module split:

- `index.ts` — flat list of re-exports, no logic. Consumers continue to
  import from `single-large-file` and the resolver picks up
  `single-large-file/index.ts` automatically.
- `concern-a.ts` — the former "Login" section, extracted into its own
  file with its own types, one focused responsibility.
- `concern-b.ts` — the former "Signup" section, same treatment.

For brevity the template stops at two extracted files; in the worked
example in the GUIDE.md `before/auth.ts` (800 lines) becomes
`after/auth/{login,signup,token-refresh,types,index}.ts`.

## Why "concern-a" instead of "login"?

Real refactors should rename to the concern (`login.ts`, `signup.ts`),
not the position (`concern-a.ts`, `concern-b.ts`). We use the generic
names in the template *only* to keep the pairing visually obvious for
readers comparing the before/after side by side. When you adopt the
pattern in your project, follow `principles/naming-by-purpose-not-type/`
and use real concern names.

## When *not* to follow this template

If the file you're looking at is large because:

- It's generated code (parser tables, protobuf output, schema dumps).
- It's a single complex algorithm whose correctness depends on tight
  control flow (a parser, a sophisticated solver).
- It's a lookup table or fixture (timezone offsets, country codes).
- It's a test file with table-driven cases legitimately enumerating
  edge cases.

… then leave it alone. The split signal is "multiple concerns
interleaved," not "many lines."

## To adopt this template

1. Identify candidate files in your codebase. The GUIDE.md ships a `find
   | wc -l | awk` snippet to surface files over 500 lines.
2. For each candidate, look for section comments — those are the
   strongest single indicator that the file wants to split.
3. Create a same-named directory and an `index.ts` (or `__init__.py`,
   `mod.rs`) re-export surface.
4. Move each concern into its own file, named after the concern, not
   its type. Update the index re-exports.
5. Run your test suite. Most call sites won't need changes if the
   resolver picks up the directory's index.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this
`template/README.md` to exist. Don't delete it before replacing.
