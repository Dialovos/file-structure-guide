// Trivial source module for the co-located-layout example.
//
// The matching test lives next to this file at ./main.test.ts.
// Vitest, Jest, and most modern JS/TS test runners discover the
// `*.test.ts` suffix by default; no separate `tests/` tree needed.

export function add(a: number, b: number): number {
  return a + b;
}

export function isEven(n: number): boolean {
  return n % 2 === 0;
}
