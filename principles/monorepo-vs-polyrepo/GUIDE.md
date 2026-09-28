## TL;DR

Decide **how many repositories hold your code** by looking at what changes together, not at what is fashionable. Put code in **one repository** (monorepo) when components are released together, share types or libraries, and are worked on by the same people: a change that spans them becomes one atomic commit and one review. Use **separate repositories** (polyrepo) when components have independent owners, release cadences, access rules, or lifecycles: each repo stays small, fast, and simple. The middle path, a monorepo with strict internal boundaries, works for most small teams and is what most guides in this repo assume when they show `apps/` and `packages/`. Whichever you choose, write it down and apply the same rule to every new component, because the expensive failure is the accidental hybrid: five repos that must always be changed together, or one repo where three unrelated teams block each other's CI.

## Principles & why

1. **Atomic change is the main benefit of a monorepo.** Renaming a shared function, updating its callers, and shipping the result is one commit. In a polyrepo it is a release of the library, then a bump in every consumer, with a window where they disagree.
2. **Independence is the main benefit of a polyrepo.** A repo has its own permissions, issue tracker, CI, and release cadence. A component that different people own, or that must be shared publicly, fits naturally.
3. **Coupling should match the repository boundary.** If two components have a version-skew problem every release, they are one component split by a repo boundary. If one repo has parts that never change together, it is several components sharing a folder.
4. **Tooling cost moves, it doesn't disappear.** Monorepos need affected-only builds, code ownership rules, and sparse checkouts as they grow. Polyrepos need dependency update automation, cross-repo search, and a template for keeping repos consistent.
5. **Boundaries inside a monorepo still matter.** A monorepo without enforced module boundaries is a polyrepo's coupling with none of its isolation.

The decision is reversible but not cheap. Splitting a monorepo keeps history if you use `git filter-repo` early; merging repos is easier when their layouts already match.

## When to use

Choose a **monorepo** when:

- A frontend, backend, and shared types ship together, and a breaking API change needs a matching client change.
- One small team owns everything and wants one CI pipeline, one issue tracker, and one place to search.
- You want a single dependency version policy (one lockfile, one toolchain).

Choose **polyrepo** when:

- Components have different owners, security boundaries, or open-source vs private status.
- Release cadences differ by an order of magnitude (a stable SDK and a weekly-deployed app).
- Repositories are consumed by third parties who should clone only what they need.

Choose a **hybrid** (one monorepo per product or team, plus a few shared library repos) when both pressures exist and you have a clear rule for which side of the line each thing falls on.

## When NOT to use

- **Don't pick a monorepo to avoid dependency management.** Internal packages still need versioned interfaces and tests; the repo boundary only hides the cost.
- **Don't pick a polyrepo to avoid design decisions.** Splitting a tangled system into repos makes the tangles into network calls and version conflicts.
- **Don't migrate for its own sake.** A working setup with clear ownership beats a fashionable one; move only when a specific, recurring pain (blocked releases, painful cross-repo changes) justifies the cost.
- **Don't put unrelated projects in one repo just to save on setup.** A personal workspace of independent projects is a folder of repositories, not a monorepo (see `workspace-root-layout`).

## Tree diagram

```
monorepo (single owner, ships together)/
├── apps/
│   ├── web/
│   └── api/
├── packages/
│   ├── shared-types/
│   └── ui/
└── README.md

polyrepo (independent owners and cadences)/
├── acme-sdk/            ← own repo, own releases
├── acme-web/            ← own repo, depends on acme-sdk by version
└── acme-infra/          ← own repo, restricted access

hybrid/
├── acme-platform/       ← monorepo: api, worker, shared packages
└── acme-sdk/            ← separate repo: public, semver'd
```

In every layout, the rule that decides where a component lives is written in the top-level README.

## Naming rules

- **Monorepo top-level** names are roles: `apps/` for deployable units, `packages/` (JS), `crates/` (Rust), or `libs/` for shared libraries. See `turborepo-monorepo`, `nx-monorepo`, and `rust-workspace` for tool-specific conventions.
- **Package names** carry a namespace or prefix (`@acme/ui`, `acme-core`) so they cannot collide with public registries.
- **Polyrepo names** share a prefix (`acme-web`, `acme-sdk`) and are lowercase kebab-case, so a GitHub organization search lists them together.
- **Tags and releases** in a monorepo are per package (`ui@2.3.0`, `api/v1.4.2`); a repo-wide `v1.0.0` tag says nothing when parts release independently.
- **Boundaries** are named in an ownership file (`CODEOWNERS`), one line per directory.

## Worked example

Three repos (`web`, `api`, `types`) need a coordinated change every week; each change takes three pull requests and a version bump.

1. Measure the pain: over the last 20 changes, count how many touched more than one repo (`git log` per repo, matched by ticket).
2. If most did, plan a merge. Create `acme-platform/` with `apps/web`, `apps/api`, `packages/types`.
3. Import each repo with history: `git filter-repo --to-subdirectory-filter apps/web` on a fresh clone of `web`, then `git remote add`, `git fetch`, `git merge --allow-unrelated-histories` into the new repo (repeat for each).
4. Replace the published `types` package with a workspace dependency (`"@acme/types": "workspace:*"`).
5. Set up one CI pipeline that builds only affected projects, and add `CODEOWNERS` entries per directory.
6. Archive the old repos with a README pointer to the new location, and update deploy pipelines.

The next cross-cutting change is one pull request, one review, and one deploy.

## Anti-patterns

- **Repo-per-function sprawl.** Twenty tiny repos for twenty tiny packages, all versioned in lockstep, is a monorepo in disguise with worse tooling.
- **The everything monorepo with no boundaries.** Any module imports any other, CI runs the whole tree, and nobody owns anything.
- **Copy-paste sharing.** Duplicating a library into several repos avoids the versioning problem by creating a synchronization problem.
- **Long-lived git submodules** as a compromise. They add the costs of both approaches, and updates go stale unnoticed.
- **Migrating without a rule.** Mixing "some things in the monorepo, others in repos" without a written criterion leads to arbitrary placement.

## Scaling & failure modes

- **Monorepo growth.** Clone and CI time rise with size. Mitigate with shallow or sparse checkout (`git sparse-checkout`), affected-only builds, remote caching, and path-filtered CI triggers.
- **Ownership at scale.** Without `CODEOWNERS` and branch protection per path, reviews become random. Add ownership as soon as a second team commits.
- **Polyrepo consistency.** Twenty repos drift in lint rules, CI, and license headers. Use a template repo or a sync tool, and automate dependency updates (Dependabot or Renovate).
- **Access control.** Monorepos expose everything to everyone with access; sensitive components belong in a separate repo.
- **Release tagging.** Independent releases inside a monorepo need per-package tags and changelogs (changesets or release-please).

## Variants

- **Single-product monorepo**: one app plus its libraries, the common case.
- **Team monorepo**: everything one team owns, with per-directory ownership.
- **Company monorepo**: hundreds of projects with build tooling such as Bazel, Buck, or Nx, and dedicated infrastructure. Only justified at scale.
- **Polyrepo with a template**: many repos, kept consistent by a template and automation.
- **Hybrid platform + SDK**: private platform monorepo, public SDK repo generated or synced from it.
- **Workspace of repos**: a folder containing independent repositories, with no shared history (see `workspace-root-layout`).

## Adoption checklist

- [ ] The rule for what goes where is written in the top-level README.
- [ ] Every cross-cutting change in the last quarter was counted; the boundary matches the results.
- [ ] Monorepos have enforced module boundaries and a `CODEOWNERS` file.
- [ ] Monorepo CI builds only what changed.
- [ ] Polyrepos have a template and automated dependency updates.
- [ ] Release tags identify the package they belong to.

## Real-world projects using this

- **Google** and **Meta** describe their very large monorepos in public engineering papers (for example "Why Google Stores Billions of Lines of Code in a Single Repository").
- **Kubernetes** keeps the core in one repository (`kubernetes/kubernetes`) while many related projects live in separate repositories under the same organization.
- **Babel**, **Jest**, and **React** use JavaScript monorepos with multiple published packages.
- **The Rust project** keeps the compiler, standard library, and Cargo-related tooling in a repository of its own while related tools live in separate repositories.
- **Tooling references:** Nx, Turborepo, Bazel, Rush, and Lerna documentation each describe the monorepo trade-offs from their perspective.

## Migration & references

- **Polyrepo to monorepo:** import each repository with history under a subdirectory (`git filter-repo --to-subdirectory-filter <dir>` then merge with `--allow-unrelated-histories`), unify CI, and replace version pins between them with workspace links.
- **Monorepo to polyrepo:** extract a directory with history (`git filter-repo --subdirectory-filter <dir>`), publish its packages, and replace workspace links with versioned dependencies.
- **Adding boundaries to an existing monorepo:** start with `CODEOWNERS`, then add an import-boundary linter (Nx tags, `eslint-plugin-boundaries`, `import-linter`).
- **References:**
  - Monorepo tooling: `code/turborepo-monorepo/`, `code/nx-monorepo/`, `code/rust-workspace/`, `code/python-uv-workspace/`.
  - Sibling principles: `principles/naming-by-purpose-not-type/`, `principles/stable-vs-volatile-separation/`.
  - Related files guide: `files/workspace-root-layout/` for a folder of independent repositories.
