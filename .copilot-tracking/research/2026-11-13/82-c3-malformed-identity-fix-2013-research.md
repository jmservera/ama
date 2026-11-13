---
title: 82-c3 malformed identity fix research
ms.date: 2026-11-13
---

Research disposition: executed. Planning Readiness: Ready.

## Findings

* F1: `grants._complete` ends with `isinstance(identity.get("oid") or "", str)`, so falsey non-string `oid` (`0`, `False`, `[]`, `{}`, `0.0`) becomes `""` and passes. Required: `oid` is `None` or `str`.
* F2: `finance._norm` is `(s or "").strip().lower()`: a truthy non-string raises `AttributeError`. `finance._independent` is called by `_grant_approve` via `_fin_independent` before `grant_eligibility_verdict`, and by every finance sign-off action (budget, commitment, invoice receive/decide/payment). `_independent` is also re-run in `validate_sql`.
* `finance._independent` raises `PermissionError` for unknown identity; callers expect `PermissionError`/`ValueError` refusals. The fix keeps that contract: non-string identity values are treated as an unknown identity (refusal), never `AttributeError`.
* `grants._same_person` uses its own isinstance-safe `_norm`, so a non-string `email`/`code` is ignored for matching, only `_complete` rejects it.
* `gates.py`: `evidence_gate`, `quality_gate`, `booking_gates` iterate `list(...)` of items; a non-string item is joined with `", ".join` (TypeError) on FAIL, or `[""]`/`[None]` reads as a gap with an empty reason. `GateResult.__post_init__` raises on blank/non-string reason (`.strip()` AttributeError for non-str); `capacity_gate`, `eligibility_gate`, `authority_gate`, `finance_gate` pass caller reasons straight through, so an empty or non-string reason raises instead of returning unknown/fail. `booking_gates` `resident_reasons` containing items is fine, but a non-iterable raises.
* No `finance_signoff_gate` function exists; the sign-off gate is `finance_action` + `_independent`, covered by `test_finance_signoffs.py`.

## Evidence

* `src/core/src/zava_forward/core/grants.py` lines 100-125, 165-185.
* `src/core/src/zava_forward/core/finance.py` lines 36-58, 182-186.
* `src/core/src/zava_forward/core/gates.py` gate functions.
* Existing tests: `test_grant_lifecycle_controls.py::test_malformed_identity_fields_return_unknown_not_error` (truthy only), `test_gates.py`.
* The named review file `82-c2-closure-review-1953-review.md` is not in the worktree; findings taken from the owner prompt.
