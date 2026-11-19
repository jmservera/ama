# Changes: EICAR detection in LocalSignatureScanner. Refs #117.

Files: src/core/src/zava_forward/core/doc_controls.py (EICAR_SIGNATURE, scan returns infected, docstring);
src/api/tests/test_document_controls.py (new test: EICAR refused for .txt and .pdf, nothing stored; a fragment stays clean).

## Validation (tier FULL only because src changed; rpi-checks --all not run per owner brief)
* api `tests.test_document_controls`: 19 tests OK. core `test_document_rescan`, `test_resident_documents`: 46 OK, 20 skipped.
* mypy in src/core and src/api (api with PYTHONPATH=../core/src:../agents/src): no issues.
* ruff format --check: not applicable to src (src-ci checks only infra files); the files already failed before the change.
* No Azure resource was created or changed; no live run was needed for this unit-level change.

## Per-criterion table (synthetic demo, desktop only)
| Criterion | Status | Basis |
| --- | --- | --- |
| Uploads are scanned before availability | Proven for the order of operations and the synthetic local scanner (now also the standard EICAR file), offline and live per docs/reference/research/issue-117-live-r3-closure-2026-11-18.md. Unproven: a real engine on the demo app path | Needs owner approval to set ZF_SCANNER=defender on ca-cutover-test-demo-api; demo storage firewall denies this identity |
| Retention job lists records past trigger and needs owner approval; legal hold blocks deletion | Proven (ticked; /api/retention 200 in r3) | r3 note |

Deployed demo still runs the old image until the owner redeploys, so live EICAR refusal is not claimed.
