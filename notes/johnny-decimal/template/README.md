# Johnny Decimal template

A bare JD vault skeleton: the system area with its index, plus stub `life/` and `work/` areas to start filing into. Demonstrates the canonical naming (`XX-YY area/`, `NN category/`, `NN.MM item.ext`) without prescribing what your real categories should be.

## What's here

- `00-09 system/00 index/.gitkeep` — placeholder for the system area; replace with the maintained `00.00 index.md` once you've copied `INDEX.md` over.
- `10-19 life/.gitkeep` — empty life area; add your real categories (`11 home/`, `12 health/`, etc.) here.
- `20-29 work/.gitkeep` — empty work area; add your client / employer / project categories here.
- `INDEX.md` — the canonical Johnny Decimal index showing how to lay out the area / category / item table. Move this to `00-09 system/00 index/00.00 index.md` once you adopt the template.
- `README.md` — this file.

## To adopt this template

1. Copy `template/` into your vault root:
   ```bash
   cp -r template/ ~/jd-vault/
   cd ~/jd-vault
   ```
2. Move the index into place and rename to the canonical filename:
   ```bash
   mv INDEX.md "00-09 system/00 index/00.00 index.md"
   ```
3. Delete the three `.gitkeep` placeholders as you start adding real categories.
4. Add your first category folders (`10-19 life/11 home/`, `20-29 work/21 client-a/`) and add the matching rows to the index.
5. Start filing items as `NN.MM short-name.ext` inside the right category.

## What to rename or remove

- The system area (`00-09 system/`) and its index folder are non-negotiable; everything else is example.
- The `10-19 life` and `20-29 work` area names are placeholders. Pick whatever top-level slices match how you actually divide the world.
- The category stubs (`11 home/`, `21 client-a/`) are examples; replace with your own.
- Remove this `README.md` once the template is in use; the verifier needs it only while it lives in this repo.

## Verifier

`docs/superpowers/scripts/verify-guideline.sh notes/johnny-decimal` checks that this README, `GUIDE.md`, `tree.md`, and the `template/` directory all exist with the required sections.
