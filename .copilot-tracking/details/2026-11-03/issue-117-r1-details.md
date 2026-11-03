---
title: Issue 117 round 1 phase details
ms.date: 2026-11-03
---

## Phase 1

* `doc_controls.py`: module logger; `open_scanner` warns for local scanner with `AzureBlobDocumentStore`. Verdict logic untouched, documents stay unavailable until clean.
* `src/api/tests/test_document_controls.py`: `test_synthetic_scanner_on_blob_store_warns_but_stays_fail_closed`.
* `src/api/README.md`: `ZF_SCANNER` row notes the warning.
* No UI change; Fluent 2, WCAG and plain-language items not affected. Manual upload path and AI-unavailable behaviour unchanged.
