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
