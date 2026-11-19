---
title: Epic 149 first unmet demo criterion, per-criterion recheck (Refs #149)
description: Recheck on 2026-11-19 of the four acceptance criteria of the UX epic for the synthetic desktop demo, with live GitHub and Azure reads and the reason no source change is justified
ms.date: 2026-11-19
---

Refs #149. Scope is the synthetic demo, desktop only, under the owner decisions of 2026-11-18 (live Azure authorised in resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change; billing reconciliation, DPO and Legal approval and person-run assistive technology testing not needed for the demo). This note ticks nothing. No source, test or Azure resource changed, so the tier is focused (documentation only).

## First unmet criterion

Criterion 1: "Complete the scoped stabilization checkpoint defined in #440 before epic closure." It is the first unticked box and it is unmet.

It is not a code criterion. #440 is OPEN (last updated 2026-11-17) with two unticked criteria: triage of confirmed findings into owner-approved RPI issues, and the research, plan, changes and independent review artifacts in a PR. The issue text states that merged children alone do not satisfy it, and that requirement changes, pivots and deliberate deferrals need owner approval. Writing code would invent work for a process and approval item.

## Live observations (2026-11-19, about 09:48Z)

* `gh issue view`: #134, #150, #152 and #156 CLOSED; #153, #154, #155 and #440 OPEN.
* #155 has one unticked box: measures are aggregate only and the audit-use statement is agreed with staff first (SA-010). That is an agreement with named staff, not a demo-provable item.
* Latest #440 comments (2026-11-16 and 2026-11-17) record unresolved owner decisions on retention of about 4.5 MB of raw checkpoint evidence and on privacy review of a preflight log, plus a retained map browser-check failure (strict-mode match on two `[role=status]` elements). They block publication of that checkpoint, not demo behaviour.
* `az containerapp show` (read-only, existing login): `ca-cutover-test-demo-api` revision `0000033` Running, image digest `sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb`; `ca-resident-demo` revision `0000014`, digest `sha256:65481780cb3f5a55621f637fa783230004b263085dcaece1dfca93a928bbbd19`.
* Local, from `src/api`: `python3 -m unittest tests.test_accessibility_baseline tests.test_content_standard` ran 48 tests, OK. This supports the already ticked accessibility and content criteria locally; it is not whole-epic acceptance.

## Per-criterion table

| # | Criterion | Demo result | Proven or unproven | Why |
| --- | --- | --- | --- | --- |
| 1 | Stabilization checkpoint #440 completed, residuals and owner decisions recorded | Not met | Unproven | #440 open with two unticked criteria and unresolved owner decisions on evidence retention and log privacy. Needs #440 closed and owner approval. |
| 2 | Child features are accepted | Not met | Unproven | Four children closed, but closed is not acceptance (issue text). #153, #154 and #155 remain open; #155 awaits the SA-010 staff agreement. |
| 3 | Accessibility, content and usability evidence recorded as test results | Already ticked | Proven locally for the engineering baseline | 48 local tests pass; earlier ticks and notes preserved. Person-run assistive technology testing is out of demo scope. |
| 4 | Design artefacts traceable to journeys and requirements | Already ticked | Not re-executed | Carried from [screen-design-traceability.md](./ux/screen-design-traceability.md); not re-verified today. |

## Residual actions

* Owner: decide the #440 evidence-retention and preflight-log questions, then record deferral or closure for each open child.
* Owner and staff: agree the SA-010 audit-use statement for #155.
* Engineering: fix the map browser-check strict-mode selector under its own isolated RPI issue, not here.

## Evidence limits

* GitHub and Azure reads are point-in-time. Raw output was not retained beyond the values quoted above.
* Criterion 4 and the closed-child states are carried from earlier records, not re-executed.
