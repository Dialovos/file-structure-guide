# Naming by purpose, not type

## TL;DR

Group files by what they *do* together, not by what they *are*. `customer-onboarding/` (with its form, API client, and types) beats `forms/`, `api/`, `types/` (with onboarding files scattered across all three). Purpose-driven layouts let a feature be deleted, moved, or owned in one move; type-driven layouts force every change to ripple through three parallel directories.

## Principles & why

A change to "customer onboarding" almost never lands in just one file type. You touch the form, you touch the API call it makes, you touch the type that flows between them. A type-driven layout (`forms/`, `api/`, `types/`) puts those three files in three different directories — every meaningful change becomes a multi-directory diff. A purpose-driven layout (`customer-onboarding/`) puts them next to each other, and the diff localises.

Co-location reduces *cognitive load*. When you open `customer-onboarding/`, everything onboarding is right there. When you open `forms/`, you see a hundred unrelated forms; you scroll past 99 to find the one you want, and the form's API and types are in two other directories you also have to open. The number of directories you must traverse to understand one feature is the metric to minimise.

Co-location also reduces *blast radius*. Deleting "customer onboarding" is `rm -rf customer-onboarding/` — one command, no orphan files. In a type-driven layout, deletion means hunting through three directories and hoping you found every reference. The probability of leaving dead code behind is much higher.

The deeper observation is that *types* are an attribute of files; *purpose* is an attribute of features. Filesystems should mirror the unit of change, and the unit of change is almost always a feature, not a file type.

## When to use

Apply this whenever code evolves as a feature:

- Application code (web apps, mobile apps, internal tools) — always purpose-first.
- Notes / knowledge bases — group by topic, not by note type (don't put all your meeting notes in `meetings/` and all your decisions in `decisions/` if both pertain to the same project).
- Service layers in microservice repos — each service is a purpose; its files are scoped to that purpose.
- Monorepos — top-level dirs by product or service (purpose), with internal layout per package.
- Whenever you find yourself naming a directory after a *layer* (`controllers/`, `models/`) or a *kind* (`forms/`, `widgets/`), check whether a feature name would serve readers better.

## When NOT to use

A few cases legitimately group by type:

- **Foundational libraries** where the "purpose" *is* the type. `lodash` groups by data-structure (`array/`, `object/`, `string/`) because that's its product. The type is the purpose.
- **Standard libraries in flat languages** — Go's `net/`, `os/`, `io/`, `fmt/` are by-type because the language ships small, narrowly-scoped packages. Within an application built on top of Go, you still go by purpose.
- **Generated code** — `proto/`, `openapi-generated/`, `migrations/`. The generator's output is type-shaped; let it be.
- **Strict layered architectures (legacy MVC)** where `controllers/`, `models/`, `views/` is a contract with the framework (older Rails, older Django apps). Modern variants of these frameworks have shifted toward purpose-style modules.

When you do go by type, do it deliberately. The signal that you're abusing it: you find yourself touching N files in N different `*/`-style dirs to make one feature change.

## Tree diagram

```
purpose-driven (good)/
├── customer-onboarding/
│   ├── form.tsx
│   ├── api.ts
│   └── types.ts
└── billing/
    ├── invoice.tsx
    ├── api.ts
    └── types.ts

type-driven (bad)/
├── forms/
│   ├── customer-onboarding.tsx
│   └── invoice.tsx
├── api/
│   ├── onboarding.ts
│   └── billing.ts
└── types/
    ├── onboarding.ts
    └── billing.ts
```

## Naming rules

1. Top-level directory names are *nouns describing a concern*, not nouns describing a kind: `customer-onboarding/`, not `forms/`.
2. Inside a purpose dir, file names *can* be type-shaped (`form.tsx`, `api.ts`, `types.ts`) — that's where types belong.
3. The opposite of "by type" is not "no types"; it's "type at the leaf, purpose at the directory".
4. Avoid framework-generic dir names (`components/`, `services/`, `utils/`) at the top level. They make every project look the same and obscure what the project actually does.
5. Two purposes that share files should either merge or extract a shared subset (`shared/auth-tokens/`), but never grow a `common/` junk drawer.
6. If a project has both purpose dirs and type dirs at the same level (`customer-onboarding/` and `forms/`), pick one and refactor — mixed shells are the worst case.

## Worked example

A React app has `components/`, `api/`, `types/`, and onboarding code is spread across all three.

1. Pick one feature and list every file that changes when it does: `git log --name-only --since=3.months -- '*onboarding*' | sort | uniq -c | sort -rn`.
2. Create `customer-onboarding/` and move that feature's files: `form.tsx`, `api.ts`, `types.ts`.
3. Rewrite imports with your editor's rename support and run the type checker.
4. Leave genuinely shared building blocks (design-system buttons) in a small `shared/` named by role, not by type.
5. Repeat for the next feature, one PR per feature.

Deleting the feature now means deleting one directory, and a code review for it touches one folder.

## Anti-patterns

- **Top-level `controllers/` `models/` `views/`** — classic MVC type-driven layout. Every feature is split across three directories. Migrate to feature folders.
- **`components/`, `services/`, `utils/`, `hooks/`** at the top of a React/Vue project — framework-generic, purpose-empty. Bulletproof React's `features/` is the canonical refactor target.
- **Database-shaped dirs** — `schemas/`, `models/`, `migrations/`, `tables/` — fine for genuine ORM-output, but if your application code mirrors them, you're naming by type.
- **`pages/` containing every route as a peer** — same problem as `forms/`. Move the route file inside its purpose dir, or use a router that supports per-feature routing.
- **`tests/` mirror at the top level** — tests live next to what they test, in the same purpose dir. A separate top-level `tests/` mirror creates two parallel trees you must keep in sync.
- **Per-language dirs (`ts/`, `tsx/`, `css/`)** — type-driven by file extension. The compiler doesn't care; readers are punished.

## Scaling & failure modes

- **Shared code** is where the rule strains. Promote code to `shared/` only after a second feature needs it, and name it for what it does (`date-formatting/`), not what it is (`utils/`).
- **Framework conventions** (Rails `models/`, Django apps) impose type-first structure at the top; apply purpose grouping inside your own layer.
- **Cross-cutting concerns** (logging, auth middleware) don't belong to one feature; give each its own purpose-named directory.
- **Team ownership** maps naturally to purpose directories, which makes CODEOWNERS entries short.

## Variants

- **Pure-purpose** (this repo's bias) — every directory names a purpose; types live only at the leaf as filenames.
- **Hybrid: top-level by purpose, leaf-level by type** — `customer-onboarding/{forms,api,types}/`. Useful when a single purpose has dozens of forms or APIs and the leaf-level type split aids navigation.
- **Strict-by-type (legacy MVC)** — `controllers/`, `models/`, `views/`. Common in older Rails / Django / ASP.NET. Recognise it; only adopt it when the framework forces you.
- **Layered (Hexagonal / Clean / Onion)** — `domain/`, `application/`, `infrastructure/`, with purpose nested inside each layer. Layer is "type-of-architecture-role"; purpose is the leaf concern. Heavyweight but explicit about dependency direction.
- **Slice-and-layer combo (Vertical Slice Architecture)** — top-level by feature (purpose), each feature internally has its own layers. Co-location wins; layered discipline preserved.

## Adoption checklist

- [ ] Removing one feature is possible by deleting one directory (plus registry entries).
- [ ] No top-level `utils/`, `helpers/`, `misc/`, or `common/`.
- [ ] Shared modules were extracted after their second consumer, not before.
- [ ] Directory names describe a capability a product person would recognize.

## Real-world projects using this

- **Bulletproof React** (`alan2207/bulletproof-react`) — the canonical `src/features/<feature>/` layout, where each feature owns its `api/`, `components/`, `types/`, `hooks/`. Hybrid (top-purpose, leaf-type).
- **Domain-Driven Design (Eric Evans)** — bounded contexts are this rule applied at the architecture level: each context names a *domain purpose*, and types live inside it.
- **Rails 6+ engines / components** — `engines/<feature>/` patterns shift from rails default `app/controllers/` toward feature-vertical layout.
- **Kubernetes** — `cmd/<binary>/` is per-purpose top-level: `cmd/kubectl/`, `cmd/kubelet/`, `cmd/kube-apiserver/`. Each has its own everything.
- **vercel/next.js app router** — `app/<route>/page.tsx` co-locates UI, layout, and route loader per route segment (a purpose).
- **golang/go cmd/** — `src/cmd/go/`, `src/cmd/gofmt/`, etc., each a purpose-named top-level binary.

## Migration & references

To refactor a type-driven layout to purpose-driven:

```bash
# 1. Pick a single feature; inventory its files
git ls-files | grep -E '(forms|api|types)/.*onboarding' \
  > /tmp/onboarding-files.txt

# 2. Move them into a single purpose dir
mkdir src/customer-onboarding
git mv src/forms/customer-onboarding.tsx src/customer-onboarding/form.tsx
git mv src/api/onboarding.ts src/customer-onboarding/api.ts
git mv src/types/onboarding.ts src/customer-onboarding/types.ts
git commit -m "refactor: collect onboarding files into customer-onboarding/"

# 3. Fix imports
git grep -l "forms/customer-onboarding\|api/onboarding\|types/onboarding" \
  | xargs sed -i \
    -e "s|forms/customer-onboarding|customer-onboarding/form|g" \
    -e "s|api/onboarding|customer-onboarding/api|g" \
    -e "s|types/onboarding|customer-onboarding/types|g"
git commit -m "refactor: update imports for customer-onboarding move"
```

Repeat per feature. Don't try to do all features in one commit — review burden becomes unmanageable.

Further reading:

- *Bulletproof React* project structure (https://github.com/alan2207/bulletproof-react) — practical reference implementation.
- *Domain-Driven Design* (Eric Evans, 2003) — bounded contexts at the architecture level.
- *Implementing Domain-Driven Design* (Vaughn Vernon, 2013), Ch. 4 — concrete bounded-context layouts.
- *Vertical Slice Architecture* (Jimmy Bogard) — slice-by-feature pattern; complements this rule for backend code.
- `principles/one-purpose-per-directory/` — sibling rule: this rule names *what* the purpose is, that one *forbids* purpose-empty names.
- `principles/depth-vs-breadth/` — purpose-driven peers stay shallow; type-driven nesting (`components/forms/login/`) goes deep fast.
