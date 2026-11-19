# Changes: issue-96-live-r3

Planned: add `docs/reference/research/issue-96-live-r3-reverification-2026-11-18.md`, update the index and log. No source change. Tier FOCUSED.

## Per-criterion table

| Criterion in #96 | Status | Evidence |
| --- | --- | --- |
| Each assisted form has an approved versioned schema | Unproven; cannot be proven for the demo | Live `/api/form-schemas` returns `{"schemas": []}`; no code path writes `Approved`; approval needs a named human and evidence (production, #1905 to #1908) |
| Candidate values carry raw value, source ID, document hash and locator (ticked) | Offline only | `core-tests.txt`, 79 tests OK |
| Accept, correct or reject per field (ticked) | Offline only | same |
| Field-specific validation (ticked) | Offline only | same |
| Reviewed export never submits (ticked) | Offline only | same |
| Dependent-only stale marking (ticked) | Offline only | same |

## Files changed

* `docs/reference/research/issue-96-live-r3-reverification-2026-11-18.md` (new)
* `docs/reference/README.md` (index sentence), `docs/reference/log.md` (entry)
* `.copilot-tracking/{research,critiques,plans,details,changes,reviews,evidence}/2026-11-18/issue-96-live-r3*` and the session state

## Validation (FOCUSED)

* Live read-only probe: schemas 0, CSV empty.
* 79 core tests OK (`core-tests.txt`). Relative links checked by file existence. No src change, so mypy, ruff and rpi-checks were not applicable.
* Witness: first `implement-start` was refused (verbatim reason: "missing persisted artifact evidence: changes") because the state lacked the changes pointer; after adding it the call succeeded with the qualification that source was already dirty. Nothing else was refused.
