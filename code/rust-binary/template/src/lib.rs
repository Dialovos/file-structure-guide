//! Library half of the `mybin` binary crate.
//!
//! Everything except `fn main()` lives here so it can be reached by
//! integration tests in `tests/`, examples in `examples/`, and any future
//! benchmarks in `benches/`.

pub mod cli;

use cli::Cli;

/// Run the program. The binary's `main` calls this and maps the result to
/// an exit code. Public so integration tests can drive it directly.
pub fn run() -> Result<(), Box<dyn std::error::Error>> {
    let args = Cli::from_args();
    let output = greet(&args.name);
    println!("{output}");
    Ok(())
}

/// Pure function used by `run`. Keep these small and side-effect free; they
/// are the easiest piece of the program to test.
pub fn greet(name: &str) -> String {
    format!("hello, {name}")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greet_uses_the_name() {
        assert_eq!(greet("alice"), "hello, alice");
    }
}
