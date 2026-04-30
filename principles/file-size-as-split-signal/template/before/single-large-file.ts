// before/single-large-file.ts
//
// This stub illustrates the smell, not the size. In a real project this
// file would be ~500-800 lines; here it's 50 lines, but the structural
// problem is identical: one file with explicit section comments, each
// section a distinct concern.
//
// The section comments themselves are the signal. When you find
// yourself writing `// === Login ===` markers to navigate a file, the
// file is asking to become a directory.

// === Login ===

export type LoginInput = { email: string; password: string };

export function login(input: LoginInput): { token: string } {
  if (!input.email || !input.password) {
    throw new Error("login: email and password required");
  }
  // ... real implementation would talk to a database, hash a password,
  // mint a token, and so on. ~150-200 lines in a real codebase.
  return { token: "fake-jwt-for-" + input.email };
}

// === Signup ===

export type SignupInput = { email: string; password: string; name: string };

export function signup(input: SignupInput): { id: string } {
  if (!input.email || !input.password || !input.name) {
    throw new Error("signup: missing required field");
  }
  // ... validate the email is unique, hash the password, persist the
  // user, send a verification email. ~150-200 lines in a real codebase.
  return { id: "user_" + Math.random().toString(36).slice(2, 10) };
}

// === Token refresh ===

export function refreshToken(oldToken: string): { token: string } {
  if (!oldToken.startsWith("fake-jwt-for-")) {
    throw new Error("refreshToken: invalid token");
  }
  // ... real implementation would verify signature, check expiry, mint
  // a new token. ~100-150 lines in a real codebase.
  return { token: oldToken + "-refreshed" };
}
