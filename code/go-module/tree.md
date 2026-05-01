```
mymodule/
├── go.mod
├── go.sum
├── README.md
├── LICENSE
├── .gitignore
├── cmd/
│   └── myapp/
│       └── main.go
├── internal/                   ← compiler-enforced privacy
│   ├── auth/
│   │   └── auth.go
│   └── store/
│       └── store.go
├── pkg/                        ← public packages (controversial; many projects skip)
│   └── client/
│       └── client.go
├── api/                        ← OpenAPI/proto specs
└── deployments/                ← Dockerfiles, Helm charts
```
