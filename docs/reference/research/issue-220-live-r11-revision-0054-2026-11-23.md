---
title: Issue 220 eleventh live run, recheck on revisions 0000054 and 0000026 (2026-11-23)
description: Live recheck that the challenge route records and corrects a constructed challenge without retaliation, inferred refusal or hazard delay, with a per-criterion proven and unproven table
author: AMA RPI agent
ms.date: 2026-11-23
ms.topic: reference
---

Refs #220. Synthetic desktop demo under the owner decisions of 2026-11-18. Not resident, production or legal evidence.

## Method and results

* Live state on 2026-11-23: `ca-cutover-test-demo-api` active revision `--0000054` (created 2026-11-22T23:14Z, 100% traffic) and `ca-resident-demo` `--0000026`. Both are unchanged since the [tenth-run note](./issue-220-live-r10-revision-0054-2026-11-22.md), and no 220 source changed on main since that run, so the probe repeats unchanged. Raw files: `.copilot-tracking/evidence/2026-11-23/issue-220-live-r11/` (`run1.py`, `run1.out.txt`, `run1.json`, `live-revision.txt`, `route-view.png`). Playwright sign-in; credentials read at run time and never printed; output has 0 `@` characters.
* Case `ZF-2025-0331` (synthetic). `nomination_record` returns 200 with the staff-recorded non-digital route, owner, next update 2026-12-02 and "Housing office phone line, staffed weekdays". `nomination_correct` returns 200 with "Re-review required; no priority or consent change".
* Assurance fields: `no_retaliation` true, `inferred_refusal` false, `hazard_response_delayed` false.
* Protected hashes (stage, days in stage, closed, resident, hazards, measure decisions) match before the record, after the correction and after the adverse inputs. Stage stays "Waiting for block programme" at 116 days; hazard hold "Repair evidenced, hold active".
* `hazard_concern` true gives a redirect to `/api/cases/{case_id}/hazard-raise` and saves nothing. `retaliation_flag`, `refusal`, `hazard_pause` and `priority_penalty` each give 400. A missing `hazard_concern` gives 400.
* Offline: 30 core tests and 10 api tests for the 220 modules pass. No source change was needed; no code gap was found.
* Side effects: one more constructed nomination in the demo data store (3 now). No Azure resource was created or changed.

## Per-criterion result

| Criterion | Result for the demo | Basis |
| --- | --- | --- |
| Digital and staff-recorded routes work | Proven live on 0000054 | Probe; tests |
| Explanations, owner, next update, resolution visible | Proven live for owner, next update, route, assurance and review status; resolution by offline tests | Probe; tests |
| Only dependent proposals and reviews stale | Proven offline; live `dependent_review_versions` empty | Tests; probe |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Proven live: protected hashes unchanged | Probe |
| No retaliation, inferred refusal or delayed hazard response | Proven live for the constructed case. Retaliation over time and real hazard-response timing need production history and are not provable in the synthetic demo | Probe; tests |

Owner-gated: ticking the final issue checkbox. Not needed for the demo: billing, DPO or Legal approval, person-run assistive-technology testing.
