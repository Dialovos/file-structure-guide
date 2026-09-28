# business-documents-layout — template

A folder skeleton for one business, with a client folder template.

## What to rename

- `my-company` to your business name
- `clients/_template/` to each client's short name

## What to fill

- `README.project-example.md` — entity facts, where documents are, who has access
- Each client's `README.md` — contacts, scope, rates, status

## What to delete

- Areas you don't use (for example `marketing/`)

## First run

```bash
cp -r template ~/business/my-company
cp -r ~/business/my-company/clients/_template ~/business/my-company/clients/acme-corp
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../receipts-and-finance/` — expense naming
