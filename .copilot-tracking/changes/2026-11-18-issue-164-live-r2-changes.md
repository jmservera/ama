---
title: Issue 164 live changes, second pass
description: Changes record and per-criterion proven/unproven table (Refs #164)
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only. Tier FOCUSED; no source change; `rpi-checks.py --all` not run. Existing `issue-164-live-state.json` and first-pass artifacts preserved.

## Changes

* Added `docs/reference/research/issue-164-live-chat-grounding-evidence-r2-2026-11-18.md`.
* Added an index row in `docs/reference/README.md` and a log entry in `docs/reference/log.md`.
* Added evidence under `.copilot-tracking/evidence/2026-11-18/issue-164-live-r2/` (driver, raw JSON, eight labelled screenshots, registry read, Azure read, offline test output).
* Added dated research, plan, details, critique, changes, review and `issue-164-live-r2-state.json`.

## Per-criterion table

| # | Unticked criterion | Result | Basis |
| --- | --- | --- | --- |
| 1 | Thresholds approved; chat task registered with accountable reviewer and enable/disable state | Partly proven | Registration and disabled state proven live; thresholds still `proposed`, accountable individual unknown |
| 2 | Results bound to serving-model and control versions with approved thresholds and outcomes | Partly proven | Versions recorded; no actual-model chat result (0 model calls) so nothing to bind |
| 3 | Competent human exercises block seeded critical suggestions | Unproven | Needs authorised competent people; not waived |
| 4 | Actual calls need approved handling and finite authority; human exercises need approvals | Partly proven | No call made, no spend; caps are "not spend authorization"; handling and consent approvals absent |
| 5 | Criteria do not authorise implementation, memory, calls, deployment or live use | Consistent | No breach observed; negative constraint |

## Validation

* Offline: from `src/agents`, `PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest tests.test_chat_heldout tests.test_chat_eval_revocation_effort tests.test_epic104_bounded_ai_invariants -v`: 54 tests OK.
* Live: 7 asks, all HTTP 200, 0 model calls, thread created and deleted (200). Azure CLI read-only.
* Documentation link and diff review. mypy, ruff and web tests not applicable (no source or web file changed).
* Not run: hosted CI, independent review, `rpi-checks.py --all`.
