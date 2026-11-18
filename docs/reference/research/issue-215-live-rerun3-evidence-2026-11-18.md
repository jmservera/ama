---
title: Regulatory Alert and Home Chat UX Live Demo Re-verification (Issue 215, run 3)
description: Third desktop Playwright run on the deployed synthetic demo; confirms the law store is still not loaded, characterises the chat axe incomplete item and records a per-criterion proven or unproven table
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

Refs #215. This note builds on [run 1](./issue-215-live-alert-chat-ux-evidence-2026-11-18.md) and [run 2](./issue-215-live-populated-states-evidence-2026-11-18.md). Read them first; their results are not repeated.

## Scope and authority

Owner decisions of 2026-11-18: synthetic demo, desktop only, live Azure authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. Nothing in Azure was created or changed (only `az containerapp show` reads), so nothing needed deleting. Credentials were read from the owner's files at run time and never printed; a literal scan of every retained text file in the evidence folder for each credential value found no match.

Target `ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000031`, image `zava-forward-api@sha256:5368f4e4...` (unchanged since run 1); resident app image `zava-resident-demo@sha256:65481780...`. Browser: Playwright Chromium 1366 by 900, 2026-11-18 about 14:30 UTC, axe-core 4.10.3 (SHA-256 in the run 1 folder). Evidence: `.copilot-tracking/evidence/2026-11-18/issue-215-live-r3/` (`run3.py`, `run3_contrast.py`, `run3-results.json`, `run3-contrast.json`). Two screenshots were taken and viewed during the run but are not retained.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Law store state | `/api/me` still reports `services.law_alerts` false; `/api/law/alerts?case=ZF-2025-0331` returns 503, status `unknown`, "The law store is not loaded; rule checks are unknown." plus the human hazard route. 0 alert cards render | `run3-results.json` |
| Alerts panel text | Hazard notice first, then plain-language explanations, then the doubt route naming the exercise owner. Still no announced mode-state text (`.regulatory-mode-state` count 0) | `run3-results.json` |
| Home chat open (correct capture) | Enter on the launcher opens a labelled dialog; the demonstration-only, AI-generated, no-approval and no-personal-data notices are shown; Escape closes it and focus returns to `employee-chat-launcher`. This replaces the defective `chat-1` and `chat-2` captures of run 1 | `run3-results.json` |
| axe on the chat dialog | 0 violations, 20 passes, 1 incomplete: `color-contrast`, "background color could not be determined because it partially overlaps other elements", on `#chat-demo-disclaimer`, `#employee-chat-question` and `#employee-chat-unsupported`. This characterises the run 1 incomplete item | `run3-results.json` |
| Manual contrast of those three elements | Computed from the nearest opaque ancestor background: 15.52, 15.52 and 10.05 to 1, all above 4.5 to 1. This is an engineering calculation, not an accessibility finding, and does not resolve the overlap caveat | `run3-contrast.json` |
| Visual clipping (adverse) | In a screenshot (observed; screenshot not retained) the helper line "Press Enter to send. Press Shift and Enter for a new line. Press Escape to close the chat." is cut off at the bottom edge of its scroll area at 1366 by 900 (the last words are partly hidden). Not investigated further; routed as a follow-up | Observed; screenshot not retained |
| Chat overlay | The open chat is a non-modal panel that covers the right of the page content, including part of a blocked-step card | Observed; screenshot not retained |
| Message send | Not done: it would call a real model, which the brief excludes | n/a |

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Alert and chat patterns per role | Ticked already; not re-tested | One test employee, so other roles cannot be signed in |
| 2 | Each alert states noticed, source and status, safe action, owner, clock | Ticked already; live proof not possible | Law store not loaded (re-confirmed); card fields proven only against mocked data in run 2 and repository tests |
| 3a | No colour-only status | Partly proven | Live unknown state has `?` and the word "unknown"; breach risk, unknown and clear proven with mocked data in run 2; attention and not-applicable not rendered |
| 3b | Keyboard operable | Proven for reachable controls | Run 1 and 2 Tab, Space, Enter, Escape walks; run 3 confirms Enter open, Escape close and focus return for the home chat |
| 3c | Plain-language mode | Partly proven | Show and hide proven with mocked data (run 2); no announced state in the deployed build, which predates the repository source |
| 3 | WCAG 2.2 AA overall | Unproven; leave unticked | Automation is engineering evidence only; one axe incomplete is contrast overlap uncertainty; the clipped helper line is an open visual finding; person-run assistive-technology testing is waived for the demo, so no conformance claim is made |
| 4 | Doubt route and no-source states | Ticked already; observed again | Live unknown state and doubt owner text; no-source wording proven with mocked data (run 2) |
| 5 | Comprehension tested with repairs, housing and grants staff | Cannot be proven for the demo | Needs real staff and scored sessions; none exist in the synthetic demo and none may be simulated. The record stays "Not run" |

## Open items

* Load a law store on the demo API and redeploy the current image to prove criteria 2, 3a and 3c live. That is an infrastructure and deployment change outside this run.
* Check the clipped helper line in the employee chat panel and the contrast overlap with a manual pass.
* Independent exact-head review and hosted CI stay outstanding. No criterion is ticked.

## Incidents

* The first script run failed on a typo in the axe incomplete extraction; the corrected script is retained as `run3.py`. No sign-in or network failures occurred.
