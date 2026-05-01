cmake_minimum_required(VERSION 3.20)
project(myproject
    VERSION 0.1.0
    DESCRIPTION "Modern CMake C++ project template."
    LANGUAGES CXX
)

# ----------------------------------------------------------------------
# Project-wide options. Prefix with the project name so they don't
# collide with parent projects when this is consumed via add_subdirectory.
# ----------------------------------------------------------------------
option(MYPROJECT_BUILD_TESTS    "Build the myproject test suite"    ON)
option(MYPROJECT_BUILD_EXAMPLES "Build the myproject examples"      ON)

# Default to a sensible build type if the user didn't pick one.
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
        Debug Release RelWithDebInfo MinSizeRel)
endif()

# Honor consumers' compile-commands choice; harmless when unused.
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# ----------------------------------------------------------------------
# The library itself. All compile knowledge lives on this target.
# ----------------------------------------------------------------------
add_subdirectory(src)

# ----------------------------------------------------------------------
# Tests are opt-out for top-level builds, opt-in when consumed.
# ----------------------------------------------------------------------
if(MYPROJECT_BUILD_TESTS AND PROJECT_IS_TOP_LEVEL)
    enable_testing()
    add_subdirectory(tests)
endif()

if(MYPROJECT_BUILD_EXAMPLES AND PROJECT_IS_TOP_LEVEL)
    add_subdirectory(examples)
endif()

# ----------------------------------------------------------------------
# Install rules. Allows downstream `find_package(myproject ... )`.
# ----------------------------------------------------------------------
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

install(TARGETS myproject
    EXPORT myprojectTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(DIRECTORY include/myproject
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    FILES_MATCHING PATTERN "*.h"
)

install(EXPORT myprojectTargets
    FILE myprojectTargets.cmake
    NAMESPACE myproject::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/myproject
)

write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/myprojectConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)
