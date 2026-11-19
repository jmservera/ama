# Changes: issue 117 live. Refs #117.
Files: docs/reference/research/issue-117-live-r5-2026-11-19.md and this RPI trail. No source change; tier FOCUSED.
Validation: api tests.test_document_controls 19 OK; core test_document_rescan and test_resident_documents 46 OK (20 skipped). mypy, ruff and rpi-checks not applicable (no src change).

| Criterion | Status | Basis |
| --- | --- | --- |
| Uploads are scanned before availability | Proven for order of operations and local scanner (marker, EICAR, type mismatch). Unproven: real engine on demo path, live EICAR | Needs owner approval of ZF_SCANNER=defender on ca-cutover-test-demo-api; storage firewall denies this identity |
| Retention listing, owner approval, legal hold | Proven (ticked) | third-pass note |
