# Research: issue 233 withheld panels on evidence screens

Date: 2026-11-04. Disposition: executed (reused prior 233 research). Planning readiness: Ready.

* Already merged (not redone): #671 trace, #713 drift, #767 guardrails, #815 and #838 withheld panels on programme-queue and resident-choice, #935 stage map, #970 and #1135 utilisation versus choice text, #980 stage map drift check.
* Gap: criterion 2 (continuity versus disclosure) shows the "Not shown for this role" panel on programme-queue, resident-choice, procurement-packages and contractor-job-pack, but not on the per-home `technical-queue` and `quality-queue` evidence screens that the stage map links to (stages 2 and 6).
* Smallest slice: one withheld panel on each, a source-level test, trace doc note. Web text only. Focused tier; no security, infrastructure, SQL or deployment change; the gate is not run.
* Cannot be proven here: rendered behaviour, EX-HOME-901 fixture and stage 1 screen, WCAG 2.2 rendered or AT evidence (#151), component verification (#150), user validation (#155).
