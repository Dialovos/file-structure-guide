## TL;DR

Organize Terraform by **blast radius and lifecycle**: reusable building blocks in `modules/`, and one **root module per environment** in `environments/<env>/` that composes them and owns its own state. Each root module is a directory you run `terraform init/plan/apply` in; each has its own backend configuration, so a mistake in `dev` cannot touch `prod` state. Modules are small, single-purpose, and have three files at minimum: `main.tf`, `variables.tf`, `outputs.tf`. Commit the **dependency lock file** (`.terraform.lock.hcl`), never the **state** or real variable values. Pin provider and Terraform versions in `versions.tf`. The result: environments are copies of one shape rather than diverging branches, plans are reviewable in pull requests, and state stays remote, locked, and separate per environment.

## Principles & why

1. **State is the unit of risk.** Everything in one state file changes together and can break together. Splitting state by environment (and, at scale, by component) limits the blast radius of an error.
2. **Modules encode reuse; environments encode difference.** Environments should mostly be a list of module calls with different inputs, not different code.
3. **Explicit inputs and outputs.** A module's `variables.tf` and `outputs.tf` are its public interface; nothing should reach across modules except through them.
4. **Pin everything that resolves.** Terraform version, provider versions, and module versions are pinned, and the provider lock file is committed, so a plan today equals a plan next month.
5. **Plans are reviewed artifacts.** The workflow is pull request, then `plan`, then review, then `apply` of that same plan, not ad-hoc applies from laptops.
6. **Secrets stay out of code and state where possible.** State can contain sensitive values; it must be remote, encrypted, and access-controlled, and variable values that are secret come from the environment or a secret manager.

## When to use

- **Any infrastructure managed as code** across more than one environment.
- **Teams sharing infrastructure**, where reviewable plans and locked state matter.
- **Projects that will grow beyond one file**: it costs little to start with `modules/` and `environments/`.

## When NOT to use

- **A single throwaway resource.** A one-file configuration is fine until it has a second environment.
- **As an application deployment tool.** Terraform provisions infrastructure; packaging and rolling out application code belongs to a deployment pipeline.
- **When another tool is already the standard** (Pulumi, CloudFormation, CDK): use its conventions; the principles (separate state, pin versions) still apply.
- **Don't create a module for every resource.** A module that wraps one resource with the same variables adds indirection without reuse.

## Tree diagram

```
infra/
├── modules/
│   ├── network/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   └── database/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   ├── dev/
│   │   ├── main.tf                  ← composes modules
│   │   ├── backend.tf               ← remote state for dev only
│   │   ├── versions.tf              ← required_version, required_providers
│   │   ├── variables.tf
│   │   ├── terraform.tfvars         ← non-secret inputs
│   │   └── .terraform.lock.hcl      ← committed
│   └── prod/
│       └── (same shape)
├── .gitignore                       ← .terraform/, *.tfstate*, secret tfvars
└── README.md
```

## Naming rules

- **Directories** are lowercase kebab-case (`environments/dev`, `modules/network`).
- **Resource and variable names** in HCL use `snake_case` (`aws_s3_bucket.logs`, `var.instance_count`), matching the language's convention.
- **Standard files** keep standard names: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `backend.tf`; larger modules may split by concern (`iam.tf`, `dns.tf`).
- **Resource names inside the cloud** follow one scheme, such as `<project>-<environment>-<purpose>`, built in a `locals` block, never typed by hand.
- **Tag or label keys** are consistent (`project`, `environment`, `owner`) and applied through provider default tags where supported.
- **Variable files**: `terraform.tfvars` for non-secret values; `*.auto.tfvars` for auto-loaded ones; secrets never in either.

## Worked example

A single `main.tf` in a `terraform/` folder deploys everything to one account, and there's a `staging.tfvars` that people sometimes forget to pass.

1. Freeze the current state: `terraform state pull > backup.tfstate` (keep it out of git), and confirm `terraform plan` shows no changes.
2. Create `modules/` and move repeated resource groups (network, database) into modules with explicit variables and outputs.
3. Create `environments/dev/` and `environments/prod/`, each with `main.tf` calling the modules with environment-specific inputs.
4. Configure a remote backend per environment (`backend.tf`), with locking and encryption, for example an object-storage bucket plus a lock table or the backend's native locking.
5. Move state into the new layout with `terraform state mv` (or `moved` blocks in the configuration), then run `terraform plan` in each environment; the goal is "no changes".
6. Pin versions in `versions.tf` and commit `.terraform.lock.hcl`.
7. In CI: `terraform fmt -check`, `terraform validate`, `tflint`, and `terraform plan -out=tfplan` posted on the pull request; apply the reviewed plan only after merge.

Each environment has its own state, pull requests show plans, and `dev` mistakes cannot reach `prod`.

## Anti-patterns

- **One state file for everything.** A bad apply in one area can block or damage all others; state locks serialize unrelated work.
- **Workspaces as environments** when environments differ meaningfully. Workspaces share code and backend configuration, which hides differences and makes accidents likelier.
- **Committing state or `.terraform/`.** State can contain secrets and is not mergeable; use a remote backend.
- **Copy-pasted environment directories that drift.** If `prod` and `dev` differ in code beyond inputs, extract the difference into module variables.
- **Unpinned providers.** A silent provider upgrade changes plans; pin and commit the lock file.
- **Applying from laptops without a reviewed plan.** Use CI to apply saved plans.

## Scaling & failure modes

- **State size and plan time** grow with resource count; split by component (network, data, application) into separate root modules with remote-state outputs or data sources between them.
- **Cross-stack dependencies**: use explicit outputs consumed through `terraform_remote_state` or data sources, and document the apply order.
- **Module versioning**: once modules are shared across repositories, publish them with tags and pin consumers to versions.
- **Drift**: scheduled `plan` runs detect manual changes; decide who reconciles.
- **Large teams**: add policy checks (OPA, Sentinel, or Checkov) to CI, and restrict who can apply to `prod`.

## Variants

- **Directory-per-environment** (this guide): explicit, easiest to reason about.
- **Workspaces**: same code, different state per workspace; suits near-identical environments such as ephemeral preview stacks.
- **Terragrunt** layout: DRY backend and inputs across many environments and components.
- **Layered stacks**: `network/`, `data/`, `apps/` as separate root modules per environment.
- **Monorepo with other IaC**: Terraform beside Kubernetes manifests or Ansible, each in its own top-level folder.

## Adoption checklist

- [ ] Each environment is a separate root module with its own remote, locked, encrypted state.
- [ ] `versions.tf` pins Terraform and provider versions, and `.terraform.lock.hcl` is committed.
- [ ] `.gitignore` excludes `.terraform/`, `*.tfstate*`, and secret variable files.
- [ ] Modules expose a documented interface through `variables.tf` and `outputs.tf`.
- [ ] CI runs `fmt -check`, `validate`, a linter, and a plan on every pull request.
- [ ] Applies happen from a saved, reviewed plan, not from laptops.

## Real-world projects using this

- **HashiCorp's Terraform documentation** describes the standard module structure (`main.tf`, `variables.tf`, `outputs.tf`) and the recommended handling of state and the lock file.
- **Terraform Registry** modules (for example the widely used `terraform-aws-modules` collection) show the module conventions at scale.
- **Gruntwork's "Terraform: Up & Running"** (Yevgeniy Brikman) popularized directory-per-environment layouts with reusable modules.
- **Terragrunt** documents the DRY layout for many environments.
- **Checkov, tflint, and tfsec/trivy** document the static-analysis side of the workflow.

## Migration & references

- **From a single directory:** create modules and environment directories, move state with `terraform state mv` or `moved` blocks, and verify with a no-change plan.
- **From workspaces to directories:** create a directory per workspace, copy state with `terraform state pull`/`push` (carefully), and retire the workspaces after a no-change plan in each.
- **From local state:** configure a remote backend and run `terraform init -migrate-state`.
- **References:**
  - `principles/config-and-secrets-placement/` for variables and secrets.
  - `principles/stable-vs-volatile-separation/` for state and generated files.
  - `code/docker-compose-services/` for the application side of local environments.
  - `principles/decision-records-adr/` for recording choices such as workspaces versus directories.
