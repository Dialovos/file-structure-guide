# Topic vs date organisation — comparison template

Three side-by-side layouts so you can see the trade-offs concretely:

- `topic-only/` — pure topic-driven (no date layer).
- `date-only/` — pure date-driven (no topical layer).
- `mixed/` — intentional mix with two non-overlapping layers (`daily/` + `topics/`).

The accidental-mix variant is intentionally *not* shown — it's the anti-pattern this guide warns against.

## Decision pros/cons

| Approach | Pros | Cons | Best for |
| --- | --- | --- | --- |
| **Topic-driven** | Direct retrieval by subject. Notes compound over years. Long-form output benefits. | No place for fleeting capture. Every note demands a curated title up front. | Researchers, essayists, technical leaders. Reference vaults. |
| **Date-driven** | Zero-friction capture. Filename is automatic. Pairs naturally with journalling. | No topical compounding without backlink-savvy tooling. Hard to find a claim across years. | Journalers, Bullet Journal converts. Roam/Logseq users. |
| **Intentional mix** | Captures both modes. Daily layer for fleeting, topical layer for durable. | Two folder structures to maintain. Requires a rule for which note goes where. | Most personal knowledge work. PARA, LYT, ACCESS users. |
| **Accidental mix** *(anti-pattern)* | None — listed only as a warning. | Files named both ways with no rule. Orientation breaks. Notes split between layers. | Avoid. Pick a rule and write it down. |

## How to choose

1. **Do you journal?** If yes, you need a date layer. Either pure-date (Roam/Logseq style) or intentional-mix.
2. **Do your notes feed long-form output?** If yes, you need a topical layer. Either pure-topic or intentional-mix.
3. **Both?** Use intentional-mix. This is the recommended default.
4. **Neither, just reference?** Pure-topic, with folders by domain.

## To adopt this template

1. Pick your approach by reading `GUIDE.md` and the table above.
2. Copy the relevant sub-folder out of `template/`:
   - Pure topic: `cp -r template/topic-only/ ~/vault/`
   - Pure date: `cp -r template/date-only/ ~/vault/`
   - Intentional mix: `cp -r template/mixed/ ~/vault/` (rename `mixed/` → vault root contents).
3. Replace example notes with real content.
4. Write your rule down (e.g. "fleeting → daily/, durable → topics/") and stick to it.

## What to rename or remove

- All example notes are placeholders — replace or delete.
- Remove this `README.md` once you've picked an approach; the verifier needs it only while it lives in this repo.

## Verifier

`docs/superpowers/scripts/verify-guideline.sh notes/topic-vs-date-organization` checks that this README, `GUIDE.md`, `tree.md`, and the `template/` directory all exist with the required sections.
