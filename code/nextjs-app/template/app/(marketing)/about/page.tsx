// /about — note the (marketing) parent folder is a *route group*: it
// organizes the route source without affecting the URL. The URL is /about,
// not /marketing/about.

export default function AboutPage() {
  return (
    <main>
      <h1>About</h1>
      <p>This page is grouped under (marketing) for organization only.</p>
    </main>
  );
}
