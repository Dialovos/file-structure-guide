## TL;DR

Use **Docker Compose** to describe a multi-service application (web, API, database, queue) as one reproducible local stack. Keep one base file, `compose.yaml`, that defines the services as they run everywhere; layer **overrides** for development (`compose.override.yaml`, loaded automatically) and for other environments (`compose.prod.yaml`, selected with `-f`). Each service that you build has its own directory under `services/<name>/` with a `Dockerfile` and a `.dockerignore`. Configuration comes from an `.env` file (gitignored) with a committed `.env.example`; data lives in **named volumes**, not in the image. Add **healthchecks** and `depends_on` with `condition: service_healthy` so startup order is real, not hoped for. The outcome: `docker compose up` gives any contributor a working stack in one command, and the same service definitions carry into CI.

## Principles & why

1. **One command to a running system.** A new contributor should need Docker and one `docker compose up`, nothing else.
2. **Base plus overrides, not copies.** The shared shape is defined once; environments differ through small override files, so drift is visible.
3. **Images are immutable, data is not.** Code and dependencies go in the image; databases and uploads live in named volumes or bind mounts, so rebuilding never destroys state.
4. **Configuration from the environment.** Services read settings from environment variables, populated from `.env` and Compose interpolation (see `config-and-secrets-placement`); no secrets in images or committed files.
5. **Ready means healthy.** A container running is not a service ready. Healthchecks and `depends_on: condition: service_healthy` encode readiness.
6. **Each service owns its build context.** A service's `Dockerfile`, ignore file, and source live together, so the context sent to the daemon is small and caching works.

## When to use

- **Local development of applications with more than one process**, such as an API with a database and a cache.
- **Integration tests in CI** that need real dependencies.
- **Small production deployments** on a single host, where Compose is sufficient.
- **Reproducible demos and onboarding environments.**

## When NOT to use

- **Multi-host, high-availability production.** Use an orchestrator (Kubernetes, Nomad, a managed container service) for scheduling across machines.
- **A single container.** `docker run` or a plain `Dockerfile` is enough.
- **Purely local tools** that need no isolation; forcing containers adds friction.
- **Secrets management.** Compose can pass secrets, but it is not a secret store (see `config-and-secrets-placement`).

## Tree diagram

```
project/
├── compose.yaml                 ← base: services as they run everywhere
├── compose.override.yaml        ← dev overrides: bind mounts, debug ports (auto-loaded)
├── compose.prod.yaml            ← production overrides (use -f)
├── .env                         ← real values, gitignored
├── .env.example                 ← names only, committed
├── services/
│   ├── api/
│   │   ├── Dockerfile
│   │   ├── .dockerignore
│   │   └── src/
│   └── web/
│       ├── Dockerfile
│       └── .dockerignore
├── db/
│   └── init/                    ← SQL run once on first start
└── README.md
```

## Naming rules

- **Compose files**: `compose.yaml` is the preferred name (`docker-compose.yml` still works); override files are `compose.override.yaml` and `compose.<env>.yaml`.
- **Service names** are lowercase kebab-case nouns (`api`, `web`, `postgres`, `redis`); they double as hostnames on the Compose network.
- **Volume names** describe content and owner (`postgres-data`, `uploads`), not the container.
- **Image names** for built services follow `<registry>/<project>/<service>:<tag>`, with tags from version or commit, never only `latest`.
- **Environment variables** are `UPPER_SNAKE_CASE` with a project prefix for anything you define; keep the list in `.env.example`.
- **Directories** under `services/` match the service names in `compose.yaml`.

## Worked example

A README says "install Postgres, Redis, and Python 3.12, then run three commands." New contributors take a day to get running.

1. Create `services/api/Dockerfile` and `.dockerignore` (exclude `.git`, `node_modules`, `.venv`, `.env`).
2. Write `compose.yaml` with `api`, `postgres`, and `redis`. Give postgres a healthcheck (`pg_isready`) and a named volume; make `api` depend on it with `condition: service_healthy`.
3. Put settings in variables: `POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?set in .env}`; the `:?` form fails fast if unset.
4. Add `.env.example` with names and no real values, and gitignore `.env`.
5. Add `compose.override.yaml` for development: bind-mount the source (`./services/api/src:/app/src`), publish debug ports, and enable reload. Use `docker compose watch` if you prefer sync-based development.
6. Validate the merged result: `docker compose config`.
7. Run: `cp .env.example .env`, fill it, then `docker compose up --build`.
8. In CI: `docker compose -f compose.yaml up -d --wait`, run tests, then `docker compose down -v`.

Setup becomes one command, and CI uses the same definitions.

## Anti-patterns

- **Secrets in `compose.yaml` or images.** Anyone with the repo or the image sees them; use `.env` (gitignored) or secret mechanisms.
- **Data inside containers.** Removing the container deletes it; use named volumes.
- **`depends_on` without health conditions** for services that need to be ready, leading to race conditions at startup.
- **One huge build context.** Building from the repository root sends everything to the daemon and breaks caching; give each service its own context.
- **`latest` tags** for base images and built images. They make builds non-reproducible.
- **Copying production values into `compose.override.yaml`.** Dev overrides are for development conveniences only.
- **Running as root** inside containers without need; set a non-root user in Dockerfiles.

## Scaling & failure modes

- **Many services**: use `profiles` to start subsets (`docker compose --profile worker up`) and `include` to compose files from several directories.
- **Build time**: order Dockerfile layers by change frequency (dependencies before source), use BuildKit cache mounts, and keep `.dockerignore` tight.
- **Environment differences**: past two environments, prefer explicit `compose.<env>.yaml` files over conditionals in one file.
- **Production growth**: when you need multiple hosts, rolling updates, or autoscaling, keep the service directories and Dockerfiles, and move deployment to an orchestrator.
- **Local resource limits**: heavy stacks strain laptops; document minimum memory, and offer a `profiles` minimal stack.

## Variants

- **Base plus override** (this guide): default development stack, production via `-f`.
- **Compose per service directory**: each service has its own `compose.yaml`, combined with `include`.
- **Dev containers**: `.devcontainer/` describes the development environment and reuses Compose services.
- **Compose for tests only**: a `compose.test.yaml` used only by CI.
- **Compose plus an orchestrator**: Compose for local, Kubernetes manifests or Helm for production, sharing Dockerfiles.

## Adoption checklist

- [ ] `cp .env.example .env && docker compose up --build` works on a clean clone.
- [ ] `docker compose config` shows the merged file without errors.
- [ ] No secret appears in `compose*.yaml`, Dockerfiles, or image layers.
- [ ] Stateful services use named volumes and healthchecks.
- [ ] Every service has a Dockerfile, a `.dockerignore`, and pinned base image tags.
- [ ] CI brings the stack up with `--wait` and tears it down with `-v`.

## Real-world projects using this

- **The Compose Specification** (compose-spec.io) and Docker's Compose documentation define file names, `include`, `profiles`, `develop.watch`, and health-based `depends_on`.
- **Docker's "awesome-compose"** repository collects sample stacks for common frameworks and databases.
- **The Twelve-Factor App** informs configuration and disposability principles used here.
- **Open-source projects** such as Sentry (self-hosted), Plausible, and Immich ship Compose files for self-hosting; reading them shows production-grade Compose conventions.

## Migration & references

- **From README-driven setup:** write the Dockerfile per service, then the base `compose.yaml`, and delete the manual steps from the README.
- **From `docker-compose.yml` v2/v3 files:** rename to `compose.yaml`, drop the obsolete top-level `version` key, and run `docker compose config` to validate.
- **From Compose to Kubernetes:** keep Dockerfiles, translate services to Deployments and Services (tools such as Kompose can start you off), and treat volumes and config as the hard parts.
- **References:**
  - `principles/config-and-secrets-placement/` for `.env` handling.
  - `code/fastapi-project/` and `code/django-project/` for typical service layouts.
  - `code/terraform-infrastructure/` for provisioning the hosts and networks around these services.
  - `principles/generated-vs-source-separation/` for what not to commit.
