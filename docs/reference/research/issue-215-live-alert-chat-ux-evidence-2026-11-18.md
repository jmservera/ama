---
title: Regulatory Alert and Home Chat UX Live Demo Proof (Issue 215)
description: Desktop Playwright and axe evidence from the deployed synthetic demo for the unticked criteria of issue 215, with what could not be proven and why
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: this is the synthetic demo, desktop only. Live
Azure was authorised (resource group `ama`, cap USD 700, no drills, no Key
Vault rotation, no production change). Person-run assistive-technology testing,
DPO and Legal approval and billing reconciliation are not needed for the demo.
Nothing in Azure was changed or created, so nothing needs deleting. Credentials
were read from the owner's files at run time and never printed; a literal scan
of every retained text evidence file for each credential value found no match,
and the screenshots were viewed and show no account name or secret.

Targets: `ca-cutover-test-demo-api` (image `zava-forward-api@sha256:5368f4e4...`,
Entra sign-in, role `Retrofit Programme Manager`) and `ca-resident-demo`.
Browser: Playwright Chromium, 1366 by 900 desktop, 2026-11-18. axe-core
with tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa` was injected
from a local copy (not committed). Scripts, redacted JSON and screenshots are in
`.copilot-tracking/evidence/2026-11-18/issue-215-live/`.

Issue #215 has two unticked criteria: WCAG 2.2 AA behaviours (no colour-only
status, keyboard operable, plain-language mode) and comprehension testing with
staff. The local protocol is
[regulatory-ux-acceptance-protocol.md](./ux/regulatory-ux-acceptance-protocol.md).

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Law alerts service on the demo | `/api/me` reports `services.law_alerts` false; `/api/law/alerts?case=...` returns 503 with status `unknown`, "The law store is not loaded; rule checks are unknown." and a safe route to the human emergency or hazard service | `employee-run1.json` |
| Alerts panel on a real demo case (16 cases listed; panel under "Blockers and safety") | The only state reachable live is the explicit unknown state: "Alert coverage unknown: the law store is not loaded, so no rule checks have run. Use the existing human emergency or hazard service; do not wait for checks." It is led by a `?` marker and the word "unknown", so status is not colour alone. 0 alert cards render | `employee-run1.json`, `alerts-1-panel-plain-on.png` |
| Hazard route above the alerts | A notice states the human emergency route is used now and nothing waits for alerts or chat | `alerts-1-panel-plain-on.png` |
| Doubt route | Role help names the exercise Legal, Compliance and DPO owner with "synthetic-demo review only" wording | `alerts-1-panel-plain-on.png` |
| axe on the alerts panel | 0 violations, 0 incomplete, 15 passes | `employee-axe-keyboard.json` |
| Keyboard walk | Tab reaches the plain-language checkbox, then "Refresh alerts", then continues out of the panel; Space toggles the checkbox; Enter on Refresh re-runs the load and keeps the unknown message; focus ring is 3px solid plus a 2px amber shadow | `employee-axe-keyboard.json`, `employee-run1.json`, `alerts-2-panel-plain-off.png` |
| Plain-language toggle | Defaults to on and toggles by keyboard. In the unknown state it changes nothing visible (no element carries the plain explanation class) and the deployed build has no announced state text (`.regulatory-mode-state` absent), unlike the repository source | `employee-run1.json` (`mode_html`, `plain_mode_state_text` null), both `alerts-*` screenshots |
| Reflow | At 683 CSS pixels wide (200 percent zoom equivalent) the page has no horizontal scroll | `employee-axe-keyboard.json` |
| Cited regulatory lookup for this role | On the "AI assistance" tab the panel says it is not available for the role, names the owner and next action, and states safety and alerts do not depend on chat; the question box is disabled, so no lookup was sent | `employee-axe-keyboard.json` |
| Home chat launcher (employee) | Visible, opens by Enter, dialog is labelled, focus moves into it, Escape closes it and focus returns to the launcher; axe 0 violations, 1 incomplete, 20 passes. The dialog states demonstration only, AI-generated, may be wrong, no DPO, Legal or RAI approval, and tells users not to enter personal data. No message was sent (that would call a real model) | `home-chat-run1.json`, `homechat-1-open.png` |
| Resident app | Shared demo sign-in works (HTTP 200); home page shows the synthetic-showcase and "Legal and DPO review outstanding" banners; a chat launcher exists; no regulatory alert UI is present, which matches the staff-only design | `home-chat-run1.json`, `resident-1-home.png` |

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Alert and chat patterns defined per role | Already ticked | Not re-tested here |
| 2 | Each alert states what was noticed, source and status, safe action, owner and clock | Already ticked; not provable live | No alert card can render: the demo law store is not loaded, so `alert_articles` is 0. The unknown state was shown instead. The card fields stay proven by the repository tests only |
| 3a | No colour-only status | Partly proven | The one live state carries a `?` marker and the word "unknown" and passes axe. Other states (breach risk, attention, clear) cannot be produced on the demo without a law store |
| 3b | Keyboard operable | Proven for the controls the demo exposes | Tab, Space and Enter walk and focus ring above; chat dialog opens by Enter and closes by Escape with focus returned. Controls that exist only with a loaded law store (cited lookup, acknowledge) were not reachable |
| 3c | Plain-language mode | Partly proven | The toggle exists, defaults on and is keyboard operable, but in the live unknown state it has no visible effect and no announced state, so the demo does not show it working. The repository source adds the announced state, so the deployed image is older than the repository head |
| 3 | WCAG 2.2 AA as a whole | Unproven, not claimable | axe and scripted keyboard checks are engineering evidence only. The owner waived person-run assistive-technology testing for the demo, and the WCAG baseline says automation does not establish conformance. Leave unticked |
| 4 | Doubt route and no-source states designed explicitly | Already ticked | The live unknown state and doubt-owner text were observed |
| 5 | Comprehension tested with repairs, housing and grants staff | Cannot be proven for the demo | It needs real staff participants, task cards and a scored session. No such staff exist in the synthetic demo and no one may be simulated. The kit and scoring tool exist; the record stays "Not run". Leave unticked |

## Gaps found

* The live demo cannot show any alert card or cited answer until a law store is
  loaded on `ca-cutover-test-demo-api`. That is an existing configuration fact,
  not a regression, and was not changed here.
* The deployed image lacks the announced plain-language state present in the
  repository source, so a redeploy is needed before the plain-language mode can
  be proven live. This note does not change source or redeploy.

## Observed incidents

* One sign-in run timed out in Entra before the callback; a retry after 20
  seconds succeeded. Early scripts failed on selectors and a hidden tab; the
  failures are not hidden and the final scripts are retained.
* The resident app cold start (minimum replicas 0) timed out the first page
  load; a `curl` warm-up fixed it.
