// Tests for the co-located-layout example.
//
// The file name (`main.test.ts`) shares its base with `main.ts` and
// adds the conventional `.test.ts` suffix. The two files sit in the
// same directory so a refactor that moves `main.ts` mechanically takes
// `main.test.ts` along with it.

import { describe, expect, it } from "vitest";

import { add, isEven } from "./main";

describe("add", () => {
  it("returns the sum of two numbers", () => {
    expect(add(2, 3)).toBe(5);
    expect(add(-1, 1)).toBe(0);
  });
});

describe("isEven", () => {
  it("identifies even and odd numbers", () => {
    expect(isEven(0)).toBe(true);
    expect(isEven(2)).toBe(true);
    expect(isEven(3)).toBe(false);
  });
});
