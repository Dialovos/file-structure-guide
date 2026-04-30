// after/single-large-file/index.ts
//
// The public surface of the module, expressed as a flat list of
// re-exports. No logic lives here; readers can scan this file and see
// what the module offers without reading any implementation.
//
// Note: imports written `from "./single-large-file"` continue to work
// because most module resolvers (TS, Node, Vite, Webpack) resolve the
// directory to its index.ts.

export { login } from "./concern-a";
export type { LoginInput } from "./concern-a";

export { signup } from "./concern-b";
export type { SignupInput } from "./concern-b";

// In a real refactor of the `before/` example, you'd typically have a
// third file (`./token-refresh.ts`) and possibly a `./types.ts` for
// shared types. For this template, two concerns are enough to convey
// the pattern.
