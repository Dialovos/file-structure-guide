// purpose/billing/invoice.tsx
// Billing has its own purpose dir with its own form, api, and types
// (only `invoice.tsx` is shown here for brevity). Notice that this file
// is *not* in a top-level `forms/` dir — `forms/` would force readers to
// hop between directories to understand "billing".

export function InvoiceView({ amount }: { amount: number }) {
  return (
    <article>
      <h1>Invoice</h1>
      <p>Amount due: ${amount.toFixed(2)}</p>
    </article>
  );
}
