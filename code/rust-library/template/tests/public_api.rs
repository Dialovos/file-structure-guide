//! Integration tests exercise the crate the way a downstream user would:
//! they only see `pub` items reachable from `lib.rs`. If you need to
//! reach private internals, that's a unit test (in `#[cfg(test)] mod
//! tests` blocks inside the file under test).

use mylib::core::greet_checked;
use mylib::{greet, MylibError};

#[test]
fn greet_returns_hello() {
    assert_eq!(greet("alice"), "hello, alice");
}

#[test]
fn greet_checked_rejects_empty_input_with_typed_error() {
    let err = greet_checked("").unwrap_err();
    assert!(matches!(err, MylibError::InvalidInput(_)));
}
