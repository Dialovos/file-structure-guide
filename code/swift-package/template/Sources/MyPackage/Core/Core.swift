import Foundation

/// Internal helper kept out of the public API surface. Anything that
/// shouldn't be visible to consumers belongs at `internal` (the Swift
/// default) — leave the `public` keyword off and the type stays
/// scoped to the `MyPackage` module.
struct Clock {
    /// Returns the current wall-clock time. Wrapped here so tests can
    /// substitute a fake without depending on `Date()` directly.
    func now() -> Date { Date() }
}
