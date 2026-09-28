## TL;DR

A **java-maven** project follows the **Maven Standard Directory Layout** (MSDL): `src/main/java/` for production sources, `src/main/resources/` for production resources (properties, YAML, templates), `src/test/java/` and `src/test/resources/` for tests, and a `pom.xml` at the repository root that names the artifact and lists dependencies. Build output goes to `target/` (gitignored). The killer feature is **convention over configuration**: any developer who knows Maven can `git clone && mvn test` and it works, no setup, no IDE-specific config. The `pom.xml` is the contract — it pins the Java version, declares deps with `<groupId>:<artifactId>:<version>`, and Maven downloads them to `~/.m2/repository/`. This guide covers the **single-module** case (one `pom.xml`, one artifact); multi-module (parent `pom.xml` + children) is a variant. Use this layout for any new Maven project; deviate only with a strong reason, because every Maven plugin in the ecosystem assumes MSDL paths and reconfiguring them creates friction with no upside.

## Principles & why

The MSDL is shaped by five principles, each of which trades some flexibility for a huge ecosystem benefit.

1. **Convention over configuration.** Every Maven plugin (`maven-compiler-plugin`, `maven-surefire-plugin`, `maven-jar-plugin`, `maven-shade-plugin`, hundreds of others) defaults to reading from `src/main/java/` and writing to `target/`. If you keep MSDL paths, your `pom.xml` stays minimal — often just `<dependencies>` and a couple of plugin versions. Move things around and every plugin needs `<sourceDirectory>` overrides; you've made a mess no future maintainer will thank you for.
2. **Separation of `main` and `test`.** Test code lives in `src/test/java/`, parallel to `src/main/java/`. The `maven-surefire-plugin` only runs tests from `src/test/`, never from `src/main/`. This means test-only deps (JUnit, Mockito, AssertJ) are scoped `<scope>test</scope>` and don't leak into the runtime classpath, which keeps your produced JAR slim.
3. **Resources travel with code.** `src/main/resources/` is copied into the JAR's root at build time. So `application.properties` at `src/main/resources/application.properties` becomes `application.properties` at JAR root, loadable via `getResourceAsStream("/application.properties")`. Same parallel for `src/test/resources/` (test classpath only).
4. **Package directories mirror Java packages.** `src/main/java/com/example/myproject/App.java` declares `package com.example.myproject;`. The directory hierarchy *is* the package hierarchy. Maven enforces this; the compiler will refuse otherwise.
5. **`pom.xml` is the single source of truth.** Java version, deps, plugins, profiles — all in `pom.xml`. No `Makefile`, no `build.sh`, no IDE-specific files committed. Anyone with Maven and a JDK can build.

The cost of this rigidity: if you have a genuinely unusual layout need (generated sources, multiple source roots, polyglot Kotlin+Java), you fight Maven harder than you'd fight Gradle. For 95% of projects, the rigidity is the feature.

## When to use

- **Any new Maven-based Java/Kotlin/Scala project.** MSDL is the default; deviate only with cause.
- **Libraries published to Maven Central.** Maven Central's release process assumes MSDL — Sonatype's `nexus-staging-maven-plugin` reads from `target/`.
- **Spring Boot apps generated from start.spring.io.** The Initializr emits exactly this layout.
- **Apache Software Foundation projects.** ASF strongly prefers Maven; the layout is universal across Apache Commons, Apache HttpClient, Hadoop, Camel, Kafka.
- **Migrating from Ant.** Ant projects often have ad-hoc layouts (`src/`, `lib/`, `build/`); converting to MSDL pays back immediately because every Maven plugin "just works" afterwards.
- **Polyglot JVM projects with one primary language.** Maven supports `src/main/kotlin/`, `src/main/scala/` (with the right plugins) using parallel naming.

## When NOT to use

- **Gradle projects.** Gradle's default layout is *also* MSDL-shaped (it shares the convention), but Gradle projects have `build.gradle.kts` instead of `pom.xml` and the file you ship is different. Use `code/java-gradle-multi/` for Gradle.
- **Multi-module Maven projects.** Still uses MSDL *within each module*, but the repo root has a parent `pom.xml` with `<packaging>pom</packaging>` and a `<modules>` list. That's the **multi-module variant** of this guide; the structure of each module follows the single-module rules below.
- **Kotlin-first or Android projects.** Use Gradle. Kotlin's compiler integration with Gradle is much smoother; Maven Kotlin support exists but lags.
- **Tiny scripts or one-class utilities.** A `pom.xml` for a 50-line file is overhead. Use `jbang` or a single `.java` file (Java 21+ supports `java MyFile.java` directly).
- **Bazel/Buck/Pants projects.** Different build system, different layout (`BUILD` files).

## Tree diagram

```
my-project/
├── pom.xml
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/myproject/
│   │   │       ├── App.java
│   │   │       └── core/
│   │   ├── resources/
│   │   │   └── application.properties
│   │   └── webapp/                   ← if web app
│   └── test/
│       ├── java/
│       │   └── com/example/myproject/
│       │       └── AppTest.java
│       └── resources/
└── target/                            ← gitignored, build output
```

## Naming rules

- **Repository directory**: `kebab-case` (`my-project/`, `acme-billing/`). Project directories don't need to match the artifact ID, but it's nicer when they do.
- **`groupId`**: reverse-DNS, lowercase, dots-as-separators. `com.example`, `org.apache.commons`, `io.micrometer`. Match the package root in `src/main/java/`.
- **`artifactId`**: `kebab-case`, no dots. `myproject`, `commons-lang3`, `spring-boot-starter-web`. The JAR's filename is `<artifactId>-<version>.jar`.
- **Java packages**: lowercase, dot-separated, mirror the directory tree. `com/example/myproject/core/UserService.java` → `package com.example.myproject.core;`.
- **Class names**: `UpperCamelCase`. One public class per file; the file is named after that class (`UserService.java` contains `public class UserService`).
- **Test classes**: end in `Test` (Surefire's default include pattern is `**/*Test.java`). `UserServiceTest.java` for unit tests; `*IT.java` for integration tests run by `failsafe-plugin`.
- **Resource files**: `application.properties`, `application.yml`, `logback.xml`, `META-INF/services/...`. Filenames usually fixed by the consuming framework.
- **`webapp/`** (servlet-based web apps only): `src/main/webapp/WEB-INF/web.xml`, JSPs, static assets. Most modern apps use Spring Boot embedded servers and skip `webapp/`.

## Worked example

A project compiles in the IDE but `mvn package` fails on CI because of missing resources and an unpinned JDK.

1. Confirm the layout: sources in `src/main/java`, resources in `src/main/resources`, tests in `src/test/java`. Move anything that isn't there.
2. Pin the toolchain in `pom.xml` with `<maven.compiler.release>21</maven.compiler.release>` and set `project.build.sourceEncoding` to `UTF-8`.
3. Add the Maven Wrapper (`mvn wrapper:wrapper`) so everyone uses the same Maven version.
4. Manage dependency versions in `<dependencyManagement>` or import a BOM.
5. Separate unit tests (`*Test`, run by Surefire) from integration tests (`*IT`, run by Failsafe in `mvn verify`).
6. Verify with `./mvnw -B verify` on a clean clone.

The build result no longer depends on the developer's machine.

## Anti-patterns

- **Source files outside `src/main/java/`.** `src/java/`, `java/`, `code/` — all of these break every Maven plugin's defaults. Move to MSDL.
- **Resources mixed with code.** `application.properties` next to `App.java` in `src/main/java/` won't be packaged into the JAR (Maven only copies non-`.java` files from `src/main/resources/`, not from source directories by default). Symptom: works in IDE, fails in built JAR.
- **Hardcoding versions instead of using `<properties>`.** Repeat `<version>5.10.0</version>` for three JUnit deps and you'll bump two of them next time. Use `<properties><junit.version>5.10.0</junit.version></properties>` and reference `${junit.version}`.
- **Committing `target/`.** It's build output; it gets stale, it bloats the repo, it conflicts in PRs. Always gitignored.
- **Committing IDE files.** `.idea/`, `*.iml`, `.classpath`, `.project`, `.settings/` are per-developer. Use `.gitignore`. Each developer's IDE re-imports from `pom.xml`.
- **Skipping `.mvn/wrapper/`.** Maven Wrapper (`./mvnw`) pins the Maven version. Without it, "works on my machine" creeps in when developers have different Maven versions.
- **Putting integration tests in `src/test/java/` and running them with Surefire.** Slow ITs blow up the unit-test cycle. Use `*IT.java` with `failsafe-plugin` and a separate phase.
- **Manual `<dependency>` declarations for Spring/JUnit BOMs instead of `<dependencyManagement>` import.** BOMs (Bill of Materials) keep transitively-related deps version-aligned. Use `spring-boot-dependencies` BOM, JUnit `junit-bom`, AWS SDK BOM.

## Scaling & failure modes

- **Multi-module growth**: a parent POM with modules is natural past one deployable; keep the parent thin (versions and plugins) and use `<packaging>pom</packaging>`.
- **Dependency conflicts** are diagnosed with `mvn dependency:tree`; enforce convergence with the enforcer plugin.
- **Slow builds**: use `-T 1C` for parallel modules and `-pl <module> -am` to build only what you touch.
- **Java package names** mirror the reverse-DNS path; deep `com/example/...` nesting is imposed and doesn't count against your depth budget.

## Variants

- **single-module** (this guide) — one `pom.xml`, one artifact. Default for libraries and small apps.
- **multi-module Maven** — parent `pom.xml` with `<packaging>pom</packaging>` and `<modules><module>core</module><module>app</module></modules>`. Each child module has its own `pom.xml` and follows MSDL internally. Use when you have ≥3 artifacts that release together (e.g., `myproject-core`, `myproject-cli`, `myproject-server`).
- **with-flatten-pom** — uses `flatten-maven-plugin` to publish a "flat" `pom.xml` to Maven Central even when the source `pom.xml` uses CI-friendly versions (`${revision}`) or property-based versions. Standard practice for projects with parent-pom inheritance that publish to Central.
- **with-dependabot** — `.github/dependabot.yml` with `package-ecosystem: maven`. Recommended for any production project to keep deps current.
- **with-spring-boot** — Spring Boot's `spring-boot-maven-plugin` repackages the JAR into an executable fat JAR. Inherits from `spring-boot-starter-parent` instead of declaring a `<parent>` of your own.
- **archetype-driven** — `mvn archetype:generate -DarchetypeArtifactId=maven-archetype-quickstart` produces this exact layout. Useful for teaching; production projects usually start from a known-good `pom.xml` rather than the bare archetype.

## Adoption checklist

- [ ] `./mvnw -B verify` passes from a clean clone.
- [ ] JDK release, encoding, and plugin versions are pinned.
- [ ] Unit and integration tests run in separate phases.
- [ ] `target/` is gitignored.
- [ ] Dependency versions are managed in one place.

## Real-world projects using this

- **Spring Boot starters** generated by `start.spring.io` — exact MSDL, single-module by default.
- **Apache Commons** projects (`commons-lang3`, `commons-io`, `commons-csv`, etc., on `apache/commons-*` GitHub repos) — MSDL across the board.
- **Hibernate ORM** (`hibernate/hibernate-orm`) — large multi-module Maven, but each module follows MSDL.
- **JHipster generated projects** (`jhipster/generator-jhipster`) — MSDL with Spring Boot conventions on top.
- **Apache Maven itself** (`apache/maven`) — multi-module Maven; the project that defines the conventions follows them.
- **Apache HttpClient 5** (`apache/httpcomponents-client`) — multi-module Maven, MSDL inside each module.
- **Mockito** (`mockito/mockito`) — Gradle, but the source layout is MSDL-shaped because the convention is shared between Maven and Gradle.

## Migration & references

- **From Ant to Maven**: move sources from `src/` to `src/main/java/`, tests from `test/` to `src/test/java/`, resources from wherever they were to `src/main/resources/`. Generate a starter `pom.xml` with `mvn archetype:generate`. The hard part is dependencies: Ant `lib/*.jar` becomes `<dependencies>` with explicit `groupId:artifactId:version`. Use https://search.maven.org/ to look up coordinates.
- **From Gradle to Maven**: tools like `gradle init` (in reverse, `mvn -N io.takari:maven:wrapper`) help; usually it's mostly `pom.xml` authoring because the source layout is identical. Plugin equivalents: Gradle's `application` plugin → Maven's `exec-maven-plugin` + `maven-shade-plugin`.
- **From Maven flat to multi-module**: create a parent `pom.xml` at the repo root with `<packaging>pom</packaging>` and `<modules>`. Move the existing project into a subdirectory (now a child module). Add a *second* child for the new code. Update `<groupId>`/`<artifactId>` consistently.
- **Adding Maven Wrapper**: `mvn wrapper:wrapper`. Commits `mvnw`, `mvnw.cmd`, `.mvn/wrapper/maven-wrapper.properties`. Now `./mvnw clean install` works without a system Maven install.
- **References**:
  - Maven docs — *Introduction to the Standard Directory Layout*: https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html
  - Maven docs — *POM Reference*: https://maven.apache.org/pom.html
  - *Maven: The Complete Reference* (Sonatype, free online).
  - Spring Initializr (https://start.spring.io) for a known-good template.
  - Sibling guides: `code/java-gradle-multi/`, `code/c-cpp-cmake/`.
