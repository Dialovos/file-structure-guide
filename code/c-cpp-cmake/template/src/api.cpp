#include "myproject/api.h"

#include <stdexcept>
#include <string>

namespace myproject {

std::string greet(const std::string& name) {
    if (name.empty()) {
        throw std::invalid_argument("name must not be empty");
    }
    return "hello, " + name;
}

}  // namespace myproject
