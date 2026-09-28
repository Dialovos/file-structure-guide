## TL;DR

A repository's **community and automation files** (workflows, issue and pull-request templates, ownership rules, dependency updates, security policy, contribution guide) are code that shapes how people work with the project. Keep them in the places the forge looks for them: everything GitHub-specific in **`.github/`** (`workflows/`, `ISSUE_TEMPLATE/`, `PULL_REQUEST_TEMPLATE.md`, `CODEOWNERS`, `dependabot.yml`), and the human-facing policy documents (`README.md`, `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`) at the root or in `.github/`. Pin third-party actions to full commit SHAs, give workflows the least permissions they need, and keep each workflow single-purpose. The payoff is a repository where a first-time contributor knows how to report a bug, propose a change, and run the tests, and where automation is reviewable and safe.

## Principles & why

1. **Put files where the platform expects them.** GitHub discovers `.github/workflows/*.yml`, `.github/ISSUE_TEMPLATE/`, `CODEOWNERS`, and the community health files by path; a wrong location silently does nothing.
2. **Least privilege for automation.** Workflows should declare `permissions:` explicitly (default to `contents: read`) and never grant more than a job needs, because workflows run code with your repository's credentials.
3. **Pin what you execute.** A third-party action referenced by a mutable tag (`@v4`) can change under you; a full commit SHA with a version comment (`# v4`) cannot.
4. **One workflow, one job to be done.** Separate `ci.yml`, `release.yml`, and `docs.yml` are easier to read, permission, and trigger than one file that does everything.
5. **Templates reduce back-and-forth.** Issue forms and a pull-request template ask for the information reviewers always request, so maintainers spend time on decisions instead of triage.
6. **Ownership is explicit.** A `CODEOWNERS` file maps paths to reviewers, so the right people are asked automatically and branch protection can require their approval.

## When to use

- **Any repository hosted on GitHub** that has, or expects, more than one contributor.
- **Open-source projects**, where outside contributors need clear paths to report, propose, and test.
- **Internal repositories** that need consistent CI and review rules across teams.
- **Repositories with automation** whose workflows deserve the same care as production code.

## When NOT to use

- **Repositories hosted elsewhere.** GitLab, Gitea, and others use different directories (`.gitlab/`, `.gitea/`) with similar ideas; adapt the principles, not the paths.
- **Throwaway or private scratch repositories** where nobody else contributes; a README and a CI file are enough.
- **As a replacement for real security review.** Templates and policies document process; they don't enforce it without branch protection and required checks.
- **To hold project documentation.** Long-form docs belong in `docs/` (see `docs-as-code-site`), not in `.github/`.

## Tree diagram

```
repo/
├── README.md
├── LICENSE
├── CONTRIBUTING.md                   ← how to set up, test, and propose changes
├── SECURITY.md                       ← how to report a vulnerability privately
├── CODE_OF_CONDUCT.md
└── .github/
    ├── CODEOWNERS
    ├── dependabot.yml
    ├── PULL_REQUEST_TEMPLATE.md
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.yml
    │   ├── feature_request.yml
    │   └── config.yml               ← disable blank issues, add contact links
    └── workflows/
        ├── ci.yml                   ← build, lint, test on push and PR
        ├── release.yml              ← tag-triggered publish
        └── codeql.yml               ← scheduled static analysis
```

## Naming rules

- **Workflow files** are lowercase kebab-case by purpose: `ci.yml`, `release.yml`, `docs.yml`; the `name:` inside matches.
- **Job and step IDs** are short lowercase names (`test`, `lint`), and step `name:` fields read as actions ("Run tests").
- **Issue forms** are `bug_report.yml` and `feature_request.yml` (YAML forms), with `config.yml` for chooser settings.
- **`CODEOWNERS`** is uppercase by GitHub convention and lives in `.github/`, the repository root, or `docs/`; keep it in one place.
- **Policy documents** use canonical uppercase names (`CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`); see `capitalization-policy`.
- **Labels** used by templates and automation are lowercase with a namespace where helpful (`type: bug`, `area: docs`).

## Worked example

A new open-source project gets drive-by issues with no reproduction steps, pull requests that skip tests, and CI that runs on every fork with broad permissions.

1. Add `CONTRIBUTING.md` at the root with four short sections: set up, run tests, style, how to propose a change. Link it from the README.
2. Add `.github/ISSUE_TEMPLATE/bug_report.yml` as an issue form that requires version, steps to reproduce, expected and actual behavior. Add `config.yml` with `blank_issues_enabled: false` and a link to discussions for questions.
3. Add `.github/PULL_REQUEST_TEMPLATE.md` with a checklist: tests added, docs updated, linked issue.
4. Add `.github/workflows/ci.yml`:
```
permissions:
  contents: read
```
and pin actions to full commit SHAs with a version comment, for example `uses: actions/checkout@<sha> # v4`. Run tests on `push` and `pull_request`.
5. Add `.github/dependabot.yml` for the ecosystems you use and for `github-actions`, so pinned SHAs are updated by pull request.
6. Add `.github/CODEOWNERS` mapping directories to teams, then enable "Require review from Code Owners" and required status checks in branch protection.
7. Add `SECURITY.md` with a private reporting channel (enable GitHub private vulnerability reporting).
8. Lint the workflows in CI with `actionlint`.

Contributors get a clear path, and automation runs with reviewed, minimal permissions.

## Anti-patterns

- **Actions pinned to tags or branches** (`@main`, `@v4`) in workflows that handle secrets or publish releases.
- **Default broad `permissions`** (`write-all`) for convenience. Declare permissions per workflow or job.
- **Using `pull_request_target` with a checkout of the pull request's code.** It runs untrusted code with repository secrets; avoid it unless you understand the trust model.
- **Secrets echoed in logs** or passed to steps that don't need them.
- **One giant workflow** that lints, tests, builds, releases, and deploys, with conditionals everywhere.
- **Issue templates with 20 required fields.** They drive people away; ask only for what maintainers always need.
- **`CODEOWNERS` with individuals who left**, or with paths that no longer exist. Review it as people and directories change.

## Scaling & failure modes

- **Many repositories**: put shared community health files (`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue templates) in a special `.github` repository at the organization level, so they apply as defaults; keep repo-specific workflows local.
- **Reusable workflows**: extract shared CI into a reusable workflow (`workflow_call`) in a central repository, pinned by SHA, to avoid copy-paste drift.
- **CI cost and time**: use path filters, caching, and matrix builds sparingly; cancel superseded runs with `concurrency`.
- **Supply-chain security**: enable Dependabot alerts, code scanning, secret scanning, and require signed or attested releases as risk grows.
- **Monorepos**: scope `CODEOWNERS` by directory and trigger workflows by path so unrelated changes don't run every job.

## Variants

- **Full open-source setup** (this guide): all community files plus CI, security, and dependency automation.
- **Minimal private repository**: `README`, a CI workflow, and `CODEOWNERS`.
- **Organization-level defaults**: community health files in the org's `.github` repository.
- **Reusable-workflow hub**: a central repository of `workflow_call` workflows consumed by many repos.
- **Other forges**: `.gitlab-ci.yml` and `.gitlab/` templates, or Gitea/Forgejo workflows, with the same principles.

## Adoption checklist

- [ ] `README`, `LICENSE`, `CONTRIBUTING.md`, and `SECURITY.md` exist and are linked from the README.
- [ ] Every workflow declares `permissions:` and pins third-party actions to full SHAs.
- [ ] Issue forms and a pull request template ask only for information maintainers always need.
- [ ] `CODEOWNERS` matches current directories and people, and branch protection requires code-owner review and passing checks.
- [ ] `dependabot.yml` covers each ecosystem plus `github-actions`.
- [ ] `actionlint` runs in CI.

## Real-world projects using this

- **GitHub Docs** ("Creating a default community health file", "Workflow syntax for GitHub Actions", "About code owners", "Security hardening for GitHub Actions") describe the locations and behaviors used here.
- **OpenSSF Scorecard** and **OpenSSF Best Practices Badge** list repository hygiene checks, including pinned dependencies and least-privilege tokens.
- **StepSecurity** and **GitHub's security hardening guide** document pinning actions by commit SHA and the risks of `pull_request_target`.
- **Large open-source projects** such as Kubernetes, Rust, and pytest keep templates, workflows, and ownership files under `.github/`; browsing them shows mature setups.
- **actionlint** (rhysd/actionlint) documents static checking of workflow files.

## Migration & references

- **From no metadata:** add `CONTRIBUTING.md` and a CI workflow first, then templates, then ownership and dependency automation.
- **From tag-pinned actions:** resolve each tag to its commit SHA, replace it with the SHA plus a version comment, and let Dependabot maintain updates.
- **From per-repo copies to organization defaults:** move shared files to the organization's `.github` repository and delete the copies that match.
- **References:**
  - `principles/hidden-files-policy/` for why `.github/` is hidden plumbing.
  - `principles/capitalization-policy/` for uppercase canonical files.
  - `principles/ai-agent-context-files/` for `copilot-instructions.md` and `AGENTS.md`.
  - `code/docs-as-code-site/` for documentation builds in CI.
