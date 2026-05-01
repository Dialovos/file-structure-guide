// API route at GET /api/hello.
// Export each HTTP method as a named function. The Request/Response objects
// are the standard Web Fetch API types — no Next-specific Req/Res shape.

import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ message: "Hello, world!" });
}
