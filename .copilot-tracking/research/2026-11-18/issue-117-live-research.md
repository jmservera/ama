---
title: Issue 117 live research
description: Research for unticked criterion "Uploads are scanned before availability" on the demo
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only. Unticked criterion: uploads are scanned before availability. Disposition: executed. Planning Readiness: Ready after evidence capture. Refs #117.

## Findings

* Issue 117 has one unticked criterion: "Uploads are scanned before availability". The retention and legal hold criterion is already ticked and is not re-audited beyond a read of the live queue.
* Source: `src/core/src/zava_forward/core/doc_controls.py` `scan_new_document` runs inside `Store.add_document` after the blob put; infected or mismatched content deletes the blob and raises before a document record exists; `require_clean` blocks reads until the scan is clean; `ZF_SCANNER` selects `local` (synthetic signature) or `defender`.
* Offline: api `test_document_controls` 18 tests OK; core `test_document_rescan` plus `test_resident_documents` 46 tests OK (20 skipped).
* Live (read-only): demo API env sets `ZF_DOC_STORE=azure-blob` and no `ZF_SCANNER`, so the synthetic local scanner guards the live blob store. Defender for Storage on `stcutovertestrzsrg` is disabled (`isEnabled` false). Blob versioning on, soft delete 30 days.
* Live upload path: `POST /api/cases/{id}/upload` with `X-ZF-CSRF: 1`; the synthetic test marker is rejected and never recorded.
* Planning Readiness: Ready.
