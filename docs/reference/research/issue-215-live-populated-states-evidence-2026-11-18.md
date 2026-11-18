---
title: Regulatory Alert and Home Chat UX, Populated-State Proof on the Live Demo Client (Issue 215, run 2)
description: Second desktop Playwright and axe run for the unticked criteria of issue 215, exercising the deployed client code against explicitly mocked alert and chat responses because the live law store is not loaded
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

Refs #215. This note extends [the first live run](./issue-215-live-alert-chat-ux-evidence-2026-11-18.md), which could only reach the explicit "coverage unknown" state. Read that note first; it is not repeated here.

## Scope and authority

Owner decisions of 2026-11-18: synthetic demo, desktop only, live Azure authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. Nothing in Azure was created or changed, so nothing needed deleting. Sign-in used the owner's credential files at run time; a literal scan of every retained text file for each credential value found no match. Screenshots show no account name.

Target: `ca-cutover-test-demo-api` (image `zava-forward-api@sha256:5368f4e4...`), role `Retrofit Programme Manager`, Playwright Chromium 1366 by 900, 2026-11-18 11:20 to 11:35 UTC. axe-core 4.10.3 (tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`; SHA-256 in `axe-4.10.3.sha256`). Evidence is in `.copilot-tracking/evidence/2026-11-18/issue-215-live/`: `prove.py` (live run), `prove_mocked.py` and `prove_lib.py` (mocked run), `results-live-run1.json`, `results-mocked.json` and the earlier mocked outputs kept as adverse evidence.

## Method and what "mocked" means

The deployed app genuinely signed in and served its real JavaScript. The browser then intercepted these requests and answered them with synthetic JSON written in `prove_mocked.py`: `/api/me` (set `services.law_alerts` true and add the `regulatory_chat` rule role), `/api/law/alerts`, `/api/chat/regulatory/status`, `/usage`, `/threads`, `/ask` and `/doubt`. This proves how the deployed client renders and behaves for populated states. It does not prove the server, a loaded law store, real alerts or real chat answers. The server stays unchanged and nothing was written to the demo.

## Results

| Observation | Result | Evidence |
| --- | --- | --- |
| Live alerts, unchanged from run 1 | `/api/law/alerts` returns 503 with status `unknown`; panel shows the coverage-unknown message and the human hazard route; axe 0 violations, 0 incomplete | `results-live-run1.json`, `live-alert-panel-coverage-unknown.png` |
| Live regulatory chat for this role | Panel states it is not available for the role, with owner and next action; question box disabled; opens by Enter on the summary and closes by Escape with focus back on the summary; axe 0 violations, 0 incomplete | `results-live-run1.json`, `live-regulatory-chat.png` |
| Each alert states what was noticed, source and status, safe action, owner and clock (mocked) | Every alert card carries the definition terms "What was noticed", "Safe action", "Decision owner", "Clock", "Check recorded at", "Current control" and "Latest check", plus a "Source and status" list with status, effective and retrieved dates | `results-mocked.json` (`dt_per_alert`, `alert_first_dd`), `mocked-alerts-populated.png` |
| No colour-only status (mocked) | Each state heading is text ("Status: breach risk", "Status: unknown", "Status: clear") with a distinct border style: 6px double, 4px dashed, 4px solid, and a leading marker. Heading text colour is the same neutral for all three, so colour carries no information | `results-mocked.json` (`state_colours`, `alert_headings`), `mocked-alerts-populated.png` |
| Keyboard operable (mocked and live) | Tab from the plain-language checkbox reaches "Refresh alerts" with a visible focus ring; Space toggles the checkbox; Enter on Refresh re-runs the load; doubt button activates by Enter; focus returns to the Refresh button after reload | `results-live-run1.json`, `results-mocked.json` (`alert_tab_walk`, `chat_doubt_after`) |
| Plain-language mode (mocked) | Switching it off removes the `plain-language` class and sets `display: none` on all 5 plain-explanation paragraphs; on, they show. axe is clean in both states (0 violations, 0 incomplete). The deployed build has no announced mode-state text, as in run 1 | `results-mocked.json` (`plain_off_class`, `plain_off_display`, `alert_axe_plain_on`, `alert_axe_plain_off`) |
| No-source state (mocked) | An alert with no citations and a refused chat turn both show "No source held for this answer. Do not infer a duty or terms; ask the named human owner." plus an "In plain words" line; an alert with no owner or clock shows "Unassigned", "No approved clock held" and "unknown, not calculated here" instead of an invented value | `results-mocked.json` (`no_source_items`, `chat_turns`, `alert_first_dd`) |
| Doubt route (mocked) | Each chat turn has "In doubt: send this turn to Juan Manuel Servera"; after Enter the status reads that it was sent to the exercise inbox with no legal approval or resident message, the button becomes "Sent to exercise owner; awaiting human review" with `aria-disabled` true, and the second turn's button stays active | `results-mocked.json` (`chat_doubt_after`) |
| Chat answer structure (mocked) | An answer shows "What the sources say", "Recorded home facts", "Unknown or missing", "Safe next action" and "Who decides", each with plain-words lines; usage text says model calls are 0 and service cost is Unknown, not zero | `results-mocked.json` (`chat_turns`) |
| axe on populated alerts and chat (mocked) | 0 violations and 0 incomplete for the alerts panel (plain on and off) and the open chat panel | `results-mocked.json` |

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Alert and chat patterns per role with know-at-least content | Already ticked; not re-tested | The role help text for Retrofit Programme Manager was observed live; other roles cannot be signed in (one test employee) |
| 2 | Each alert states what was noticed, source and status, safe action, owner and clock | Already ticked; client rendering proven with mocked data only | Not provable live: the demo law store is not loaded, so no real alert exists. The deployed client renders all fields from a mocked payload |
| 3a | No colour-only status | Proven for client rendering of three states (mocked data); breach-risk, unknown and clear only | Text label, marker and border style per state; attention and not-applicable states were not rendered |
| 3b | Keyboard operable | Proven for the controls reachable by this role | Tab, Space, Enter and Escape recorded; the lookup form submit by Enter was exercised only against mocked responses |
| 3c | Plain-language mode | Proven for show and hide (mocked populated state); announced state text is not in the deployed build | The repository source adds `regulatory-mode-state`; the deployed image predates it |
| 3 | WCAG 2.2 AA as a whole | Unproven; leave unticked | Automated axe and scripted keyboard checks are engineering evidence only; manual contrast on populated states, screen-reader output and other roles were not tested |
| 4 | Doubt route and no-source states designed explicitly | Already ticked; observed again | Live unknown state, and doubt and no-source rendering with mocked data |
| 5 | Comprehension tested with repairs, housing and grants staff before use | Cannot be proven for the demo | Needs real staff participants and a scored session; none exist in the synthetic demo and none may be simulated. The record stays "Not run" |

## Limits and adverse observations

* All populated-state results depend on mocked server responses; none shows real alert logic or data.
* Only one role (Programme Manager) was available; the cited lookup is role-gated, so its live form was never usable.
* The deployed image is older than the repository head: no announced plain-language state, a differently worded "Active bounded control" label and no plain-summary paragraph on alerts. Results describe the deployed build, not head.
* Screenshots capture the viewport, not the full panel; the Tab walk is limited to controls inside each panel, and `Check recorded at` text shows `[email]` because the page mask also rewrites `card@version` strings.
* Early runs failed on a Content Security Policy that blocks script tags (axe was injected by evaluation instead), on a hidden tab panel, and on an Entra sign-in timeout that passed on retry. The earlier mocked outputs (`results-mocked-run1-empty-tabwalk.json`, `results-mocked-run2.json`) are retained.
* The first-run artifacts for #215 on this branch were preserved; this run uses `-r2` and `-state-run1` names.
* Independent exact-head review and hosted CI are outstanding. No criterion is ticked.
