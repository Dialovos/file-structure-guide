# One-purpose-per-directory template

A side-by-side layout: three "good" directories named by their single purpose,
and one "bad" directory (`bad-utils/`) showing what happens when unrelated
code is dumped into a junk drawer.

## What's here

- `good-string-formatting/format.ts` — string display helpers, nothing else.
- `good-date-parsing/parse.ts` — calendar parsing helpers, nothing else.
- `bad-utils/everything.ts` — a single file mixing string, date, HTTP, and auth concerns. The header comment explains why it is wrong.

The directory names use a `good-` / `bad-` prefix only so the contrast is
visible in a flat listing. In a real project, drop the prefixes; the directory
names would simply be `string-formatting/`, `date-parsing/`, etc.

## To adopt this template

1. Copy each `good-*/` directory under your `src/` (renaming to drop the `good-` prefix): `cp -r template/good-string-formatting/ src/string-formatting/`.
2. Each peer directory is independently testable. Add `*.test.ts` files alongside.
3. Resist the urge to create a `utils/` next to them when the next file doesn't obviously belong. Instead, write the file's single-sentence purpose; that sentence names the next peer directory.
4. Delete `bad-utils/` before shipping. It exists only to demonstrate the anti-pattern.

## Acceptance test

Before declaring this layout adopted, ask of every directory you added: *"Can I describe what's in here in one sentence with no 'and'?"* If yes, the rule holds. If no, split.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this `template/README.md` to exist. Don't delete it before replacing.
