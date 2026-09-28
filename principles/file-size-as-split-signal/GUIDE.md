# File size as a split signal

## TL;DR

When a single file grows past roughly **500 lines**, treat that as a *signal* — not a hard rule — that it wants to become a directory. The number is heuristic; the underlying smell is "this file is doing more than one thing." Two stronger smells co-occur with the line count: multiple distinct responsibilities in one module, and visible "section comments" (`// === Login ===`, `// --- helpers ---`) used to navigate it. When you see those, lift each section into its own module under a directory named after the original file.

## Principles & why

The 500-line threshold is calibrated to two facts about reading code. First, most editors and code-review tools display roughly 30-60 lines at a time; once a file's logical units stop fitting in a single screen, you start scrolling and lose context. Second, most languages let you reasonably express one cohesive responsibility in 100-300 lines. When you've blown past that on a single file, statistically you're holding two or three responsibilities together by gravity.

Splitting a too-large file into a directory pays compound interest. Each smaller file has a focused name (`auth/login.ts`, not "the part of `auth.ts` that handles login"), so finding the relevant code is a directory lookup instead of a scroll-and-search. Each file gets independent test coverage, version history, ownership lines, and code-review attention. Cross-cutting concerns become real imports, which forces you to think about whether they should be there.

The threshold is a *signal*, not a *rule*, because some files genuinely need to be large: a complex algorithm whose correctness depends on a single dense control flow, a generated lookup table, a schema definition, a state-machine definition. Those files don't suffer from the same cognitive load — there's still only one thing happening. The right test is "are there multiple concerns interleaved?" Line count is just the first indicator that points your attention there.

## When to use

Reach for the split when *any* of these are true:

- The file is **>500 lines** and growing.
- The file contains **section comments** organising it into named regions (`// === Login ===`, `// --- Token refresh ---`, `// === Helpers ===`). Those are markers a future you wrote because the file was already too big to navigate.
- The file has **multiple distinct responsibilities** — e.g. login, signup, and token refresh all in one `auth.ts`. Each is a coherent unit on its own.
- The **import surface** of the file is heterogeneous — different functions inside the file import disjoint sets of dependencies. That's a sign the functions don't really belong together.
- **Multiple contributors edit the file in unrelated PRs** repeatedly, causing merge conflicts. The file is a coordination point for things that don't share concerns.
- The **public API of the file** is many independent surfaces (`login`, `signup`, `refreshToken`, `validatePassword`, `hashPassword`, `verifyEmail` ...) rather than one cohesive surface plus its helpers.

## When NOT to use

Some files are large because they need to be. Splitting them makes things worse:

- **Generated code** — schemas, parser tables, protobuf output, OpenAPI clients. Splitting a generated file means owning a fork of the generator.
- **Schema or constant definitions** — a 1500-line `schema.sql`, an enum of 800 country codes, a config file. The bulk is data, not logic; there's nothing to split into.
- **Single-function complex algorithms** — a 600-line implementation of a tricky algorithm where the logic is necessarily interleaved (a parser, a sophisticated solver). Splitting it spreads correctness across files, which is harder to reason about than one long file.
- **Lookup tables / fixtures** — `lookups/timezone-offsets.ts` with 600 mapping entries. Move it to a JSON file or leave it; don't split it into `lookups/timezone-offsets/{a-h,i-r,s-z}.ts`.
- **Test files that legitimately enumerate many cases** — a 700-line table-driven test exhaustively covering a small function's edge cases. Splitting fragments coverage; collapse with table-driven helpers if it's painful.

The litmus test: "after splitting, is each new file *cohesive on its own*, or does it still depend tightly on the others?" If still tight, the split was wrong.

## Tree diagram

```
before/
└── auth.ts                 ← 800 lines, multiple concerns

after/
└── auth/
    ├── index.ts            ← public API, 30 lines
    ├── login.ts            ← 200 lines
    ├── signup.ts           ← 200 lines
    ├── token-refresh.ts    ← 150 lines
    └── types.ts            ← 80 lines
```

## Naming rules

1. **The directory inherits the original file's name** (`auth.ts` -> `auth/`). Imports that previously read `from './auth'` keep working with most module resolvers, because resolving `./auth` finds either `auth.ts` or `auth/index.ts`.
2. **`index.ts`** (or `__init__.py`, `mod.rs`, `lib.rs`) **is the public re-export surface.** Keep it tiny — a flat list of `export { X } from "./x"`. No logic. Readers should be able to scan the index and see the module's surface in 30 lines or less.
3. **Each split file is named after its concern**, not its type. `login.ts`, `signup.ts`, `token-refresh.ts` — not `handlers.ts`, `helpers.ts`, `utils.ts`. Type-named files are usually a sign the split was lazy and the concerns weren't actually identified.
4. **Shared types and helpers go in `types.ts`** (interfaces, enums) and `internal.ts` or `shared.ts` (functions used across the module's files but not exported externally). Don't sprawl into ten utility files.
5. **Keep the split shallow.** One level of subdirectory. If `auth/login/` is itself becoming a directory, that's a second iteration of the same rule, not a deeper hierarchy from day one.
6. **Update imports atomically** in the same commit as the split, or stage them in a single PR. Don't leave the codebase half-migrated.

## Worked example

`auth.ts` is 812 lines. It contains login, signup, token refresh, and a block of types, separated by comments like `// === Token refresh ===`.

1. Confirm the smell: `wc -l auth.ts` and `grep -n '^// ===' auth.ts`. Section comments are the split lines.
2. Create `auth/` and move one section at a time: `login.ts`, `signup.ts`, `token-refresh.ts`, `types.ts`. Run the tests after each move.
3. Add `auth/index.ts` that re-exports only the public API. Callers keep importing from `./auth`, so nothing outside the directory changes.
4. Delete the section comments; the filenames replaced them.
5. Commit each move separately so history stays reviewable.

Result: five files of 30 to 200 lines, and a file-level diff for a login change no longer touches token code.

## Anti-patterns

- **Splitting too eagerly.** A 200-line file with one cohesive responsibility doesn't need a directory. The threshold isn't 200; it's the smell of multiple concerns plus the line count.
- **Splitting by file *type* instead of concern.** `controllers.ts`, `services.ts`, `helpers.ts`, `utils.ts` — that's the *opposite* mistake from a too-big single file. You've spread one concern across many type-shaped files. (See `principles/naming-by-purpose-not-type/`.)
- **Empty `index.ts`** that re-exports nothing. The directory should expose the module's public surface; an empty index forces every consumer to know the internal layout.
- **`index.ts` with logic in it.** The whole point is that the index is a flat re-export. Logic belongs in named sibling files.
- **Half-migration.** `auth.ts` deleted, `auth/login.ts` and `auth/signup.ts` created, but token refresh still copy-pasted in three callers because nobody finished the refactor. Either complete the split or revert.
- **Fighting the threshold with sub-thresholds.** Inventing rules like "split at 200 lines" makes most reasonable code split unnecessarily. 500 is calibrated against real codebases; pick a different number only with intent.

## Scaling & failure modes

- **The number is a signal, not a rule.** A 900-line generated parser or a flat table of constants can be fine. The trigger is multiple responsibilities, not the count.
- **Splitting too early** produces `auth/` folders with three 20-line files and an index that only re-exports them. Wait for the second responsibility.
- **Cyclic imports** appear when sections shared private helpers. Extract those into their own module before moving anything.
- **Large test files** follow the same rule; split by behavior under test, not by test type.

## Variants

- **200-line threshold (very strict).** Some teams (often functional-programming heavy, or working in highly modular Lisp/Clojure styles) keep files under 200 lines. Encourages small modules; risks fragmentation and over-imports.
- **500-line (this repo's heuristic).** A pragmatic compromise: catches most "this file is doing too much" cases without forcing premature splits.
- **No fixed threshold; cohesion-rules-only** (Robert Martin / "Clean Code" school). Split when there are multiple reasons to change the file, regardless of size. More principled but harder to enforce mechanically; tends to produce files of wildly varying length.
- **1000+ lines acceptable for stable, low-churn modules.** Some long-lived modules in stdlib codebases reach 1000-2000 lines because they're stable and the unit is genuinely cohesive. Acceptable for low-churn code; don't aim for it.
- **Linter-enforced threshold.** Tools like `max-lines` (ESLint), `max-file-size` (custom), or repo-level CI checks that fail builds on files over a threshold. Useful as a tripwire; pair with an "ignore" mechanism for legitimately-large files (generated code, fixtures).

## Adoption checklist

- [ ] `git ls-files '*.ts' | xargs wc -l | sort -rn | head` has been reviewed this quarter and each file over ~500 lines has a stated reason to stay.
- [ ] Each split keeps a single public entry point (`index.*`) so callers don't change.
- [ ] Section-divider comments inside files are treated as split candidates.
- [ ] Tests still pass after every individual move, not only at the end.

## Real-world projects using this

- **Linus Torvalds and the Linux kernel** — repeatedly cited the principle of splitting kernel files when they "get too big to think about." The kernel tree shows the pattern: subsystems start as single files, grow into directories with focused submodules.
- **Martin Fowler's *Refactoring*** — "Extract Class" is the codified refactor for this signal. The 1999 (and 2018) editions both name "Large Class" / "Long Method" as code smells with extract-class as the response.
- **VS Code (`microsoft/vscode`)** — its `src/vs/editor/` and `src/vs/workbench/` trees are full of former-monolith files that became directories over years (`editor.ts` -> `editor/`, `workbench.ts` -> `workbench/`).
- **TypeScript compiler (`microsoft/TypeScript`)** — `src/compiler/checker.ts` is the famous counter-example: a 50,000-line single file deliberately *not* split, because the type-checking algorithm's correctness depends on tight coupling. It's the "single complex algorithm" exception in its purest form.
- **React (`facebook/react`)** — has gone through multiple rounds of splitting `ReactDOM.js`, `Reconciler.js`, etc. into subdirectories as features were added.
- **Django (`django/django`)** — `django/contrib/admin/options.py` was split out into the modern `admin/` package over several major versions; the history demonstrates the iterative split-when-it-hurts pattern.

## Migration & references

To find candidates in your repo:

```bash
# 1. Find files over the threshold (tweak 500 to taste).
find . -type f \( -name '*.ts' -o -name '*.js' -o -name '*.py' -o -name '*.rs' \) \
  -not -path '*/node_modules/*' -not -path '*/dist/*' -not -path '*/target/*' \
  | xargs wc -l 2>/dev/null \
  | awk '$1 > 500 && $2 != "total" {print}' \
  | sort -nr

# 2. For each candidate, look for section comments — the secondary smell.
grep -nE '^[[:space:]]*//[[:space:]]*={3,}|^[[:space:]]*#[[:space:]]*={3,}|^[[:space:]]*//[[:space:]]*-{3,}' path/to/big-file.ts
```

The mechanical refactor:

```bash
# Suppose auth.ts is 800 lines with === Login ===, === Signup ===, === Token refresh === sections.
mkdir -p src/auth

# Move the original aside; you'll cannibalise it.
git mv src/auth.ts src/auth/_original.ts

# Create one file per section, copying the relevant lines.
# (Manual step: open _original.ts in your editor, cut out each section.)
touch src/auth/login.ts src/auth/signup.ts src/auth/token-refresh.ts \
      src/auth/types.ts src/auth/index.ts

# After splitting, _original.ts should be empty. Delete it.
rm src/auth/_original.ts

# Update src/auth/index.ts to re-export the public surface:
# export { login } from "./login";
# export { signup } from "./signup";
# export { refreshToken } from "./token-refresh";

# Update imports across the rest of the codebase. Most module resolvers
# treat `from "./auth"` as either `./auth.ts` or `./auth/index.ts`, so
# call sites don't need to change.

# Verify tests still pass, then commit as a single refactor.
git add src/auth/
git commit -m "refactor: split auth.ts into auth/ directory by concern"
```

Further reading:

- *Refactoring* (Martin Fowler, 2nd ed., 2018) — Chapter 3 "Bad Smells in Code" and Chapter 7 "Encapsulation" formalise the signal and the response.
- *Working Effectively with Legacy Code* (Michael Feathers) — chapters on identifying seams in oversized classes; same principle applied to legacy refactors.
- `principles/one-purpose-per-directory/` — sibling rule. After the split, the new directory should follow it.
- `principles/naming-by-purpose-not-type/` — informs naming the split files (`login.ts`, not `handlers.ts`).
- `principles/depth-vs-breadth/` — keep the resulting directory shallow.
