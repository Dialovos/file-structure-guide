# Receipts-and-finance template

A skeleton showing the year-month directory structure and one example filename in the `YYYY-MM-DD <vendor> $<amount> <description>.pdf` form.

## What's here

- `2026/2026-04/2026-04-30 example $00.00.pdf` — a zero-byte placeholder demonstrating the canonical filename. Four fields separated by single spaces: date, vendor, amount (with `$` prefix and two decimals), description.
- `2026/2026-05/` — empty next-month directory, pre-created to show the month progression.

The placeholder is intentionally empty — it exists to demonstrate the path and filename shape, not to open in a PDF reader.

## To adopt this template

1. Copy the structure into your archive root: `cp -r template/ ~/finance/` or `cp -r template/ /mnt/archive/finance/`.
2. As receipts arrive, file each as `<txn-date> <vendor-slug> $<amount> [description].pdf` inside the matching `YYYY/YYYY-MM/` directory.
3. Keep vendor slugs consistent — pick one form per vendor (`amazon`, not also `Amazon` and `amzn`) and stick to it.
4. Always use two decimal places in the amount (`$108.42`, not `$108.4` or `$108`) and never use thousands separators (`$1850.00`, not `$1,850.00`). The fixed format is what makes the regex `\$[0-9]+\.[0-9]{2}` reliable.
5. Add new month directories (`2026-06/`, `2026-07/`) as the year progresses.

## Year-end one-liner

The whole point of putting the dollar amount in the filename:

```bash
grep -rEho '\$[0-9]+\.[0-9]{2}' finance/2026/ | tr -d '$' | \
  awk '{s+=$1} END {printf "Total: $%.2f\n", s}'
```

That tallies every receipt for the year. Filter by month by narrowing the path. Filter by vendor by adding a `--include` glob. The whole financial archive is text-grep-able with no extra tooling.

## What to rename or remove

- Delete the `2026-04-30 example $00.00.pdf` placeholder once you have real receipts in that month — it's only a shape demo.
- Add new year directories as needed (`2025/`, `2027/`); the template only ships one to keep the demo small.
- Drop this `README.md` once the template has been adapted (the verifier requires it while it lives in the repo).

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.

## Refunds

File refunds as separate documents with a leading minus sign inside the dollar segment: `2026-04-23 amazon -$42.18 office-chair-cushion-return.pdf`. The minus stays inside the regex match so totals naturally net out.

## Multi-currency

Prefix non-USD amounts with the ISO 4217 code: `2026-04-15 hotel €120.50 paris-trip.pdf`. The currency symbol then becomes a per-currency anchor for your tally script.
