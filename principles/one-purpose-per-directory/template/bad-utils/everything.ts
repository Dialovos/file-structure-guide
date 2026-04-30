// bad-utils/everything.ts
//
// ANTI-PATTERN — DO NOT COPY THIS LAYOUT.
//
// This file is the symptom of a junk-drawer directory. A single file
// (and a single directory holding it) mixes string formatting, date
// parsing, HTTP retry, and auth-token helpers. None of these have any
// reason to live together. They have different callers, different
// dependencies, and different reasons to change.
//
// The fix: split into peer directories named by purpose —
//   string-formatting/, date-parsing/, http-retry/, auth-tokens/
// Each becomes independently testable, ownable, and deletable.

export function formatString(s: string): string {
  return s.trim();
}

export function parseDate(s: string): Date {
  return new Date(s);
}

export async function retryHttp<T>(fn: () => Promise<T>, tries = 3): Promise<T> {
  let lastError: unknown;
  for (let i = 0; i < tries; i++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
    }
  }
  throw lastError;
}

export function tokenHelpers(token: string): string {
  return `Bearer ${token}`;
}
