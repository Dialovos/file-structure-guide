# Multi-module Gradle (Kotlin DSL) — template

A `cp -r`-able starter for a multi-module Gradle project using the
**Kotlin DSL** with a **version catalog**. Three modules are wired in:

- `core/` — shared library (`com.example.core`).
- `api/` — adapter that depends on `:core` and re-exports part of it.
- `app/` — runnable entry point (`application` plugin) that depends on
  `:api` and `:core`.

## Layout at a glance

```
.
├── settings.gradle.kts             # include(":core", ":api", ":app")
├── build.gradle.kts                # subprojects { ... } shared config
├── gradle.properties               # parallel, caching, JVM args
├── gradle/
│   ├── libs.versions.toml          # version catalog
│   └── wrapper/
└── {core,api,app}/build.gradle.kts # per-module
```

## What to rename

`my-project` and `com.example` appear in several places. Pick a real
name (kebab-case) and group (reverse-DNS):

- `settings.gradle.kts` — `rootProject.name`.
- Root `build.gradle.kts` — `group = "com.example"`.
- `core/src/main/java/com/example/core/` — rename the package
  directory.
- `api/src/main/java/com/example/api/` — same.
- `app/src/main/java/com/example/app/` — same.
- `app/build.gradle.kts` — `application.mainClass`.
- This `README.md`.

## What to fill

- `gradle/libs.versions.toml` — add libraries you actually use.
  Examples (`spring-boot`, `jackson`, `kotlin-stdlib`) are commented
  in the file.
- Each module's `build.gradle.kts` — declare deps via `libs.foo`.
- `LICENSE` — replace `{{YEAR}}` and `{{NAME}}`.

## What to delete

- This template `README.md`.
- The `CoreUtils` / `ApiClient` / `App` stubs once you have real code.
- Any module you don't need (e.g. delete `app/` and remove `:app` from
  `settings.gradle.kts` if you're shipping a library).

## Populating the wrapper

This template ships **placeholder** `gradlew` and `gradlew.bat` and a
`gradle-wrapper.properties` that pins Gradle 8.10.2. Before first run,
populate the real wrapper:

```bash
# Requires a system Gradle; only needed once.
gradle wrapper --gradle-version 8.10.2
```

That generates:

- `gradle/wrapper/gradle-wrapper.jar` (the actual wrapper bootstrap)
- Real `gradlew` and `gradlew.bat` scripts

After that, never invoke a system Gradle again — always `./gradlew`.

## First run

```bash
./gradlew build              # compile + test all modules
./gradlew :app:run --args="alice"   # → "hello, alice"
./gradlew :core:test         # test only core
./gradlew tasks              # list everything
```

## Adding a new module

```bash
mkdir -p feature-billing/src/main/java/com/example/billing
# Write feature-billing/build.gradle.kts (apply java-library, deps).
# Add ":feature-billing" to include(...) in settings.gradle.kts.
./gradlew :feature-billing:build
```

## Adding a dependency

Edit `gradle/libs.versions.toml`:

```toml
[versions]
caffeine = "3.1.8"

[libraries]
caffeine = { module = "com.github.ben-manes.caffeine:caffeine", version.ref = "caffeine" }
```

Then in any module's `build.gradle.kts`:

```kotlin
dependencies {
    implementation(libs.caffeine)
}
```

## Pair this with

- `../GUIDE.md` — full reasoning for multi-module Gradle.
- `../../java-maven/` — single-module Maven alternative.
- `../../turborepo-monorepo/` — analogous JS/TS multi-package monorepo.
