// after/single-large-file/concern-a.ts
//
// This file holds what was the `// === Login ===` section in the
// before/ version. One concern, one file. In a real project this file
// would be named after its concern (`login.ts`), not generically
// (`concern-a.ts`); we use the generic name in the template only so
// the pairing with concern-b.ts is obvious at a glance.

export type LoginInput = { email: string; password: string };

export function login(input: LoginInput): { token: string } {
  if (!input.email || !input.password) {
    throw new Error("login: email and password required");
  }
  // Real implementation: look up user, verify hashed password, mint
  // JWT, log the login event, etc.
  return { token: "fake-jwt-for-" + input.email };
}
