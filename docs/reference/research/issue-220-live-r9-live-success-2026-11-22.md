---
title: Issue 220 ninth live run, staff-recorded route succeeds (2026-11-22)
description: Live proof on revision 0000053 that the challenge route records and corrects a constructed challenge without retaliation, inferred refusal or hazard delay
author: AMA RPI agent
ms.date: 2026-11-22
ms.topic: reference
---

Refs #220. Synthetic desktop demo under the owner decisions of 2026-11-18. Not resident, production or legal evidence.

## Method and results

* Target `ca-cutover-test-demo-api`, active revision `--0000053` (created 2026-11-22T19:38Z), the first live image to carry the oid-less roster fix recorded in the [run 8 note](./issue-220-live-r8-oid-less-roster-2026-11-21.md). Raw files: `.copilot-tracking/evidence/2026-11-22/issue-220-live-r9/` (`run1.py`, `run1.out.txt`, `run1.json`, `live-revision.txt`, `route-view.png`). Playwright sign-in; credentials read at run time and never printed; emails scrubbed.
* Case `ZF-2025-0331` (synthetic). The staff-recorded `nomination_record` write now returns 200 (run 8: 403). One constructed challenge `NOM-1f49...` was created in the demo data store with a named owner, next update 2026-12-02 and the non-digital route "Housing office phone line, staffed weekdays". No Azure resource was created.
* `nomination_correct` returns 200; the record shows "Re-review required; no priority or consent change", `automatic_acceptance` false, `automatic_sanction` false, and the server-built assurance `no_retaliation` true, `inferred_refusal` false, `hazard_response_delayed` false, with the three plain-language guarantees.
* Hashes of stage, days in stage, closed, resident, hazards and measure decisions are identical before the record, after it, after the correction and after all adverse inputs. Stage stays "Waiting for block programme", days in stage 116, hazard hold stays Active.
* `hazard_concern` true gives 400 and redirects to the independent hazard intake, saving nothing. `retaliation_flag`, `refusal`, `hazard_pause` and `priority_penalty` each give 400 before any write. A missing `hazard_concern` gives 400. The route view shows the protection wording.
* Offline: 36 tests in `test_no_retaliation_guard_220`, `test_challenge_no_retaliation_220`, `test_issue_220_challenge_route`, `test_challenges` and `test_challenge_signed_in_principal_220` pass.

## Per-criterion result

| Criterion | Result for the demo | Basis |
| --- | --- | --- |
| Digital and staff-recorded routes work | Proven: staff-recorded record and digital correction both 200 live | Probe; tests |
| Explanations, owner, next update, resolution visible | Proven live for owner, next update, route, assurance and review status; resolution by offline tests | Probe; tests |
| Only dependent proposals and reviews stale | Proven offline; live correction shows `dependent_review_versions` empty | Tests; probe |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Proven live: protected hashes unchanged | Probe |
| No retaliation, inferred refusal or delayed hazard response | Proven live for the constructed case: guard fields refused, state unchanged, hazard hold active, hazard concern routed to the hazard service. Retaliation over time and real hazard-response timing need production history and cannot be shown in the synthetic demo | Probe; tests |

The issue checkbox is left for the owner to tick.
