---
title: Epic 81 safety, consent and lifecycle audit with live form retest (Refs #81)
description: Per-criterion proven/unproven table for epic 81, the nomination form defect #1837 retested live on 2026-11-18, and the FULL-tier need for its fix
ms.date: 2026-11-18
---

Refs #81. Scope is the synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive Azure billing reconciliation, DPO and Legal approval and person-run assistive technology testing. This note ticks nothing. No source code changed (FOCUSED tier, documentation only) and no Azure resource was created.

## Method and retained evidence

* Issue state read with `gh issue view` for #81, #82 to #88, #130, #131, #440 and #1837 on 2026-11-18.
* Azure CLI, read-only: app `ca-cutover-test-demo-api` revision `ca-cutover-test-demo-api--0000031`, image digest `sha256:5368f4e4...c17e5fb` (unchanged from the #104 and #130 notes, so no fix has been deployed since).
* Playwright Chromium 1366 by 900, signed in as the employee demo account; credentials read at run time by the shared helper, never printed or saved. The probe is in `.copilot-tracking/evidence/2026-11-18/issue-81-live/` (`probe.py`, `probe.json`, `azure_revision.json`, `route-view-81.png`). Output holds no e-mail addresses.
* The probe sent three `application/x-www-form-urlencoded` POSTs to `/api/cases/ZF-2025-0331/resident` (the transport the standalone browser forms use) with a nonexistent nomination id, so no record could be written. Nomination records stayed at 0 before and after.

## Live observation: #1837 reproduces on the deployed image

| Form action | HTTP status | Error body |
| --- | --- | --- |
| `nomination_acknowledge` | 400 | Could not read that. |
| `nomination_correct` | 400 | Could not read that. |
| `challenge_open` | 400 | Could not read that. |

The 400 is a transport rejection before any domain check. The earlier #130 note showed that JSON bodies reach domain rules (a 403 asking for a refreshed staff identity, and field-level 400s that name the rejected fields), which is the control. The case read and the route view both returned 200. My `forms_present` check came back false for all three form names because the HTML view is returned inside a JSON wrapper that the check did not unwrap, so it does not show the forms are absent; the screenshot is orientation only. The 2026-11-17 reports that #130 listed as "not retested" are now retested and match.

## Epic 81 acceptance criteria

| # | Criterion (issue state) | Proven for the demo? | Evidence | Why |
| --- | --- | --- | --- | --- |
| 1 | Stabilization checkpoint #440 (unticked) | Unproven | The [#440 triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md) gives #81 the verdict Fix, gated by #1837; #440 is OPEN with two unticked criteria (triaged RPI issues with owner approval, and PR artifacts); the criterion also says merged children alone do not satisfy it | Needs #1837 fixed or deferred by the owner, then #440 closed |
| 2 | All child features closed or deferred (unticked) | Unproven | #82, #83, #84, #85, #86, #87, #88 and #131 are CLOSED (read 2026-11-18). #130 is OPEN; no recorded owner deferral | #130 is open, and its acknowledgement, correction and challenge forms fail live as shown above |
| 3 | No controlled progression with unresolved safety evidence in the exercise scenarios (ticked) | Not re-examined | No contradiction found in this run | Ticked earlier; this run did not exercise those scenarios |
| 4 | No work started without valid resident agreement or authorised exception in the exercise scenarios (ticked) | Not re-examined | No contradiction found in this run | Same as above |

## Fix decision

The defect is a source and gate-semantic change in the form transport and endpoint contract. That needs a unit test, touches a browser-facing and security boundary (same-origin and CSRF), and takes the FULL tier. FULL tier is required and was not attempted; `rpi-checks.py --all` was not run. The owner-authored fix is a separate local candidate on #1837 (frozen at `33b9c828`, then `1e0a5d0a`), which an independent inspection stopped for a concurrent-form error case. Reimplementing it here would duplicate and diverge from that work, so none was made.

## Residual and recommendation

* Verdict stays Fix: publish #1837 through its own FULL loop, redeploy, rerun this probe expecting non-400 domain responses, then close #130 and re-evaluate criterion 2.
* Criterion 1 additionally needs the owner decisions recorded under #440.
* Nothing in this note changes the ticked criteria 3 and 4.
