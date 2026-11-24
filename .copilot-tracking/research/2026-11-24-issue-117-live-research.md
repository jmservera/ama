# Research 2026-11-24 issue 117 live

Task: prove "Uploads are scanned before availability" on main, or add the missing gate.

* Disposition: executed. Planning Readiness: Ready.
* Finding: the gate exists (`store.add_document` -> `scan_new_document`; `read_document` and download -> `ensure_scanned` + `require_clean`). Infected or mismatched content is deleted and never recorded; pending is unavailable; no scanner fails closed.
* Tests: core 59 OK (20 skipped), api `test_document_controls` 23 OK.
* Live: `ca-cutover-test-demo-api` runs `ZF_SCANNER=defender` with Defender on-upload scanning enabled; EICAR and clean uploads start `pending`, EICAR is removed on rescan, clean passes.
* Open: HTTP 500 on a second read of a clean document (SQL `ProgrammingError`), unrelated to the gate.
* Full evidence: [research note](../../docs/reference/research/issue-117-upload-scan-proof-2026-11-24.md).
* Decision: no src change; focused tier.
