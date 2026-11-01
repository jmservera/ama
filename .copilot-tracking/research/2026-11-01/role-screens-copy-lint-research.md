---
title: Role-screens copy lint research
---

Research disposition: executed (direct). Planning Readiness: Ready.

* Failure: `tests/test_content_standard.py::CopyAudit::test_no_internal_terms_in_web_copy` reports 16 lines in `role-screens.js` containing banned terms (hold, holds, provenance).
* Standard: `docs/reference/research/ux/content-standard.md` maps internal terms to plain words; "pause" and "source" are the replacements.
* Constraints: keep data field names (`h.hold`, `inv.hold`, `decision_holds`, `q.on_hold`). `decision_holds` and `on_hold` do not match `\bholds?\b`, so need no allowance.
* Follow-ups: none beyond the fix.
