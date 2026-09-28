## TL;DR

A **swift-package** is a Swift project managed by Swift Package Manager (SwiftPM): a `Package.swift` manifest at the root, source files under `Sources/<Target>/`, tests under `Tests/<Target>Tests/`. The same shape is used by tiny libraries, by Apple's own systems libraries (`apple/swift-collections`, `apple/swift-argument-parser`), and by full server applications built on Vapor. Folder, target, and module names are **PascalCase** per Swift convention — that's the documented exception to the kebab-case-default in this guide, because the manifest, the import statements, and the framework names that ship to the SwiftPM registry all use PascalCase. Importantly, the *package directory* name (your repo's root) and the *package name* in `Package.swift` should match: cloning `MyPackage` and opening it in Xcode just works. SwiftPM enforces a fairly rigid layout — it walks `Sources/` and `Tests/` automatically; you only need a `targets:` array if you're departing from defaults. This guide describes a library + executable + tests layout that scales from "a single-source-file utility" up through "Vapor server with several internal targets," all using the same conventions.

## Principles & why

The Swift Package Manager layout is shaped by SwiftPM's own conventions and by Swift's module system.

1. **`Package.swift` is the single source of truth.** No `Cargo.toml` + `Cargo.lock`-equivalent split: the manifest declares targets, products, dependencies, platforms, and Swift tools version. SwiftPM walks the directory tree from there.
2. **`Sources/<Target>/` is auto-discovered.** Each subdirectory of `Sources/` is one Swift target (one module) by default; Swift compiles every `.swift` file beneath it. You can override the path in `Package.swift` if needed (`path: "Custom/Sources/Foo"`), but the default rules are strong enough that almost no real package overrides them.
3. **`Tests/<Target>Tests/` mirrors `Sources/`.** Conventionally, the test target name is `<TargetName>Tests` and lives in `Tests/<TargetName>Tests/`. SwiftPM auto-detects it and generates an XCTest runner.
4. **The package name and directory name should match.** A package whose `Package.swift` declares `name: "MyPackage"` should live in a directory called `MyPackage/`. Xcode's SwiftPM integration assumes the symmetry; mismatches lead to confusing "couldn't find package" errors.
5. **PascalCase is enforced by Swift's import statement.** `import MyPackage` matches the target name `MyPackage`; the directory name `Sources/MyPackage/` matches the import. Departing from PascalCase makes imports look strange (`import my_package` is grammatical but un-Swiftic).
6. **`// swift-tools-version: X.Y` is the first line.** SwiftPM reads this magic comment to decide which manifest API to expose. Newer features (e.g., `swiftLanguageVersions`, `swiftSettings: [.enableExperimentalFeature("StrictConcurrency")]`) are gated by this version.
7. **Everything not under `Sources/`, `Tests/`, or named in `Package.swift` is invisible** to SwiftPM. A `Resources/` folder must be declared via `.process()` or `.copy()` in the target's `resources:` array; otherwise it's not packaged.

The "why" is that SwiftPM aggressively prefers convention over configuration. Following the layout means your `Package.swift` stays small (often <30 lines for libraries with a few targets); diverging means writing increasingly long path overrides that newcomers can't navigate.

## When to use

- **Swift libraries published to the Swift Package Index** (https://swiftpackageindex.com). The Index expects this layout.
- **Server-side Swift on Vapor.** Vapor templates produce exactly this shape — `Sources/App/`, `Sources/Run/main.swift` (or modern `@main`), `Tests/AppTests/`.
- **Cross-platform Swift libraries** targeting Linux + macOS + iOS. SwiftPM is the only build system that works across all three; the layout is non-negotiable.
- **Any project where you'd want Xcode integration.** SwiftPM packages open in Xcode without a `.xcodeproj`; SwiftPM generates the project on demand. Standard layout = it just works.
- **Command-line tools written in Swift.** `Sources/<Tool>/main.swift` (or `@main` struct in newer Swift) plus a `swift-argument-parser` dependency is the canonical Swift CLI shape.
- **When Swift 5.9+ macros and concurrency features are required.** `swift-tools-version` and `swiftSettings:` controls live in `Package.swift`; this layout is the only sane home for them.

## When NOT to use

- **Pure iOS apps with no shared library.** A single `.xcodeproj` in the standard Xcode layout (Storyboard/SwiftUI app target, asset catalogs) is simpler and uses Xcode's built-in dependency manager (which under the hood now calls SwiftPM, but the surface is different).
- **CocoaPods-only consumers.** Some legacy iOS projects can't or won't switch to SwiftPM; they use a Podspec instead. Less common in 2025; still relevant for some shops.
- **Non-Swift projects "just because the team likes Swift's tooling."** SwiftPM has no Objective-C-only mode; mixed-language packages are awkward.
- **Pre-Swift 5.5 projects.** Older Swift versions had a different `Package.swift` API; the migration path is well-trodden but not zero-cost.
- **Single-file experiments.** `swift run` against a flat `main.swift` works without a package; only formalise into SwiftPM when you have multiple files or want tests.

## Tree diagram

```
MyPackage/
├── Package.swift
├── README.md
├── LICENSE
├── .gitignore
├── Sources/
│   ├── MyPackage/
│   │   ├── MyPackage.swift
│   │   └── Core/
│   │       └── Core.swift
│   └── MyPackageCLI/
│       └── main.swift
├── Tests/
│   └── MyPackageTests/
│       └── MyPackageTests.swift
└── .swiftpm/                       ← gitignored, IDE state
```

## Naming rules

- **Package name**: PascalCase, matches the root directory and the `name:` field in `Package.swift`. `MyPackage`, `Vapor`, `Alamofire`.
- **Target names**: PascalCase. The library target is usually the same as the package name (`MyPackage`); supplementary targets get suffixes (`MyPackageCLI`, `MyPackageMacros`, `MyPackageDB`).
- **Test target**: `<TargetName>Tests`. Folder: `Tests/<TargetName>Tests/`. Test files inside: `<TestSuite>Tests.swift` containing one or more XCTestCase subclasses. (Swift Testing — the new `@Test` attribute — uses similar naming.)
- **Module imports**: `import MyPackage` must match the target name. Don't try to rename a target without updating every importer.
- **Type, struct, class, enum names**: PascalCase. `URLLoader`, `HTTPClient`, `User`. Acronyms uppercased fully (`URL`, not `Url`).
- **Function, variable, parameter names**: camelCase. `loadProfile(forUserID:)`, `accessToken`.
- **Constants**: camelCase by convention (`let maxRetries = 3`). Some shops use `UPPER_SNAKE`; Apple's own libraries use camelCase.
- **Protocols**: PascalCase, often a noun or adjective. `Equatable`, `Codable`, `RandomNumberGenerator`. Avoid `IFoo`-style prefixes (Java/C# leakage; not Swift-idiomatic).
- **File names**: PascalCase, matching the primary type defined inside (`URLLoader.swift` defines `struct URLLoader`). Avoid generic names like `Helpers.swift`.
- **Avoid**: Hyphens, spaces, and lower-case-first letters in target/folder names. SwiftPM tolerates them; the rest of the ecosystem doesn't.

## Worked example

An app's networking code is copied between two projects.

1. Create `swift package init --type library` and rename the target to `MyPackage`.
2. Move code under `Sources/MyPackage/`, marking the API `public` and everything else internal.
3. Add tests in `Tests/MyPackageTests/` using Swift Testing or XCTest.
4. Declare platforms and products in `Package.swift` (`platforms: [.iOS(.v17), .macOS(.v14)]`, `products: [.library(name: "MyPackage", targets: ["MyPackage"])]`).
5. Consume it from apps with a local path during development (`.package(path: "../MyPackage")`), then by URL and version.
6. Run `swift build && swift test` in CI on macOS and Linux if the code is portable.

Both apps share one tested module with a defined public surface.

## Anti-patterns

- **Custom `path:` overrides for every target** when the conventional `Sources/<Target>/` layout would have worked. Bloats the manifest and confuses Xcode.
- **Mismatched package name vs. directory name.** A `Package.swift` that says `name: "Foo"` in a directory called `bar/` confuses Xcode's "open package" UI.
- **Putting tests in `Sources/`.** SwiftPM compiles them as part of the library target; they ship to consumers. Move to `Tests/`.
- **`Package.resolved` policy ambiguity.** Apps usually commit `Package.resolved` (so installs are reproducible). Libraries usually *don't* commit it (so consumers' resolutions take priority). Pick a side and document it.
- **`.swiftpm/` committed.** That directory holds Xcode-generated artefacts (build state, scheme definitions); it's local IDE state and belongs in `.gitignore`.
- **Skipping `swift-tools-version`.** SwiftPM defaults to Swift 4 syntax for missing version comments — extremely confusing for a 2025-era project.
- **Mixing executable and library logic in one target.** Executables need a `main.swift` or `@main` entry; libraries don't. If you want both, split into two targets (a `MyPackage` library and a `MyPackageCLI` executable that depends on it).
- **`Resources/` folder without manifest declaration.** Files dropped into a target's directory without `.process()` or `.copy()` in `resources:` are silently ignored at build time.
- **Cross-target file references via relative paths in code.** Targets are modules; refer to other targets by `import <Target>`, not by file paths.
- **Public types where internal would do.** Swift's default access level is `internal` (visible within the module). `public` is the package's external API surface — every `public` declaration is a stability commitment.

## Scaling & failure modes

- **Access control** discipline (internal by default) prevents accidental API commitments.
- **Resource bundling** (`resources: [.process("Assets")]`) has quirks; test resource loading from a consumer.
- **Multiple targets** should mirror dependency boundaries; avoid cyclic target dependencies.
- **Semantic versioning** via git tags is the release mechanism; tag deliberately.

## Variants

- **library-only** (this guide can collapse to this) — only `Sources/MyPackage/`, no executable. Most published libraries (`swift-collections`, `swift-argument-parser`).
- **executable-only** — `Sources/MyTool/main.swift`, no library. Pure CLI tool.
- **library + executable** (this guide as written) — `Sources/MyPackage/` library + `Sources/MyPackageCLI/` thin CLI front-end. Common when shipping both an SDK and a reference CLI.
- **multi-target** — multiple peer targets under `Sources/` (`Sources/Foo/`, `Sources/Bar/`, `Sources/Baz/`) with internal dependencies declared in `Package.swift`. Used by Vapor's own `vapor` repo (`Vapor`, `Routing`, `Logging`, etc.).
- **Swift Concurrency strict-mode** — same layout, plus `swiftSettings: [.enableExperimentalFeature("StrictConcurrency")]` in each target. Required for Swift 6 ahead of full strict-mode default.
- **macro-package** — adds a `MyPackageMacros` target with `swift-syntax` dependency for compile-time macros. Layout is identical; manifest declares it as `.macro()`.
- **Vapor server** — `Sources/App/` (the library with controllers and configure.swift), `Sources/Run/main.swift` (entry point). Tests in `Tests/AppTests/`. Identical otherwise.

## Adoption checklist

- [ ] `swift build && swift test` pass from a clean clone.
- [ ] Public API is explicit; the rest is internal.
- [ ] Platforms and minimum versions are declared in `Package.swift`.
- [ ] Releases are git tags following semver.
- [ ] `.swiftpm/` and `.build/` are gitignored.

## Real-world projects using this

- **apple/swift-collections** — the reference for "a small, focused Swift library." Multi-target (Deque, OrderedSet, etc.), all under `Sources/<Module>/`.
- **apple/swift-argument-parser** — Apple's official CLI argument parser; library + a few example executables, canonical layout.
- **apple/swift-package-manager** — SwiftPM is itself a Swift Package; the bootstrapping is famously complex, but the layout is conventional.
- **vapor/vapor** — the most-used Swift web framework; multi-target Swift Package layout, runs on Linux + macOS.
- **pointfreeco/swift-composable-architecture** — popular state-management library; library + extensive test target.
- **groue/GRDB.swift** — SQLite database access; multi-target library, used in many production iOS apps.
- **hummingbird-project/hummingbird** — lightweight server framework alternative to Vapor; same SwiftPM layout.

## Migration & references

- **From Xcode-only project to SwiftPM**: at the project root, run `swift package init --type library` (or `--type executable`). Move sources from `MyApp/Classes/` to `Sources/MyApp/`, tests to `Tests/MyAppTests/`. Keep the `.xcodeproj` if you still need it for app-target builds; SwiftPM and Xcode can coexist (Xcode just needs the package added as a Swift Package dependency or opened directly).
- **From CocoaPods to SwiftPM**: in `Podfile`, mark each pod as "transitioning"; for each, find the SwiftPM equivalent (most pods now ship a `Package.swift`). In your project, `File > Add Packages...` to add the SPM URL. Once all deps are SPM, delete `Podfile` and `Pods/`.
- **Adding a CLI executable to a library package**: add a new target in `Package.swift`:
  ```swift
  .executableTarget(name: "MyPackageCLI", dependencies: ["MyPackage"]),
  ```
  Create `Sources/MyPackageCLI/main.swift` (or `@main struct CLI { ... }`).
- **Adopting Swift Testing** (the new `@Test` framework, vs. legacy XCTest): bump `swift-tools-version` to 5.10 or 6.0 and write tests using `import Testing; @Test func foo() { ... }`. SwiftPM auto-detects both runners.
- **References**:
  - Apple — *Swift Package Manager* documentation: https://www.swift.org/documentation/package-manager/
  - Apple — *Bundling resources with a Swift package*: https://developer.apple.com/documentation/xcode/bundling-resources-with-a-swift-package
  - Swift Package Index: https://swiftpackageindex.com
  - Swift Testing (new framework): https://github.com/apple/swift-testing
  - Sibling guide: `code/rust-library/` — analogous pattern in Rust (`Cargo.toml` + `src/`).
