# Scanned-documents template

A skeleton showing the year-month directory structure plus one example filename in the `YYYY-MM-DD - source - description.pdf` form.

## What's here

- `2026/2026-04/2026-04-30 - example-source - example.pdf` — a zero-byte placeholder demonstrating the canonical filename. The triple `<date> - <source> - <description>` is the entire indexing scheme; everything depends on the order and the space-dash-space separators.

The placeholder is intentionally empty — it exists to demonstrate the path and filename shape, not to open in a PDF reader.

## To adopt this template

1. Copy the structure into your archive root: `cp -r template/ ~/scans/` or `cp -r template/ /mnt/archive/scans/`.
2. As scans arrive, OCR them first (`ocrmypdf input.pdf output.pdf`) so the PDFs are full-text searchable.
3. File each scan as `<doc-date> - <source-slug> - <short-description>.pdf` inside the matching year/month directory.
4. Add new month directories (`2026-05/`, `2026-06/`) as the year progresses; pre-creating them is unnecessary.
5. If you use paperless-ngx, point its `CONSUMPTION_DIR` at an inbox and let it rename + file; the resulting layout will mirror this template.

## What to rename or remove

- Delete the `2026-04-30 - example-source - example.pdf` placeholder once you have a real PDF in that month — it serves only as a shape demo.
- Add new year directories as needed (`2025/`, `2027/`); the template only ships one to keep the demo small.
- Drop this `README.md` once the template has been adapted (the verifier requires it while it lives in the repo).

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires `template/README.md` to exist. Keep it in place until the template is no longer needed.

## OCR before filing

A scan that is not OCR'd is image-only and cannot be searched. Always run OCR — `ocrmypdf` (open source) is the simplest path, paperless-ngx does it as part of ingestion. The directory layout is the index of *last resort*; OCR is the index of *first resort*.

## Document date vs scan date

The date in the filename is the *document date* (when the bill was issued, when the appointment occurred), not the date you scanned it. If the document genuinely has no date, use the scan date and append a `~` marker — `2026-04-30~ - source - description.pdf` — to flag the inferred date for your future self.
