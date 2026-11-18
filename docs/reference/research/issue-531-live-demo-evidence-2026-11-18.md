---
title: Employee loading feedback and Today's briefing live demo evidence (Refs #531)
description: Per-criterion record of what the live demo proves for issue 531, including the unticked criterion 7 (live verification), with limits and adverse observations
ms.date: 2026-11-18
---

Refs #531. Scope is the synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive billing reconciliation, DPO and Legal approval and person-run assistive technology testing. No source code changed and no Azure resource was created or modified. Azure CLI was used read-only (`az containerapp show`, revision and replica listing). The briefing review controls were opened and cancelled; no review was recorded.

## Method

* Playwright Chromium, 1366 by 900, signed in to `ca-cutover-test-demo-api` with the employee demo account (read at run time, never printed; a literal scan of the retained JSON and the two scripts found neither the user id nor the secret, and the probe JSON holds no e-mail address). Driver: `.copilot-tracking/evidence/2026-11-18/issue-531-live/live_531_probe.py`; output `live_531_probe.json`; screenshots in the same folder. Parity check: `parity.py`, `deployed_hashes.json`.
* Three kinds of evidence, kept apart below. Observed: the real live page and API. Simulated: browser-side request holds, aborts or response rewrites on the live site (the server was not changed). Not exercised: anything needing a server state change.
* axe-core 4.10.3 (from the phase-witness store) ran with the tags wcag2a, wcag2aa, wcag21aa and wcag22aa.

## Deployed build versus the branch

The deployed revision `ca-cutover-test-demo-api--0000031` (created 2026-11-17T19:42Z, two replicas running, `minReplicas` 0, `cooldownPeriod` 300 s) serves `workspace-shell.js` and `async-action.js` byte-identical to this branch (main `9f175bd3d`). Its `app.js` matches commit `fa8329d51` (2026-11-16) and its `style.css` matches `14296ce86`, so the live site is behind main for those two files. The diff from `fa8329d51` to main touches chat origin labels, an exception-screen wording change and a regulatory-mode layout rule; it contains no briefing, startup, loading or retry change. The findings below therefore describe the deployed build and are expected to hold for main, but that is an inference from the diff, not a live observation of main.

## Observations (2026-11-18)

| Area | Result | Kind |
| --- | --- | --- |
| Shell before scripts | With JavaScript disabled, `/app` shows the heading "Starting the workspace" and the status "Starting the workspace, this can take up to a minute when the service has been idle." in `role="status"`, `aria-live="polite"`. The page is not blank. | Observed |
| Held `app.js` (cold-start stand-in) | 0.3 s: start message, no Try again button. 5.6 s: "Still starting the workspace. The service may have been idle. You can wait or try again." with a visible Try again button. 16.7 s: "The workspace is taking longer than expected. Try again. If this continues, contact application support." Releasing the script removed the shell and showed the briefing at 17.9 s. | Simulated |
| Async feedback | Refresh briefing held 80 ms: status "Reading case summaries... Refreshing today's briefing. The current text stays visible until the new one is ready.", content `aria-busy`, mode control disabled, no spinner yet. After 500 ms: two spinners and "Refresh briefing: working..." and "Loading workspace data: working..." feedback; spinner appears only after the 200 ms threshold. Released, the status returned to "Briefing ready. Check the sources, then choose how to review the draft." | Simulated hold, real controls |
| Reduced motion | `.async-spinner` computed `animation-name` is `none` under `prefers-reduced-motion: reduce` and `async-spin` (1 s, infinite) otherwise. Text feedback carries the state either way. | Observed |
| Script retry | With `/ops.js` aborted, opening a case made four requests for it (one load plus three retries), the status read "Loading workspace files. Please wait.", then "Workspace unavailable: Required workspace files did not load: /ops.js. Reload this page to try again. If this continues, ask application support to check these files." with a "Reload workspace" button and a `role="alert"` copy. | Simulated |
| Briefing structure | Heading "Today's briefing"; label "Summary by rules. Not an instruction."; basis list (Priority: set by fixed rules, not by AI; Wording: written by rules and templates, no AI was used; Your control); section "Rules-derived summary and its sources"; per statement "Sources used (2)" disclosures whose items link to `#/case/{id}`; "Prepared at: 18 Nov 2026, 11:44:00 UTC" in a `time` element with a datetime value; "Template draft, not approved. Not an instruction. Not reviewed by a person yet."; "Confidence: not provided. Confidence is not accuracy."; "Why listed" text per statement; feedback guidance paragraph. | Observed |
| Review wording | Group "Review this draft" with "Use this draft", "Edit this draft", "Do not use this draft"; no text box visible initially. Edit shows "Edited draft" and "Reason" and "Save edited draft review"; reject shows only "Reason" and "Record rejection". An empty reason on either path set `aria-invalid="true"` (focus moved to Reason on edit) and sent no `/api/ai/review/` request. Cancel review returned to the three buttons with zero requests sent. | Observed |
| Mode control | Control with "Allow AI suggestions" and "Use rules and templates, without AI"; the old "Workflow only (no AI)" checkbox is gone. | Observed |
| AI and unverified labelling | With the live `/api/briefing` response rewritten in the browser (source `ai`, `validated` false, one unresolved reference): label "AI suggestion, not approved. Not an instruction."; section "Generated briefing and its sources"; wording "Summarised by AI. Check it against the sources."; "These references do not match the record: ZF-SIM-0000: Stage. Do not rely on this statement." and "Unverified: its sources do not match the case record. Check it before use." | Simulated |
| axe | 0 violations on `.briefing` (20 passes) and on the whole page (28 passes), WCAG 2.2 AA tag set. | Observed |

Screenshots: `shell-no-javascript-1366.png`, `coldstart-sim-initial-1366.png`, `coldstart-sim-slow-1366.png`, `coldstart-sim-deadline-1366.png`, `briefing-live-1366.png`, `briefing-source-expanded-1366.png`, `briefing-edit-open-1366.png`, `briefing-refresh-pending-1366.png`, `briefing-simulated-ai-unverified-1366.png`, `script-retry-failure-1366.png`.

## Per-criterion result

| # | Criterion | Demo result | Evidence and limit |
| --- | --- | --- | --- |
| 1 | Loading state before scripts and per panel, with live region, slow-load hint and retry | Already ticked; re-observed on the live build | Static shell, polite live region, 4 s hint with Try again, 15 s message, per-panel "Reading case summaries..." and `aria-busy`, 200 ms spinner, retry and persistent-failure wording. The timing and failure paths were simulated in the browser. |
| 2 | Cold-start simulated in a browser check without a blank page | Already ticked; re-observed against the live site | The held-script run shows the message at 0.3 s and no blank body. A real scale-from-zero start was not observed: two replicas were running with other work active, and forcing zero would change the app. |
| 3 | AI, rules-derived content and sources distinguished; HAX guidelines in a design note | Already ticked; rules path observed, AI path simulated | The live demo produced only the rules-derived summary (see adverse observations). AI wording came from a rewritten response. The design note is [briefing-hax-design-note.md](./ux/briefing-hax-design-note.md); it was not re-read here. |
| 4 | Outcome-based action wording; behaviour and boundaries unchanged and tested | Already ticked; wording and reason requirement observed | Wording is "Use this draft", "Edit this draft", "Do not use this draft", not the "Approve" examples in the issue text. The recorded-review behaviour, the tests and the approval boundary were not exercised live; a review cannot be undone, so none was recorded. |
| 5 | Sources and refresh time shown; unverified output labelled | Already ticked; sources and time observed, unverified simulated | Real briefing shows sources and a UTC refresh time. Unverified wording appeared only under the rewritten response. |
| 6 | Automated browser and axe checks pass; screen-reader and voice-control acceptance not claimed | Already ticked; live axe 0 violations | Screen-reader and voice-control acceptance is still not claimed and was waived for the demo. |
| 7 | Live verification on the employee site recorded separately | Proven for the demo, with the limits stated here | A signed-in employee session on the redeployed demo build showed the loading shell, the briefing structure, the review wording and reason rules, async feedback and axe results above. It was not a real cold start, it did not record a review, it saw no AI-generated briefing, and the live `app.js` and `style.css` are two days behind main. It does not prove screen-reader or voice-control behaviour. |

Net: criterion 7 is evidenced for the demo build in the sense the 2026-11-04 check described (an employee session against the redeployed site, including Today's briefing). The owner can tick it on that basis, or hold it until a genuine cold start, a recorded review and an AI-written briefing are observed.

## Adverse and incidental observations

* The live briefing is rules-derived. The page shows "Release admission denied: no approved release matches (approved, unexpired release record). Owner: RAI task owner not appointed (OQ-017; project contact: Juan Manuel Servera). Manual route: use the ordinary case controls." So the AI-generated path cannot be shown live without an approved release, and the review buttons are drawn but a real submission was not attempted.
* The first exploratory sign-in attempt timed out on the Microsoft sign-in page and the next attempt succeeded; no retained run is affected.
* The "Download handoff waiting times for Excel" control carries a long explanatory paragraph inside the same block as the button; this is outside #531 and was not changed.
* Button wording differs from the issue's example set; the owner comment of 2026-10-28 asked for plain-language outcome labels, which the current wording meets.
* The focus box on the Reason field in `briefing-edit-open-1366.png` shows the invalid state through an outline plus the `aria-invalid` attribute; the on-screen error text was not separately captured.

## Resources and residue

No Azure resource, role assignment or setting was created or changed. No chat threads or review records were created. Local evidence only; Focused tier (no source change); no `rpi-checks.py --all`; independent review and hosted CI outstanding.

## Evidence limits

* One browser (Chromium), one viewport, one account, one run of each probe step.
* Simulated steps show the shipped client code under held, aborted or rewritten requests, not a real cold start or real AI output.
* Live assets are not main; the comparison to main rests on the file diff.
* axe is automated and finds only part of the issues; no assistive technology was run.
