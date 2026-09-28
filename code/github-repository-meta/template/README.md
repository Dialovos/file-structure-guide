# github-repository-meta — template

The community and automation files for a GitHub repository, with least-privilege CI and templates ready to edit.

## What to rename

- `@your-org/your-team` in `CODEOWNERS` to real teams or users
- Contact and reporting details in `SECURITY.md`

## What to fill

- `.github/workflows/ci.yml` — replace the test command with your own
- `CONTRIBUTING.md` — your real setup and test commands

## What to delete

- Templates and workflows you don't use (for example `release.yml`)

## First run

```bash
# after pushing, open a pull request and confirm the templates, CI, and code-owner review requests appear
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../../../principles/capitalization-policy/` — uppercase canonical files
