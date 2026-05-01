add_library(myproject
    core.cpp
    api.cpp
)
add_library(myproject::myproject ALIAS myproject)

target_include_directories(myproject
    PUBLIC
        $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

target_compile_features(myproject PUBLIC cxx_std_17)

# Reasonable warnings. Consumers don't inherit these — they're PRIVATE.
if(MSVC)
    target_compile_options(myproject PRIVATE /W4 /permissive-)
else()
    target_compile_options(myproject PRIVATE
        -Wall -Wextra -Wpedantic -Wshadow -Wnon-virtual-dtor
    )
endif()

set_target_properties(myproject PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
)
