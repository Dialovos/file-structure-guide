# Anti-patterns

Cross-cutting bad habits. Each violates one or more of the seven values in [PHILOSOPHY.md](PHILOSOPHY.md).

## 1. The kitchen-sink directory

`utils/`, `misc/`, `stuff/`, `helpers/`. A dir whose name doesn't tell you what's in it is a junk drawer. Junk drawers grow.

**Fix:** name by purpose, not "everything that didn't fit." Three small purpose-named dirs beat one `utils/`. See [`principles/naming-by-purpose-not-type/`](principles/naming-by-purpose-not-type/).

## 2. Nesting deeper than 4 levels

`src/main/components/forms/inputs/text/numeric/` is a sign the layout has lost the plot. Each level adds a click and a working-memory slot.

**Fix:** flatten by purpose-naming or by extracting subtrees into peer dirs. See [`principles/depth-vs-breadth/`](principles/depth-vs-breadth/).

## 3. Mixed concerns at one level

A dir containing source code, CI logs, and personal scratch files. Clean and gitignored content tangle.

**Fix:** separate by stability (daily vs yearly). See [`principles/stable-vs-volatile-separation/`](principles/stable-vs-volatile-separation/).

## 4. Date-stamps as status

`old-2024/`, `final-final/`, `backup-2025-01/`. Status encoded into names instead of structure.

**Fix:** use an `archive/` dir for sunset content; let git history serve "old". See [`principles/status-based-organization/`](principles/status-based-organization/).

## 5. Cryptic abbreviations

`prj-mgmt-v2-final/`. Abbreviations save typing once but cost reading forever.

**Fix:** use full words. Editors autocomplete. See [`principles/naming-conventions/`](principles/naming-conventions/).

## 6. Inconsistent casing within one tree

`Documents/` next to `notes/` next to `Old_Stuff/`. The eye can't lock onto a pattern, so every lookup is a search.

**Fix:** pick a casing rule and apply it everywhere; document it in your repo's `CONTRIBUTING.md`. See [`principles/capitalization-policy/`](principles/capitalization-policy/).

## 7. README absent at navigation points

A user lands on a directory and has to grep its files to know what they're looking at.

**Fix:** every directory a stranger might enter gets a `README.md` — even a 5-line one. See [`principles/readme-placement/`](principles/readme-placement/).

## 8. Versioning via `_v2` suffix

`config_v2.yaml` beside `config_v3.yaml` beside `config_old.yaml`. The filesystem becomes a bad version-control system.

**Fix:** keep one canonical name; let git tags carry version. See [`principles/versioning-in-paths/`](principles/versioning-in-paths/).

## 9. "TBD" / "temp" / "new" dirs that outlive their purpose

`temp/` for "I'll move this in a minute" — five years later it has 4 GB.

**Fix:** if it's worth keeping, give it a real name now. If it's not, delete it. Never let provisional names persist past a sprint.

## 10. Hidden state in non-hidden files

A non-dotfile holding your auth token. Hiding by convention only.

**Fix:** secrets in dotfile-named files (`.env.local`) explicitly listed in `.gitignore`. See [`principles/hidden-files-policy/`](principles/hidden-files-policy/).

---

*Phase 7 of the build will append 3–5 more anti-patterns surfaced while writing the 79 guidelines.*
