# One purpose per directory

## TL;DR

A directory should answer exactly one question. The moment you reach for `utils/`, `misc/`, `helpers/`, `common/`, or `lib/` as a destination, you've stopped naming and started avoiding. Replace those buckets with directories that name what their contents *do*: `string-formatting/`, `date-parsing/`, `http-retry/`, `auth-tokens/`. If you can't name the directory by its purpose, you don't yet understand what's in it.

## Principles & why

A directory name is a contract with future readers: "everything inside answers this question." Junk-drawer names — `utils`, `misc`, `helpers`, `core`, `common` — break that contract by promising "everything else", which is no promise at all. The reader has to open every file inside before they know whether to keep looking.

The cost compounds. Junk drawers attract junk. Once a `utils/` exists, the path of least resistance for any new file that doesn't fit elsewhere is to drop it in `utils/`. Six months later the directory has 80 files spanning seven domains, no internal hierarchy, and three different `format()` functions that do unrelated things. Splitting it costs more than naming it correctly the first time.

The deeper principle is *cohesion*: things that change together live together. A directory of cohesive code can be tested as a unit, owned by one team, deleted in one move. A junk drawer can do none of those — its files are coupled to seven different parts of the system, so any reorganisation ripples everywhere. Naming by purpose forces you to find the cohesion before you write the import path.

## When to use

Always — this is the default. Apply it on every directory creation:

- Before creating a new directory, write its single-sentence purpose. If the sentence contains "and", "various", "miscellaneous", or "stuff", split it.
- When a feature dir grows past ~10 files and they don't all serve the same question, split it into peers named by purpose.
- When you find yourself reaching for `utils/`, write down what the file *does* and use that as the directory name instead.
- During code review, flag any new file landing in `utils/`, `misc/`, `helpers/`, or `common/` and ask the author to name the purpose.

This rule pairs with breadth-over-depth: peers named by purpose stay shallow because each peer is independently meaningful.

## When NOT to use

A few cases tolerate purpose-less names without harm:

- **Type-only declarations** — a `shared/types/` dir with nothing but `.d.ts` files is fine because the type *is* the purpose. The trap to avoid is letting it grow runtime code.
- **Build / vendor / generated content** — `dist/`, `build/`, `vendor/`, `node_modules/`. The tool defines the purpose; the directory name is a tooling contract, not a human-readable label.
- **Single-file proxy dirs** — sometimes a feature is genuinely one file (`telemetry.ts`); skip the directory entirely. Don't create `telemetry/` just for symmetry.
- **One genuine `shared/`** — many projects accept exactly one `shared/` for code with no domain (logger, config loader). The discipline is "one, no more"; the moment a second appears, the rule has failed.

Even in those cases, the test is "can I write the purpose in one sentence". `shared/` passes only if the sentence is "primitives with no domain attachment", and you'll defend that line.

## Tree diagram

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

## Naming rules

1. The directory name must complete the sentence "Everything in here is about ___." If you can't fill the blank in five words or less, the directory is too broad.
2. Forbid `utils/`, `misc/`, `helpers/`, `common/`, `core/`, `stuff/`, `things/`, `extras/` as new directory names. They're symptoms, not designs.
3. Prefer noun phrases that describe a domain (`auth-tokens/`, `pdf-rendering/`) over verb phrases that describe an action (`do-things/`).
4. When two purpose names overlap (`auth/` and `auth-tokens/`), the more specific one wins; merge or rename to clarify the boundary.
5. Use kebab-case for the directory name (`http-retry/`, not `httpRetry/` or `HTTPRetry/`) unless the ecosystem mandates otherwise.
6. If a directory's purpose changes, rename it in a single commit. Don't let the old name persist out of inertia — it lies to readers.

## Anti-patterns

- **`utils/` as default destination** — the canonical junk drawer. Once it exists, every "I don't know where this goes" file lands there.
- **`helpers/` next to a feature** — implies the feature has a "main" part and a "helper" part, but the helper has no name of its own. Name it.
- **`common/` shared by everything** — reads as "everything depends on this", which is a structural smell. Cohesive shared code has a domain (`logging/`, `config/`).
- **`core/` for the bits the author cares about** — `core` means "important", which is opinion, not purpose. Rename to the actual function (`engine/`, `runtime/`, `dispatch/`).
- **Numbered or ordinal dirs** — `utils1/`, `helpers-old/`, `misc-backup/`. The number is admitting the original name didn't work; rename properly.
- **Personal-name dirs** — `bobs-stuff/`, `legacy-from-jane/`. Code outlives ownership; the dir name should describe the code, not its author.

## Variants

- **Strict purpose-only** (this repo's bias) — no util-style dirs allowed anywhere. Forces every dir to earn its name. Highest discipline, highest payoff.
- **Pragmatic single-shared** — exactly one `shared/` per project for genuinely domain-free primitives (logger, config). Two `shared/` directories means the rule failed.
- **Feature-vertical** — every directory is a feature; "purpose" is the feature, and inside it you find code, tests, and types together. Strongly purpose-driven by construction.
- **Domain-driven (DDD)** — purpose maps to a *bounded context*; each top-level dir is a context with its own model, language, and team. The strongest version of this principle.
- **Layer-then-purpose hybrid** — top-level by layer (`api/`, `domain/`, `infra/`), purpose inside each layer (`api/auth-tokens/`). Common in Hexagonal/Clean architectures; the layer is the type, the purpose is the leaf.

## Real-world projects using this

- **Bulletproof React** — its `src/features/<feature>/` layout is a textbook application of the rule: every feature is a purpose, no util/misc dumping ground at the feature level.
- **kubernetes/kubernetes** — `pkg/<area>/` directories (e.g. `pkg/scheduler/`, `pkg/kubelet/`) each name a single concern; cross-cutting code is in named packages (`pkg/util/<specific>/`), never a bare `util/`.
- **Domain-Driven Design (Eric Evans)** — the bounded-context concept *is* this rule formalised at the architecture level.
- **prettier/prettier** — `src/language-js/`, `src/language-css/`, `src/language-markdown/` are purpose-named language directories with no shared `utils/`.
- **rust-lang/rust** compiler — `compiler/rustc_*` crates name their purpose (`rustc_parse`, `rustc_lexer`, `rustc_ast`); the crate name *is* the purpose.
- **vercel/next.js** — `packages/next/src/server/`, `packages/next/src/client/`, etc., split by execution context (a clear purpose), not by file type.

## Migration & references

To migrate an existing `utils/` directory:

```bash
# 1. List what's actually in there
ls -1 src/utils/

# 2. Group by purpose on paper, then move file-by-file
git mv src/utils/format_string.ts src/string-formatting/format.ts
git mv src/utils/parse_date.ts src/date-parsing/parse.ts
git commit -m "refactor: split utils/ by purpose (string-formatting, date-parsing)"

# 3. Fix imports
git grep -l "from '.*utils/format_string'" -- '*.ts' \
  | xargs sed -i "s|utils/format_string|string-formatting/format|g"
git commit -m "refactor: update imports for string-formatting move"

# 4. Repeat per group; delete utils/ when empty
rmdir src/utils
git commit -m "chore: drop empty utils/ after split"
```

Further reading:

- *Domain-Driven Design* (Eric Evans, 2003), Part II — bounded contexts as the formal version of "one purpose per dir".
- *Clean Architecture* (Robert C. Martin), §"Screaming Architecture" — your top-level dirs should scream what the system does, not what framework it uses.
- `principles/depth-vs-breadth/` — sibling rule: peers-by-purpose stay shallow; nested-by-type goes deep fast.
- `principles/naming-by-purpose-not-type/` — applies the same idea but to *what to name* dirs once you've decided to split.
- Bulletproof React project structure (https://github.com/alan2207/bulletproof-react) — practical application in TypeScript.
