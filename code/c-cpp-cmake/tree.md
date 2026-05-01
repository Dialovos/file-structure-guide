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
