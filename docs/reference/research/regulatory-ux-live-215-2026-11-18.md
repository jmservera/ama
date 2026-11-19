---
title: Regulatory Alerts and Home Chat Live Proof on the Synthetic Demo (#215)
description: Playwright evidence for the WCAG, keyboard and plain-language criterion of #215 on the live demo, and why staff comprehension testing stays unproven
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope

Two criteria of #215 are unticked: "WCAG 2.2 AA: no colour-only status, keyboard operable, plain-language mode" and "Comprehension tested with repairs, housing and grants staff before use". The other three are ticked and were not reopened. Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure authorised, person-run assistive-technology testing and DPO or Legal approval not needed. No source code changed, and no Azure resource was created or modified.

## Target

`ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000032`, image digest `sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb`. Signed in as the staff test user (credentials read at runtime, never printed). Case `ZF-2025-0122`, desktop viewport 1440 by 900. Axe-core is the pinned copy with SHA-256 `880970c0...8a68bb`, verified by the probe before use.

## Method

* [login.py](./regulatory-ux-live-215-2026-11-18/login.py) signs in and writes a scratch session (deleted after use).
* [probe-alerts.py](./regulatory-ux-live-215-2026-11-18/probe-alerts.py) reads the alerts panel, walks it by keyboard, toggles plain-language mode with Space, runs axe (WCAG 2.0/2.1/2.2 A and AA tags) on the alerts panel and the cited-lookup panel, measures target sizes and strips colour to check status text. Raw output: [probe-alerts.out.json](./regulatory-ux-live-215-2026-11-18/probe-alerts.out.json).
* Screenshots: the three captures showed a named staff member and are not retained; the script writes them to the folder given as its second argument.

## Results

| Check | Observed |
| --- | --- |
| Alerts panel state | Zero alerts. Status text: "Alert coverage unknown: the law store is not loaded, so no rule checks have run. Use the existing human emergency or hazard service; do not wait for checks." The panel carries the `state-unknown` class and the status is words, not colour |
| Role guidance and doubt route | Role help text and "In doubt:" owner line present; hazard route notice shown first |
| Keyboard, alerts panel | Tab path: plain-language checkbox, then "Refresh alerts"; both show a 3px solid outline plus shadow on focus |
| Plain-language mode | Space unchecks the box; the panel class drops `plain-language`; Space restores it |
| Axe, alerts panel | 0 violations, 0 incomplete, 16 passes |
| Target size | No control under 24 by 24 CSS pixels |
| Colour removed | Status label text is unchanged with all colours forced to black on white |
| Cited lookup panel | Reached through the "AI assistance" tab (Enter), the outer "Ask the assistant" disclosure (Enter) and the lookup summary (Enter). Escape closes it and returns focus to the summary |
| Axe, lookup panel | 0 violations, 0 incomplete, 18 passes |
| Lookup controls | Question box and "Look up cited sources" are disabled because the law store is not loaded; the doubt inbox button is enabled |

## Verdict

| Part of the criterion | Verdict |
| --- | --- |
| Keyboard operable | Proven live on desktop for the panels reachable now |
| Plain-language mode | Proven live: toggle works by keyboard and changes the panel state |
| No colour-only status | Proven for the one state the live demo can show (unknown, stated in words). Alert states breach risk, attention, clear and not applicable cannot be rendered live because the law store is not loaded; they stay covered only by the local fixture check `regulatory_ux_check.py` and unit tests, not re-run here |
| WCAG 2.2 AA as a whole | Automated axe pass on two panels only; manual AT testing is excluded by the owner. The criterion therefore remains unproven as written |
| Comprehension tested with staff | Unproven and unprovable here. It needs repairs, housing and grants staff to complete a task set; no such participants or recorded results exist, and automation cannot substitute for them |

The issue boxes should stay unticked unless the owner accepts the live automated evidence for the demo (criterion 3) and the absence of staff testing (criterion 5).

## Observations and limits

* The live image differs from `main`: the deployed plain-language toggle is a bare label wrapping the checkbox, with no `regulatory-mode-state` announcement element that current `chat.js` renders. Live proof therefore describes the deployed build; the announcement behaviour in source was not observable. Redeploying is a production change and was not done.
* The law store being unloaded means the live demo cannot show real alert content (what was noticed, source and status, safe action, owner and clock); that part of ticked criterion 2 was not re-proven live.
* Single run, one case, one account.
