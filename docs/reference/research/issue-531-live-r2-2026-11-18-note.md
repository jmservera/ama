---
title: Employee loading feedback and Today's briefing live re-verification, second pass (Refs #531)
description: What a second live run adds to the merged demo evidence for issue 531, with per-criterion proven and unproven results
ms.date: 2026-11-18
---

Refs #531. Synthetic demo, desktop only; owner decisions of 2026-11-18 apply (live Azure in resource group `ama`, no drills, no production change, no assistive-technology testing). No source file or Azure resource changed; nothing needed deleting. Evidence folder: [issue-531-live-r2-2026-11-18/](./issue-531-live-r2-2026-11-18/).

This note adds to [issue-531-live-demo-evidence-2026-11-18.md](./issue-531-live-demo-evidence-2026-11-18.md), which already records the shell, held-script, async feedback, reduced motion, retry, wording and axe observations. Those were not repeated; the original probe is copied as [scripts/live_531_probe.py](./issue-531-live-r2-2026-11-18/scripts/live_531_probe.py) for reference.

## New evidence

* Cold start attempt. `az containerapp replica list` was polled every 45 s from 14:03Z to 14:13Z against `ca-cutover-test-demo-api` (`minReplicas` 0, cooldown 300 s). It showed one to two replicas throughout, because other work shares the app, so the app never scaled to zero. Forcing zero would change the app, which the owner excluded. A real cold start was therefore not observed.
* Deployed parity. Revision `ca-cutover-test-demo-api--0000031` is still current. `workspace-shell.js` and `async-action.js` match this branch; `app.js` and `style.css` do not ([live_531_delta.json](./issue-531-live-r2-2026-11-18/live_531_delta.json)). The earlier note's diff analysis (no briefing, startup or retry change between the deployed commit and main) still stands.
* Recorded review through the UI ([scripts/live_531_delta.py](./issue-531-live-r2-2026-11-18/scripts/live_531_delta.py)). Choosing "Do not use this draft", entering a reason and selecting "Record rejection" sent one `POST /api/ai/review/{id}/reject` and received 200. The record showed review state `Rejected` and the text "Rejected as a draft by a person. This is not an approval, consent or safety decision. Reason: ... Recorded in the audit log." The controls then reduced to "Hide briefing" and "Refresh briefing". Screenshot not retained: the capture showed resident names and addresses. This left one rejected review record on a synthetic case; it cannot be undone.
* Secret check: a literal search of the folder for the sign-in values found no match.

## Per-criterion result

| # | Criterion | Result | Basis |
| --- | --- | --- | --- |
| 1 | Loading state before scripts and per panel, live region, slow-load hint, retry | Proven on the live build (observed shell and live region; timing and retry simulated in the browser) | Earlier note, rows "Shell before scripts", "Held app.js", "Async feedback", "Script retry" |
| 2 | Cold start shows message without a blank page | Proven for the simulation; real scale-from-zero unproven | No scale-to-zero in 10 minutes; forcing it is excluded |
| 3 | AI, rules and source content distinguished; HAX note | Rules path proven live; AI path unproven live (simulated only) | Release admission denied (OQ-017), so no AI briefing exists |
| 4 | Outcome wording; behaviour and approval boundary unchanged | Proven live: wording, empty-reason refusal (earlier note) and now a recorded reject with "not an approval" labelling. Approve and edit submissions not run live | New reject record above |
| 5 | Sources and refresh time shown; unverified labelled | Sources and UTC time proven live; unverified label proven only on a rewritten response | Earlier note |
| 6 | Browser and axe checks pass; no AT claim | axe 0 violations live (earlier note); no screen-reader or voice-control claim, waived for demo | Earlier note |
| 7 | Live verification recorded separately | Proven for the demo build with the limits above: not a real cold start, no AI briefing, `app.js` and `style.css` behind main | This note and the earlier note |

Reduced motion was observed in the earlier run (spinner animation `none` under `prefers-reduced-motion: reduce`) and was not repeated.

## Follow-ups

* Redeploy the demo so `app.js` and `style.css` match main, then repeat the parity check.
* Observe a genuine cold start in a quiet window or on a dedicated throwaway app, if the owner wants criterion 2 proven beyond simulation.
* Observe an AI-written briefing once a release is approved.

## Evidence limits

* One Chromium run at 1366 by 900 with one account; one reject recorded, no accept or edit.
* axe is automated and does not establish accessibility acceptance.
* The Focused tier applied (documentation and evidence only); independent review and hosted CI are outstanding.
