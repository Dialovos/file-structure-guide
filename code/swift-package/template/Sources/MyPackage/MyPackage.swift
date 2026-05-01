import Foundation

/// `MyPackage` is the library's primary entry type. It exposes one
/// example function (``greet(_:)``) so the template demonstrates the
/// public surface; replace it with your real API as the package
/// grows.
public struct MyPackage {
    public init() {}

    /// Returns a friendly greeting for `name`. Falls back to "world"
    /// when `name` is empty or whitespace-only.
    public func greet(_ name: String) -> String {
        let trimmed = name.trimmingCharacters(in: .whitespacesAndNewlines)
        let target = trimmed.isEmpty ? "world" : trimmed
        return "hello, \(target)"
    }
}
