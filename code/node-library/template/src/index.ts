// Public API barrel.
//
// Only re-export what consumers should depend on. Anything not re-exported
// here is a private implementation detail, even if it's `export`-ed from
// its own module. Keep this file scannable: it doubles as documentation
// of the public surface.

export { greet } from "./core.js";
export type { GreetOptions } from "./core.js";
