# Principles

Sixteen cross-cutting principles that thread every other guideline in this repo. When two layout guides disagree, the resolution usually lives here.

These are deliberately narrow — each principle owns one decision so it can be cited without ambiguity.

## The 16 principles

1. [`naming-conventions/`](naming-conventions/) — kebab-case default, ecosystem-mandated exceptions
2. [`iso-date-formats/`](iso-date-formats/) — `YYYY-MM-DD` everywhere
3. [`depth-vs-breadth/`](depth-vs-breadth/) — when to flatten, when to nest
4. [`readme-placement/`](readme-placement/) — every navigational point gets one
5. [`status-based-organization/`](status-based-organization/) — `active/` vs `archive/` vs `someday/`
6. [`versioning-in-paths/`](versioning-in-paths/) — never; use git tags
7. [`indexes-and-mocs/`](indexes-and-mocs/) — when to add an `INDEX.md` or MOC
8. [`gitignore-and-keep-files/`](gitignore-and-keep-files/) — `.gitignore` patterns and `.gitkeep` discipline
9. [`one-purpose-per-directory/`](one-purpose-per-directory/) — anti-junk-drawer rule
10. [`stable-vs-volatile-separation/`](stable-vs-volatile-separation/) — daily vs yearly content
11. [`naming-by-purpose-not-type/`](naming-by-purpose-not-type/) — `customer-onboarding/` over `forms/`
12. [`capitalization-policy/`](capitalization-policy/) — UPPERCASE only for canonical files
13. [`hidden-files-policy/`](hidden-files-policy/) — when to use a leading dot
14. [`test-colocation-vs-separation/`](test-colocation-vs-separation/) — `tests/` dir vs co-located
15. [`generated-vs-source-separation/`](generated-vs-source-separation/) — `dist/`, `build/`, `target/` discipline
16. [`file-size-as-split-signal/`](file-size-as-split-signal/) — when a file becomes a directory

## How to use this category

Open a principle's `GUIDE.md` to read the rule, the rationale, and concrete cases. Most principles also include a `template/` showing a tiny example tree the principle endorses.
