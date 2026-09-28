## TL;DR

A **java-gradle-multi** project is a multi-module Gradle build: a root `settings.gradle.kts` lists the modules, a root `build.gradle.kts` carries shared configuration (Java toolchain, repositories, common plugins), and each subproject has its own `build.gradle.kts`. Source layout inside each module follows the Maven Standard Directory Layout (`src/main/java/`, `src/test/java/`) — Gradle inherits this convention from Maven on purpose. The big payoff over Maven multi-module: **typed Kotlin DSL** (compile errors instead of runtime XML errors), **incremental + parallel builds** (Gradle only rebuilds what changed and runs subprojects in parallel by default), and **version catalogs** (`gradle/libs.versions.toml`) — one place to declare all dependency coordinates so they don't drift across modules. The Gradle wrapper (`gradlew`, `gradlew.bat`, `gradle/wrapper/`) pins the Gradle version so anyone who clones gets the same build, regardless of system Gradle install. Use this layout whenever you have ≥2 build artifacts that release together; below 2 modules, a single `build.gradle.kts` at the root is enough.

## Principles & why

A multi-module Gradle build is shaped by six principles that diverge meaningfully from Maven.

1. **`settings.gradle.kts` is the contract for module membership.** `include(":core", ":api", ":app")` is the canonical list. Add a directory to disk without `include`-ing it and Gradle ignores it. This is the opposite of Maven's "directory presence implies inclusion if listed in `<modules>`" but is functionally similar.
2. **Root `build.gradle.kts` configures *all* subprojects at once.** A `subprojects { ... }` block (or, modernly, a *convention plugin* in `buildSrc/`) applies the same Java toolchain, repositories, and common deps to every module. Reduces boilerplate enormously vs. Maven's `<parent>` inheritance.
3. **Version catalogs (`gradle/libs.versions.toml`) centralise dependency coordinates.** `[versions]`, `[libraries]`, `[plugins]` sections name every dep once. Modules reference them as `libs.junit.jupiter` (typed accessor in Kotlin DSL). Bumping a dep version: edit one TOML line, every module gets it. This replaces the Maven `<properties>` + `<dependencyManagement>` pattern with something better.
4. **Inter-module deps are first-class.** `dependencies { implementation(project(":core")) }` in `app/build.gradle.kts` declares that `app` depends on `core`. Gradle figures out the build order, builds in parallel where possible, and re-uses cached outputs.
5. **The Gradle wrapper pins the Gradle version.** `gradle/wrapper/gradle-wrapper.properties` declares the distribution URL (`gradle-8.x-bin.zip`). `./gradlew build` downloads exactly that version. This is non-negotiable for reproducible builds across machines and CI.
6. **`implementation` vs `api` matters.** `implementation` deps are private to the module (consumers can't see them); `api` deps are re-exported. Getting this wrong leaks transitive deps and slows down compilation. The default rule of thumb: prefer `implementation`; use `api` only when a type from that dep appears in your public API.

The cost: Gradle is more powerful than Maven, which means more rope to hang yourself with. A `build.gradle.kts` that runs custom Groovy/Kotlin logic is harder to reason about than a static `pom.xml`. Use convention plugins to keep DSL surface small and predictable.

## When to use

- **Multi-module Java projects** with ≥2 artifacts that release on the same cadence.
- **Spring Boot apps split into modules** (e.g., `core/`, `web/`, `worker/` as siblings).
- **Android projects with feature modules.** Android's build system is Gradle-only; `app` + `feature:home` + `feature:checkout` is canonical (see Now in Android).
- **Kotlin Multiplatform projects.** KMP requires Gradle.
- **Libraries with optional integration modules.** A core lib + `myproject-spring`, `myproject-jackson`, `myproject-jdbc` adapters; the multi-module layout makes adapter modules natural.
- **Projects where you'd otherwise struggle with Maven plugin authoring.** Custom build logic in Kotlin/Groovy is much nicer than writing a Maven plugin in Java.

## When NOT to use

- **Single-module projects.** A single `build.gradle.kts` at the repo root with `src/main/java/` is fine and simpler. Adopt multi-module when you split.
- **Maven shop.** Use `code/java-maven/` if your team and CI are Maven-first.
- **Tiny scripts or one-class utilities.** Use `jbang` or single-file Java; no build system at all.
- **Pure Bazel/Buck/Pants ecosystems.** Different build system, different layout (`BUILD` files).
- **Cases where Maven's stricter conventions are a feature, not a bug.** Junior teams sometimes benefit from Maven's "less rope" philosophy.

## Tree diagram

```
my-project/
├── settings.gradle.kts
├── build.gradle.kts                ← root (plugins, repositories, shared deps)
├── gradle.properties
├── gradle/
│   ├── wrapper/
│   │   ├── gradle-wrapper.jar
│   │   └── gradle-wrapper.properties
│   └── libs.versions.toml          ← version catalog
├── gradlew
├── gradlew.bat
├── README.md
├── core/
│   ├── build.gradle.kts
│   └── src/main/java/...
├── api/
│   ├── build.gradle.kts
│   └── src/main/java/...
└── app/
    ├── build.gradle.kts
    └── src/main/java/...
```

## Naming rules

- **Repository directory**: `kebab-case` (`my-project/`).
- **Module directories**: `kebab-case` or single lowercase word (`core/`, `api/`, `app/`, `data-store/`). Keep them short; the `:`-prefixed module path you'll type a lot (`./gradlew :core:test`) gets unwieldy fast.
- **Module path in Gradle**: prefixed with `:` (`:core`, `:api`). Nested: `:feature:home`.
- **Java packages**: lowercase, dot-separated, mirror the directory. `com.example.core`, `com.example.api`. Modules typically own a package prefix (`com.example.<module>`).
- **`group` in root `build.gradle.kts`**: reverse-DNS, matches your package root. `group = "com.example"`.
- **Module artifact names**: by default, the artifact ID is the module directory name. Override with `archivesName.set("myproject-core")` to publish as `myproject-core-0.1.0.jar`.
- **Version catalog accessors**: `libs.junit.jupiter` corresponds to `junit-jupiter` in TOML (`-` and `.` map to the same accessor). Stick to one separator per project — `kebab-case` keys read most cleanly.
- **Convention plugins (when used)**: `buildSrc/src/main/kotlin/myproject.java-conventions.gradle.kts`. The dotted ID becomes a plugin you `apply` in module `build.gradle.kts`.

## Worked example

A Maven parent POM with five modules takes 9 minutes to build; dependency versions differ between modules.

1. Add `settings.gradle.kts` with `include("core", "api", "app")`.
2. Create `gradle/libs.versions.toml` with `[versions]`, `[libraries]`, and `[plugins]` blocks; reference entries as `libs.spring.boot.starter`.
3. Move shared build logic into a convention plugin in `build-logic/` (or `buildSrc/` for a small project) so each module's `build.gradle.kts` is about ten lines.
4. Declare inter-module dependencies with `implementation(project(":core"))`, and use `api` only for types that appear in a module's public signatures.
5. Enable the build cache and parallel execution in `gradle.properties`.
6. Confirm with `./gradlew build --scan` and compare timings.

Module builds are incremental, so touching `app` no longer rebuilds `core`.

## Anti-patterns

- **Skipping the wrapper** (`gradle/wrapper/`). Without it, "works on my machine" creeps in. Always commit `gradlew`, `gradlew.bat`, and `gradle/wrapper/*` (including the JAR — it's tiny and signed).
- **Mixing Groovy DSL and Kotlin DSL.** Pick one. Kotlin DSL gives compile-time errors and IDE completion; Groovy is more permissive. New projects: Kotlin DSL.
- **Not using a version catalog.** Declaring `"org.junit.jupiter:junit-jupiter:5.10.0"` as a string literal in three modules → drift. Move to `libs.versions.toml`.
- **Using `compile` configuration.** `compile` was deprecated years ago. Use `implementation` (private to module) or `api` (re-exported). `compile` is gone in Gradle 8.
- **Cross-module access via paths instead of `project(":core")`.** `dependencies { implementation(files("../core/build/libs/core.jar")) }` will silently break parallel builds. Use `project(":core")`.
- **Putting all logic in the root `build.gradle.kts`.** Once it grows past ~100 lines, extract to convention plugins under `buildSrc/`. Otherwise the file becomes a tar pit.
- **Per-module `gradle/wrapper/` directories.** Only the root has the wrapper. Subprojects share it.
- **Committing `.gradle/` or `build/`.** Build outputs and caches; gitignored.
- **Skipping `org.gradle.parallel=true` in `gradle.properties`.** Default in recent Gradle, but worth being explicit. Combined with multi-module, this is where the speed wins come from.

## Scaling & failure modes

- **`buildSrc` invalidation**: any edit reruns the whole build's configuration; move to composite `build-logic` when the project grows.
- **Configuration time** rises with module count; use configuration cache and avoid heavy logic in build scripts.
- **Circular module dependencies** are rejected by Gradle; treat that error as a design signal.
- **Version alignment** across many libraries is easiest with the catalog plus `platform()` BOMs.

## Variants

- **Groovy DSL** — `build.gradle` instead of `build.gradle.kts`. Older syntax, more permissive, less IDE help. Many existing projects use it; new projects should pick Kotlin DSL.
- **Kotlin DSL** (this guide) — `*.gradle.kts`, typed, IDE autocomplete works, refactor-safe. Current preferred style.
- **Composite builds** — `includeBuild("../sibling-project")` in `settings.gradle.kts` lets you depend on another standalone Gradle project as if it were a subproject. Useful for "I want to develop two repos side by side without publishing." Different from a multi-module *single repo*; sometimes used together.
- **`buildSrc/` for convention plugins** — `buildSrc/` is a magic directory; Gradle compiles it before evaluating any `build.gradle.kts`. Define a convention plugin there (`myproject.java-conventions.gradle.kts`) and apply it in each module to dedupe Java toolchain + Checkstyle + dependencies setup.
- **Gradle's *included builds* (`includeBuild`) for build logic** — newer than `buildSrc/`, more flexible (the build-logic project is just another Gradle project, no magic). Consider for large projects.
- **With Spotless / Checkstyle / Detekt** — formatting + linting plugins applied in the root or via convention plugins.

## Adoption checklist

- [ ] `./gradlew build` succeeds from a clean clone using the wrapper.
- [ ] All dependency versions come from `libs.versions.toml`.
- [ ] Repeated module configuration lives in a convention plugin.
- [ ] `api` vs `implementation` choices are deliberate.
- [ ] Build cache and configuration cache are enabled and verified.

## Real-world projects using this

- **Spring Boot itself** (`spring-projects/spring-boot`) — large multi-module Gradle build with convention plugins; reference for serious production use.
- **OkHttp** (`square/okhttp`) — multi-module Gradle, Kotlin DSL.
- **Now in Android** (`android/nowinandroid`) — feature-modular Android app, Kotlin DSL, version catalogs, convention plugins. Reference for modern Android.
- **Gradle's own samples** (`gradle/gradle-build-action`, `gradle/gradle/subprojects/docs/src/snippets/`) — canonical examples maintained by the Gradle team.
- **Kotlin Multiplatform projects** like `Kotlin/kotlinx.coroutines` — multi-module, Kotlin DSL, multi-target.
- **Android Open Source samples** (`android/architecture-samples`) — Compose + multi-module patterns.
- **Detekt** (`detekt/detekt`) — large Kotlin tool, multi-module Gradle, convention plugins.

## Migration & references

- **From Maven multi-module to Gradle multi-module**: `gradle init --type pom` reads the parent `pom.xml` and emits a starting `settings.gradle.kts` + `build.gradle.kts`. The result usually needs cleanup (Gradle and Maven represent things differently — `<dependencyManagement>` becomes a version catalog or `dependencies { constraints { ... } }`), but the source tree under each module doesn't move; both tools share `src/main/java/` conventions.
- **From single-module Gradle to multi-module**: create `settings.gradle.kts` if you don't have one, add `include(":new-module")`, create `new-module/build.gradle.kts`, move sources under `new-module/src/main/java/`. Move shared config from the existing `build.gradle.kts` into a `subprojects { }` block or convention plugin.
- **From Groovy DSL to Kotlin DSL**: rename `build.gradle` → `build.gradle.kts`. Replace string-typed config with typed equivalents (`apply plugin: 'java'` → `plugins { java }`). Most projects do this incrementally, one module at a time.
- **Adopting version catalogs**: create `gradle/libs.versions.toml` with `[versions]`, `[libraries]`, `[plugins]`. Replace string deps with `libs.foo` accessors. Modules pick this up automatically; no module-level wiring needed.
- **References**:
  - Gradle docs — *Structuring and Building a Software Project* (multi-project builds): https://docs.gradle.org/current/userguide/multi_project_builds.html
  - Gradle docs — *Sharing dependency versions between projects* (version catalogs): https://docs.gradle.org/current/userguide/platforms.html
  - *Now in Android* repo (https://github.com/android/nowinandroid) — best public example of modern Gradle conventions for an app project.
  - Sibling guides: `code/java-maven/`, `code/turborepo-monorepo/`, `code/nx-monorepo/`.
