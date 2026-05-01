//! CLI argument parsing.
//!
//! Kept separate from `lib.rs` so that the parsed `Cli` struct is the only
//! coupling between the entrypoint and the rest of the program. Tests can
//! construct `Cli` values directly without going through argv.

use clap::Parser;

/// Replace this with a one-line description of your tool.
#[derive(Debug, Parser)]
#[command(author, version, about, long_about = None)]
pub struct Cli {
    /// Whom to greet (positional argument).
    #[arg(default_value = "world")]
    pub name: String,

    /// Increase output verbosity. Repeat for more (-v, -vv, -vvv).
    #[arg(short, long, action = clap::ArgAction::Count)]
    pub verbose: u8,
}

impl Cli {
    /// Parse from `std::env::args_os()`. Equivalent to `Cli::parse()` but
    /// named to make test seams obvious.
    pub fn from_args() -> Self {
        Self::parse()
    }
}
