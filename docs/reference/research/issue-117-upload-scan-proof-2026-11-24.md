---
title: Issue 117 upload scan gate proof (2026-11-24)
description: Evidence that uploads are scanned before availability on main and on the live demo API, with a per-criterion table
ms.date: 2026-11-24
---

Scope: the synthetic demo only. Refs #117. No source change was needed.

## Finding

The gate is already on main. `DocControlsMixin.scan_new_document` runs inside the upload transaction in `Store.add_document` (`src/core/src/zava_forward/core/store.py`, around line 1732), and the scan record is stored on the document. A document is available only when its status is `clean` (`is_clean_document` and `require_clean` in `src/core/src/zava_forward/core/doc_controls.py`). `read_document` and the download path call `ensure_scanned` then `require_clean`, so a pending or unknown result blocks use, a missing scanner fails closed, and an infected or mismatched file is deleted and never recorded.

## Local test evidence (run 2026-11-24 in the issue worktree, sequentially)

* `src/core`: `python3 -m unittest tests.test_document_rescan tests.test_documents tests.test_resident_documents` ran 59 tests, OK, 20 skipped (SQL-backed variants that need a database).
* `src/api`: `python3 -m unittest tests.test_document_controls` ran 23 tests, OK. It includes the clean upload, infected, mismatched and EICAR refusals, the pending Defender result blocking until clean, rescan on read and by job, and quarantine blocking download and derivative use.

## Live demo evidence (2026-11-24, `ca-cutover-test-demo-api`)

Configuration read with the Azure CLI (no secrets): `ZF_DOC_STORE=azure-blob`, `ZF_SCANNER=defender`; subscription plan `StorageAccounts` is Standard with `OnUploadMalwareScanning` enabled; the storage account `stcutovertestrzsrg` has on-upload malware scanning on (cap 10000 GB per month).

A signed-in Playwright session (credentials read at runtime, never printed) uploaded a synthetic EICAR text file and a synthetic clean PDF to case ZF-2025-0148 through `/api/cases/{id}/upload`. Script and raw output: [live_scan_proof.py](evidence/issue-117/live_scan_proof.py), [live-run-output.txt](evidence/issue-117/live-run-output.txt), screenshot [live-workbench.png](evidence/issue-117/live-workbench.png).

| Step | Observed |
| --- | --- |
| Both uploads, immediately | Accepted with scan status `pending` by `defender-for-storage`; not yet available |
| Read of the EICAR file | 400 "That file failed the content check and was removed." Defender flagged it, the record and blob were removed |
| Read of the clean file | Rescan on first use returned `clean` ("No threats found"); the read then succeeded |
| Later rescan of the EICAR file | 404 case document gone, which confirms removal |
| Second read of the clean file | 500 `ProgrammingError` on the SQL path (see open item) |

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Uploads are scanned before availability | Proven for the demo | Code path above, 59 core and 23 API passing tests, and the live run: uploads start `pending`, are unavailable until Defender returns `clean`, and a malicious result removes the document |
| Retention job lists records past trigger and needs owner approval; legal hold blocks deletion | Already ticked; not re-proven here | The retention and legal hold tests sit in `test_document_controls.py` (23 passing) |

Limits: the local scanner is a synthetic signature check, not an antivirus engine. The live proof used Defender for Storage on a demo account; production scanning, tuning and the DPO and Legal retention schedule are outside the demo.

## Open item

The second read of an already clean document returned HTTP 500 (`ProgrammingError`, `exceptions.py` frame, no traceback in the container log tail) on the live SQL-backed app. The first read worked, so the scan gate is not implicated, but the cause is unknown and was not investigated or fixed here. It needs its own issue. The clean synthetic PDF (`synthetic117-clean.pdf`) remains on the demo case; the app exposes no delete route for it, and retention approval needs a due date, so it was left in place as demo data.

## Recommendation

Tick "Uploads are scanned before availability" on #117 for the demo, citing this note, and open a follow-up for the 500.
