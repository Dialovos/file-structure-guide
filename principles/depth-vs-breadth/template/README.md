# Depth-vs-breadth template

Two trees side by side: a shallow good example and a deliberately-too-deep
counter-example.

## What's here

- `shallow-example/` — three peer directories (`auth/`, `billing/`) at one level. Leaf depth is 2 (template root → feature dir → file). This is the shape to copy.
- `deep-counter-example/a/b/c/d/e/` — five empty wrapper directories nested inside each other. Nothing meaningful lives at the bottom. The wrappers are doing no work; this is the shape to refactor away from.

## Why the counter-example matters

Reading `a/b/c/d/e/.gitkeep` requires loading five context labels just to find a stub. In a real project the equivalent is `src/main/app/modules/feature/components/forms/login.ts` — eight levels for a single component. Each level was probably added "to keep things organised", but the cumulative cost is borne on every traversal.

## To adopt this template

1. Copy `shallow-example/` as your starting point: `cp -r template/shallow-example/ <your-target>/src/`.
2. Rename `auth/` and `billing/` to whatever your real top-level concerns are. Keep the depth: peers, not children.
3. Resist adding a wrapper around them ("just to group the features"). If you find yourself wanting one, the right move is usually to split a peer into two peers, not to add depth.
4. Delete `deep-counter-example/` before shipping. It exists only to demonstrate the anti-pattern.

## When to keep some depth

If your ecosystem requires it (Maven's `src/main/java/com/example/...`, Python's `src/<package>/__init__.py`), follow the ecosystem rule. Add a one-line note to the project's `README.md` explaining why the depth is non-negotiable.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this `template/README.md` to exist. Don't delete it before replacing.
