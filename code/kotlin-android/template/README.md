# MyApp — multi-module Android template

A `cp -r`-able starter for a modern, multi-module Android project
following the Now-in-Android conventions: `:app` + `:feature:*` +
`:core:*`, Gradle Kotlin DSL, version catalog, and `build-logic/`
convention plugins.

## Layout at a glance

```
.
├── settings.gradle.kts                 # includes every module
├── build.gradle.kts                    # plugin classpath, all `apply false`
├── gradle/
│   ├── libs.versions.toml              # version catalog
│   └── wrapper/                        # gradle-wrapper.properties
├── build-logic/                        # convention plugins (sub-build)
│   └── convention/
│       ├── build.gradle.kts            # registers the convention plugins
│       └── src/main/kotlin/
│           ├── AndroidApplicationConventionPlugin.kt
│           ├── AndroidLibraryConventionPlugin.kt
│           └── AndroidFeatureConventionPlugin.kt
├── app/                                # the only :application module
│   ├── build.gradle.kts
│   └── src/main/
│       ├── AndroidManifest.xml
│       └── kotlin/com/example/myapp/MainActivity.kt
├── feature/
│   ├── home/                           # one screen group per module
│   │   ├── build.gradle.kts
│   │   └── src/main/...
│   └── settings/
└── core/
    ├── data/                           # repositories
    │   └── src/main/kotlin/.../UserRepository.kt
    ├── domain/                         # use cases
    ├── designsystem/                   # Compose theme + widgets
    └── network/                        # HTTP / Retrofit
```

## What to rename

`MyApp` (project name) and `com.example.myapp` (package / namespace)
are placeholders. Rename:

- `rootProject.name` in `settings.gradle.kts`.
- The `namespace = "..."` in every `android { }` block.
- The `applicationId` (in the `app` convention plugin or `app/build.gradle.kts`).
- The `package com.example.myapp....` declaration in every Kotlin file.
- The directory layout `kotlin/com/example/myapp/...` to mirror the
  new package.

```bash
# Replace text occurrences:
find . -type f \( -name '*.kt' -o -name '*.kts' -o -name '*.xml' \
                 -o -name '*.toml' -o -name 'README.md' \) \
  -exec sed -i 's/com\.example\.myapp/com.yourorg.yourapp/g' {} +
find . -type f \( -name '*.kts' -o -name '*.toml' -o -name 'README.md' \) \
  -exec sed -i 's/MyApp/YourApp/g' {} +

# Move the package directories under each module:
for m in app feature/home feature/settings core/data; do
  d="$m/src/main/kotlin"
  [ -d "$d/com/example/myapp" ] && \
    mkdir -p "$d/com/yourorg/yourapp" && \
    mv "$d/com/example/myapp"/* "$d/com/yourorg/yourapp"/ && \
    rmdir "$d/com/example/myapp" "$d/com/example" 2>/dev/null
done
```

## Bootstrapping the Gradle wrapper

The template ships placeholder `gradlew` / `gradlew.bat`. Real
projects need the binary `gradle-wrapper.jar` plus the platform
launcher scripts. After cloning, run **once**:

```bash
gradle wrapper --gradle-version 8.9
```

(That requires a system Gradle install. The CI workflow uses
`gradle/actions/setup-gradle@v3` and bootstraps the wrapper itself.)

## What to fill

- `gradle/libs.versions.toml` — pin versions you actually need; remove
  unused entries.
- `core/data/src/main/kotlin/.../UserRepository.kt` — replace with
  your real repositories.
- `core/domain/`, `core/designsystem/`, `core/network/` — start with
  empty `.gitkeep`s; add Kotlin files as the layers grow.
- `feature/home/HomeScreen.kt` — your real Home screen + ViewModel.
- `feature/settings/` — an analogous screen.
- `app/MainActivity.kt` — wire a `NavHost` once you have multiple
  features to route to.
- `LICENSE` — replace `{{YEAR}}` and `{{NAME}}`. Default Apache 2.0;
  swap for MIT / proprietary as you prefer.

## What to delete

- This template `README.md`.
- Any `core:*` modules you don't need (e.g., `:core:network` for
  offline-only apps). Remove the `include(":core:network")` line and
  the `core/network/` directory.

## First run (after wrapper bootstrap)

```bash
./gradlew assembleDebug
./gradlew testDebugUnitTest
./gradlew :app:installDebug   # device or emulator must be attached
```

## Adding a new feature module

```bash
mkdir -p feature/profile/src/main/kotlin/com/example/myapp/feature/profile
cat > feature/profile/build.gradle.kts <<'EOF'
plugins {
    alias(libs.plugins.myapp.android.feature)
    alias(libs.plugins.compose.compiler)
}
android { namespace = "com.example.myapp.feature.profile" }
dependencies {
    implementation(project(":core:domain"))
    implementation(project(":core:designsystem"))
}
EOF
echo '<?xml version="1.0" encoding="utf-8"?><manifest xmlns:android="http://schemas.android.com/apk/res/android" />' \
  > feature/profile/src/main/AndroidManifest.xml
```

Then add `include(":feature:profile")` to `settings.gradle.kts` and
`implementation(project(":feature:profile"))` to `app/build.gradle.kts`.

## Adding a dependency

1. In `gradle/libs.versions.toml`, add a `[versions]` entry and a
   `[libraries]` entry pointing at it.
2. In the consuming module's `build.gradle.kts`, write
   `implementation(libs.your.lib)`.

## Pair this with

- `../GUIDE.md` — full reasoning, including the cross-feature
  dependency rule and the `build-logic/` rationale.
- `../../java-gradle-multi/` — the JVM-only sibling layout (no
  Android plugin).
- `../../swift-package/` — the equivalent shape on Apple platforms.
- **Now in Android** (https://github.com/android/nowinandroid) — read
  the modularization document for the project's design rationale.
