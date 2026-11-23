---
title: Epic 218 live recheck, RAI readiness and criteria status (2026-11-23)
description: Live read-only probe of the RAI exercise acceptance and real-AI delivery gate, a traceability defect found and fixed, and a per-criterion proven or unproven table for epic 218
author: AMA RPI agent
ms.date: 2026-11-23
ms.topic: reference
---

Refs #218. Synthetic desktop demo under the owner decisions of 2026-11-18. Not resident, production or legal evidence. Evidence: `.copilot-tracking/evidence/2026-11-23/issue-218-live/` (`probe.py`, `probe.json`, `probe.out.txt`, `live-revision.txt`, `workbench.png`). Playwright sign-in; credentials read at run time and never printed; the outputs hold no email address.

## Observations (2026-11-23)

* Children: #219, #221, #222, #224 closed; #220 and #223 open. #440 open with its two unticked criteria; the [post-demo deferral wording](./issue-440-post-demo-deferral-wording-2026-11-22.md) is still awaiting owner approval.
* Live app `ca-cutover-test-demo-api--0000055`, 100% traffic, Healthy.
* `GET /api/governance` and `GET /api/assistants` return 200 with `rai_exercise_acceptance` and `real_ai_delivery_gate` as separate sections (`independent_of_real_ai_delivery_gate: true`).
* `real_ai_delivery_gate` is `blocked`: provider configured, durable SQL release store and no active suspension pass; named live releases (OQ-017), appointed authority holders (OQ-017), live fairness thresholds (OQ-018) and Legal/DPO determination (OQ-019) fail. All 11 enabled tasks list as unapproved for live use, so no live AI activation exists without named approval.
* `rai_exercise_acceptance` was `failed` live: seven of eight checks passed; `requirement_traceability_complete` was false although its own detail reported 15 of 15 covered.
* `GET /api/ai/report` answered 503 `sql-write-lock-busy`, then 500 on a retry. The app log shows concurrent writes from other workers on the same demo store. Not investigated further; live report coverage is unproven.

## Defect found and fixed

Cause: the container image ships `src/*/src` only, so the AST scan of `src/core/tests/*.py` finds no test files and reports every target unresolved. The check failed the whole exercise acceptance on every deployment and its detail text said the opposite. Offline and in CI the check passes.

Fix (`rai_control_plane.py`): `verify_traceability_targets` reports `test_tree_present`; `traceability_summary` reports `target_verification` of `verified`, `test_tree_not_shipped` or `unresolved`. A deployment with no test tree is complete when no required ID is missing or untraced; a test tree with unresolved targets still fails closed. The check detail and the readiness payload state the mode. Tests: `test_traceability_is_complete_when_deployment_ships_no_test_tree` and an extended fail-closed assertion.

Validation (FULL tier, src change): `tests.test_rai_control_plane_218` 8 tests OK; core RAI, governance and assistant suites OK (38 and 88 with 18 skipped, 5); `src/api` `tests.test_rai_release_readiness_api_218` 5 tests OK; `ruff check` and `ruff format --isolated --line-length 100` clean on the changed files; `mypy` in `src/core` shows the same three errors with and without the change (OpenTelemetry stubs, one unused ignore). Hosted CI is not read; nothing was pushed. The fix is not deployed, because a redeploy changes a shared demo estate that other workers use, so the live `failed` to `passed` change is unproven.

## Per-criterion result

| Criterion | Result for the demo | Basis |
| --- | --- | --- |
| Stabilization checkpoint (#440) | Unproven | #440 open; triage filing and PR-delivered independent review need the owner and a pull request. Merged children cannot satisfy it |
| All child features closed or deferred by the owner | Unproven | #220 and #223 open; no owner deferral recorded. #220 criterion 5 is proven live for the constructed case ([r11](./issue-220-live-r11-revision-0054-2026-11-23.md)) but its final checkbox is owner-gated; #223 needs real reviewers and OQ-017 holders |
| No live activation of an AI task without named approval (OQ-017) | Proven again (ticked) | Live gate lists 0 approved and 11 unapproved live tasks; offline `test_live_release_post_without_named_approval_is_rejected_with_oq017_and_audited` passes |
| Each requirement traces to a passing check or a recorded deferral | Proven offline (ticked) | 15 of 15 covered, targets resolved in the repo; live detail now accurate after the fix, not yet deployed |
| Exercise acceptance reports RAI checks separately from the real-AI gate | Proven live (ticked) | Two separate sections with `independent_of_real_ai_delivery_gate: true` and different statuses |

The issue stays open: the two unticked criteria need the owner. Billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo.
