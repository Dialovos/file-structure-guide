# MyPackage — Swift Package template

A `cp -r`-able starter for a SwiftPM package: a `Package.swift` manifest,
one library target (`MyPackage`), one executable target (`MyPackageCLI`),
one test target (`MyPackageTests`). Builds and runs on Linux, macOS,
iOS, tvOS, and watchOS.

## Layout at a glance

```
.
├── Package.swift                       # manifest (swift-tools-version 5.9)
├── Sources/
│   ├── MyPackage/                      # library target
│   │   ├── MyPackage.swift             # public struct MyPackage
│   │   └── Core/
│   │       └── Core.swift              # internal helpers
│   └── MyPackageCLI/                   # executable target
│       └── main.swift
├── Tests/
│   └── MyPackageTests/
│       └── MyPackageTests.swift        # XCTest cases
└── .github/workflows/ci.yml            # swift test on Linux + macOS
```

## What to rename

`MyPackage` is the placeholder. Rename it everywhere:

- The directory at the repo root (the package is conventionally in a
  folder named after itself).
- `Package.swift` — the `name:` argument and every target name.
- `Sources/MyPackage/`, `Sources/MyPackageCLI/`, `Tests/MyPackageTests/`
  directory names.
- The `import MyPackage` lines in `Sources/MyPackageCLI/main.swift`
  and `Tests/MyPackageTests/MyPackageTests.swift`.
- The `struct MyPackage` definition in `Sources/MyPackage/MyPackage.swift`.

A repo-wide find/replace covers most of the text changes:

```bash
find . -type f \( -name '*.swift' -o -name 'README.md' \) \
  -exec sed -i 's/MyPackage/YourPackage/g' {} +

mv Sources/MyPackage Sources/YourPackage
mv Sources/MyPackageCLI Sources/YourPackageCLI
mv Tests/MyPackageTests Tests/YourPackageTests
```

(Use `gsed` on macOS if `sed -i` doesn't accept the in-place flag.)

## What to fill

- `Package.swift` — replace `MyPackage` and bump `platforms:` to your
  minimum supported OS versions.
- `Sources/MyPackage/MyPackage.swift` — your real public API.
- `Sources/MyPackage/Core/Core.swift` — internal helpers; expand as
  needed (or split into more files / submodules).
- `Sources/MyPackageCLI/main.swift` — when adding real flags, prefer
  `swift-argument-parser`:

  ```swift
  // In Package.swift dependencies:
  .package(url: "https://github.com/apple/swift-argument-parser", from: "1.3.0"),
  // In the executable target:
  .executableTarget(
      name: "MyPackageCLI",
      dependencies: [
          "MyPackage",
          .product(name: "ArgumentParser", package: "swift-argument-parser"),
      ]
  ),
  ```

- `Tests/MyPackageTests/MyPackageTests.swift` — add cases. Consider
  Swift Testing (`import Testing; @Test`) when targeting Swift 5.10+.
- `LICENSE` — replace `{{YEAR}}` and `{{NAME}}`.

## What to delete

- This template `README.md`.
- The `MyPackageCLI` target if you only ship a library: remove the
  `.executable()` product and `.executableTarget()` from
  `Package.swift`, then `rm -r Sources/MyPackageCLI`.
- The `Core/` subdirectory if you don't need internal helpers.

## First run

```bash
swift build
swift test
swift run mypackage-cli alice
# → hello, alice
```

## Adding a target

In `Package.swift`:

```swift
.target(name: "MyPackageDB", dependencies: ["MyPackage"]),
```

Then create `Sources/MyPackageDB/` and start adding `.swift` files —
SwiftPM auto-discovers them.

## Adding a dependency

```swift
// In Package.swift dependencies:
.package(url: "https://github.com/groue/GRDB.swift", from: "6.0.0"),
// In the consuming target:
.target(
    name: "MyPackage",
    dependencies: [.product(name: "GRDB", package: "GRDB.swift")]
),
```

`swift package resolve` updates `Package.resolved`. See the comment in
`.gitignore` for whether to commit it.

## Pair this with

- `../GUIDE.md` — full reasoning, including the library/executable
  split and the `Resources/` declaration rules.
- `../../rust-library/` — analogous library layout in Rust.
- `../../node-library/` — analogous shape in npm/TypeScript.
