# Review: issue #176 generator determinism and manifest fields

* Date: 2026-11-14
* Review execution: executed once, self-review of the final diff (test-only)
* Outcome: conformant for the in-repo generators; no material findings open

## Acceptance criteria

* AC1 byte-identical output for same seed and as-of: proven for stock register, sensor backfill, sensor scenarios, sensor stream, stock fabric, scale fixture (matrix test across hash seeds with clock/uuid banned; existing audit also covers public-pack and stock-epc).
* AC2 manifests record seed, version, generator revision: asserted for every generator in `determinism_audit.GENERATORS`.
* AC3 (refresh policy) was already ticked.

## Caveats

* The original private 60,000-home register generator is not in the repository; the audit reports it unavailable. The criterion is proven for the fictional in-repo register only. The owner may prefer `Refs #176`; `Closes #176` is justified if the criterion is read as in-repo generators.
* Full `src/core` discovery was not run locally; hosted CI is the remaining check. Human review and approval remain required.

## Follow-ups

* Optional: make `resident_preview_fixture` use a fixed as-of instead of `_today()` (in-memory fixture, low value).
* Optional: add the matrix to the hosted core workflow if it is path-filtered.
