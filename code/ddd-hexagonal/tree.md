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
