// good-date-parsing/parse.ts
// Single purpose: parse calendar input into Date objects.
// Formatting dates as strings belongs elsewhere (string-formatting/
// or a sibling date-formatting/ if it grows enough to deserve its own dir).

export function parseISODate(input: string): Date {
  const ts = Date.parse(input);
  if (Number.isNaN(ts)) {
    throw new Error(`not an ISO 8601 date: ${input}`);
  }
  return new Date(ts);
}

export function parseUnixSeconds(input: number): Date {
  return new Date(input * 1000);
}

export function isISODate(input: string): boolean {
  return /^\d{4}-\d{2}-\d{2}(T.*)?$/.test(input);
}
