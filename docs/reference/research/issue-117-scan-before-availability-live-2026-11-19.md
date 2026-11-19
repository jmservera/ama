---
title: Issue 117 uploads scanned before availability (demo)
description: Evidence for the one unticked criterion of issue 117, with the part that is unproven for the demo
ms.date: 2026-11-19
---

Scope: the synthetic demo, desktop only. Source read at branch `test/code-live-20261119T154344Z` (base 7ea3a1ff6).

## Criterion

"Uploads are scanned before availability" (issue 117, unticked).

## Mechanism in source

* `Store.add_document` (`src/core/src/zava_forward/core/store.py`) writes the blob, then calls `scan_new_document` before the record is appended. An `infected` or `mismatch` verdict deletes the blob and raises, so no record exists.
* A `pending` verdict is stored on the record. `is_available_case_document`, `is_clean_upload` and `require_clean` (`doc_controls.py`) treat anything other than `clean` as unavailable and fail closed on missing or malformed scan data.
* `ZF_SCANNER=defender` reads the Defender for Storage blob index tag; an unwritten tag stays `pending` until `rescan_document` sees a clean tag.

## Commands run and results

| Command | Result |
| --- | --- |
| `src/api`: `python3 -m unittest tests.test_document_controls -q` (with the documented `PYTHONPATH`) | 19 tests, OK |
| `src/core`: `PYTHONPATH=src:tests python3 -m unittest tests.test_document_rescan tests.test_documents -q` | 50 tests, OK (20 MSSQL cases skipped, no SQL Server) |

Relevant cases: `test_standard_eicar_file_is_refused_and_not_kept`, `test_unscanned_document_is_blocked_while_scan_pending`, `test_pending_defender_scan_blocks_until_clean`, `test_failed_verdict_stays_quarantined_until_manual_rescan_persists_clean`.

## Finding

The scan-before-availability mechanism is built and tested for the demo, so no source change was needed. The criterion stays unticked because the demo app (`ca-cutover-test-demo-api`) has no `ZF_SCANNER` setting in its environment variable names, so it uses the synthetic local signature scanner (marker, EICAR and magic-byte checks), which the code itself says gives no malware assurance on Azure Blob. A real engine needs Defender for Storage on the storage account, a subscription-level change excluded by the "no production changes" boundary. No live upload was attempted: the app is not changed and the unit tests already exercise the same code path.
