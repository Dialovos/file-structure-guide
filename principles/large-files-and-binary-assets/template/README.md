# large-files-and-binary-assets — template

A repository skeleton showing where large assets live and how their pointers and manifest are declared.

## What to rename

- `assets/media/` to your asset directory names

## What to fill

- `.gitattributes` — patterns for large files (remove if you use DVC only)
- `assets/media/media.manifest` — real names, sizes, and `sha256` hashes
- `README.md` — your actual fetch commands

## What to delete

- Asset directories you don't use
- The example manifest lines

## First run

```bash
git lfs install && git lfs pull  # or: dvc pull
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../../generated-vs-source-separation/` — what never to commit
