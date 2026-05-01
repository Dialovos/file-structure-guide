// Home page at "/". This is a Server Component — runs only on the server,
// ships zero JS for itself. Mark a child component "use client" if it needs
// hooks, event handlers, or browser APIs.

export default function HomePage() {
  return (
    <main>
      <h1>My App</h1>
      <p>Edit <code>app/page.tsx</code> to start.</p>
    </main>
  );
}
