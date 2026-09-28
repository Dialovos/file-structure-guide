# github-repository-meta — canonical tree

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
