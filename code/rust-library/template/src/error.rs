//! Public error type for the crate.
//!
//! Uses `thiserror` to produce a typed, matchable error enum. Consumers
//! can match on individual variants — that's the whole reason a library
//! prefers `thiserror` over `anyhow` for its public surface.

use thiserror::Error;

/// All errors returned by `mylib`.
#[derive(Debug, Error)]
#[non_exhaustive]
pub enum MylibError {
    /// The caller passed an empty or otherwise unusable input.
    #[error("invalid input: {0}")]
    InvalidInput(String),

    /// An I/O error occurred while doing work on the caller's behalf.
    #[error("i/o error: {0}")]
    Io(#[from] std::io::Error),
}
