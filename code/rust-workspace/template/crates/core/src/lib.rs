//! # myworkspace-core
//!
//! Shared core library used by every binary in the workspace. Keep it
//! free of CLI parsing and IO concerns; expose pure functions and typed
//! errors here.

#![deny(missing_docs)]

use thiserror::Error;

/// Errors returned by the core library.
#[derive(Debug, Error)]
#[non_exhaustive]
pub enum CoreError {
    /// The caller passed an empty or otherwise unusable input.
    #[error("invalid input: {0}")]
    InvalidInput(String),
}

/// Greet someone by name. Empty input returns a typed error so callers
/// can decide whether to fall back to a default or surface the failure.
pub fn greet(name: &str) -> Result<String, CoreError> {
    if name.is_empty() {
        return Err(CoreError::InvalidInput("name must not be empty".into()));
    }
    Ok(format!("hello, {name}"))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greet_returns_typed_error_on_empty() {
        assert!(greet("").is_err());
    }

    #[test]
    fn greet_uses_the_name() {
        assert_eq!(greet("alice").unwrap(), "hello, alice");
    }
}
