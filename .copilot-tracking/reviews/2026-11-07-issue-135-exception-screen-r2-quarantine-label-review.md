---
title: Issue 135 exception screen r2 quarantine label correction review
ms.date: 2026-11-07
---

* Review executed once by the implementing agent after implementation (author review, not independent). Scope: the r2 diff against `26ce7c7`. Web Interface Guidelines re-fetched before this Review (HTTP 200, identical to the pre-edit fetch).
* Outcome: conformant for the r2 correction, with the open items below. This does not replace or resolve the original Review (F1 to F6), which is unchanged.

## Guideline findings (file:line)

* `role-screens.js:876-879`: no new element, so semantics, focus and the labelled table region are unchanged. Wording is plain text through `h()`, never HTML. No finding.
* `test_exception_register_screen.py:24-47`: synthetic data only. No finding.

## Findings

* R2-1 (Medium, open): F1 is not closed. Only the unit regression has run. The real-DOM story (conflicts, denial, 500, malformed, not JSON, network clearing, stale navigation, keyboard, narrow reflow) must be run on the frozen head.
* R2-2 (Low, recorded): `status.toLowerCase()` also accepts values such as `QUARANTINED`. It is intentionally lenient, only for the quarantine label, and no other status is normalised.
* R2-3 (Low, recorded): a returned non-quarantined failed-AI item with a reason is still labelled a fallback. That follows the feed contract (fallback requires a reason) but is inferred, not returned as a field.
* R2-4 (Info): the r1 helper expectation error (2 versus 3 failed-AI rows) is not a source defect and is preserved separately.
* Unchanged open items: F3 to F6, human and assistive-technology acceptance (#151/#155), actual staff naming and runbooks, producers and durable recovery.
