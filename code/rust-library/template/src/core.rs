//! Core public API.
//!
//! This module holds the crate's primary functionality. Keep the public
//! surface small and well-documented; private helpers live in
//! `#[cfg(test)] mod tests` blocks or sibling private modules.

use crate::error::MylibError;

/// Greet someone by name.
///
/// Returns `"hello, <name>"`. An empty `name` is rejected with
/// [`MylibError::InvalidInput`] so callers see a typed error rather than
/// a silent empty string.
///
/// # Example
///
/// ```
/// use mylib::core::greet_checked;
/// assert_eq!(greet_checked("world").unwrap(), "hello, world");
/// assert!(greet_checked("").is_err());
/// ```
pub fn greet_checked(name: &str) -> Result<String, MylibError> {
    if name.is_empty() {
        return Err(MylibError::InvalidInput("name must not be empty".into()));
    }
    Ok(format!("hello, {name}"))
}

/// Infallible variant of [`greet_checked`] that defaults to "world" on
/// empty input. Provided as a convenience for examples and quick demos.
pub fn greet(name: &str) -> String {
    let n = if name.is_empty() { "world" } else { name };
    format!("hello, {n}")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greet_checked_rejects_empty() {
        assert!(greet_checked("").is_err());
    }

    #[test]
    fn greet_falls_back_to_world() {
        assert_eq!(greet(""), "hello, world");
    }
}
