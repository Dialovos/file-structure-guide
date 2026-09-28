## TL;DR

Keep **configuration** (values that differ between environments) and **secrets** (values that grant access) out of source code, and put each kind in a predictable place. Non-secret defaults live in a committed file (`config/default.yaml`, `settings/base.py`). Environment-specific overrides live in committed per-environment files or in the deployment system. Secrets never enter git: locally they live in a gitignored `.env` (or, better, the desktop keyring or a password manager), and in production they come from a secret manager or the platform's encrypted variables. A committed `.env.example` lists every variable name with no real value, so a new contributor knows what to provide. The test is simple: could you make the repository public tomorrow without rotating a credential? If not, something is in the wrong place.

## Principles & why

1. **Separate code from config.** The same build should run in dev, staging, and production, with differences supplied from outside (the twelve-factor "config in the environment" rule).
2. **Secrets are a different category from config.** Config can be reviewed and diffed in the open; secrets need access control, rotation, and audit. Storing both in one file makes the strictest policy apply to everything or, worse, the loosest.
3. **Documented names, hidden values.** The list of required variables is public knowledge; their values are not. `.env.example` is the contract.
4. **One source of truth per value.** A value duplicated across `.env`, CI settings, and a config file will drift. Decide which system owns each value.
5. **Assume leaks and plan rotation.** Any secret that has been in git history, a log, or a screenshot must be treated as compromised. Layout should make rotation a one-place change.
6. **Fail loudly on missing config.** A missing required variable should stop startup with a clear message, not silently fall back to a default that points at production.

## When to use

- **Every project with credentials**: API keys, database URLs, tokens, signing keys.
- **Every project with environment differences**: hostnames, feature flags, log levels.
- **Shared repositories and public projects**, where a leaked value is an incident.
- **Workspaces used with automation or AI assistants**, where files may be read by tools; keep secrets out of files those tools can open (see `ai-agent-context-files`).

## When NOT to use

- **Don't treat this as a replacement for a secret manager** in production. A `.env` file on a server is better than committed secrets, but a manager gives rotation and audit.
- **Don't externalize constants that never vary.** A retry count that is the same everywhere belongs in code with a name, not in a config file.
- **Don't use environment variables for large or structured blobs** (certificates, JSON credentials) without a plan; mount them as files with restricted permissions instead.
- **Don't encrypt-and-commit as a first resort.** Tools like `sops` or `git-crypt` work, but add key management; start with keeping secrets out of git entirely.

## Tree diagram

```
project/
├── .env                  ← real values, gitignored
├── .env.example          ← names only, committed
├── .gitignore            ← lists .env and *.local
├── config/
│   ├── default.yaml      ← non-secret defaults, committed
│   ├── development.yaml
│   └── production.yaml   ← non-secret overrides, committed
├── src/
│   └── settings.py       ← reads config + environment, validates
└── deploy/
    └── secrets.README.md ← says where production secrets live (never the values)
```

Secret *values* appear nowhere in this tree except the gitignored `.env`.

## Naming rules

- **Variable names** are `UPPER_SNAKE_CASE`, prefixed by the app or service (`ACME_DATABASE_URL`, `ACME_LOG_LEVEL`) to avoid clashes with system variables.
- **Example file** is `.env.example` (some tools use `.env.template`); pick one and keep it in sync with the code that reads variables.
- **Per-environment files** are named by environment (`development.yaml`, `production.yaml`), never by person (`alice.yaml`).
- **Local-only overrides** use a `.local` suffix (`config/settings.local.yaml`) and are gitignored.
- **Secret references** in config use a scheme (`secret://db-password`) or a name in the secret manager, not a value.

## Worked example

A project has `DATABASE_URL` hard-coded in `settings.py`, and a token was once committed.

1. Rotate first: assume the committed token is compromised. Issue a new one at the provider and revoke the old.
2. Create `.env.example` listing names with empty values (`ACME_DATABASE_URL=`, `ACME_API_TOKEN=`), and add `.env` to `.gitignore`.
3. Load variables in one module (`settings.py`) with validation, for example with `pydantic-settings`; fail at startup if a required value is missing.
4. Move non-secret defaults (timeouts, log level) into `config/default.yaml`.
5. Scan the repository and its history for leaks: `gitleaks detect` or `trufflehog git file://.`. If a secret is in history, rotating it matters more than rewriting history.
6. Add a pre-commit or CI secret scanner so it can't recur.
7. In production, inject values from the platform's secret store, and document where in `deploy/secrets.README.md`.

The repository can now be shared without leaking anything, and onboarding is "copy `.env.example` to `.env` and fill it in.

## Anti-patterns

- **Committing `.env`** "just for the team." History is forever; rotate and remove.
- **Secrets in build arguments or images.** Docker build args and layers are readable; pass secrets at runtime or use build secrets.
- **Secrets in config files under a `secrets/` folder that is committed.** The folder name doesn't protect the contents.
- **Environment-specific `if` blocks in code** (`if env == "prod"`). Move differences to config so the same code runs everywhere.
- **Logging full configuration** at startup. It writes secrets into logs; log names and non-secret values only.
- **Sharing one credential across all environments.** A dev leak then compromises production.

## Scaling & failure modes

- **Many services**: a per-service `.env.example` plus a shared naming prefix keeps variable lists comprehensible; a central secret manager avoids copying values around.
- **Rotation**: design for a two-key overlap so rotation doesn't cause downtime, and track expiry dates.
- **Team growth**: `.env` sharing by chat leaks values; move to a password manager vault or a secret manager with per-user access.
- **CI/CD**: use the CI system's encrypted secrets with least privilege, scoped per environment, and prefer short-lived tokens (OIDC federation) over stored keys.
- **Local dev without secrets**: provide safe fake values or a local emulator so most work doesn't need real credentials.

## Variants

- **Env file plus example** (this guide): simple, works for small projects.
- **Keyring-backed local secrets**: read values from the OS keyring (`secret-tool` on Linux, Keychain on macOS) at runtime; nothing sits in a plaintext file.
- **Encrypted-in-repo** (`sops`, `git-crypt`, `age`): secrets committed encrypted, with keys held elsewhere. Adds key management.
- **Secret manager at runtime** (Vault, cloud providers' managers): applications fetch values by name on start.
- **Platform-injected variables**: the hosting platform sets environment variables from its own encrypted store.

## Adoption checklist

- [ ] `.env` is in `.gitignore` and `.env.example` lists every required variable with no values.
- [ ] Startup fails with a clear message when a required variable is missing.
- [ ] A secret scanner runs in pre-commit or CI, and the history was scanned once.
- [ ] Every secret ever committed has been rotated.
- [ ] Production secrets come from a store, and the README says where.
- [ ] Development and production use different credentials.

## Real-world projects using this

- **The Twelve-Factor App** (12factor.net), factor III "Config", is the widely cited source for keeping config in the environment.
- **GitHub secret scanning and push protection** and the open-source scanners **gitleaks** and **trufflehog** are common tools for detecting committed secrets.
- **Mozilla SOPS** and **age** document the encrypted-in-repo pattern.
- **HashiCorp Vault** and the cloud providers' secret managers document runtime secret retrieval.
- **Django, Rails, and Laravel** all ship a convention for an ignored local environment file plus a committed example.

## Migration & references

- **Cleaning an existing repository:** rotate exposed credentials first, add `.env` to `.gitignore`, create `.env.example`, move values into the environment, then consider history rewriting (`git filter-repo`) only after rotation.
- **From committed encrypted files to a secret manager:** load values by name at startup, keep the encrypted files as a fallback for one release, then remove them.
- **From one shared `.env` to per-developer credentials:** issue individual, revocable tokens and document where each one is obtained.
- **References:**
  - `principles/gitignore-and-keep-files/` for the ignore patterns.
  - `principles/hidden-files-policy/` for why `.env.example` is hidden but committed.
  - `code/fastapi-project/` and `code/django-project/` for framework-specific settings layouts.
  - `principles/ai-agent-context-files/` for keeping credentials away from AI tooling.
