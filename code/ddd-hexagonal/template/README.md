# DDD + hexagonal — template

A `cp -r`-able starter for a Domain-Driven Design service organised
around hexagonal (ports & adapters) layers. The dependency rule:
domain <- application <- infrastructure. The domain has zero
framework imports; adapters in infrastructure implement domain ports;
interfaces/ wires everything up at the composition root.

## What to rename

- `myservice` → your service name in `pyproject.toml`,
  `src/myservice/__init__.py`, `tests/unit/test_place_order.py`,
  the `infrastructure/http/fastapi_app.py` title, and any
  cross-references.
- `Order`, `OrderRepository`, `PlaceOrder` are placeholders.
  Replace with your real first aggregate, port, and use case once
  you've identified them.

## What to fill

- **`domain/models/`** — your real aggregates and value objects.
  Keep them framework-free.
- **`domain/ports/`** — every outbound dependency (storage,
  messaging, third-party APIs) gets a port here.
- **`application/commands/`** — one use case per file
  (`<verb>_<noun>.py`).
- **`infrastructure/persistence/`** — adapters per backing store.
  Add Alembic migrations alongside.
- **`interfaces/api/`** — HTTP routes that translate requests into
  use-case calls. Keep transport concerns out of `application/`.
- **`LICENSE`** — replace `{{YEAR}}` and `{{NAME}}`.

## What to delete

- This `README.md` once you have a real one.
- The placeholder `Order`/`PlaceOrder`/`SqlAlchemyOrderRepository`
  example once your real domain lands.

## First run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest tests/unit          # fast, no DB
uvicorn myservice.infrastructure.http.fastapi_app:build_app --factory --reload
```

## Layout cheat-sheet

| You're looking for…              | Path                                                         |
|----------------------------------|--------------------------------------------------------------|
| Aggregate / entity               | `src/myservice/domain/models/order.py`                       |
| Domain event                     | `src/myservice/domain/events/order_placed.py`                |
| Outbound interface (port)        | `src/myservice/domain/ports/order_repository.py`             |
| Use case                         | `src/myservice/application/commands/place_order.py`          |
| DB adapter (implements port)     | `src/myservice/infrastructure/persistence/sqlalchemy_order_repo.py` |
| HTTP composition root            | `src/myservice/infrastructure/http/fastapi_app.py`           |
| Unit test (no DB, fake repo)     | `tests/unit/test_place_order.py`                             |

## Dependency rule (do not break)

```
interfaces/  -->  infrastructure/  -->  application/  -->  domain/
                                          ^                 ^
                                          |                 |
                                       (consumes ports)  (defines ports)
```

If `domain/` ever imports from `infrastructure/`, the architecture
has inverted; fix immediately or the layout buys you nothing.

## Pair this with

- `../GUIDE.md` — reasoning behind the layout.
- `../python-src-layout/` — this template builds on src layout.
- `../fastapi-project/` — start there if you don't have rich domain
  logic yet; graduate to hexagonal when you do.
- `../plugin-architecture/` — related dependency-inversion pattern.
