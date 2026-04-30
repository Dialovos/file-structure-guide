// good-string-formatting/format.ts
// Single purpose: turn arbitrary values into display strings.
// Adding date logic, HTTP logic, or auth logic here is a smell —
// those belong in their own peer directories.

export function formatTitle(input: string): string {
  return input.trim().replace(/\s+/g, " ");
}

export function truncate(input: string, max: number): string {
  if (input.length <= max) return input;
  return input.slice(0, Math.max(0, max - 1)) + "…";
}

export function pluralize(noun: string, count: number): string {
  return count === 1 ? noun : `${noun}s`;
}
