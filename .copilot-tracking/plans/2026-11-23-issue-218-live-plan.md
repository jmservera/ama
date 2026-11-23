# Plan and critique: issue 218 live (2026-11-23)

## Findings driving the plan

* Live revision 0000055 `GET /api/governance` and `/api/assistants`: `rai_exercise_acceptance` is `failed` only because `requirement_traceability_complete` is false while its own detail says 15 of 15 trace. Cause: the image ships `src/*/src` only, so `_scan_traceability_targets` cannot find `src/core/tests/*.py` ("test file does not exist"). Real defect (false failure, misleading detail). Offline the check passes.
* `/api/ai/report` returned 503 `sql-write-lock-busy` (shared demo app contention from other workers). Not a 218 defect; recorded, retried.
* #440 and child #220/#223 remain owner or human gated.

## Steps

1. `rai_control_plane`: add `test_tree_present` to `verify_traceability_targets`; `traceability_summary` reports `target_verification` (`verified`, `unresolved`, `test_tree_not_shipped`) and treats a deployment without any test tree as structurally complete only when no ID is missing or untraced; unresolved targets with a test tree present still fail closed. Make the check detail state the verification mode.
2. Add focused tests in `src/core/tests/test_rai_control_plane_218.py`.
3. Run targeted core and api tests, mypy, ruff. Tier FULL (src change); no `rpi-checks.py --all`; stays a local commit.
4. Do not redeploy (deployment is a shared-system change with other workers active); live proof of the fix is therefore unproven and recorded as such.
5. Research note with per-criterion table; changes record; review.

## Critique (executed once)

* Risk: treating an absent test tree as pass is fail-open. Mitigation: only when `src/core/tests` is absent; the field `target_verification: test_tree_not_shipped` is surfaced in the payload and detail; CI (repo tree) still verifies targets. Accepted.
* Risk: cached default scan. The new flag is computed outside the lru cache from the root. Accepted.
* Verdict: proceed.
