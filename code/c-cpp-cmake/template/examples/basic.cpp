#include <iostream>

#include "myproject/api.h"
#include "myproject/core.h"

int main(int argc, char** argv) {
    const std::string name = (argc > 1) ? argv[1] : "world";
    std::cout << myproject::greet(name) << '\n';
    std::cout << "2 + 3 = " << myproject::add(2, 3) << '\n';
    return 0;
}
