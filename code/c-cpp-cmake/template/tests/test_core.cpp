#include <catch2/catch_test_macros.hpp>

#include "myproject/api.h"
#include "myproject/core.h"

TEST_CASE("add returns the sum of two ints", "[core]") {
    REQUIRE(myproject::add(2, 3) == 5);
    REQUIRE(myproject::add(-1, 1) == 0);
}

TEST_CASE("greet returns a hello string", "[api]") {
    REQUIRE(myproject::greet("alice") == "hello, alice");
}

TEST_CASE("greet rejects an empty name", "[api]") {
    REQUIRE_THROWS_AS(myproject::greet(""), std::invalid_argument);
}
