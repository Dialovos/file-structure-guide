# Receipts and finance

## TL;DR

Every receipt, invoice, and financial document lands at `finance/YYYY/YYYY-MM/YYYY-MM-DD <vendor> $<amount> <description>.pdf`. Four fields, one separator (single space), one canonical order: date, vendor, amount, description. The amount lives in the filename — not in a sibling spreadsheet, not in metadata — so a year-end one-liner can pluck the dollar figures out with `grep` or `awk` and total them. The directory hierarchy gives chronological browsability for free; the filename gives query power for free. The whole scheme is text-grep-able, sort-able, and bash-tally-able without ever opening a single PDF or a database. It also survives every cloud move, every backup, every migration intact: the data is the path.

## Principles & why

A finance archive has to satisfy three different consumers, and the layout is designed to serve all three from the same encoding:

1. **You, mid-year, looking up "did I expense the office chair?"** — answered by scrolling the month directory and reading filenames. No tool needed; `ls` is the query engine.
2. **You, at year-end, totaling tax-deductible expenses** — answered by `awk`-ing the dollar values out of filenames in matching directories. The amount is *in the path*, so no spreadsheet lookup is required.
3. **Your accountant or future-you reconstructing context** — answered by the description field. "Office chair cushion" is more useful three years later than "purchase #4571".

The order **date → vendor → amount → description** is deliberate. Date first because lexicographic sort = chronological sort and that's the dominant browsing axis. Vendor second because grouping receipts from the same vendor in a directory listing is the second-most-common visual query. Amount third because that's the field a totaller cares about and putting it in a fixed position relative to the date and vendor makes regex extraction trivial. Description last because it's the longest and most variable field — pushing it to the end keeps the leading columns aligned for visual scanning.

The dollar sign is not decoration. It's a pinned anchor: `\$[0-9]+\.[0-9]{2}` finds every amount in every filename across the entire archive, regardless of vendor name length or description content. That regex is the basis of every total-summing one-liner you'll ever write against this layout.

## When to use

- Tracking deductible business expenses for a sole proprietor, freelancer, or small LLC where the volume is too low to justify Expensify or QuickBooks but too high to wing it.
- Monthly personal budgeting where you want filesystem-grade durability — receipts you scan once and reference for years.
- Year-end tax preparation when you want a single grep-able archive an accountant can also browse.
- Combining with a `tax-deductible/` directory or filename suffix (`...office-chair-cushion [tax].pdf`) so the deductible subset is queryable in one pass.
- Sole proprietorship or hobby-business record-keeping where IRS guidance recommends keeping receipts for 3–7 years and the filesystem is the cheapest reliable archive.
- Households tracking shared expenses where partners need to grep "who paid for the new fridge" without logging into a SaaS.

## When NOT to use

- You already use Expensify, YNAB, Wave, FreshBooks, QuickBooks, or any tool that ingests receipts and produces reports. The data lives there; mirroring it to the filesystem is wasted effort and a divergence risk.
- High-volume retail or e-commerce books where double-entry accounting and proper general-ledger software (hledger, Beancount, Ledger CLI) are doing the real work — the directory becomes a *document store* attached to the journal, with linkage by transaction ID, not the indexing scheme itself.
- You receive only digital receipts that arrive as email attachments — those want a Gmail label or a paperless-ngx pipeline, not manual filing.
- You don't itemise on your taxes and aren't running a business — three folders ("rent", "groceries", "everything else") is enough; the discipline of this scheme exceeds the value at that scale.
- You want OCR-and-search-as-the-primary-interface — paperless-ngx does that better than the filesystem; this guide is for the filesystem-first crowd.

## Tree diagram

```
finance/
└── 2026/
    ├── 2026-04/
    │   ├── 2026-04-01 amazon $42.18 office-chair-cushion.pdf
    │   ├── 2026-04-15 landlord $1850.00 rent.pdf
    │   └── 2026-04-22 grocery-co $108.42.pdf
    └── 2026-05/
```

## Naming rules

1. Top-level is `finance/`. Not `Receipts/` (too narrow), not `Documents/Finance/` (couples to a generic Documents tree). The single-purpose root means a backup or sync rule can target finance distinctly.
2. Year directory: `YYYY/`. Mirrors `files/date-archive/` and the ISO-date convention.
3. Month directory: `YYYY-MM/` — the redundant year prefix means a month directory remains self-describing if it's ever moved or symlinked elsewhere.
4. Filename form: `YYYY-MM-DD <vendor> $<amount> <description>.pdf`. Single space as separator (not space-dash-space) — this is the strongest deviation from the scanned-documents guide and exists because the dollar sign already serves as a strong visual delimiter for the amount.
5. The date is the *transaction date* (when the charge cleared, when the receipt was issued), not the scan date. For a monthly bill, use the issue date. For a card statement, expand to per-charge entries dated to each transaction.
6. Vendor slug is short kebab-case lowercase ASCII: `amazon`, `landlord`, `grocery-co`. Pick one form per vendor and never deviate; consistency is what makes vendor-grouped queries work.
7. Amount is `$<dollars>.<cents>` with two decimal places always, no thousands separator: `$1850.00` not `$1,850` and not `$1850`. The fixed format is what makes the regex `\$[0-9]+\.[0-9]{2}` reliable.
8. Description is optional but recommended for non-obvious purchases. Omit it for self-explanatory recurring costs (`rent`, `internet`) where the vendor field already tells the story. Include it for variable purchases (`office-chair-cushion`, `flight-jfk-lhr`).
9. Refunds are filed as separate documents with a leading minus sign in the amount: `2026-04-23 amazon -$42.18 office-chair-cushion-return.pdf`. The minus inside the dollar segment keeps the regex consistent.
10. Multi-currency: prefix non-USD amounts with the ISO 4217 code: `2026-04-15 hotel €120.50 paris-trip.pdf`. The dollar sign convention then becomes a per-currency anchor and your tally script needs a currency-aware pass.

## Anti-patterns

- **Amount in a spreadsheet, not the filename** — defeats the entire scheme; the filesystem becomes a dumb file store and you've reinvented Expensify badly. The amount must live in the path.
- **Comma thousands separators** (`$1,850.00`) — breaks the regex and breaks `awk -F'$'`. Always raw `$1850.00`.
- **Vendor inconsistency** — `amazon`, `Amazon`, `amazon-com`, `amzn` for the same vendor breaks vendor-grouped queries. Pick one form, stick to it, document it in `finance/VENDORS.md` if needed.
- **Receipt-shaped image PDFs without OCR** — fine for this scheme since the filename carries the data, *but* if you ever want to verify the amount from the document, OCR helps. Run `ocrmypdf` on ingestion as a no-cost insurance policy.
- **Mixing receipts with statements** — credit card statements and bank statements are aggregates of receipts; filing both in the same tree double-counts. Use `finance/statements/` as a sibling of `finance/YYYY/` for monthly statements.
- **Per-vendor top-level directories** — `finance/amazon/2026-04-01...pdf`. Loses chronological browsability and complicates monthly totals; vendor grouping is better served by filename ordering.
- **Trailing description with the file extension as the de-facto separator** — `2026-04-01-amazon-42.18-cushion.pdf` runs everything together; the dollar sign is what makes the amount visually findable, removing it kills the entire ergonomics.
- **Forgetting to file refunds** — credits without matching refund records make year-end totals wrong. Always file the refund the day it posts.
- **Over-categorising in the filename** — `2026-04-01 amazon $42.18 [office] [furniture] [tax-deductible] cushion.pdf` is bracket soup; use a sibling tag file or a directory for tags.

## Variants

- **date-vendor-amount-desc** (this guide) — the recommended form; fixed-position amount enables one-liner totals.
- **date-amount-vendor-desc** — `2026-04-01 $42.18 amazon office-chair-cushion.pdf`. Amount-led; useful when the dominant query is "what did I spend more than $100 on this month" but loses vendor-clustering in directory listings.
- **by-category-then-date** — `finance/tax-deductible/2026/2026-04-01 amazon $42.18 cushion.pdf`. Adds a category root; useful for tax-prep workflows but you must duplicate or symlink across categories.
- **per-vendor archive** — `finance/vendors/amazon/2026-04-01 $42.18 cushion.pdf` plus a flat `finance/by-date/` view via symlinks. Two queries, one source of truth.
- **paperless-managed flat** — paperless-ngx handles correspondents and tags; the filesystem is just a consume directory. Loses bash-grep ergonomics, gains full-text search.
- **hledger-driven sidecar** — receipts under `finance/documents/` referenced by transaction ID from a `journal.ledger` file in the project root. The journal is the source of truth; the receipts are evidence.
- **encrypted root** — `finance/` lives inside a gocryptfs or age-encrypted directory; same internal layout, encryption at rest.

## Real-world projects using this

- **hledger** — plain-text accounting, popular for personal finance; has a `documents/` convention parallel to the journal where receipts live, often using a YYYY/YYYY-MM date layout. https://hledger.org/
- **Beancount** — Python plain-text accounting; the `documents` directive points to a directory with this exact date-prefixed layout. https://beancount.github.io/
- **Ledger CLI** — the original plain-text accounting tool that inspired hledger and Beancount; same documents-directory pattern.
- **paperless-ngx** — open-source DMS frequently used for receipts, with tag-based organisation that complements (and can replace) the filename scheme. https://github.com/paperless-ngx/paperless-ngx
- **Firefly III** — self-hosted personal finance manager with an attachments scheme that mirrors this layout. https://www.firefly-iii.org/
- **GnuCash** — cross-platform double-entry; users frequently keep a parallel `finance/` documents tree for source-of-truth receipts.
- **YNAB import users who keep filesystem backups** — many users mirror their YNAB transactions into a filesystem archive in this exact form for long-term durability after they cancel the subscription.
- **Johnny.Decimal users** — the `21.01 Receipts/2026/` adaptation of the system maps cleanly onto this guide's layout.

## Migration & references

To impose this layout on an existing pile of receipts in `~/Downloads/` or a flat `~/Receipts/`, drive the rename from PDF metadata or a manual ingest pass:

```bash
# Year-end total for tax-deductible expenses (any month):
grep -rEho '\$[0-9]+\.[0-9]{2}' finance/2026/ | tr -d '$' | \
  awk '{s+=$1} END {printf "Total: $%.2f\n", s}'

# Per-vendor totals for the year:
find finance/2026/ -name '*.pdf' -printf '%f\n' | \
  awk '{
    match($0, /\$[0-9]+\.[0-9]+/); amt = substr($0,RSTART+1,RLENGTH-1)+0
    # vendor is the second whitespace-delimited token (after date)
    split($0, t, " "); vendor = t[2]
    totals[vendor] += amt
  } END { for (v in totals) printf "%-20s $%.2f\n", v, totals[v] }'

# Filter for a specific month:
grep -rEho '\$[0-9]+\.[0-9]{2}' finance/2026/2026-04/ | tr -d '$' | \
  awk '{s+=$1} END {printf "April 2026: $%.2f\n", s}'
```

For ingest from a download inbox:

```bash
# Move and rename a fresh receipt by hand:
mv ~/Downloads/receipt-4571.pdf "finance/2026/2026-04/2026-04-22 grocery-co \$108.42.pdf"

# Bulk-rename existing flat archive using PDF creation date:
for f in ~/Receipts/*.pdf; do
  d=$(pdfinfo "$f" 2>/dev/null | awk -F': +' '/^CreationDate/ {print $2}' | \
       python3 -c 'import sys,datetime;print(datetime.datetime.strptime(sys.stdin.read().strip(),"%a %b %d %H:%M:%S %Y").strftime("%Y-%m-%d"))' 2>/dev/null)
  [[ -z "$d" ]] && continue
  echo mv "$f" "finance/${d:0:4}/${d:0:7}/${d} unknown-vendor \$0.00 imported.pdf"
done
```

For paperless-ngx users: configure correspondents to match your vendor slugs and a filename template of `{created} {correspondent} {title}` to produce filenames close to this layout from paperless's database.

Further reading:

- hledger documentation, particularly the `documents` and `attachments` patterns — https://hledger.org/
- Beancount's "Importing Documents" guide — https://beancount.github.io/docs/
- IRS Publication 583 for record retention guidance (US small-business context).
- `files/scanned-documents/` — the related but distinct scheme for non-financial paper.
- `files/date-archive/` — the date-rooted directory layout this guide nests inside.
- `principles/iso-date-formats/` — the YYYY-MM-DD convention the filenames depend on.
- `principles/naming-by-purpose-not-type/` — why the amount is encoded in the name, not a sidecar.
