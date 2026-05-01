// Thin entrypoint. All logic lives in `lib.rs` so it can be reached by
// integration tests, examples, and benchmarks.
//
// The pattern: parse, dispatch, exit. Anything more complex belongs in `lib::run`.

use std::process::ExitCode;

fn main() -> ExitCode {
    match mybin::run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(err) => {
            eprintln!("error: {err}");
            ExitCode::FAILURE
        }
    }
}
