// GET /api/hello
// File name maps directly to the route: <name>.<method>.ts
// defineEventHandler is auto-imported (it's a Nuxt-provided server util).

export default defineEventHandler(() => {
  return { message: "Hello, world!" };
});
