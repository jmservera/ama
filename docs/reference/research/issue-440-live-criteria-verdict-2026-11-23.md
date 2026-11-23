---
title: Issue 440 live criteria verdict at head 6815bc595d (2026-11-23)
description: Live and local re-observation for the stabilization checkpoint, one tooling defect fixed, and a proven or unproven verdict for criteria 7 and 8
ms.date: 2026-11-23
ms.topic: reference
---

Scope: synthetic demo, desktop only, head `6815bc595dbae39bcd4647067ed61acd3df9d0c5`. Refs #440. The only change is a tooling allowlist entry; no `src/` change, no Azure resource created or changed, no issue filed, no push. Credentials were read at runtime and never printed. This note follows [the 2026-11-21 third pass](./issue-440-live-criteria-verdict-2026-11-21-r3.md) and [the 2026-11-22 deferral draft](./issue-440-post-demo-deferral-wording-2026-11-22.md), which stay unchanged.

## Observations

| Item | Observation | Class |
| --- | --- | --- |
| D1 `/api/time/status` | Signed in as the employee account on `ca-cutover-test-demo-api` with Playwright: `/api/me` 200, `/api/time/status` 200 (`enabled: false`, "Time capture is switched off."), `/api/continuity` 200, `#/time` renders. Probe, redacted output and screenshot in [the evidence folder](../../../.copilot-tracking/evidence/2026-11-23/issue-440-live-20261123T205011Z/live_findings_probe.json). | Azure observed |
| D1 local | `test_timecapture` and `test_timecapture_copy`: 41 tests OK, 5 skipped. | Local observed |
| `/api/law` | 404 `{"error": "Not found."}` (503 on 2026-11-21). The route answer changed; not a #440 finding and not investigated further. | Azure observed |
| Legacy-reference guard | 1 violation at this head: `.github/rubric/scripts/test_prepare.py:335`, introduced by #2329. `tools/test_check_legacy_references.py::test_repository_has_no_violations` failed. | Local observed (defect) |
| Fix | The file is a regression guard that must name the retired paths; it is added to `GUARD_FILES` in `tools/check-legacy-references.py`. After: guard `references: 0 violation(s)`, 8 of 8 guard tests pass, ruff check and format clean. Existing test is the regression test. | Local observed |
| Filed findings | #2301 (Refs #440) filed #2303, #2304 and #2320 with reproduction; all open. #1837 remains the gating finding. No open `bug`-labelled issue. | Local observed |

## Criterion verdicts

| Criterion | Verdict | Reason |
| --- | --- | --- |
| 1 to 6 | Ticked on the issue | Not reassessed. |
| 7 Triage, gating, owner approval | Proven for triage, filing and gating; owner approval unproven | Confirmed findings are filed or delivered with reproduction (#2303, #2304, #2320, #1837); gating limited to the blocking finding. The owner approval of requirement changes, pivots and deferrals is human evidence a worker cannot supply, so the tick stays with the owner. |
| 8 Artifacts in a PR, independent review, Major HVE behavior | Unproven | No PR may be opened and the reviewer is the author; the coordinator section is unchanged since #2229, so no new behavior test was run. Native-host discovery of the agent was resolved on 2026-10-24, which does not establish behavior acceptance. |

## Limits

* Focused tier: no `src/` change; no full suite and no `rpi-checks.py` run.
* Hosted CI for the exact head is not observed here.
