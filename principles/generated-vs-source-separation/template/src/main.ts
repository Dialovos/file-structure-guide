// Source file (tracked).
//
// In a real project, the build pipeline (tsc, esbuild, Vite, Rollup,
// etc.) compiles this file and writes the output to `dist/`, which is
// gitignored. Running the build is what regenerates `dist/main.js` —
// the source here is the authoritative version.

export function greet(name: string): string {
  return `Hello, ${name}!`;
}

export function farewell(name: string): string {
  return `Goodbye, ${name}.`;
}

if (typeof require !== "undefined" && require.main === module) {
  console.log(greet("world"));
}
