---
title: Issue 531 residual scope research
ms.date: 2026-11-01
---

* Task: issue-531-briefing-feedback. Research disposition: executed (code and docs read; no live access).
* Evidence: merged #538, #581 and #604 already deliver the startup shell (`workspace-shell.js`, `index.html`), script-retry messaging, per-panel `AsyncAction` feedback, outcome-worded review buttons (Use this draft, Edit this draft, Do not use this draft), source lists, unverified labelling, prepared-at time and the HAX mapping in `src/api/README.md` (HAX design mapping).
* Existing check: `src/api/checks/loading_briefing_browser_check.py` covers cold start, retry, review outcomes and pinned axe 4.10.3.
* Gap found: the issue asks the briefing to say how to give feedback or correct it; no visible statement existed (G15 in the mapping was implicit).
* Unmet and out of scope: acceptance criterion 7, live employee-site verification. No live sign-in, Azure change or assistive-technology claim is allowed.
* Planning Readiness: Ready.
