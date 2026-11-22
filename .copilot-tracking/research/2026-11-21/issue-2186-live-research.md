# Research: issue 2186 docs-only main moves and full receipts

Disposition: executed. Planning Readiness: Ready. Findings are in docs/reference/research/issue-2186-live-full-receipt-docs-move-2026-11-21.md.

* Head dd8df9631a: base_relaxation exists but validate_receipt only relaxes partial receipts; full receipts raise "Reviewed base differs".
* Verify already prints a BASE RELAXED line; code/tool/image changes already invalidate via moved_path_blocker and identity digests.
* Real defect: criterion 1 (full receipts) is unmet.
