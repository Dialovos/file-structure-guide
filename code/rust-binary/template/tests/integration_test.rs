//! Integration tests run against the *library* half of the crate. They
//! cannot reach `main.rs` — that's why all the real logic lives in
//! `lib.rs`. Each `.rs` file in `tests/` compiles as its own crate.

use mybin::greet;

#[test]
fn greet_default() {
    assert_eq!(greet("world"), "hello, world");
}

#[test]
fn greet_handles_unicode() {
    assert_eq!(greet("世界"), "hello, 世界");
}
