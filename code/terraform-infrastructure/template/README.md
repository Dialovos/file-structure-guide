# terraform-infrastructure — template

A provider-free skeleton showing modules, per-environment root modules, and the files that stay out of git. It runs with `terraform init` and `plan` as-is; add your provider and resources.

## What to rename

- `acme` in variable defaults to your project name

## What to fill

- `environments/*/backend.tf` — real remote backend settings
- `environments/*/versions.tf` — provider requirements
- `modules/naming/` — replace with your real modules

## What to delete

- The `naming` module once you have real modules

## First run

```bash
cd environments/dev && terraform init -backend=false && terraform validate && terraform plan
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../../../principles/config-and-secrets-placement/` — variables and secrets
