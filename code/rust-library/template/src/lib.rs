//! # mylib
//!
//! Replace this crate-level doc comment with a real summary of what the
//! crate does, who it's for, and a runnable example.
//!
//! ## Example
//!
//! ```
//! use mylib::greet;
//! assert_eq!(greet("world"), "hello, world");
//! ```

#![deny(missing_docs)]
#![warn(rust_2018_idioms)]
#![cfg_attr(docsrs, feature(doc_cfg))]

pub mod core;
pub mod error;

// Re-export the most-used public surface so consumers can write
// `use mylib::greet;` instead of `use mylib::core::greet;`.
pub use crate::core::greet;
pub use crate::error::MylibError;
