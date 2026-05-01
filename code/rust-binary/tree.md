```
mybin/
├── Cargo.toml
├── Cargo.lock
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   ├── main.rs
│   ├── cli.rs              ← CLI args parsing (clap)
│   └── lib.rs              ← optional, exposes guts as a library too
├── tests/
│   └── integration_test.rs
└── examples/
    └── basic.rs
```
