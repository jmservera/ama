---
title: Issue 220 tenth live run, recheck on revision 0000054 (2026-11-22)
description: Live recheck that the challenge route still records and corrects a constructed challenge without retaliation, inferred refusal or hazard delay on the current image
author: AMA RPI agent
ms.date: 2026-11-22
ms.topic: reference
---

Refs #220. Synthetic desktop demo under the owner decisions of 2026-11-18. Not resident, production or legal evidence.

## Method and results

* Run 9 proved the criterion on revision 0000053. The active revision of `ca-cutover-test-demo-api` is now `--0000054` (created 2026-11-22T23:14Z), so the [ninth-run note](./issue-220-live-r9-live-success-2026-11-22.md) no longer describes the live image. This run repeats its probe unchanged. Raw files: `.copilot-tracking/evidence/2026-11-22/issue-220-live-r10/` (`run1.py`, `run1.out.txt`, `run1.json`, `live-revision.txt`, `route-view.png`). Playwright sign-in; credentials read at run time and never printed; emails scrubbed (0 `@` in the output).
* Case `ZF-2025-0331` (synthetic). `nomination_record` returns 200 with the staff-recorded non-digital route, a named owner, next update 2026-12-02 and "Housing office phone line, staffed weekdays". `nomination_correct` returns 200 with "Re-review required; no priority or consent change", `automatic_acceptance` false, `automatic_sanction` false and empty `dependent_review_versions`.
* Server-built assurance: `no_retaliation` true, `inferred_refusal` false, `hazard_response_delayed` false, plus the three plain-language guarantees.
* Protected hashes (stage, days in stage, closed, resident, hazards, measure decisions and related fields) are identical before the record, after the correction and after all adverse inputs. Stage stays "Waiting for block programme", days in stage 116, hazard hold "Repair evidenced, hold active".
* `hazard_concern` true gives 400, routes to `/api/cases/{case_id}/hazard-raise` and saves nothing. `retaliation_flag`, `refusal`, `hazard_pause` and `priority_penalty` each give 400. A missing `hazard_concern` gives 400. The route view shows the protection wording.
* Offline: 30 core tests (`test_no_retaliation_guard_220`, `test_challenge_no_retaliation_220`, `test_issue_220_challenge_route`, `test_challenges`) and 10 api tests (`test_challenge_no_retaliation_api_220`, `test_challenge_non_retaliation_hazard_guard`) pass.
* Side effects: two constructed nominations now exist in the demo data store (runs 9 and 10). No Azure resource was created or changed.

## Per-criterion result

| Criterion | Result for the demo | Basis |
| --- | --- | --- |
| Digital and staff-recorded routes work | Proven live on 0000054 | Probe; tests |
| Explanations, owner, next update, resolution visible | Proven live for owner, next update, route, assurance and review status; resolution by offline tests | Probe; tests |
| Only dependent proposals and reviews stale | Proven offline; live `dependent_review_versions` empty | Tests; probe |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Proven live: protected hashes unchanged | Probe |
| No retaliation, inferred refusal or delayed hazard response | Proven live for the constructed case. Retaliation over time and real hazard-response timing need production history and cannot be shown in the synthetic demo | Probe; tests |

The issue checkbox is left for the owner to tick.
