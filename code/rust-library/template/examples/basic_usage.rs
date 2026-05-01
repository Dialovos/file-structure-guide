//! Run with: `cargo run --example basic_usage`
//!
//! Examples link against the library exactly the way a downstream
//! consumer would. They're free CI: every example must compile.

use mylib::greet;

fn main() {
    println!("{}", greet("example"));
}
