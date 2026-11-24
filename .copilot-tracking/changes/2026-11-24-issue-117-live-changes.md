# Changes 2026-11-24 issue 117 live

Tier: focused. No `src/` change; the gate already exists on main.

## Files

* `docs/reference/research/issue-117-upload-scan-proof-2026-11-24.md` (new)
* `docs/reference/research/evidence/issue-117/` (script, raw output, screenshot)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (entry)

## Validation run

* `src/core` document tests: 59 OK, 20 skipped. `src/api` `test_document_controls`: 23 OK.
* Live demo upload run recorded in the evidence folder. Hosted CI for this local commit not observed; nothing was pushed.
* Not run: `rpi-checks.py` (no src change), SQL variants of the tests (skipped without a database).

## Per-criterion table

| Criterion | Verdict | Evidence |
| --- | --- | --- |
| Uploads are scanned before availability | Proven (demo) | Code path, passing tests, live Defender run: pending until clean, malicious removed |
| Retention job lists records past trigger and needs owner approval; legal hold blocks deletion | Already ticked; not re-proven | Existing tests in `test_document_controls.py` pass |

Open: HTTP 500 on a second read of a clean document on the live SQL app (cause unknown); throwaway `synthetic117-clean.pdf` left on case ZF-2025-0148 (no delete route).
