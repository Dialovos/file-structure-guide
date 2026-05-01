// Auto-imported as useAuth() in any <script setup> or composable.
// Replace the stub with real auth logic (NextAuth-equivalent for Vue:
// nuxt-auth-utils, sidebase/nuxt-auth, or hand-rolled with a session
// cookie + server middleware).

export type User = {
  id: string;
  email: string;
};

export function useAuth() {
  // useState is request-scoped in SSR — safe shared state per user.
  const user = useState<User | null>("auth:user", () => null);

  function signIn(email: string) {
    user.value = { id: "stub", email };
  }

  function signOut() {
    user.value = null;
  }

  return { user, signIn, signOut };
}
