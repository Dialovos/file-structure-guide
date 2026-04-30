# Versioning in paths

## TL;DR

Don't version files via filename or path suffix. `_v2`, `-old`, `-final`, `_FINAL_USE_THIS` are anti-patterns: the filesystem is a bad VCS. Use git tags, branches, and history. Reserve path-based versioning for the rare cases where multiple versions deliberately coexist (public API namespaces, releasable artifacts).

## Principles & why

A file's job is to have a *canonical* name — the name everyone refers to, the name that survives across history. The moment you save `report_v2.md` next to `report.md`, you've forked a question every future reader has to answer: which is the real one? "Final" usually isn't, and the dance of `report_v3_REAL_FINAL.md` is the predictable end state.

Git already solves this. Every commit *is* a version; every tag *is* a named version; every branch *is* a parallel version under your control. Filenames don't need to encode any of it, because the VCS does — losslessly, with diffs, with provenance, and with a reliable answer to "what changed and when".

Path-based versions also break tooling. A reader's grep matches all five copies. A linter checks them all. A CI pipeline can't tell which one to deploy. Renames lose history. Cross-references rot the moment you advance from `_v2` to `_v3` because no link tracker knew about the rename.

The narrow exception: when *multiple versions deliberately coexist*. A REST API exposing `/v1/` and `/v2/` simultaneously isn't superseding — it's contracting with two cohorts of clients. A released artifact `my-app-1.2.3.tar.gz` puts the version in the *identity* because the file is immutable and shipped. These are versions-as-namespaces, not versions-as-edits.

## When to use

The honest answer for a git-tracked working file: **never.** Every editable file in your repo should have a canonical name and rely on git for history.

The legitimate exceptions, where path-based versioning is correct:

- **Public API namespaces** — `/v1/users`, `/v2/users` peer-deployed because clients on the old contract still call you. The path *is* the contract.
- **Released artifact filenames** — `kubernetes-1.30.0.tar.gz`, `node-v22.0.0.tar.gz`. The version is part of the artifact's identity; an "unversioned" version makes no sense.
- **Schema migrations / data versions** — `schema_v1.sql`, `schema_v2.sql` when both are intentionally retained as a migration history. (Many teams instead use timestamped names like `2026-04-30-migrate.sql` — also fine, see `principles/iso-date-formats/`.)
- **Multi-version documentation hosting** — `docs.example.com/v3/...` vs `docs.example.com/v4/...` so users can pin to the version they're running.
- **Specs and protocols where back-compat matters** — `RFC-9999-v1.md`, `RFC-9999-v2.md` if the spec is canonically multi-version. Rare; usually better as a single file with a "Versions" section.

## When NOT to use

Don't put a version in the path for any of these — even though it's tempting:

- **Working source files.** `auth_v2.ts` next to `auth.ts` is the canonical anti-pattern. Use a branch.
- **Configuration files.** `config_v2.yaml` is git's job; the live file is `config.yaml`, history lives in commits.
- **Drafts.** `proposal-old.md` next to `proposal.md` is what the parent's `archive/` directory is for, or what `git log` gives you for free.
- **"Just in case" backups.** `report.md.bak`, `report.md.old` — your VCS already does this, perfectly, automatically.
- **Renames you're nervous about committing.** Use `git mv`. Don't keep both around "until I'm sure".

The fail-safe heuristic: if you can't articulate why two versions need to coexist *as published artifacts at the same time*, you don't need a version in the path.

## Tree diagram

```
good/
├── config.yaml          ← canonical name, history in git
├── api-spec.md          ← same
└── README.md

bad/
├── config_v1.yaml
├── config_v2.yaml
├── config_v2_final.yaml
├── config_v2_FINAL_USE_THIS.yaml
└── api-spec-old.md
```

## Naming rules

1. The canonical filename has **no version suffix**: `config.yaml`, not `config_v1.yaml`. Even when there's only one version. Especially when there's only one version.
2. For legitimate multi-version namespaces (APIs, docs sites), use **major-version directories** at the *namespace* level: `api/v1/`, `api/v2/`. Not version-suffixed filenames inside one directory.
3. Released artifacts use **semver in the filename**: `my-app-1.2.3.tar.gz`. Pre-1.0 use `0.x.y`. Append `-rc1`, `-beta1` for prereleases.
4. Migration files use **timestamps** rather than `_v2`: `2026-04-30-add-users.sql` is better than `migration_v2.sql` because timestamps total-order without ambiguity.
5. Don't reuse `v` for non-version meanings (`v_data/` for "verified data"). The convention is too entrenched; pick another letter.
6. Never write `_FINAL`, `_REAL`, `_USE_THIS`, `_NEW`, `-good`, `-correct`. These betray a missing VCS workflow, not a real disambiguator.

## Anti-patterns

- **The death spiral**: `report.md` → `report_v2.md` → `report_v2_final.md` → `report_v2_final_FINAL.md` → `report_v2_USE_THIS_ONE.md`. The classic. Solve with `git mv` and `git log`.
- **Old-keeping**: `auth.ts` and `auth-old.ts`, "in case we need to roll back". You can roll back with `git checkout`. Delete the old file.
- **Date-suffix versions**: `proposal-2025-12-01.md`, `proposal-2026-01-15.md`. Either you want every snapshot (use git), or you want one canonical `proposal.md`. The middle ground is just clutter.
- **Backup-suffix versions**: `.bak`, `.orig`, `~` files committed to the repo. These are editor artifacts; they belong in `.gitignore`, not history.
- **Mixed conventions**: `auth_v2.ts` next to `billing-old.ts` next to `users-FINAL.ts` in the same project. Even if one were defensible, mixing three is chaos.
- **Path versions inside a versioned namespace**: `api/v1/users_v2.ts`. The path's outer `v1` is the namespace; you don't get a second version inside it. Use the namespace's own version bump.
- **Major-version namespaces with a single version**: creating `api/v1/` "in anticipation" before there's ever been a v2. Adds nesting without value.

## Variants

- **strict-no-version-in-path** (this repo's recommendation) — never. Every working file has a canonical name; git handles history. Public APIs use *URL* versioning, not source-tree versioning.
- **allow-major-version-namespace** — strict for working files, but `api/v1/`, `api/v2/` peer directories are permitted when you genuinely deploy both. Most production services land here.
- **release-artifacts-only** — strict for sources and configs, but artifacts (`*.tar.gz`, `*.whl`, `*.deb`) include semver in their filename. Universal in package ecosystems.
- **edition-based** — Rust's `edition = "2021"` model: source files unversioned, but the toolchain reads a single edition declaration that selects compatibility. Single-version-at-a-time, declared once.
- **Date-stamped migrations** — for schema and data migrations specifically, prefer ISO dates over `_v` suffixes (`2026-04-30-add-users.sql`). Same idea: external ordering signal, no VCS reinvention.

## Real-world projects using this

- **Stripe API** (`https://api.stripe.com/v1/`) — major-version namespace at the URL level; sources in their repo are unversioned. The contract is versioned, the source isn't.
- **Semantic Versioning spec** (https://semver.org) — names release artifacts with version triples; doesn't recommend versioning *source* files in the same way.
- **Rust editions** — `edition = "2021"` in `Cargo.toml`, no `lib_2021.rs` files. Edition is metadata, not a path suffix.
- **Linux kernel releases** (`linux-6.8.tar.xz`, `linux-6.9.tar.xz`) — versioned tarballs, but the working tree is one branch with tags.
- **AWS API versions** — every service exposes `2010-05-08`-style date versions in request signatures, but service source code is unversioned in their internals.
- **PostgreSQL major versions** (`postgres-15`, `postgres-16` packages) — released as separate distributable artifacts; the source repo is one tree per release line.

## Migration & references

To find filename-versioning anti-patterns in an existing repo:

```bash
# Hunt for the usual suspects
find . -type f \( \
     -iname '*_v[0-9]*' \
  -o -iname '*-v[0-9]*' \
  -o -iname '*-old.*' \
  -o -iname '*_old.*' \
  -o -iname '*-final.*' \
  -o -iname '*_FINAL*' \
  -o -iname '*-bak.*' \
  -o -iname '*.bak' \
  -o -iname '*.orig' \
\) -not -path './.git/*'
```

Migration steps:

1. **Identify the canonical version.** Usually the one most recently edited or most-referenced.
2. **Move it to the canonical name** (`git mv config_v2.yaml config.yaml`).
3. **Delete the others** (`git rm config_v1.yaml config_v2_FINAL.yaml`). Their content is preserved in `git log`.
4. **Tag if needed.** If the deleted versions corresponded to releases, ensure those tags exist (`git tag v1.0.0`).
5. **Update references.** Search for `_v2` mentions in docs, CI configs, and READMEs.

Further reading:

- Pro Git book, "Git Basics — Tagging" (https://git-scm.com/book/en/v2/Git-Basics-Tagging) — the right way to mark versions.
- Semantic Versioning 2.0 spec (https://semver.org) — for release artifacts.
- `principles/iso-date-formats/` — when you do need a time-ordered suffix, use ISO dates not `_v2`.
- `principles/status-based-organization/` — `archive/` is the right home for retired versions, not a filename suffix.
- Stripe's API versioning blog post — case study of "stable URLs, versioned at the namespace, never at the file" applied at scale.
