# Modern CMake C++ — template

A `cp -r`-able starter for a C/C++ library + tests + examples using
**modern CMake** (≥3.20) with target-centric configuration. The library
is named `myproject`; consumers depend on the namespaced alias
`myproject::myproject` whether they vendor it (`add_subdirectory`) or
install it (`find_package`).

## Layout at a glance

```
.
├── CMakeLists.txt              # top-level
├── include/myproject/          # public headers — namespaced
│   ├── core.h
│   └── api.h
├── src/                        # sources + per-dir CMakeLists
│   ├── CMakeLists.txt
│   ├── core.cpp
│   └── api.cpp
├── tests/                      # Catch2 via FetchContent + CTest
│   ├── CMakeLists.txt
│   └── test_core.cpp
├── examples/basic.cpp          # consumes myproject::myproject
└── cmake/                      # custom Find* / helpers (empty here)
```

## What to rename

`myproject` is everywhere. Pick a real name (lowercase; underscores or
kebab-case both work):

- `CMakeLists.txt` — `project(myproject ...)`, every `MYPROJECT_*`
  option, every install path, every `myproject::` alias.
- `include/myproject/` — rename the directory to your project name.
  All public headers move with it.
- `src/CMakeLists.txt` — `add_library(myproject ...)` and the alias.
- `src/*.cpp` — `#include "myproject/..."` paths and the
  `namespace myproject {}` blocks.
- `tests/test_core.cpp`, `examples/basic.cpp` — same headers and
  namespace.
- This `README.md`.

## What to fill

- `CMakeLists.txt` — bump `VERSION 0.1.0` as you release; describe
  your project in `DESCRIPTION`.
- `include/myproject/api.h` and `include/myproject/core.h` — your real
  public API.
- `LICENSE` — replace `{{YEAR}}` and `{{NAME}}`.

## What to delete

- This template `README.md`.
- The `add` / `greet` stubs once you have real code.
- `examples/` if you don't ship examples; remove the
  `add_subdirectory(examples)` call too.

## First build

```bash
cmake -B build -S .
cmake --build build --parallel
ctest --test-dir build --output-on-failure
```

Run the example:

```bash
./build/examples/basic alice
# → "hello, alice"
# → "2 + 3 = 5"
```

Switch build type:

```bash
cmake -B build -S . -DCMAKE_BUILD_TYPE=Debug
cmake --build build
```

Ninja generator (faster, recommended):

```bash
cmake -B build -S . -G Ninja
cmake --build build
```

## Consuming this library

### As a vendored subdirectory

```cmake
add_subdirectory(third_party/myproject)
target_link_libraries(my_app PRIVATE myproject::myproject)
```

### As an installed package

```bash
cmake --install build --prefix /opt/myproject
```

Then in the consumer:

```cmake
find_package(myproject 0.1 REQUIRED)
target_link_libraries(my_app PRIVATE myproject::myproject)
```

The `myproject::myproject` target name is identical in both cases —
this is the modern-CMake portability win.

## Pair this with

- `../GUIDE.md` — full reasoning for modern CMake.
- `../../rust-library/` — the Rust analogue (Cargo enforces a similar
  shape automatically).
- `../../go-module/` — the Go analogue (no build system, but
  comparable layout conventions).
