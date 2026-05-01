// Auth helpers stub. Replace with your real auth library (NextAuth, Clerk,
// Lucia, hand-rolled). Server-side only.

export type Session = {
  userId: string;
  email: string;
};

export async function getSession(): Promise<Session | null> {
  return null;
}
