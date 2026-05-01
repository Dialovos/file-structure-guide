## TL;DR

The **layered FastAPI layout** separates the HTTP boundary from the domain so a service can scale past the `main.py`-with-everything stage. The shape: `app/main.py` builds the FastAPI instance and includes versioned routers. `app/api/v1/routers/<resource>.py` holds endpoints. `app/schemas/` holds Pydantic request/response shapes. `app/models/` holds SQLAlchemy ORM models. `app/services/` holds business logic that the routers call. `app/db/` holds the engine + session factory. `app/core/` holds configuration (`pydantic-settings`) and security helpers. `alembic/` holds migrations. The discipline: routers are thin (parse, call service, return); services own logic; schemas describe the wire; models describe the DB. The layout is the one popularized by tiangolo's `full-stack-fastapi-template` and zhanymkanov's `fastapi-best-practices` — it's table-stakes for any FastAPI service that has more than two endpoints. Adopt it on day one and the service will absorb growth without restructuring.

## Principles & why

The layered FastAPI layout enforces three separations.

1. **HTTP layer vs domain.** A FastAPI router translates HTTP into function calls and back. It should not contain business logic. When a router calls `services.users.create_user(db, payload)`, the service can be reused by a Celery task, a CLI, or a different transport (gRPC, WebSocket) without rewriting the logic.
2. **Wire shape vs storage shape.** `schemas/` (Pydantic) and `models/` (SQLAlchemy) are *not* the same types. Coupling them to a single class is the most common FastAPI sin. Schemas evolve at the speed of API consumers; models evolve at the speed of the database. Forcing them to share a class freezes both.
3. **Config in one place.** `app/core/config.py` with `pydantic-settings` reads environment variables once and exposes a typed `Settings` object. Every other module imports `settings`; nothing else touches `os.environ`. This makes the config surface grep-able (`from app.core.config import settings`) and testable (override via fixture).

The layout makes versioning explicit (`api/v1/`). When you ship `v2`, you add `api/v2/` next to `v1/` and switch `main.py` to mount both. Old clients keep working; new clients use the new shape. This is the version-of-the-API-as-a-folder pattern, not version-via-Accept-header.

The trade: more files for tiny services. A 50-line FastAPI demo doesn't need this; one `main.py` is honest. The break-point is around 5–10 endpoints or any service shipping to production. Past that, the layout pays for itself.

## When to use

- **Production FastAPI services** that grew beyond `main.py` or are about to.
- **Teams with separate frontend and backend developers.** Predictable directory layout means the frontend dev can locate the schema for `POST /users` in seconds.
- **Services that will outlive their first version of the API.** The `api/v1/` folder is forward-compatible with `api/v2/`.
- **Services with non-trivial business logic.** The `services/` layer keeps domain code testable in isolation from FastAPI and SQLAlchemy.
- **Anything you'd Dockerize.** The layout pairs naturally with a Dockerfile (`COPY app /app`, `uvicorn app.main:app`).

## When NOT to use

- **Single-file FastAPI demos.** `main.py` with `app = FastAPI()` and a few endpoints is the right size for tutorials and 50-line APIs.
- **Notebooks-with-an-endpoint** experiments. Use `main.py` until the demo lands; then refactor.
- **Non-FastAPI Python web frameworks.** Starlette, Litestar, Falcon — similar shape but different conventions; check the framework's own template.
- **Services that are really CLIs in disguise.** If the HTTP layer is a thin wrapper around a `click` command, structure as a CLI tool first; expose the HTTP layer when needed. See `code/cli-tool/`.
- **DDD / hexagonal projects.** The layered layout is fine but the DDD-flavored variant (`code/ddd-hexagonal/`) is closer to what you want — explicit ports/adapters.

## Tree diagram

```
myapi/
├── pyproject.toml
├── README.md
├── app/
│   ├── __init__.py
│   ├── main.py                 ← FastAPI() instance, includes routers
│   ├── core/
│   │   ├── config.py           ← pydantic-settings
│   │   └── security.py
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── routers/
│   │       │   ├── users.py
│   │       │   └── items.py
│   │       └── __init__.py
│   ├── models/                 ← SQLAlchemy models
│   ├── schemas/                ← Pydantic schemas (request/response)
│   ├── services/               ← business logic
│   └── db/
│       ├── base.py
│       └── session.py
├── alembic/                    ← migrations
├── tests/
└── .env.example
```

## Naming rules

- **Top-level package**: `app/`. Singular, generic — convention from `tiangolo/full-stack-fastapi-template`. Don't rename it without reason; tooling and docs assume it.
- **Routers**: one file per resource, plural noun matching the URL — `users.py` for `/users`, `items.py` for `/items`. Each file exposes one `router = APIRouter(prefix="/users", tags=["users"])`.
- **Schemas**: `app/schemas/users.py` exports `UserCreate`, `UserRead`, `UserUpdate`. Use the `Create` / `Read` / `Update` suffix so router signatures are self-documenting.
- **Models**: `app/models/user.py` exports a single `User` SQLAlchemy class. Singular here, plural in routers and schemas — the naming reflects the underlying shape (one row class, many request shapes).
- **Services**: `app/services/users.py` exports functions, not classes by default. Functions take a DB session and a schema, return a model or schema. Move to classes only when you have shared state.
- **Files inside `app/api/v1/routers/`** mirror resource names; the v1 router (`app/api/v1/__init__.py`) `include_router`s each one.
- **Tests**: `tests/test_users.py` mirrors `app/api/v1/routers/users.py`. Same names, same plurality.
- **Settings class**: `app/core/config.py` exports `class Settings(BaseSettings)` and a module-level `settings = Settings()`. Every other module imports the *instance*, not the class.

## Anti-patterns

- **Fat routers.** Endpoint functions doing 80 lines of DB queries and business rules. Push that into a service; routers should be 3–10 lines.
- **Sharing a single class for ORM model and Pydantic schema.** The `from_orm` shortcut makes this seem like a feature; it's a future-pain debt. Keep them separate. (FastAPI's docs nudge you toward separation in the SQL tutorial.)
- **`os.environ.get()` scattered across modules.** Centralize in `app/core/config.py`. If you find a module reading env vars directly, refactor it to import `settings`.
- **Versioning via the Accept header alone.** Folder versioning is the simpler convention. Header versioning is fine *also* but should not be your first move.
- **One giant `models.py`.** SQLAlchemy models grow; split per entity into `app/models/user.py`, `app/models/order.py`. Same for `schemas/`.
- **Tests that import the live `engine`.** Tests should override the `get_db` dependency with a session bound to a transactional test fixture. Otherwise tests pollute or are polluted by dev data.
- **Routers importing other routers.** Routers compose at the app/v1 level, not at the resource level. If `users.py` needs something from `items.py`, that "something" is a service.
- **`main.py` doing all the wiring inline.** Keep it minimal: create the `FastAPI` instance, include the v1 router, register lifespan events. Move config-heavy setup into helpers.

## Variants

- **layered** (this guide) — the default: routers / services / schemas / models / db / core.
- **feature-vertical** — `app/features/users/{router,model,schema,service}.py`. Each feature is one folder. Easier to delete a feature; harder to scan all routers at once. Common in larger codebases that have outgrown layered.
- **DDD-hexagonal** — domain / application / infrastructure / ports&adapters. More ceremony; pays off for long-lived services with rich domain logic. See `code/ddd-hexagonal/`.
- **layered + Celery** — add `app/tasks/` for Celery tasks; tasks call the same services as routers do.
- **layered + GraphQL** — replace or supplement `app/api/v1/routers/` with `app/api/graphql/` (Strawberry / Ariadne); services stay the same.
- **One-file `main.py`** — the right size for demos and ≤5-endpoint services. Refactor to layered when growth is real, not anticipated.

## Real-world projects using this

- **`tiangolo/full-stack-fastapi-template`** — the canonical reference; this guide is a slimmed version of its backend.
- **`zhanymkanov/fastapi-best-practices`** (GitHub repo) — a curated list of the conventions this guide encodes.
- **Netflix Dispatch** — open-source FastAPI app for incident response; layered backend.
- **Gravitational Teleport's `web/`** — internal FastAPI services in a similar shape.
- **Many SaaS startups' FastAPI backends** — Render's, Sentry's auxiliary services, plus countless smaller examples on GitHub.
- **Sanic / Starlette / Litestar communities** — similar conventions; the layered shape is broadly applicable across async Python web frameworks.

## Migration & references

- **From `main.py`-with-everything**: extract one resource at a time. Move endpoint functions to `app/api/v1/routers/<resource>.py`. Move logic into `app/services/<resource>.py`. Define schemas in `app/schemas/<resource>.py` and ORM models in `app/models/<resource>.py`. Update `main.py` to `include_router(v1_router)`. Run tests after each resource moves.
- **From version-in-URL but no folder split**: create `app/api/v1/` and move existing routers under it. Add `app/api/v1/__init__.py` that mounts each resource router on a single `APIRouter()`. `main.py` mounts only the v1 router.
- **From shared model/schema classes**: introduce `<Entity>Read`, `<Entity>Create`, `<Entity>Update` Pydantic schemas alongside the ORM `<Entity>`. Update routers to use schemas; keep the ORM class for DB only. Removing the conflation is mechanical but takes a sweep.
- **From scattered config**: create `app/core/config.py` with `pydantic-settings`. Replace every `os.environ` lookup with a `settings.<field>` reference. Add `.env.example` documenting all settings.
- **References**:
  - `tiangolo/full-stack-fastapi-template` — the layout this guide compresses.
  - `zhanymkanov/fastapi-best-practices` — conventions and pitfalls.
  - FastAPI docs — *Bigger Applications* chapter (canonical for routers).
  - SQLAlchemy 2.0 docs — async session + dependency-injection pattern.
  - Pydantic v2 / pydantic-settings docs — config patterns.
  - Sibling guides: `code/python-src-layout/` (when you publish the `app` package), `code/python-flat-layout/` (the underlying flat shape this layout is built on), `code/ddd-hexagonal/` (when domain logic justifies the heavier pattern), `principles/depth-vs-breadth/` (why `app/api/v1/routers/` is depth, not bureaucracy).
