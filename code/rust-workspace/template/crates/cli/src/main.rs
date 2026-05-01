//! CLI frontend. Stays thin: parse args, call into `myworkspace_core`,
//! print the result, exit. All real logic belongs in the core crate so
//! it can be reused by future frontends (server, WASM, FFI).

use clap::Parser;
use myworkspace_core::greet;
use std::process::ExitCode;

#[derive(Debug, Parser)]
#[command(author, version, about = "myworkspace CLI", long_about = None)]
struct Cli {
    /// Whom to greet.
    #[arg(default_value = "world")]
    name: String,
}

fn main() -> ExitCode {
    let cli = Cli::parse();
    match greet(&cli.name) {
        Ok(msg) => {
            println!("{msg}");
            ExitCode::SUCCESS
        }
        Err(err) => {
            eprintln!("error: {err}");
            ExitCode::FAILURE
        }
    }
}
