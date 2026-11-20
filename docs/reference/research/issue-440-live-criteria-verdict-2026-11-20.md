---
title: Issue 440 live criteria verdict at head 7c5aca476 (2026-11-20)
description: Live and local re-observation of the four triage drafts and a proven or unproven verdict for criteria 7 and 8
ms.date: 2026-11-20
ms.topic: reference
---

Scope: synthetic demo, desktop only, head `7c5aca476dffbd79b6d8012a2bbdfec3457f59f5`. Refs #440. No source change, no GitHub issue created, no Azure resource created or changed. This note supersedes [the 2026-11-19 verdict](./issue-440-live-criteria-verdict-2026-11-19.md) and [refresh](./issue-440-live-checkpoint-refresh-2026-11-19.md) for criterion 7 and keeps them unchanged.

## Observations

| Draft from the [2026-11-18 triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md) | Observation on 2026-11-20 | Class |
| --- | --- | --- |
| D1 `/api/time/status` returned 500 on Azure SQL | Signed in as the employee test account on `ca-cutover-test-demo-api` (revision `0000035`, active since 2026-11-20T19:09Z): `/api/time/status` returns 200 with `enabled: false`, `flag_on: false`, `reason: "Time capture is switched off."`, `storage: "the shared SQL store"`. `/api/me` 200, `/api/continuity` 200. Probe: [live_probe.py](../../../.copilot-tracking/evidence/2026-11-20/issue-440-live-20261120T212807Z/live_probe.py), output in `live_probe.json` beside it. The fix is `7306458` (ledger-safe `notice_version` upgrade), merged in #2155 as `21b810439`. Local: `python3 -m unittest tests.test_timecapture` from `src/api` ran 28 tests, OK, including `test_ledger_safe_notice_version_upgrade_and_legacy_rows`. | Azure observed and local observed. Delivered. |
| D2 legacy-reference guard | `python3 tools/check-legacy-references.py` at head: `references: 0 violation(s); links: 0 violation(s)`. The 2026-11-19 residual at `docs/reference/README.md` is gone. | Local observed. Delivered. |
| D3 unreachable `ChatIsolation.turn` | `grep -rn "def turn" src --include=*.py` finds no definition and no non-test `.turn(` caller. | Local observed. Dead code no longer present. |
| D4 AI golden path | `src/agents/tests/test_ai_eval.py:27` asserts the `ZF_AI_GOLDEN` configuration error (unchanged from the 2026-11-19 note). | Implemented, residual unverified. |
| Open issues matching D1 to D4 | `gh issue list --state open --search` finds none, and none is needed: no confirmed finding is open. | Local observed. |

Incidental observation: `/api/law` returns 503 `{"error": "The law store is not loaded."}` for the employee account on the demo. It is a deployment state of the regulatory assistant, outside the scope of #440, and is recorded without a verdict.

## Criterion verdicts

| Criterion | Verdict | Reason |
| --- | --- | --- |
| 1 to 6 | Ticked on the issue | Not reassessed. |
| 7 Triage confirmed findings into issues, gate epics, owner approval | Proven for the demo as bounded below; tick left to the owner | Every confirmed finding from the first checkpoint and the 2026-11-18 triage is now delivered or removed (D1, D2, D3), so no confirmed finding needs a new issue and none gates an epic. The PERF-440 timing failure of the 2026-10-23 checkpoint is owned by the later checkpoint and full-gate records, not re-proven here. Owner approval of any requirement change, pivot or deliberate deferral is a human step and none is proposed. |
| 8 Artifacts and independent review in the PR; Major HVE Builder behavior | Unproven | Needs a published PR and a reviewer who is not this worker; this branch is local and unpushed by instruction. Native host validation of the coordinator is not repeated here and the coordinator is not changed. |

## Limits

* The browser step navigated to `/#/time` but the page rendered the signed-out welcome page, so there is no screenshot of the time capture screen. The API response is the evidence.
* D4's non-editable-install criterion is not verified.
* No full local suite or `rpi-checks.py --all` run (not permitted here); the tier is focused because no source changed.
