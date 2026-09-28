## TL;DR

A modern multi-module Android project splits the codebase into three categories: **`app/`** (the application module that produces the APK/AAB), **`feature/<name>/`** (per-feature library modules — one screen group per module), and **`core/<area>/`** (shared infrastructure: `core:data`, `core:domain`, `core:designsystem`, `core:network`). The build is driven by **Gradle Kotlin DSL** (`*.gradle.kts`) with a **version catalog** (`gradle/libs.versions.toml`) for centralised dependency versions and **`build-logic/`** convention plugins that capture repeated build configuration as reusable Gradle plugins (so every Android library module just `apply` a single convention plugin instead of repeating 50 lines of boilerplate). The reference implementation is Google's **Now in Android** (https://github.com/android/nowinandroid), which Google maintains explicitly as the canonical demonstration of these patterns. Use this layout for any production Android app with more than a handful of screens, or when separate teams own different features. For demos and tutorials, the default Android Studio template (a single `app/` module) is fine — don't pre-emptively split a one-screen app into seven modules.

## Principles & why

The multi-module Android layout exists to address two specific problems: **incremental build time** and **architectural enforcement at the module boundary**.

1. **`app/` is the only Android *application* module.** It applies the `com.android.application` Gradle plugin and produces an installable artifact (APK or AAB). Every other module is an Android *library* (`com.android.library`) or pure Kotlin/JVM library — they compile to AARs / JARs, not standalone APKs.
2. **`feature/<name>/`** modules each implement one user-facing feature (Home, Settings, Profile, Search). They depend on `core:*` modules for shared infrastructure. Crucially, **features do not depend on each other** — cross-feature navigation goes through `app/` (or a `core:navigation` module). This eliminates a major source of dependency cycles in older monolithic-`app/` codebases.
3. **`core/<area>/`** modules host the shared infrastructure. Common splits: `core:data` (repositories), `core:domain` (use cases), `core:network` (HTTP clients), `core:designsystem` (Compose theme + reusable composables), `core:database` (Room), `core:datastore` (Preferences). Each is small, focused, and can be unit-tested without booting the whole app.
4. **Gradle Kotlin DSL** (`*.gradle.kts`) replaces Groovy `*.gradle`. Stronger typing, IDE autocomplete, refactoring support. Marginally slower to build than Groovy on first run; faster everywhere else.
5. **Version catalog** (`gradle/libs.versions.toml`) is the single source of dependency versions. Modules reference deps as `libs.androidx.compose.material3` instead of `androidx.compose.material3:material3:1.2.0`. Bumping a version touches one file.
6. **`build-logic/`** convention plugins encapsulate repeated build-script logic. Without them, every `feature/*/build.gradle.kts` repeats `android { compileSdk = 34, defaultConfig = {...} }` and 30 more lines. With them, you write `plugins { alias(libs.plugins.myapp.android.feature) }` and the convention plugin handles the rest. Now in Android pioneered this pattern publicly; it's now standard.
7. **Module boundaries enforce architecture.** A `feature:home` module *cannot* accidentally `import` something from `feature:settings` because Gradle doesn't expose it. The compiler enforces what's exposed (visibility modifiers + Gradle dependency declarations); the architect doesn't have to police it manually.

The trade-off: every new module adds a `build.gradle.kts` and at least one `AndroidManifest.xml`. For a small app the ceremony is overhead; for an app with 50 features and 20 engineers the modularity pays back many times over in build time, code ownership, and architectural clarity.

## When to use

- **Production Android apps with more than ~5 screens.** The build time win alone justifies the split; once you have 30+ screens, monolithic `app/` becomes painful to navigate.
- **Apps with separate teams owning different features.** Each team owns its `feature/<name>/` module; merge conflicts are rare; ownership in CODEOWNERS is straightforward.
- **Apps that already use Jetpack Compose.** Compose-first apps benefit hugely from `core:designsystem` (theme, typography, reusable composables) shared across features.
- **Apps that want fast incremental builds.** Gradle's parallel module compilation kicks in once you have multiple modules; the difference between "10s incremental build" and "60s incremental build" matters for daily productivity.
- **When you intend to ship feature flags / dynamic feature modules.** The `:feature:<name>` structure maps cleanly onto Play Feature Delivery.
- **When unit tests should run without Android instrumentation.** `core:domain` as a pure Kotlin library means use-case tests run on the JVM in milliseconds.

## When NOT to use

- **Single-screen demos and tutorials.** The default Android Studio template (one `app/` module) is right.
- **Apps targeting non-Android Kotlin** (multiplatform, server, CLI). Use `code/java-gradle-multi/` style for shared Kotlin/JVM, or Kotlin Multiplatform's own conventions for KMP projects.
- **Tiny one-off apps that will never grow.** Modularising prematurely adds friction without payoff.
- **Teams unfamiliar with Gradle.** Convention plugins, version catalogs, and Kotlin DSL all have learning curves; if your team is shipping with vanilla Groovy `app/build.gradle`, rolling out the modern stack is its own project.
- **Hybrid apps where most logic is in React Native / Flutter.** The Android-side wrapper is usually small and doesn't benefit from heavy modularisation.

## Tree diagram

```
MyApp/
├── settings.gradle.kts
├── build.gradle.kts
├── gradle/
│   ├── libs.versions.toml
│   └── wrapper/...
├── build-logic/                    ← convention plugins for build logic
│   └── convention/
│       └── src/main/kotlin/
├── app/
│   ├── build.gradle.kts
│   └── src/main/...
├── feature/
│   ├── home/
│   │   ├── build.gradle.kts
│   │   └── src/main/...
│   └── settings/
└── core/
    ├── data/
    ├── domain/
    ├── designsystem/
    └── network/
```

## Naming rules

- **Project (root) directory**: PascalCase by Android Studio default (`MyApp/`). The `rootProject.name` in `settings.gradle.kts` matches.
- **Module directories**: lowercase, single segment per directory. `app/`, `feature/home/`, `core/data/`. The Gradle path is `:feature:home`, `:core:data`.
- **Module names** in `settings.gradle.kts`: `:app`, `:feature:home`, `:feature:settings`, `:core:data`, `:core:domain`. Colons separate directory levels; dashes inside a single segment are tolerated but most teams prefer single words.
- **Application ID** in `app/build.gradle.kts`: reverse-DNS, lowercase. `com.example.myapp`. Different from `rootProject.name`.
- **Package names** in Kotlin sources: same reverse-DNS root + module identifier. `com.example.myapp.feature.home`, `com.example.myapp.core.data`. Mirrors the module path (Now in Android convention).
- **Class names**: PascalCase (`HomeScreen`, `UserRepository`).
- **Function and property names**: camelCase (`fun fetchUsers()`, `val userId`).
- **Composable function names**: PascalCase, by Compose convention (`@Composable fun HomeScreen()`).
- **Resource IDs**: `snake_case` (`activity_main`, `ic_home`); enforced by AAPT2.
- **Version catalog keys** in `libs.versions.toml`: dotted, lowercase. `androidx.compose.material3`, `kotlinx.coroutines.android`. Referenced from build scripts as `libs.androidx.compose.material3`.
- **Convention plugins**: descriptive PascalCase (`AndroidLibraryConventionPlugin`, `AndroidApplicationConventionPlugin`); registered in `build-logic` with kebab-case ids (`myapp.android.library`, `myapp.android.application`).

## Worked example

A single `app` module takes 4 minutes to build and any change recompiles everything.

1. Add a version catalog `gradle/libs.versions.toml` and move all dependency versions into it.
2. Create `build-logic/convention/` with plugins such as `android.library`, `android.feature`, and `android.compose`.
3. Extract shared infrastructure into `core/{data,domain,designsystem,network}`.
4. Extract each screen group to `feature/<name>/`; a feature module depends on `core` modules, never on another feature.
5. Keep `app/` for navigation wiring and the application class.
6. Check the graph with `./gradlew projects` and build times with `--scan`.

Changing one feature recompiles that module only, and features can be built and tested alone.

## Anti-patterns

- **Monolithic `app/` module** with 50+ screens. Slow incremental builds, merge conflict magnet, no architectural enforcement.
- **Cross-feature dependencies.** `feature:home` depending on `feature:settings` defeats the modularity. Route through `app/` or a `core:navigation` module.
- **Repeating build-script boilerplate** across 20 modules. Use `build-logic/` convention plugins.
- **Hard-coded versions in `build.gradle.kts`** instead of the version catalog. Bumps become find/replace; you'll miss one.
- **Putting application code in `core/*` modules.** `core/` is for shared infrastructure; UI screens belong in `feature/`.
- **Using Groovy and Kotlin DSL mixed.** Pick one. Mixed projects have one of each plugin syntax to remember.
- **Skipping `applyDsl()` plugin registration in `build-logic/`.** Convention plugins must be registered (`gradlePlugin { plugins { ... } }`) to be applied via id.
- **Committing `local.properties`.** It contains the SDK path and sometimes API keys; gitignore it.
- **Ignoring R8 / ProGuard configuration per module.** Each library module that contains code needing keep-rules should ship a `consumer-rules.pro`.
- **Using `dagger.hilt.android.plugin` without the corresponding KSP setup.** Modern Hilt uses KSP, not kapt; old templates that mix kapt + KSP cause hard-to-debug build failures.
- **Storing API keys in `gradle.properties`.** Use `local.properties` (gitignored) or a secrets-injection plugin.
- **A single huge `:designsystem` module** that depends on every Compose dependency. Split if it grows beyond ~30 composables.

## Scaling & failure modes

- **Module granularity**: too many tiny modules increases configuration time; too few loses incremental builds. Aim for feature-sized modules.
- **Feature-to-feature navigation** needs an abstraction (a navigation interface in `core`, or type-safe routes in a shared module) to avoid cross-feature dependencies.
- **Convention plugins** are code; test them and keep them small.
- **Baseline profiles and shrinking** belong in `app` and a benchmark module, not in every library.

## Variants

- **Now-in-Android style** (this guide) — `:app` + `:feature:*` + `:core:*` + `:build-logic`. Canonical 2025 layout.
- **older `app/`-only** — single-module project, everything under `app/src/main/`. Default Android Studio template; right for very small apps.
- **package-by-feature in a single module** — features as Kotlin packages inside `app/`, no Gradle module split. Used by some teams resistant to multi-module overhead; loses the build-time and enforcement wins.
- **Compose Multiplatform shared module** — adds a `:shared` Kotlin Multiplatform module exposing Compose UI for both Android and iOS (via Compose for iOS). Layout is otherwise the same; the `:shared` module's `build.gradle.kts` is more complex.
- **Dynamic Feature Modules** — `feature:` directory but each module declares `com.android.dynamic-feature` instead of `com.android.library`, enabling Play Feature Delivery (install on demand). Used by larger apps to keep base APK small.
- **Modularisation by layer** — `:data`, `:domain`, `:presentation` instead of `:feature:*` + `:core:*`. Older convention, still seen; weaker for parallel team ownership.

## Adoption checklist

- [ ] Features depend on `core` modules only, and `./gradlew projects` shows no feature-to-feature edge.
- [ ] All versions come from the catalog and repeated configuration lives in convention plugins.
- [ ] Each feature module has its own tests and runs them alone.
- [ ] Build scan shows cache hits on unchanged modules.
- [ ] `app` contains wiring only.

## Real-world projects using this

- **android/nowinandroid** — Google's reference architecture demo. Maintained as the canonical "modern Android" example. Mirror this exactly when starting greenfield.
- **chrisbanes/tivi** — popular OSS TV-show tracker by a Google Android engineer; long-running real-world example of the pattern.
- **skydoves/Pokedex** — Compose + Hilt + multi-module reference, well-known in the Android community.
- **DroidKaigi conference apps** — `DroidKaigi/conference-app-2023` (and the yearly successors) are community-maintained, multi-module, fully Compose. Excellent reference for "what the Android Kotlin community converges on."
- **JetBrains/compose-multiplatform** samples — JetBrains' Compose Multiplatform samples use multi-module layouts that include shared KMP modules alongside the standard `:app`/`:feature`/`:core` split.
- **android/architecture-samples** — Google's older architecture samples (MVVM, MVP, etc.); some branches use multi-module layouts and are worth comparing.
- **square/anvil** & related Square Android projects — heavy multi-module use to enforce DI boundaries and improve build times.

## Migration & references

- **From single-module to multi-module**: start by extracting `core:designsystem` (Compose theme + reusable widgets). Move the relevant files, create `core/designsystem/build.gradle.kts`, add `include(":core:designsystem")` to `settings.gradle.kts`, depend on it from `app/`. Verify the build. Repeat for the next layer (`core:data`, then a feature). Don't try to extract everything in one PR.
- **Adopting `build-logic/` convention plugins**: create `build-logic/convention/` as a standalone Gradle build (with its own `settings.gradle.kts`). Move repeated config out of module build scripts into a plugin class extending `Plugin<Project>`. Register the plugin id in `gradlePlugin {}`. Apply via `plugins { alias(libs.plugins.myapp.android.library) }`.
- **Adopting the version catalog**: at the repo root, `gradle/libs.versions.toml` with `[versions]`, `[libraries]`, `[plugins]` blocks. Replace `implementation("group:artifact:1.2.3")` with `implementation(libs.group.artifact)`. Gradle 7.4+ ships catalog support natively.
- **Migrating from Groovy to Kotlin DSL**: rename `build.gradle` → `build.gradle.kts`. Rewrite using Kotlin syntax (`apply plugin: 'foo'` → `plugins { id("foo") }`). Migrate one module at a time; Groovy and Kotlin DSL coexist.
- **From kapt to KSP** (Hilt, Room, Moshi): swap the Gradle plugin (`kotlin-kapt` → `com.google.devtools.ksp`); change `kapt(...)` to `ksp(...)` in dependencies. KSP is faster and supports Kotlin 2.0 better.
- **References**:
  - **Now in Android** repo: https://github.com/android/nowinandroid — read the modularization document for the project's design rationale.
  - Google — *Guide to app architecture*: https://developer.android.com/topic/architecture
  - Google — *Modularization* guide: https://developer.android.com/topic/modularization
  - Gradle — *Sharing build logic via convention plugins*: https://docs.gradle.org/current/userguide/sharing_build_logic_between_subprojects.html
  - Gradle — *Version catalogs*: https://docs.gradle.org/current/userguide/platforms.html
  - Sibling guides: `code/java-gradle-multi/` (the JVM-only counterpart), `code/swift-package/` (the equivalent shape on Apple platforms).
