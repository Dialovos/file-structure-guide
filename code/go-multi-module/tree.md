```
my-repo/
├── README.md
├── core/
│   ├── go.mod
│   └── core.go
├── client/
│   ├── go.mod                  ← depends on core via replace or version
│   └── client.go
├── server/
│   ├── go.mod
│   └── server.go
└── tools/
    └── go.mod                  ← independent from main modules
```
