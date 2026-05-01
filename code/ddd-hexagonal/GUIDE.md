## TL;DR

The **DDD-hexagonal layout** organises a service into three concentric layers — `domain/`, `application/`, `infrastructure/` — plus a thin `interfaces/` rim where transports live. The dependency rule is *inward*: infrastructure imports domain, never the other way around. The shape: `domain/` holds entities, value objects, domain events, and **ports** (abstract interfaces like `OrderRepository`); it has zero framework imports — no FastAPI, no SQLAlchemy, no `requests`. `application/` holds use cases (`commands/place_order.py`, `queries/...`) that orchestrate domain objects via ports; it depends only on `domain/`. `infrastructure/` holds **adapters** that implement the ports — `SqlAlchemyOrderRepository`, `RabbitPublisher`, `FastAPIApp` — and depends on whatever vendor library each adapter wraps. `interfaces/` (`api/`, `cli/`, `worker/`) is the entry-point rim: it wires the application layer up to a transport. Tests mirror the layers: `tests/unit/` runs against fakes (no DB), `tests/integration/` runs adapters against real systems, `tests/e2e/` runs the whole hexagon. Adopt this when the domain is rich enough to model and you'll pay to make it replaceable. Skip it for CRUD shells whose "domain" is the database schema with a coat of paint.

## Principles & why

Hexagonal architecture (Cockburn 2005) and DDD (Evans 2003) converge on the same shape because they're solving the same problem: keep business logic isolated from incidental technology choices.

1. **Dependency direction is inward.** The domain knows nothing about the database, the message bus, or the HTTP framework. Adapters in `infrastructure/` import domain types and implement ports defined in `domain/ports/`. This means: replacing Postgres with DynamoDB, RabbitMQ with Kafka, or FastAPI with gRPC is a pure infrastructure change. The use cases never know.
2. **Ports and adapters are explicit.** A port is an interface owned by the domain ("we need somewhere to save orders" → `OrderRepository`). An adapter is a concrete implementation owned by infrastructure (`SqlAlchemyOrderRepository`). The use case takes the port as a parameter; the composition root (in `interfaces/api/` or `interfaces/cli/`) injects the adapter. Tests inject fakes. The pattern collapses to "constructor injection of an interface" — Python uses `Protocol` or `ABC`.
3. **Use cases are the application layer.** `application/commands/place_order.py` is a thin orchestrator: load aggregates via repository ports, call domain methods, publish domain events, save. It contains no business rules — those live in domain methods on the entities themselves. It contains no transport details — those live in `interfaces/api/`. Use cases are the script the domain follows when something happens; nothing more.

The trade-off is real: more files, more classes, more thinking before any line of code runs. The reward is replaceability, testability without test-only frameworks, and a domain model that survives technology changes. CRUD apps should not pay this cost; the domain is the schema. Long-lived services with non-trivial business rules should pay it on day one — retrofitting the inversion later is a rewrite.

## When to use

- **Long-lived services with rich domain logic.** Order management, billing, payments, scheduling, anything where business rules change without the database changing.
- **Teams committing to TDD or property-based testing.** Domain unit tests run in milliseconds with fakes; this layout makes that the default mode.
- **Services where the technology stack will change.** Migrating from a SQL DB to a document store, swapping HTTP for gRPC, replacing a third-party API with an in-house one — hexagonal pays for itself the first time this happens.
- **Microservices owned by small, autonomous teams.** Clear boundaries inside the service mirror clear boundaries between services; the team can move faster within their hexagon.
- **Event-driven and CQRS systems.** The CQRS variant fits the hexagon naturally: queries live in `application/queries/`, commands in `application/commands/`, events in `domain/events/`.

## When NOT to use

- **CRUD shells whose "domain" is the database schema.** If the use case for "create user" is `INSERT INTO users; return row`, you have no domain — use `code/fastapi-project/` or `code/django-project/` and skip the ceremony.
- **Prototypes and spikes.** The point of a prototype is to find out what the domain is. Build it concretely, then refactor toward hexagonal once you know which parts deserve isolation.
- **Tiny services (≤3 endpoints, no business rules).** A layered FastAPI service is plenty.
- **Junior teams without DDD experience.** The layout is mechanical; the discipline is not. Without someone enforcing the dependency rule, everyone reaches into infrastructure from domain and the architecture quietly inverts. Start with `code/fastapi-project/` and graduate when the team is ready.
- **Frontend apps.** Hexagonal works on the backend because there are real adapters to swap (DBs, queues, HTTP clients). Frontend "infrastructure" is the framework itself; you'll fight more than you gain. Use `code/feature-based-frontend/` or `code/atomic-design/`.

## Tree diagram

```
myservice/
├── README.md
├── pyproject.toml
├── src/
│   └── myservice/
│       ├── domain/                     ← entities, value objects, domain services
│       │   ├── models/
│       │   │   └── order.py
│       │   ├── events/
│       │   └── ports/                  ← interfaces (e.g., OrderRepository)
│       │       └── order_repository.py
│       ├── application/                ← use cases / orchestration
│       │   ├── commands/
│       │   │   └── place_order.py
│       │   ├── queries/
│       │   └── handlers/
│       ├── infrastructure/             ← adapters
│       │   ├── persistence/
│       │   │   └── sqlalchemy_order_repo.py    ← implements port
│       │   ├── messaging/
│       │   │   └── rabbit_publisher.py
│       │   └── http/
│       │       └── fastapi_app.py
│       └── interfaces/                 ← entry points (HTTP, CLI, worker)
│           ├── api/
│           └── cli/
└── tests/
    ├── unit/                           ← no infrastructure
    ├── integration/                    ← infra + app, no HTTP
    └── e2e/
```

## Naming rules

- **Top-level package**: the service name in snake_case (`myservice/`). One service per repository; sub-services are separate repositories.
- **Domain entities**: singular, business names — `Order`, `Customer`, `Invoice`. Files are `domain/models/order.py` (one entity per file once they grow). Avoid technology suffixes (`OrderModel`, `OrderEntity`) — the domain doesn't know it's "a model."
- **Value objects**: `domain/models/value_objects/money.py`, `domain/models/value_objects/email.py`. Frozen dataclasses or Pydantic-strict; equality is structural.
- **Ports**: `domain/ports/<entity>_repository.py` for storage, `domain/ports/<service>_gateway.py` for outbound calls. The class is `OrderRepository` — *not* `IOrderRepository` (the leading-`I` is a C# habit; Python uses `Protocol` or `ABC` and skips the prefix).
- **Use cases**: `application/commands/<verb>_<noun>.py` for state-changing (`place_order.py`, `cancel_subscription.py`); `application/queries/<noun>_by_<criterion>.py` for read-only.
- **Adapters**: `infrastructure/<concern>/<technology>_<port>.py` — e.g., `infrastructure/persistence/sqlalchemy_order_repo.py` implements `OrderRepository`. The technology in the filename is intentional; another adapter for the same port is `infrastructure/persistence/dynamo_order_repo.py`.
- **Domain events**: `domain/events/<entity>_<past_tense_verb>.py` — `order_placed.py`, `payment_failed.py`. Past tense matters; events describe what happened.
- **Handlers**: `application/handlers/on_<event>.py` — one handler per event subscription.

## Anti-patterns

- **Domain importing infrastructure.** `from sqlalchemy import Column` in `domain/models/order.py` is the cardinal sin. The domain must not know its persistence story. Fix: keep the entity a plain dataclass; let the adapter do the SQLAlchemy mapping.
- **Anaemic domain model.** Entities that are pure data with all logic in services. The DDD term is "anaemic"; the symptom is `OrderService.calculate_total(order)` where it should be `order.calculate_total()`. Push behaviour onto the entity until services orchestrate, not compute.
- **Repositories that return DTOs instead of entities.** `OrderRepository.find_by_id` returns a `dict` to "decouple from the domain." Now the domain is decoupled from itself. Repositories return domain objects; the use case decides whether to expose them.
- **Use cases doing transport work.** `application/commands/place_order.py` reading HTTP headers or parsing JSON. That's `interfaces/api/`. The use case takes parsed parameters and does business orchestration.
- **Ports owned by infrastructure.** Defining `OrderRepository` in `infrastructure/` means infrastructure is dictating the domain's needs. The port lives in `domain/ports/`; infrastructure is the implementation, not the spec.
- **One giant application service.** `OrderService` with 40 methods. Split into one use case per file (`place_order.py`, `cancel_order.py`, `refund_order.py`). The naming is verbose; the discoverability is excellent.
- **Tests that hit the real DB by default.** Unit tests should not need Docker. Use an in-memory `FakeOrderRepository` that satisfies the port; reserve real DB tests for `tests/integration/`.

## Variants

- **Classic DDD 3-layer** (this guide) — domain / application / infrastructure with `interfaces/` for transports. The mainstream Python interpretation, popularised by *Cosmic Python*.
- **CQRS-extended** — separate command and query stacks. `application/commands/` writes through the domain; `application/queries/` reads from a denormalised projection. Pays off when read and write workloads diverge.
- **Event-sourced** — aggregates are reconstructed from event streams; the source of truth is `domain/events/`, not a relational table. Heavier; correct for audit-heavy domains.
- **Onion architecture** (Jeffrey Palermo) — same idea, different naming: domain → domain services → application services → infrastructure. The layers are concentric and the rule is the same; the diagrams differ. Treat it as a re-skin of hexagonal.
- **Clean Architecture** (Robert Martin) — same shape with another naming convention (entities / use cases / interface adapters / frameworks). Use whichever vocabulary your team prefers; the structure is identical.
- **Hexagonal lite** — collapse `application/` into `domain/` for very small services. Re-emerge `application/` once you have more than ~5 use cases.

## Real-world projects using this

- **Cosmic Python** (`cosmicpython/code`, by Harry Percival & Bob Gregory) — the canonical Python reference; the book *Architecture Patterns with Python* walks through this exact layout.
- **Vaughn Vernon's `iddd_samples`** — Java sample code from *Implementing Domain-Driven Design*; the Python community borrows freely from it.
- **Microsoft's `eShopOnContainers`** — .NET reference architecture for microservices; explicit hexagonal/DDD layering. Translates straight to Python.
- **DDD-ified Django apps** — projects that move logic out of `models.py` and `views.py` into a `domain/` package; Django itself doesn't enforce the layout, but several open-source projects (e.g., `django-cqrs` examples) do.
- **AWS sample event-driven architectures** — `aws-samples/aws-serverless-airline-booking` adopts a CQRS/hexagonal split.
- **Internal services at large companies** — Spotify's backend conventions, Monzo's microservice templates, and many fintech codebases ship with a similar shape; not always public but widely discussed in conference talks.

## Migration & references

- **From a layered service** (`code/fastapi-project/`): pick one resource. Move its model out of `models/<resource>.py` into `domain/models/<resource>.py` as a plain dataclass. Define `domain/ports/<resource>_repository.py` as a `Protocol`. Wrap the existing SQLAlchemy code as `infrastructure/persistence/sqlalchemy_<resource>_repo.py`. Move the service code to `application/commands/`. The router in `interfaces/api/` constructs the adapter and calls the use case. Repeat per resource.
- **From an anaemic model**: list the methods on the service that take an entity as the first argument. Each is a candidate for a method on the entity. Move them one at a time; let the service shrink. Stop when the service only orchestrates (load → call entity method → save).
- **From scattered ports**: any abstract base class or `Protocol` that `application/` consumes goes into `domain/ports/`. Any concrete implementation goes into `infrastructure/<concern>/`. Don't move the implementation back across the line.
- **From mixed transports**: split `interfaces/` into `interfaces/api/`, `interfaces/cli/`, `interfaces/worker/`. Each transport is independently testable; each constructs its own composition root. The application layer doesn't change.
- **References**:
  - *Architecture Patterns with Python* (Harry Percival & Bob Gregory) — the book this guide most closely tracks; also at `cosmicpython.com`.
  - *Implementing Domain-Driven Design* (Vaughn Vernon) — the book that grounded modern DDD; samples in `iddd_samples`.
  - Alistair Cockburn's original *Hexagonal Architecture* article (`alistaircockburn.com/Hexagonal+architecture`) — short, formative.
  - Robert C. Martin, *Clean Architecture* — same shape, different vocabulary.
  - Microsoft's `eShopOnContainers` repo — concrete reference architecture (.NET).
  - Sibling guides: `code/fastapi-project/` (start here, graduate to hexagonal when domain warrants), `code/python-src-layout/` (this guide builds on src layout), `code/plugin-architecture/` (related dependency-inversion pattern), `principles/depth-vs-breadth/`.
