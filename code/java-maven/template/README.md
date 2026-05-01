# Maven single-module — template

A `cp -r`-able starter for a single-module Maven project following the
**Maven Standard Directory Layout** (MSDL). One artifact, one `pom.xml`,
JUnit 5 wired in, GitHub Actions CI included.

## Layout at a glance

```
.
├── pom.xml                                   # the contract
└── src/
    ├── main/
    │   ├── java/com/example/myproject/       # production code
    │   │   ├── App.java
    │   │   └── core/                         # subpackages live here
    │   └── resources/                        # bundled into the JAR
    │       └── application.properties
    └── test/
        ├── java/com/example/myproject/       # tests, mirrors main/
        │   └── AppTest.java
        └── resources/                        # test classpath only
```

## What to rename

`com.example.myproject` and `myproject` appear in several places. Pick a
real `groupId` (reverse-DNS, e.g. `org.acme`) and `artifactId`
(kebab-case, e.g. `acme-billing`):

- `pom.xml` — `<groupId>`, `<artifactId>`, `<name>`, `<description>`.
- `src/main/java/com/example/myproject/` — rename the directory tree to
  match your reverse-DNS package (`src/main/java/org/acme/billing/`).
- `src/test/java/com/example/myproject/` — same as above.
- `src/main/java/.../App.java` and `AppTest.java` — update the
  `package` declaration on line 1.
- `application.properties` — adjust `app.name`.
- This `README.md`.

A repo-wide `find . -type d -name myproject` followed by `git mv` is the
fastest way.

## What to fill

- `pom.xml` — your `<groupId>` / `<artifactId>` / `<version>`. Decide
  whether to inherit from `spring-boot-starter-parent` (Spring Boot)
  or stay self-contained (this template).
- `LICENSE` — replace `{{YEAR}}` and `{{NAME}}`.
- `README.md` — replace this file with one that describes your project.

## What to delete

- This template `README.md`.
- `App.java` / `AppTest.java` once you have real code and tests.
- The empty `core/` and `src/test/resources/` placeholders if you don't
  need them yet.
- `.github/workflows/ci.yml` if you don't use GitHub Actions.

## First run

```bash
# Compile and run unit tests
mvn test

# Full verify (compile + test + package)
mvn verify

# Run the built JAR
mvn package
java -cp target/myproject-0.1.0-SNAPSHOT.jar com.example.myproject.App
# → "hello, world"
```

If you want a single executable JAR with deps bundled, add the
`maven-shade-plugin` or use `spring-boot-maven-plugin`.

## Adding dependencies

Look up coordinates at https://search.maven.org/, then:

```xml
<dependency>
  <groupId>org.slf4j</groupId>
  <artifactId>slf4j-api</artifactId>
  <version>2.0.13</version>
</dependency>
```

For test-only deps, add `<scope>test</scope>`. For deps you need at
compile time but not runtime (annotation processors, e.g. Lombok), use
`<scope>provided</scope>`.

## Adding Maven Wrapper

```bash
mvn wrapper:wrapper
```

This commits `mvnw`, `mvnw.cmd`, and `.mvn/wrapper/`. Now developers
without a system Maven can run `./mvnw verify`.

## Pair this with

- `../GUIDE.md` — full reasoning for MSDL, anti-patterns, and variants.
- `../../java-gradle-multi/` — multi-module Gradle alternative.
- `../../c-cpp-cmake/` — analogous "build-system-as-contract" guide for
  C/C++.
