//! Run with: `cargo run --example basic`
//!
//! Examples link against the library half of the crate, so they double as
//! living documentation that must compile in CI.

fn main() {
    let msg = mybin::greet("example");
    println!("{msg}");
}
