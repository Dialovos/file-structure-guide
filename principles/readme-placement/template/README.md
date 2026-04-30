# README placement template

Demonstrates the "navigational points get READMEs" rule by example. This file
itself is doing double duty: it's the template's own usage doc *and* an
illustration of a junction README — exactly the role the principle endorses.

## What's here

- `with-readme/` — a small dir with a `README.md` and one content file. This is what a junction looks like: short README that orients the reader.
- `without-readme/` — a small dir with no `README.md`, just one content file whose own header explains why a README would be redundant. The rationale is captured in that file's body so the omission is intentional, not accidental.

## To adopt this template

1. Copy the relevant subtree into your repo: `cp -r template/with-readme/ <your-target>/billing/`.
2. Rename the directory to your real concept (e.g. `with-readme/` → `billing/`).
3. Edit the new `billing/README.md` to answer three questions in five lines or fewer:
   - **What's here** — one line.
   - **How it's organised** — one line about naming or layout conventions.
   - **Where to next** — one or two links to parent or sibling.
4. Decide whether each sub-directory needs its own README. Use the heuristic from `GUIDE.md`: if you couldn't add anything beyond the directory name without padding, don't add the file.
5. Delete `without-readme/` if your real subtree has no analogous case. Keep it if you want a documented reminder of when *not* to add a README.

## Adopting in an existing repo

Audit script (also in `GUIDE.md`):

```bash
find . -type d -not -path './.git/*' | while read d; do
  count=$(find "$d" -maxdepth 1 -mindepth 1 | wc -l)
  if [[ $count -gt 1 && ! -f "$d/README.md" ]]; then
    echo "missing: $d"
  fi
done
```

Triage the output by hand. Not every hit needs a README — but every hit deserves a deliberate decision.

## Verifier check

`docs/superpowers/scripts/verify-guideline.sh` requires this file to exist. Don't delete it before replacing.
