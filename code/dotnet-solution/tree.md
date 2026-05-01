```
MySolution/
├── MySolution.sln
├── README.md
├── LICENSE
├── .gitignore
├── .editorconfig
├── Directory.Build.props           ← shared MSBuild properties
├── Directory.Packages.props        ← central package versioning
├── src/
│   ├── MySolution.Core/
│   │   ├── MySolution.Core.csproj
│   │   └── Class1.cs
│   ├── MySolution.Api/
│   │   └── MySolution.Api.csproj
│   └── MySolution.Cli/
│       └── MySolution.Cli.csproj
└── tests/
    ├── MySolution.Core.Tests/
    │   ├── MySolution.Core.Tests.csproj
    │   └── Class1Tests.cs
    └── MySolution.Api.Tests/
```
