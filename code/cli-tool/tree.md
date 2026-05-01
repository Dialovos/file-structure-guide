```
mytool/
├── README.md
├── LICENSE
├── go.mod                  ← or pyproject.toml / Cargo.toml / package.json
├── cmd/
│   └── mytool/
│       ├── main.go         ← thin entry: parse, route to subcommand
│       └── completion.go   ← shell completion generation
├── internal/
│   └── commands/
│       ├── root.go
│       ├── foo.go          ← `mytool foo`
│       └── bar.go          ← `mytool bar`
├── docs/
│   └── manpage.md
└── completions/
    ├── _mytool             ← zsh
    ├── mytool.bash
    └── mytool.fish
```
