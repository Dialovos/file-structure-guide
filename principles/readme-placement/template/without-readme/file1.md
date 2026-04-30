# Example document in a directory without a README

This directory deliberately omits a `README.md`. The omission is OK because:

1. The directory's purpose is obvious from its name (`without-readme/` is the
   counter-example slot in this template; in a real repo, think `migrations/`
   or `fixtures/` where the naming pattern speaks for itself).
2. It contains a single self-describing file. Adding a README would mostly
   restate the file's own header.
3. There are no naming or contribution conventions a contributor would need
   to know before adding a sibling.

If any of those three reasons stop being true — the directory grows, the
purpose stops being obvious, or contribution rules emerge — promote it to a
junction by adding a `README.md` at that point.
