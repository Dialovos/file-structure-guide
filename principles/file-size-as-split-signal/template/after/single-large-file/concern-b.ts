// after/single-large-file/concern-b.ts
//
// This file holds what was the `// === Signup ===` section in the
// before/ version. One concern, one file. In a real project this would
// be named `signup.ts` after its concern, per the
// naming-by-purpose-not-type rule.

export type SignupInput = { email: string; password: string; name: string };

export function signup(input: SignupInput): { id: string } {
  if (!input.email || !input.password || !input.name) {
    throw new Error("signup: missing required field");
  }
  // Real implementation: validate email uniqueness, hash password,
  // persist the user, dispatch verification email.
  return { id: "user_" + Math.random().toString(36).slice(2, 10) };
}
