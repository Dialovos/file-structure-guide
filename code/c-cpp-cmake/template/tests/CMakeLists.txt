include(FetchContent)

FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG        v3.7.0
)
FetchContent_MakeAvailable(Catch2)

add_executable(test_core test_core.cpp)
target_link_libraries(test_core
    PRIVATE
        myproject::myproject
        Catch2::Catch2WithMain
)
target_compile_features(test_core PRIVATE cxx_std_17)

add_test(NAME test_core COMMAND test_core)
