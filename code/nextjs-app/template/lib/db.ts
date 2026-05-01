// Database client stub. Replace with your real ORM/driver (Prisma, Drizzle,
// pg, etc.). Importing this file from a Client Component is an anti-pattern —
// keep DB calls server-side only.

export async function query<T = unknown>(_sql: string, _params: unknown[] = []): Promise<T[]> {
  throw new Error("lib/db.ts: implement query() with your real database driver");
}
