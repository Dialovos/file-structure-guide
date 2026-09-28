## TL;DR

A **dotnet-solution** is the canonical .NET multi-project layout: a `.sln` file at the repo root, every shippable assembly under `src/<Project>/`, and every test project under `tests/<Project>.Tests/`. Folder, project, namespace, and assembly names are **PascalCase** by ecosystem convention — that's the documented exception to the "kebab-case for everything" rule, because the .NET tooling (Visual Studio, `dotnet new`, NuGet packers) generates PascalCase by default and treats the folder name as the assembly name. Modern solutions add **Central Package Management** via `Directory.Packages.props` (single source of NuGet versions for the whole repo), shared MSBuild settings via `Directory.Build.props` (target framework, nullable reference types, language version), and a CI workflow that runs `dotnet test`. This is the layout you see across `dotnet/runtime`, `dotnet/aspnetcore`, `NuGet/NuGet.Client`, and most JetBrains and Octopus Deploy OSS projects. The `.sln` is technically optional — `dotnet build` walks the directory tree without one — but having it gives Visual Studio, Rider, and `dotnet sln` a single entry point and explicit project ordering, which matters for IDE workflows and for newcomers cloning the repo.

## Principles & why

The .NET layout is shaped by a handful of MSBuild and Roslyn behaviours that make the file structure load-bearing.

1. **`*.sln` is the IDE-and-tooling entry point.** `dotnet sln`, Visual Studio, and Rider all key off it. CI scripts that run `dotnet build MySolution.sln` get a deterministic build order; running `dotnet build` against a directory works for most cases but is less explicit.
2. **`Directory.Build.props` cascades.** MSBuild walks up from each `.csproj` looking for `Directory.Build.props`; the first one it finds is imported automatically before any targets. Putting the file at the repo root sets target framework, language version, nullable reference types, and analyzers for *every* project in one place. Per-project overrides still work — they just apply on top.
3. **`Directory.Packages.props` enables Central Package Management (CPM).** With `<ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>`, individual `.csproj` files use `<PackageReference Include="X" />` (no version), and the version comes from `Directory.Packages.props`. This eliminates "two projects pull different versions of Newtonsoft.Json and runtime gets confused" — the most common cause of NuGet upgrade pain.
4. **Folder name = project name = assembly name = root namespace** (by default). PascalCase folders mean PascalCase assemblies and namespaces — `src/MySolution.Core/` ships `MySolution.Core.dll` whose root namespace is `MySolution.Core`. Don't fight this; the entire .NET ecosystem assumes the symmetry.
5. **`src/`/`tests/` separation is convention but ubiquitous.** It makes the test/non-test split obvious to humans and lets `.sln` solution folders mirror the directory layout. The `dotnet/runtime` and `dotnet/aspnetcore` repos both follow it.
6. **Test projects mirror their target.** `MySolution.Core.Tests` tests `MySolution.Core`. The `.Tests` suffix is the convention; some teams use `.UnitTests` / `.IntegrationTests` to distinguish, but the suffix-on-target-name pattern is universal.
7. **`.editorconfig` carries the style contract.** Roslyn analyzers and IDE formatters both read it. C# projects rely heavily on `.editorconfig` rules (`csharp_*` keys) for naming conventions, brace style, `var` policy, etc.

The "why" boils down to: **the toolchain assumes this layout.** Diverging means writing custom MSBuild plumbing to undo defaults, and you'll spend more time fighting tooling than getting work done. PascalCase isn't a stylistic choice; it's how the framework's reflection, NuGet packing, and language defaults all interlock.

## When to use

- **Any non-trivial .NET project.** A library + tests, a web API + library + tests, a CLI + library + tests — all benefit from the `src/` + `tests/` split and shared `Directory.Build.props`.
- **Multi-project solutions with a shared core.** A reusable domain library used by an API, a worker, and a CLI is the textbook case for this layout.
- **Anywhere CI matters.** `dotnet build MySolution.sln` and `dotnet test MySolution.sln` are a uniform pair; CI pipelines stay short.
- **Teams using Visual Studio or Rider.** The `.sln` is the "open this project" target; without one, IDE workflows degrade.
- **Repos publishing NuGet packages.** Central Package Management plus per-project `<IsPackable>true</IsPackable>` and `<PackageId>` makes the NuGet pipeline straightforward.
- **Solutions targeting multiple frameworks.** `<TargetFrameworks>net8.0;net6.0</TargetFrameworks>` in a Library SDK project, controlled centrally by `Directory.Build.props`.

## When NOT to use

- **Single-project tutorials and demos.** `dotnet new console -o HelloWorld` produces a flat `HelloWorld.csproj` + `Program.cs`; adding `src/` for a one-file demo is overhead nobody benefits from.
- **Single-file scripts** using top-level statements or `dotnet-script`. `.csx` files in a flat folder are simpler.
- **Mono-repos with no .NET-specific tooling intent.** If you're cross-language and `.NET` is one of many languages, the .NET solution might live in a subdirectory and the larger repo follows the conventions of `monorepo-tools`.
- **Legacy `.NET Framework` projects** still using `packages.config`. Those follow an older layout (no SDK-style `.csproj`, no `Directory.Build.props`). Migrate to SDK-style first; then this guide applies.
- **You have one team, one project, no tests.** Even then, the `src/` + `tests/` skeleton costs you almost nothing and pays off the first time you add a second project.

## Tree diagram

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

## Naming rules

- **Solution name**: PascalCase, matches the company/product (`MySolution`, `Octopus`, `NuGet`). The `.sln` filename is `<Solution>.sln`.
- **Project (assembly) names**: PascalCase, dotted-segments to namespace the assembly within the solution. `MySolution.Core`, `MySolution.Api`, `MySolution.Data.Sql`. The folder `src/MySolution.Core/` mirrors the assembly name.
- **Namespaces**: match the assembly name; nested namespaces follow folder structure inside the project. `MySolution.Core/Models/Foo.cs` → `namespace MySolution.Core.Models { public class Foo { } }`. The default templates and most analyzers assume this.
- **Test project suffix**: `.Tests` for unit tests; some teams add `.IntegrationTests`, `.UnitTests`, `.E2E`. Pick one and stick to it.
- **Class / interface / method names**: PascalCase. Interfaces start with `I` (`IFoo`, `IUserService`).
- **Local variables, parameters, fields**: camelCase; private fields can use `_camelCase` (Microsoft style) — set this via `.editorconfig`.
- **Constants**: PascalCase by convention (`public const int MaxRetries = 3;`). Some shops use `UPPER_SNAKE`; .NET prefers PascalCase.
- **`csproj` filenames**: must match the project's folder/assembly name exactly. `src/MySolution.Core/MySolution.Core.csproj`, not `MySolution.Core/Project.csproj`.
- **MSBuild property files**: `Directory.Build.props` and `Directory.Packages.props` (PascalCase, dotted) are the magic names; do not rename.
- **Avoid**: `MySolution.Common`, `MySolution.Utils`, `MySolution.Helpers` projects; like Go's `util/`, they accrete grab-bag code. Pick a feature-oriented name.

## Worked example

Three projects each pin different versions of the same NuGet packages and share copy-pasted `PropertyGroup` blocks.

1. Create `Directory.Build.props` at the root with shared properties (`TargetFramework`, `Nullable`, `ImplicitUsings`, `LangVersion`, `TreatWarningsAsErrors`).
2. Create `Directory.Packages.props` with `<ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>` and one `<PackageVersion Include="..." Version="..."/>` per package.
3. Strip `Version` attributes from each `.csproj`'s `PackageReference`.
4. Put projects under `src/` and tests under `tests/<Project>.Tests/`, then `dotnet sln add` each.
5. Verify: `dotnet build -warnaserror && dotnet test`.

Upgrading a package is now a one-line change in one file.

## Anti-patterns

- **Flat layout (no `src/`/`tests/`)** with 20+ projects mixed at the root. Works for 2–3 projects; chaos at scale.
- **Per-project NuGet versions** (no `Directory.Packages.props`). Two projects pulling different `Microsoft.Extensions.Logging.Abstractions` versions will *appear* to compile, then fail at runtime with method-not-found exceptions.
- **No `Directory.Build.props`.** Every `.csproj` repeats the target framework, language version, nullable settings. Drift across projects is inevitable.
- **`packages.config`** in any project new enough to use SDK-style `.csproj`. Migrate first.
- **Test projects in `src/`.** Confuses CI scripts that try to "build everything in `src/`" or "publish everything in `src/`."
- **Project references via absolute paths.** `<ProjectReference Include="C:\Repos\MySolution\src\MySolution.Core\MySolution.Core.csproj" />` is non-portable; relative paths are mandatory.
- **Missing `<Nullable>enable</Nullable>`** in greenfield code. Modern C# (8+) has nullable reference types; turning them off forfeits a major source of compile-time bug catches.
- **Not running `dotnet format`** in CI. The `.editorconfig` becomes decorative; style drifts.
- **Committing `bin/`, `obj/`, `*.user`, `.vs/`.** Standard .NET `.gitignore` covers these; missing them leads to massive merge conflicts.
- **Solution folders that don't mirror disk layout.** Visual Studio lets you create solution folders independently of disk; doing so creates two truths and confuses everyone.

## Scaling & failure modes

- **Project count**: one project per deployable or per architectural layer is normal; a project per class is not. Merge projects that always change together.
- **Build time** improves with a shared `Directory.Build.props` and `<Deterministic>` plus `dotnet build --no-restore` in CI.
- **Analyzers** belong in `Directory.Build.props` so every project gets the same rules.
- **Multi-targeting** (net8.0;net10.0) doubles build and test time; use it only for libraries with real consumers on old runtimes.

## Variants

- **classic `src/` + `tests/`** (this guide) — most common modern layout; what `dotnet/runtime` and `dotnet/aspnetcore` use internally.
- **flat layout** — projects directly under the repo root, no `src/` directory. Used by some smaller libraries and most `dotnet new sln`-based tutorials. Fine for 2–4 projects, doesn't scale.
- **with-Central-Package-Management** (this guide includes) — `Directory.Packages.props` at root, `<PackageReference>` versions stripped from `.csproj`. Strongly recommended for any solution with >2 projects.
- **legacy `packages.config`** — old `.NET Framework` style with per-project `packages.config` listing NuGet versions. Avoid for new code; migrate when you can.
- **multi-targeted libraries** — `<TargetFrameworks>net8.0;netstandard2.0</TargetFrameworks>` in libraries that ship to both modern and older .NET. Common in NuGet libraries supporting downstream .NET Framework consumers.
- **monorepo-with-`Directory.Build.targets`** — adds `Directory.Build.targets` (imported *after* targets, not before) to inject custom build steps repo-wide. Used by `dotnet/runtime` for its complex code-generation pipeline.
- **`global.json`-pinned SDK** — `global.json` at the repo root pins the .NET SDK version. Mandatory for reproducible CI on shared agents.

## Adoption checklist

- [ ] `dotnet build -warnaserror && dotnet test` passes from a clean clone.
- [ ] Package versions are set only in `Directory.Packages.props`.
- [ ] Each shippable assembly is in `src/` and each test project mirrors it in `tests/`.
- [ ] `.editorconfig` and analyzers apply solution-wide.
- [ ] `bin/` and `obj/` are gitignored.

## Real-world projects using this

- **dotnet/runtime** — the .NET runtime itself. `src/` (split into `coreclr`, `mono`, `libraries`), `tests/`, `Directory.Build.props`, central package management. The reference for "very large .NET solution."
- **dotnet/aspnetcore** — ASP.NET Core. Same shape: `src/`, `Directory.Build.props`, `Directory.Packages.props`. Hundreds of projects under one solution.
- **NuGet/NuGet.Client** — NuGet client tooling. Same `src/` + `tests/` + central package management.
- **JetBrains/dotPeek-Plugin samples**, **JetBrains/resharper-unity** — JetBrains' .NET OSS uses the canonical layout.
- **OctopusDeploy/CLI**, **OctopusDeploy/sashimi** — Octopus Deploy's open-source CLI and adapters; consistent `src/`/`tests/` solution layout.
- **MicrosoftDocs/dotnet-style-guide** — official Microsoft style guide, exemplifies the `Directory.Build.props` + `.editorconfig` combo.
- **Polly-Contrib/Polly** (resilience library) — small but exemplary `src/`+`tests/` with central package management.

## Migration & references

- **From flat to `src/`+`tests/`**: `mkdir src tests`, `git mv MySolution.Core MySolution.Core.Api MySolution.Core.Cli src/`, `git mv *.Tests tests/`. Update relative paths in `.sln` and any `<ProjectReference>` between projects (`..\MySolution.Core\` → `..\..\src\MySolution.Core\` for tests). Visual Studio will offer to "fix" the solution if the relative paths are wrong; let it.
- **Adopting Central Package Management**: create `Directory.Packages.props` at the root with `<ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>` and `<PackageVersion Include="X" Version="1.2.3" />` entries. Then strip `Version="..."` from every `<PackageReference>` in every `.csproj`. The .NET SDK has a built-in migration command: `dotnet new packagesconfig` is the *legacy* opposite; CPM migration is largely manual but trivial with find-replace.
- **From `packages.config` to SDK-style**: use the `Try-Convert` tool (`dotnet tool install --global try-convert`) and run `try-convert` in the project directory. It rewrites the `.csproj` to SDK style and removes `packages.config`. Verify the result builds before committing.
- **Adding `Directory.Build.props`**: create at the repo root, move repeated properties (`<TargetFramework>`, `<Nullable>`, `<LangVersion>`) out of every `.csproj` into the props file. Test: `dotnet build` should still succeed; if a project needed an override, it can re-declare the property.
- **References**:
  - .NET docs — *Common project structure*: https://learn.microsoft.com/en-us/dotnet/core/project-sdk/overview
  - .NET docs — *Central Package Management*: https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management
  - .NET docs — *Customize your build with Directory.Build.props*: https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory
  - .NET docs — *Framework Design Guidelines* (PascalCase, naming, etc.): https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/
  - Sibling guide: `code/java-gradle-multi/` — analogous "library + tests + multiple sub-projects" layout in Java.
