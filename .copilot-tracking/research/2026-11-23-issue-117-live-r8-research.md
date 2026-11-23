# Issue 117 research, 2026-11-23

Refs #117. Synthetic demo, desktop only. Research disposition: executed (reuses the 2026-11-19 live notes as evidence). Planning Readiness: Ready.

## Unticked criteria

* Uploads are scanned before availability (the only one; retention and legal hold is ticked).

## Evidence

* [Sixth pass](../../docs/reference/research/issue-117-live-r7-2026-11-19.md) and [fifth pass](../../docs/reference/research/issue-117-live-r6-2026-11-19.md): Defender for Storage is enabled on `stcutovertestrzsrg`; the demo API sets no `ZF_SCANNER`; a direct blob probe was refused by storage network rules; enabling `ZF_SCANNER=defender` is a deployment change outside the brief ("do not change the Azure estate unless the goal says so").
* `src/core/src/zava_forward/core/doc_controls.py`: `DefenderForStorageScanner`, `open_scanner`, `blob_tags`.
* Existing tests cover order of operations, pending, malicious and tag-value fall-backs (`src/api/tests/test_document_controls.py`, `src/core/tests/test_document_rescan.py`).
* Coverage gap found by grep: nothing tests `blob_tags` itself (non-200 response, unreadable XML, real XML round trip) or the `open_scanner` configuration errors (`ZF_SCANNER=defender` without an Azure blob store, unknown value). These are the fail-closed edges of the scan-before-availability control.

## Selected work

Add focused tests for those edges in `src/core/tests/test_document_rescan.py`. No source change expected; Focused tier.
