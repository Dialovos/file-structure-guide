```
myworkspace/
├── Cargo.toml              ← [workspace] members = ["crates/*"]
├── Cargo.lock
├── README.md
├── LICENSE
├── .gitignore
├── crates/
│   ├── core/
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   ├── cli/
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   └── server/
│       ├── Cargo.toml
│       └── src/main.rs
└── target/                  ← gitignored, shared by all crates
```
