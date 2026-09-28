# docs-as-code-site — template

An MkDocs skeleton with the four Diátaxis sections, a strict build, and a starter page in each.

## What to rename

- `site_name` and `repo_url` in `mkdocs.yml`

## What to fill

- Each page under `docs/` — replace the placeholders with real content
- `mkdocs.yml` `nav` — add pages as you write them

## What to delete

- Sections you don't need yet (keep at least tutorials and reference)

## First run

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-docs.txt
mkdocs build --strict
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../../../principles/readme-placement/` — README versus docs
