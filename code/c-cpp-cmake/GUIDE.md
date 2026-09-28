## TL;DR

A **c-cpp-cmake** project uses **modern CMake** (3.20+) with a top-level `CMakeLists.txt`, source files under `src/`, public headers under `include/<project>/`, tests under `tests/`, and an out-of-source `build/` directory (gitignored). The `include/<project>/` namespacing is critical: it means downstream consumers `#include <myproject/core.h>` (never `#include "core.h"`), which prevents header collisions when your library is dropped into a project that already has a `core.h` of its own. Each subdirectory has its own `CMakeLists.txt` brought in by `add_subdirectory()`, keeping the top-level file small. Modern CMake is **target-centric**: you create targets (`add_library`, `add_executable`), set their properties (`target_include_directories`, `target_compile_features`, `target_link_libraries`), and let CMake's transitive `PUBLIC`/`INTERFACE`/`PRIVATE` keywords propagate them. Avoid global directives (`include_directories(...)`, `link_libraries(...)`) — they pollute every target and are the legacy CMake equivalent of global mutable state. Use this layout for any new C/C++ project, library or application; the structure scales from a 200-line library to wasmtime-sized projects without changes.

## Principles & why

Modern CMake is shaped by six principles that distinguish it from legacy (pre-3.0) CMake.

1. **Targets, not directories.** `add_library(myproject src/core.cpp)` creates a target named `myproject`. All compilation knowledge — include paths, compile features, link deps, definitions — attaches to that target via `target_*` commands. Consumers depend on the target by name, not by directory or include path. This is the single biggest mental shift from legacy CMake.
2. **`PUBLIC` / `INTERFACE` / `PRIVATE` propagation.** `target_include_directories(myproject PUBLIC include)` means: this target itself uses `include/`, *and* anything that links against `myproject` also gets `include/` on its include path. `PRIVATE` is "for me only", `INTERFACE` is "for consumers only" (header-only libraries). Get this right and consumers `target_link_libraries(consumer PRIVATE myproject::myproject)` and have everything they need.
3. **Out-of-source builds, always.** `cmake -B build -S .` creates `build/` next to the source tree. All artifacts go there; the source stays clean. `cmake --build build` runs the actual build. `git status` stays meaningful because `build/` is gitignored.
4. **Public headers under `include/<project>/`.** Your public API headers live at `include/myproject/foo.h`. Consumers write `#include <myproject/foo.h>`. This namespaces your headers under your project name, which is essential when your library is consumed by a project that has files with the same names (every C++ project has a `util.h` somewhere).
5. **Use `find_package`-friendly install rules.** Generate a `myprojectConfig.cmake` so downstream consumers can `find_package(myproject 1.0 REQUIRED)`. `CMakePackageConfigHelpers` automates this. The result: your library is consumable both via `add_subdirectory()` (vendored) and `find_package()` (installed). Pre-modern projects forced one or the other; modern projects support both.
6. **`enable_testing()` + `add_test()` + CTest.** Tests are first-class. `ctest --test-dir build --output-on-failure` runs every test the project knows about. Use `FetchContent` (or vcpkg/Conan) to grab a test framework like Catch2 or GoogleTest.

The cost: CMake DSL is its own language and an awkward one. Macros, generator expressions (`$<...>`), policy versioning, generator differences (Make vs. Ninja vs. MSBuild) — there's a learning curve. The payoff is that every C/C++ project on every platform can be built by anyone with CMake installed.

## When to use

- **New C/C++ libraries and applications.** CMake is the de facto cross-platform build system; pick it unless you have a strong reason not to.
- **Cross-platform projects.** CMake supports Linux/macOS (Make, Ninja), Windows (MSBuild, Ninja), and embedded toolchains. The same `CMakeLists.txt` works everywhere.
- **Libraries published for consumption by other CMake projects.** `find_package` integration is the killer feature.
- **Mixed C/C++ projects.** CMake supports `LANGUAGES C CXX` in one project, with per-target standards.
- **Projects with optional features (CUDA, OpenMP, MPI, etc.).** CMake has battle-tested `find_package` modules for almost every numerical/parallel library.
- **Anything destined for vcpkg, Conan, or system package managers.** The packagers consume CMake projects natively.

## When NOT to use

- **Pure Bazel/Buck/Pants ecosystems.** Different build system, different files (`BUILD`, `BUCK`).
- **Header-only libraries with trivial layouts.** A header-only lib *can* use CMake (and benefit from `find_package`), but a single-header file (`stb`-style) doesn't need any build system. Just ship the header.
- **Pure Make / autotools projects.** They work; CMake is usually nicer, but if your project is already heavily invested in autotools (most of GNU), the migration cost is real.
- **Modern C++ projects choosing Meson.** Meson is a real alternative; it's a build system, not just a generator. Some projects (systemd, GNOME) prefer it. Pick one.
- **Single-file scripts.** A 200-line C utility doesn't need CMake. Just `cc -o foo foo.c`.

## Tree diagram

```
myproject/
├── CMakeLists.txt              ← top-level
├── README.md
├── LICENSE
├── .gitignore
├── include/
│   └── myproject/
│       ├── core.h
│       └── api.h
├── src/
│   ├── CMakeLists.txt
│   ├── core.cpp
│   └── api.cpp
├── tests/
│   ├── CMakeLists.txt
│   └── test_core.cpp
├── examples/
│   └── basic.cpp
├── cmake/                      ← CMake helper modules
│   └── FindFoo.cmake
└── build/                      ← gitignored, out-of-source build
```

## Naming rules

- **Project directory and CMake project name**: lowercase, often `kebab-case` or single word (`myproject`, `nlohmann_json`, `fmt`). The `project(myproject ...)` name is what consumers see.
- **Target names**: lowercase. Library target is usually the project name (`myproject`); executables get descriptive names (`myproject-cli`, `bench-core`).
- **Namespaced alias targets**: `add_library(myproject::myproject ALIAS myproject)`. Consumers can write `target_link_libraries(consumer PRIVATE myproject::myproject)` whether they got `myproject` via `find_package` or `add_subdirectory`. This `<project>::<target>` convention is universal.
- **Public headers**: `include/<project>/foo.h`. Always namespaced under the project directory.
- **Source files**: `src/foo.cpp`, `src/foo/bar.cpp` (subdirs as needed). C++ uses `.cpp` (most common) or `.cc` (Google-style); pick one.
- **Test files**: `tests/test_*.cpp` or `tests/*_test.cpp`. Consistent prefix/suffix lets you wildcard.
- **CMake module files**: `cmake/FindFoo.cmake` for find-modules, `cmake/myprojectConfig.cmake.in` for the project config template.
- **Variables**: `UPPER_SNAKE_CASE` for CMake variables, but namespaced (`MYPROJECT_BUILD_TESTS`, not `BUILD_TESTS`). Project-scoped variables avoid global pollution.

## Worked example

A library builds with a hand-written Makefile and consumers copy headers into their tree.

1. Create the skeleton: `include/mylib/`, `src/`, `tests/`, `cmake/`.
2. Move public headers to `include/mylib/` and include them as `#include <mylib/core.h>` everywhere, including inside `src/`.
3. Write target-based CMake:
```
add_library(mylib src/core.cpp)
target_include_directories(mylib PUBLIC include)
target_compile_features(mylib PUBLIC cxx_std_20)
```
4. Add tests with `enable_testing()` and `add_test`, and build out of source: `cmake -S . -B build && cmake --build build && ctest --test-dir build`.
5. Add `install(TARGETS ...)` and a package config so consumers can `find_package(mylib)`.

The Makefile goes away, `build/` is gitignored, and a consumer needs one `target_link_libraries(app PRIVATE mylib)` line.

## Anti-patterns

- **`include_directories(...)` at the top level.** Adds an include path to every target globally; one wrong header shadows another. Use `target_include_directories(<tgt> ...)` instead.
- **`link_libraries(...)`** (without `target_`). Same problem. Use `target_link_libraries(<tgt> ...)`.
- **Headers next to sources** (no `include/<project>/`). Works for the in-tree consumer; breaks the moment you install or vendor. Always use `include/<project>/`.
- **In-source builds.** Running `cmake .` in the source dir litters CMake artifacts among your files. Always `cmake -B build`.
- **Hardcoded compiler flags.** `set(CMAKE_CXX_FLAGS "-O3 -Wall")` overrides the user's choice and breaks debug builds. Use `target_compile_options(<tgt> PRIVATE ...)` and respect `CMAKE_BUILD_TYPE`.
- **Using `file(GLOB ...)` for source lists.** New files added to `src/` don't trigger a re-glob; CMake misses them. List sources explicitly. (CMake 3.27+ has `CONFIGURE_DEPENDS` to mitigate this, but it's a build-time hit.)
- **Skipping `target_compile_features`**. Without it, a target compiles with whatever C++ standard the toolchain defaults to. `target_compile_features(myproject PUBLIC cxx_std_17)` is the modern way.
- **Mixing `add_subdirectory` and `find_package` for the same dep.** Pick one strategy per dep.
- **Missing `cmake_minimum_required(VERSION 3.20)` at the top.** Without it, CMake uses very old policy defaults; nothing modern works.

## Scaling & failure modes

- **Global commands** (`include_directories`, `add_definitions`) leak into every target and cause the most confusing failures. Keep everything on targets with `PUBLIC`/`PRIVATE`/`INTERFACE`.
- **Dependencies** grow slowly into a mess. Choose one mechanism (`find_package`, `FetchContent`, or a package manager such as vcpkg or Conan) and stay with it.
- **Build times** rise with header-only-heavy code; use precompiled headers or unity builds selectively and measure first.
- **Multi-platform matrices** belong in `CMakePresets.json` so CI and developers run identical configurations.

## Variants

- **modern CMake** (≥3.20, this guide) — target-centric, `target_*` everything.
- **legacy CMake** (pre-3.0) — directory-centric, `include_directories` / `link_libraries` global. Avoid for new projects; only use when working in a codebase that hasn't been modernised.
- **CMake + Conan** — `conanfile.txt` or `conanfile.py` declares deps; `conan install` produces a CMake toolchain that pre-provides packages. Common in C++ industry.
- **CMake + vcpkg** — `vcpkg.json` manifest mode declares deps; `vcpkg install` populates a triplet directory; `CMAKE_TOOLCHAIN_FILE=vcpkg.cmake` makes them findable. Microsoft's package manager.
- **CMake + FetchContent** — `FetchContent_Declare` + `FetchContent_MakeAvailable` pulls deps from git/zip at configure time. Simplest for small projects; doesn't scale to dozens of deps.
- **Header-only library variant** — no `src/` directory, just `include/<project>/`. CMake target is `INTERFACE`. `target_include_directories(myproject INTERFACE include)`.
- **Multi-target project** — multiple libraries + executables, each with its own `add_library`/`add_executable`. Common when you have a core lib + CLI + tests + examples.

## Adoption checklist

- [ ] `cmake -S . -B build && cmake --build build && ctest --test-dir build` works from a clean clone.
- [ ] Public headers live in `include/<project>/` and are included with angle brackets and the project prefix.
- [ ] No `include_directories()` or `link_libraries()` at directory scope.
- [ ] `CMakePresets.json` captures the configurations CI runs.
- [ ] `build/` is ignored and no generated file is tracked.

## Real-world projects using this

- **nlohmann/json** (`nlohmann/json`) — single-header JSON library; CMake-based; reference for a header-only library with `find_package` support.
- **fmtlib/fmt** (`fmtlib/fmt`) — formatting library; modern CMake; reference for both `add_subdirectory` and `find_package` consumption.
- **Catch2** (`catchorg/Catch2`) — testing framework; CMake-native.
- **GoogleTest** (`google/googletest`) — testing framework; CMake-native, FetchContent-friendly.
- **abseil-cpp** (`abseil/abseil-cpp`) — Google's foundational C++ libraries; large CMake project with namespaced targets.
- **wasmtime** (`bytecodealliance/wasmtime` C-API) — large project; CMake for the C API.
- **OpenCV** (`opencv/opencv`) — huge CMake project with optional modules; reference for "every kind of dependency option you can imagine."
- **CLI11** (`CLIUtils/CLI11`) — single-header CLI parser; clean modern CMake.

## Migration & references

- **From Make to CMake**: list source files explicitly in a top-level `CMakeLists.txt`, recreate compiler flags via `target_compile_options`, replace `-I` flags with `target_include_directories`, replace `-l` flags with `target_link_libraries`. The first pass usually goes faster than expected.
- **From legacy CMake (pre-3.0) to modern**: replace every `include_directories`, `link_libraries`, `add_definitions` with their `target_*` equivalents. Bump `cmake_minimum_required(VERSION 3.20)`. Add namespaced alias targets (`add_library(myproject::myproject ALIAS myproject)`). Daniel Pfeifer's "Effective CMake" talk (CppCon 2017) walks through this.
- **Adding install rules retrofit**: install the library and its headers (`install(TARGETS myproject EXPORT myprojectTargets ... )`), generate `myprojectConfigVersion.cmake` via `write_basic_package_version_file`, install a `myprojectConfig.cmake.in` template via `configure_package_config_file`. Now downstream `find_package(myproject)` works.
- **Adopting FetchContent for tests**: replace a vendored `tests/catch.hpp` with `FetchContent_Declare(Catch2 GIT_REPOSITORY https://github.com/catchorg/Catch2.git GIT_TAG v3.7.0)` + `FetchContent_MakeAvailable(Catch2)`. Now CI fetches it on build.
- **References**:
  - CMake docs (https://cmake.org/cmake/help/latest/) — *cmake-language*, *cmake-buildsystem*, *cmake-packages*.
  - *Effective Modern CMake* (gist by Manuel Binna): https://gist.github.com/mbinna/c61dbb39bca0e4fb7d1f73b0d66a4fd1
  - *Modern CMake* online book (https://cliutils.gitlab.io/modern-cmake/) by Henry Schreiner.
  - Daniel Pfeifer, *Effective CMake* (CppCon 2017) — the talk that defined the modern style.
  - Sibling guides: `code/rust-library/`, `code/go-module/`.
