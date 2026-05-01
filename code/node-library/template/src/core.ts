/**
 * Options for {@link greet}.
 */
export interface GreetOptions {
  /** Whether to shout the greeting (uppercase). */
  loud?: boolean;
}

/**
 * Greet someone by name.
 *
 * @example
 * greet("world")                // → "hello, world"
 * greet("world", { loud: true }) // → "HELLO, WORLD"
 */
export function greet(name: string, options: GreetOptions = {}): string {
  if (!name) {
    throw new Error("name must not be empty");
  }
  const message = `hello, ${name}`;
  return options.loud ? message.toUpperCase() : message;
}
