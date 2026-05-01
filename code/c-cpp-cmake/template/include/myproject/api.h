#pragma once

#include <string>

namespace myproject {

/// Returns a friendly greeting for the given name.
///
/// Throws std::invalid_argument if the name is empty.
std::string greet(const std::string& name);

}  // namespace myproject
