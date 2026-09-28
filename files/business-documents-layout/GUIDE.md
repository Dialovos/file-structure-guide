## TL;DR

Give each business (or side business) **one folder** with the same six areas every time: **branding**, **plans**, **clients**, **finance**, **legal**, and **archive**, plus **marketing** if you publish content. Inside `clients/`, each client gets one folder holding everything for that client (proposals, contracts, deliverables, notes), so a project is findable by name and closable as a unit. Financial documents follow a dated structure (see `receipts-and-finance`), and legal and identity documents are kept apart, with tighter access and encrypted backups. Deliverables sent to clients are copies of finished work, kept with the sent version and date; working files stay separate from what you delivered. The goal is that you can answer "what did we agree, what did we send, what did we invoice, and where is the signed copy?" for any client in under a minute, and that closing a client or a year is a move, not a clean-up project.

## Principles & why

1. **One business, one root.** Mixing businesses (or business and personal) in one tree makes access control, taxes, and handover harder. A separate folder per entity keeps each one self-contained.
2. **Group by relationship, then by document type.** For client work, you think "client X" first; keeping everything for X together makes retrieval and closure simple.
3. **Signed and sent copies are evidence.** Keep the exact version of contracts, proposals, and deliverables that were signed or sent, with dates. Working drafts are different and can be discarded.
4. **Sensitive material is separated.** Legal, identity, tax, and banking documents need tighter permissions and encrypted backups; a distinct `legal/` and `finance/` area makes that possible.
5. **Money documents are dated and immutable.** Invoices and receipts are named by date, party, and amount, and never edited after issue; corrections are new documents.
6. **Closing is a move.** A finished client or completed tax year goes to `archive/` with its name and dates intact, keeping the active tree small.

## When to use

- **Freelancers, consultants, and sole proprietors** with several clients.
- **Small businesses and early-stage startups** without a document management system.
- **Side projects that may become businesses**, where handover or tax reporting will need organized records.
- **Anyone who needs to hand documents to an accountant, lawyer, or successor.**

## When NOT to use

- **Regulated industries** (healthcare, finance, legal practice) with specific record-keeping and security requirements; use compliant systems.
- **Team-scale businesses** needing permissions, audit logs, and collaboration; a proper document platform is better.
- **Source code and product repositories**; those are Git projects (see `workspace-root-layout`).
- **Accounting itself.** Use accounting software for the books; this layout stores the supporting documents.

## Tree diagram

```
business/
└── my-company/
    ├── README.md                      ← entity facts, where things are, who has access
    ├── branding/
    │   ├── logo/
    │   ├── palette-and-fonts.md
    │   └── voice.md
    ├── plans/
    │   ├── business-plan.md
    │   └── 2026-annual-goals.md
    ├── clients/
    │   └── acme-corp/
    │       ├── README.md              ← contact, scope, rates, status
    │       ├── proposals/
    │       ├── contracts/             ← signed copies
    │       ├── deliverables/
    │       │   └── 2026-04-30-report-v1-sent.pdf
    │       └── notes/
    ├── finance/
    │   ├── invoices/
    │   │   └── 2026/2026-04-30-acme-corp-invoice-0042.pdf
    │   ├── expenses/                  ← see receipts-and-finance
    │   └── tax/
    │       └── 2025/
    ├── legal/
    │   ├── formation/
    │   ├── licenses-and-insurance/
    │   └── policies/
    ├── marketing/
    └── archive/
        └── 2025-clients/
```

## Naming rules

- **Entity folder** is the business name in kebab-case (`my-company`); a README states legal name, registration details location, and access.
- **Client folders** are the client's short name in kebab-case (`acme-corp`); one per client, never per project unless projects are independent engagements.
- **Dated documents** start with an ISO date (`2026-04-30-...`); see `iso-date-formats`.
- **Invoices** are `YYYY-MM-DD-<client>-invoice-<number>.pdf` with sequential invoice numbers; never reuse or renumber.
- **Sent deliverables** carry their state in the name (`...-report-v1-sent.pdf`) because the sent version is a record; working files aren't versioned in names (see `versioning-in-paths`).
- **Contracts** are `YYYY-MM-DD-<client>-<type>-signed.pdf`, and the unsigned draft is kept separately or discarded.

## Worked example

A freelancer's client work is spread across email attachments, a `Documents/` folder, and a shared drive. Tax time and a client dispute both need documents quickly.

1. Create `business/my-company/` with `branding/`, `plans/`, `clients/`, `finance/`, `legal/`, `marketing/`, and `archive/`, and write the README with entity facts and where the backups are.
2. For each client, create `clients/<client>/` with `proposals/`, `contracts/`, `deliverables/`, and `notes/`, and a short README (contacts, scope, rates, status, key dates).
3. Move signed contracts into `contracts/` with names that include the date and `-signed`. Locate missing signed copies in email and request them if needed.
4. Save each sent deliverable into `deliverables/` with the date and `-sent`, exactly as the client received it.
5. Move invoices to `finance/invoices/YYYY/` with sequential numbers, and expense documents to `finance/expenses/` using the dated naming in `receipts-and-finance`.
6. Put formation documents, insurance, and licenses into `legal/`, restrict who can access that folder, and make sure it is in an encrypted backup (see `backup-3-2-1-layout`).
7. When a client engagement ends, add a closing note (what was delivered, what was paid, lessons), and move the folder to `archive/<year>-clients/`.
8. At year end, give your accountant `finance/` for the year, and archive it with a short index.

For any client, the agreement, what was sent, and what was billed sit in one folder.

## Anti-patterns

- **Filing by document type across clients** (`all-contracts/`, `all-invoices/`). It's efficient for accounting, terrible for client questions; use client folders and generate cross-client views.
- **Working files with no record of what was sent.** If a dispute arises, the sent copy is what matters.
- **Editing issued invoices.** Issue a credit note or a new invoice; keep the original.
- **Sensitive documents in shared folders** with broad access. Separate and encrypt.
- **One folder for two businesses** or for business and personal. It complicates taxes and handover.
- **Renaming after the fact** to make things tidy, losing the original dates. Preserve names of signed and sent documents.
- **Unsigned drafts mistaken for signed copies.** Only signed versions go in `contracts/`, with `-signed` in the name.

## Scaling & failure modes

- **Many clients**: keep `clients/` flat and use each client's README plus a top-level `clients/INDEX.md` table (client, status, start date, value) (see `indexes-and-mocs`); archive inactive ones yearly.
- **Employees or contractors**: move to a system with permissions and audit trails; keep this layout as the folder convention inside it.
- **Multiple entities or brands**: one root per legal entity, and a `README.md` at the parent describing which is which.
- **Regulatory retention**: add retention periods to the entity README (for example how many years to keep invoices and contracts in your jurisdiction) and delete deliberately after that.
- **Handover or sale**: an organized tree with a README and index is itself a due-diligence asset.
- **Automation**: invoice numbering and document naming can be scripted; keep templates in `finance/templates/`.

## Variants

- **Client-first** (this guide): best for service businesses.
- **Project-first**: `projects/<name>/` when work isn't tied to a single client (products, internal projects).
- **Function-first**: `sales/`, `operations/`, `finance/`, `legal/`, for teams with functional roles.
- **Johnny.Decimal numbering**: `10-19 finance`, `20-29 clients`, etc., for those who want numeric addresses (see `johnny-decimal`).
- **Document platform**: the same folders inside a hosted document system with permissions.

## Adoption checklist

- [ ] Each business or legal entity has its own root with a README.
- [ ] Every client has one folder with proposals, signed contracts, sent deliverables, and notes.
- [ ] Signed and sent copies are preserved with dates in their names.
- [ ] Invoice numbers are sequential, and invoices are never edited after issue.
- [ ] `legal/` and `finance/` are access-restricted and included in encrypted, tested backups.
- [ ] Finished clients and years are archived with their original names.

## Real-world projects using this

- **Small-business and freelancer guides** from tax and government agencies (for example the US Small Business Administration and the UK's GOV.UK guidance on keeping records) list the records to retain and for how long.
- **Johnny.Decimal** users publish numbered business-folder structures; see `johnny-decimal`.
- **Accounting software documentation** (for example for QuickBooks, Xero, and GnuCash) describes attaching supporting documents to transactions, which pairs with this layout.

## Migration & references

- **From scattered email and drives:** create the tree, then sweep by client, starting with active clients and signed contracts; leave old material in a dated `archive/legacy-YYYY-MM/` folder and refile only when you need it.
- **From a document platform:** mirror the folder conventions inside it, and export a yearly snapshot into `archive/`.
- **To an accountant's system:** give the `finance/<year>/` folder and a short index; keep your copy.
- **References:**
  - `files/receipts-and-finance/` for expense and receipt naming.
  - `files/scanned-documents/` for scanning paper contracts.
  - `files/backup-3-2-1-layout/` for backups and restore tests.
  - `principles/iso-date-formats/`, `principles/versioning-in-paths/` for names.
  - `files/workspace-root-layout/` for where `business/` sits.
