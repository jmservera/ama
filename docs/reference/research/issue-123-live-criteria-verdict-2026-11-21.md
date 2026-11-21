---
title: Issue 123 live criteria verdict at head 0c497160e (2026-11-21)
description: Re-observation of the two open #123 criteria, the child feature states, a local governance regression run and a live signed-in probe that found an unaccepted-handoff failure
ms.date: 2026-11-21
ms.topic: reference
---

Scope: synthetic demo, desktop only, head `0c497160e995204a1aa880fb7470788b3b44152c`, focused tier because no source changed. Refs #123. No GitHub issue was created, ticked or closed, and no Azure resource was created or changed. This note builds on the [2026-11-19 D4 note](./issue-123-live-d4-golden-error-2026-11-19.md) and the [2026-11-21 #440 verdict](./issue-440-live-criteria-verdict-2026-11-21.md), which stay unchanged.

## Observations

| Item | Observation on 2026-11-21 | Class |
| --- | --- | --- |
| Child features of #123 (sub-issues API) | #124, #125, #128 and #129 closed on 2026-11-19, #127 closed on 2026-10-15; #126 and #440 are open. | Local observed (GitHub state) |
| #440 | Criteria 1 to 6 ticked; criterion 7 proven for the demo and left for the owner to tick; criterion 8 unproven (needs a published PR, a non-worker reviewer and behavior tests of the current coordinator). See the [#440 verdict](./issue-440-live-criteria-verdict-2026-11-21.md). | Local and Azure observed |
| #126 | Five unticked boxes: protocol, DPIA and lawful basis approved before Phase 0 capture; track eleven residuals and eleven unassessed checks with owner and disposition; fresh current-source assessment; qualified-owner acceptance; delivered build satisfies the version-linked AI, SQL and Azure contract. Each needs a named human decision, a DPO or Legal approval, or an independent assessment. | Local observed (issue body) |
| Governance regression | From `src/core` with `PYTHONPATH=src:tests`: `python3 -m unittest tests.test_gates tests.test_governance tests.test_synthetic_phase_gate_traceability tests.test_restart_gate_sql_fences tests.test_rai_control_plane_218 tests.test_regulatory_eval_gates_216`: 175 tests, OK, 18 skipped. | Local observed |
| Legacy-reference guard | `python3 tools/check-legacy-references.py`: `references: 0 violation(s); links: 0 violation(s)`. | Local observed |
| Live app | `ca-cutover-test-demo-api` revision `ca-cutover-test-demo-api--0000038` running; `/healthz` 200; employee sign-in with Playwright reached "My cases today"; `/api/me` 200 (role Retrofit Programme Manager), `/api/continuity` 200. Probe: [live_probe.py](../../../.copilot-tracking/evidence/2026-11-21/issue-123-live-20261121T073416Z/live_probe.py), output [live_probe_output.json](../../../.copilot-tracking/evidence/2026-11-21/issue-123-live-20261121T073416Z/live_probe_output.json). | Azure observed |

## Finding: unaccepted-handoff queue fails as a whole on the live demo data

The signed-in "Handoff waiting times" screen at `/app#/handoff-waiting` shows its plain-language failure message ("Handoff waiting times could not load ... Owner: application support") and `GET /api/handoffs/unaccepted` and `.csv` return HTTP 500. The container log records `ValueError at=workflows.py:393:handoff_ageing`, which is the guard `Handoff offered_at needs a timezone.` Screenshot: [handoff-waiting-screen.png](../../../.copilot-tracking/evidence/2026-11-21/issue-123-live-20261121T073416Z/handoff-waiting-screen.png) (email addresses redacted before capture). Second probe: [live_probe2_output.json](../../../.copilot-tracking/evidence/2026-11-21/issue-123-live-20261121T073416Z/live_probe2_output.json).

* `/api/handoffs`, `/api/handoffs/unowned` and `/api/handoffs/escalated` return 200 on the same data.
* The four open handoffs (cases `ZF-2025-0029` to `ZF-2025-0032`) carry `offered_at` in the shape `9999-99-99T99:99`, a minute-precision timestamp with no timezone. Current code writes timezone-aware values (`_now()` uses UTC), so these are seeded data values, not newly written ones.
* Local reproduction with `offered_at="2026-11-18T09:30"`: `handoff_view` returns `elapsed_hours: None` (tolerated) and `handoff_ageing` raises `ValueError: Handoff offered_at needs a timezone.`

The behavior is the designed fail-closed contract: `test_missing_offered_at_is_tolerated_in_view_and_rejected_in_ageing` in `src/core/tests/test_handoff_escalation_83.py` asserts that ageing rejects a handoff with no usable offered time, and the web client (`waitingRows` in `app.js`) rejects any row whose `age_hours` is not a finite number. A tolerant row would change the API contract (`age_hours: null`), the web validator, the CSV and the exception feed, and the choice of how to read an ambiguous naive time (assume UTC, or show "unknown") is a product decision. No source change is made here. Options for the owner:

| Option | Effect | Cost |
| --- | --- | --- |
| Normalise the four seeded `offered_at` values in the demo store | Screen and CSV load; no code change | Azure data change, not authorised in this run |
| Show an unreadable-time row with `age_hours: null` | One bad record no longer hides the queue | FULL tier: core, API contract, web client and accessibility and content tests |
| Keep fail-closed | Honest failure, but staff see no queue | None; demo screen stays broken |

This is a demo-data and contract finding for the handoff work in #83, not a #123 criterion.

## Criterion verdicts

| #123 criterion | Verdict | Reason |
| --- | --- | --- |
| Complete the scoped #440 stabilization checkpoint before closure | Unproven; cannot be proven by this run | The checkpoint is substantively delivered for the demo (#440 criteria 1 to 7), but #440 criterion 8 is unproven and the issue's own text says merged children alone do not satisfy it. The 175-test governance run and the live probe show no regression in the gate, restart and RAI control code, and one new live finding is recorded above. Owner decision, a published PR and an independent reviewer remain. |
| All child features closed or deferred | Unproven | #126 and #440 are open. Closing or deferring them is an owner decision, and #126 needs DPO, Legal and independent-assessment steps that are out of scope for the demo. |

## Limits

* No full local suite and no `rpi-checks.py` run; the tier is focused.
* The live probe used one employee account; the handoff data values were read as shapes only, with no case content recorded.
* The regulatory standing of any governance gate is not assessed here.
