---
title: Issue 440 live criteria verdict at head b6d215334 (2026-11-21)
description: Live and local re-observation of the stabilization findings with a signed-in time capture screenshot, and a proven or unproven verdict for criteria 7 and 8
ms.date: 2026-11-21
ms.topic: reference
---

Scope: synthetic demo, desktop only, head `b6d2153341c1cc6866cb838c8537aa2e0272972e`. Refs #440. No source change, no GitHub issue created, no Azure resource created or changed. This note supersedes [the 2026-11-20 verdict](./issue-440-live-criteria-verdict-2026-11-20.md) for criterion 7 and keeps earlier notes unchanged. The 2026-11-20 note lacked a screenshot of the time capture screen; this note supplies it.

## Observations

| Item | Observation on 2026-11-21 | Class |
| --- | --- | --- |
| D1 `/api/time/status` returned 500 on Azure SQL | Signed in with the employee test account on `ca-cutover-test-demo-api`: `/api/me` 200, `/api/time/status` 200 with `enabled: false`, `flag_on: false`, `dpia_recorded: false`, `reason: "Time capture is switched off."`, `storage: "the shared SQL store"`, `/api/continuity` 200. Probe: [live_probe.py](../../../.copilot-tracking/evidence/2026-11-21/issue-440-live-20261121T032743Z/live_probe.py), output [live_findings_probe.json](../../../.copilot-tracking/evidence/2026-11-21/issue-440-live-20261121T032743Z/live_findings_probe.json). | Azure observed. Delivered. |
| D1 screen | Playwright, desktop 1366 by 900, clicking the "Time capture" navigation link at `/app#/time`: heading "Staff time capture", the plain statement that time capture is switched off with owner and next action, and six "Missing:" prerequisites. Screenshot: [time-capture-screen.png](../../../.copilot-tracking/evidence/2026-11-21/issue-440-live-20261121T032743Z/time-capture-screen.png). | Azure observed (UI). |
| D1 local | `python3 -m unittest tests.test_timecapture` from `src/api`: 28 tests, OK. | Local observed. |
| D2 legacy-reference guard | `python3 tools/check-legacy-references.py`: `references: 0 violation(s); links: 0 violation(s)`. | Local observed. Delivered. |
| D3 unreachable `ChatIsolation.turn` | `grep -rn "def turn" src --include=*.py` finds no definition (only a nested test helper `turns`). | Local observed. Delivered. |
| D4 AI golden path | Unchanged since 2026-11-20: `ZF_AI_GOLDEN` configuration assertion in `src/agents/tests/test_ai_eval.py`; non-editable-install criterion not verified. | Implemented, residual unverified. |
| Open findings | `gh issue list --state open --label bug` returns none. The one triaged blocking finding still open is the existing #1837 (nomination submissions, state OPEN on 2026-11-21), already filed so no duplicate is created, and it gates #81 through its child #130 as recorded in the [2026-11-18 triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md#part-2-which-epics-each-blocking-finding-gates). Its live re-proof is in the [#1837 live note](./issue-1837-live-demo-evidence-2026-11-20.md). | Local observed (issue state); gating per triage record. |

Correction to the 2026-11-20 limit: that run opened `/#/time`, which is the signed-out welcome route. The signed-in workbench is served at `/app`, so the earlier missing screenshot was a probe path error, not a product defect.

Incidental: `/api/law` returns 503 `{"error": "The law store is not loaded."}` for the employee account. This is the designed unloaded-store response, asserted by `src/api/tests/test_procurement_api.py:204` and `src/api/checks/expected_denials_browser_check.py:149`, and is a deployment state outside #440.

## Criterion 8 sub-claims

| Sub-claim | Observation | Verdict |
| --- | --- | --- |
| Native host discovery of the coordinator | The coordinator file `.github/agents/ama-backlog-delivery-coordinator.agent.md` has changed since the 2026-10-24 discovery candidate (`git diff --stat 1bb637a74 HEAD -- <file>`: 794 insertions, 115 deletions, last touched by `9fa2dbeaa`). In this session, started with the worktree as cwd, the agent catalogue lists "AMA Backlog Delivery Coordinator" with a description identical in the October candidate and the current file. | Name discovered; the current body version is not verifiable from the description. Worker-attested, no transcript. |
| Behavior testing of the coordinator | Not run for the current file. Prior seven scenarios were simulated proxies against the October candidate. | Unproven. |
| Independent review artifact in a PR | No PR exists (branch is local by instruction) and the reviewer in this loop is the worker's own review phase. | Unproven. |
| Coordinator change treated as Major HVE Builder change | #440 itself does not change the coordinator in this run. | Not applicable to this run; unproven historically. |

## Criterion verdicts

| Criterion | Verdict | Reason |
| --- | --- | --- |
| 1 to 6 | Ticked on the issue | Not reassessed. |
| 7 Triage confirmed findings into issues, gate epics, owner approval | Proven for the demo as bounded; tick left to the owner | D1, D2 and D3 are delivered or removed (D1 observed on Azure and locally, D2 and D3 locally); every confirmed finding is either delivered or already filed (#1837, which gates #81 through its child #130 and nothing else), so no new issue is needed and gating stays on that blocking finding only. Owner approval for requirement changes, pivots or deferrals is a human step and none is proposed. |
| 8 Artifacts, independent review, Major HVE behavior | Unproven | Requires a published PR, a non-worker reviewer and behavior tests of the current coordinator. Discovery of the current file is worker-attested only. |

## Limits

* No full local suite and no `rpi-checks.py` run; the tier is focused because no source changed.
* The screenshot shows the display initials and first name of the synthetic demo test account; email addresses were redacted in the page before capture.
* D4's non-editable-install criterion remains unverified.
