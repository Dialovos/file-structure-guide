# FastAPI project — template

A `cp -r`-able starter for a layered FastAPI service. Routers stay
thin, services hold logic, schemas describe the wire, models describe
the database, config lives in one place. Modeled after
`tiangolo/full-stack-fastapi-template` and the conventions in
`zhanymkanov/fastapi-best-practices`.

## What to rename

- `myapi` → your service name in `pyproject.toml`,
  `app/__init__.py`, and the `app_name` default in
  `app/core/config.py`.
- The `users` and `items` resources are placeholders; rename or
  remove them once you have your real first resource.

## What to fill

- **`app/core/config.py`** — add settings as the service grows
  (Redis URL, S3 bucket, third-party keys). All env vars belong here.
- **`app/core/security.py`** — replace the SHA-256 stubs with
  `passlib` bcrypt and JWT issuance via `python-jose`.
- **`app/db/session.py`** — switch from SQLite to Postgres in
  `.env` (`DATABASE_URL=postgresql+psycopg://...`) and update
  `pool_*` settings as you scale.
- **`app/models/`** — replace `User` and `Item` with your real
  entities; remember to register them in `app/models/__init__.py`.
- **`alembic/`** — initialise migrations: `alembic init alembic`
  inside this directory (the `.gitkeep` is a placeholder until you
  do).
- **`LICENSE`** — replace `{{YEAR}}` and `{{NAME}}`.

## What to delete

- This `README.md` once you have a real one.
- The placeholder users/items resources once your real domain
  lands.

## First run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the auto-generated Swagger UI,
`/api/v1/users/1` to hit the stub, and `/healthz` for the liveness
probe.

Run tests with:

```bash
pytest
```

## Layout cheat-sheet

| You're looking for…              | Path                                  |
|----------------------------------|---------------------------------------|
| The FastAPI instance             | `app/main.py`                         |
| Endpoints for `/api/v1/users`    | `app/api/v1/routers/users.py`         |
| Pydantic request/response shapes | `app/schemas/users.py`                |
| SQLAlchemy ORM classes           | `app/models/user.py`                  |
| Business logic                   | `app/services/users.py`               |
| Config / env vars                | `app/core/config.py`                  |
| DB engine + session              | `app/db/session.py`                   |
| Migrations                       | `alembic/`                            |

## Pair this with

- `../GUIDE.md` — full reasoning behind the layered layout.
- `../../python-flat-layout/` — the underlying Python layout shape.
- `../../ddd-hexagonal/` — when domain logic justifies the heavier
  pattern.
- `../../django-project/` — when you want batteries-included instead.
