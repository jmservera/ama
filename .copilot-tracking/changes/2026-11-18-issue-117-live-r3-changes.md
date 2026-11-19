# Issue 117 live r3 changes (2026-11-18)

Tier: FOCUSED, docs and evidence only. Classification basis: no `src/`, workflow, dependency, Dockerfile, SQL or infrastructure edit; no Azure resource created or changed.

## Files

* `docs/reference/research/issue-117-live-r3-closure-2026-11-18.md` and `issue-117-live-r3-raw/` (new)
* `docs/reference/README.md` (issue 117 paragraph), `docs/reference/log.md` (entry)
* `.copilot-tracking/` research, plan, details, critique, changes, review, state and `evidence/2026-11-18/issue-117-live-r3/`

## Per-criterion table

| Criterion | Proven | Unproven or excluded |
| --- | --- | --- |
| Uploads are scanned before availability | Source order (scan before record append); 64 offline tests OK; live synthetic marker upload refused (HTTP 400), live type mismatch refused (HTTP 400), document list 5 before and 5 after; Defender malware scanning on upload enabled on the demo account | Real malware engine guarding the app path: `ZF_SCANNER` unset on `ca-cutover-test-demo-api`, changing it was not authorised; account firewall `Deny` blocks a direct test blob |
| Retention job lists records past trigger and needs owner approval; legal hold blocks deletion (already ticked) | `/api/retention` HTTP 200 with the placeholder label | Live legal hold and approved deletion not exercised (state-changing). Production-only: DPO and Legal approved periods (PR-003, OD-14), immutability lock |

## Validation

* `cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests.test_document_controls`: 18 tests OK
* `cd src/core && PYTHONPATH=src:tests:../agents/src python3 -m unittest tests.test_document_rescan tests.test_resident_documents`: 46 tests OK, 20 skipped
* Live probe and read-only `az` settings: raw files in the research raw folder. Not run: mypy, ruff, `rpi-checks.py` (no source change).
* Not satisfied: hosted CI, independent exact-head review and human approval remain with the coordinator and owner.
