import { describe, it, expect } from "vitest";
import { greet } from "../src/index.js";

describe("greet", () => {
  it("returns a default greeting", () => {
    expect(greet("world")).toBe("hello, world");
  });

  it("shouts when loud is true", () => {
    expect(greet("world", { loud: true })).toBe("HELLO, WORLD");
  });

  it("rejects empty input", () => {
    expect(() => greet("")).toThrow(/must not be empty/);
  });
});
