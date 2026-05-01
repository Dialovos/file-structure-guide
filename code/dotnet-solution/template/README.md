# MySolution — .NET solution template

A `cp -r`-able starter for a multi-project .NET solution: `.sln` at
the root, `src/<Project>/` for each shippable assembly, `tests/<Project>.Tests/`
mirroring. Folder, project, and namespace names are PascalCase per
.NET convention.

## Layout at a glance

```
.
├── MySolution.sln                          # solution entry point
├── Directory.Build.props                    # repo-wide MSBuild props
├── Directory.Packages.props                 # central NuGet versions
├── src/
│   ├── MySolution.Core/                    # shared domain library
│   │   ├── MySolution.Core.csproj
│   │   └── Class1.cs                       # Greeter type
│   ├── MySolution.Api/                     # ASP.NET Core minimal API
│   │   ├── MySolution.Api.csproj
│   │   └── Program.cs
│   └── MySolution.Cli/                     # console app
│       ├── MySolution.Cli.csproj
│       └── Program.cs
├── tests/
│   ├── MySolution.Core.Tests/              # xUnit
│   │   ├── MySolution.Core.Tests.csproj
│   │   └── Class1Tests.cs
│   └── MySolution.Api.Tests/               # add when ready
└── .github/workflows/ci.yml                # restore, build, test, format
```

## What to rename

`MySolution` is the placeholder. Rename it everywhere:

- The `.sln` filename and all `Project(...)` lines in the file.
- Every directory under `src/` and `tests/` that starts with `MySolution.`.
- Every `.csproj` filename and the `<RootNamespace>` / `<AssemblyName>`
  inside it.
- The `namespace` declaration and any `using MySolution....` lines in
  every `.cs` file.

A repo-wide find/replace covers most of it:

```bash
# At the template root, after copying:
find . -type f \( -name '*.cs' -o -name '*.csproj' -o -name '*.sln' \
                 -o -name '*.props' -o -name '*.yml' -o -name 'README.md' \) \
  -exec sed -i 's/MySolution/YourSolution/g' {} +

# Rename directories.
for d in src/MySolution.* tests/MySolution.*; do
  mv "$d" "${d/MySolution/YourSolution}"
done
mv src/MySolution.* src/YourSolution.* 2>/dev/null || true

# Rename csproj files.
find src tests -name 'MySolution.*.csproj' | while read f; do
  mv "$f" "${f/MySolution/YourSolution}"
done

# Rename the .sln itself.
mv MySolution.sln YourSolution.sln
```

## What to fill

- `Directory.Packages.props` — pin the NuGet versions you actually use.
- `src/MySolution.Core/Class1.cs` — replace `Greeter` with your domain.
- `src/MySolution.Api/Program.cs` — flesh out the API.
- `src/MySolution.Cli/Program.cs` — adopt System.CommandLine for real
  arg parsing.
- `tests/MySolution.Core.Tests/Class1Tests.cs` — add real test cases.
- `tests/MySolution.Api.Tests/` — add a Web SDK test project when ready.
- `LICENSE` — replace `{{YEAR}}` and `{{NAME}}`.

## What to delete

- This `README.md` once the project has its own.
- Projects you don't need (Api, Cli, etc.). Remove them from the
  `.sln` with `dotnet sln MySolution.sln remove src/MySolution.Cli/MySolution.Cli.csproj`.

## First run

```bash
dotnet restore MySolution.sln
dotnet build MySolution.sln
dotnet test MySolution.sln
dotnet run --project src/MySolution.Cli alice
# → hello, alice
dotnet run --project src/MySolution.Api
# → listening on http://localhost:5000
```

## Adding a new project

```bash
dotnet new classlib -o src/MySolution.NewThing -n MySolution.NewThing
dotnet sln MySolution.sln add src/MySolution.NewThing/MySolution.NewThing.csproj

# Add a test project for it:
dotnet new xunit -o tests/MySolution.NewThing.Tests -n MySolution.NewThing.Tests
dotnet sln MySolution.sln add tests/MySolution.NewThing.Tests/MySolution.NewThing.Tests.csproj
dotnet add tests/MySolution.NewThing.Tests/MySolution.NewThing.Tests.csproj \
  reference src/MySolution.NewThing/MySolution.NewThing.csproj
```

## Adding a NuGet dependency

With Central Package Management, declare the version *once*:

1. In `Directory.Packages.props`, add
   `<PackageVersion Include="Polly" Version="8.4.0" />`.
2. In the project that needs it, add
   `<PackageReference Include="Polly" />` (no `Version`).

## Pair this with

- `../GUIDE.md` — full reasoning, including the `Directory.Build.props`
  + `Directory.Packages.props` combo.
- `../../java-gradle-multi/` — analogous multi-project layout in Java.
- `../../node-library/` — the equivalent shape for npm libraries.
