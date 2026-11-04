# Research: issue 233 choice-before-capacity on resident-choice

Date: 2026-11-04. Disposition: executed. Planning readiness: Ready.

* Already merged (not redone): #671 trace and checker, #713 status drift, #767 guardrails, #815 and #838 withheld panels, #935 stage map, #970 utilisation rule on the package screen, #980 stage map drift check. PR 495 closed unmerged.
* Gap: criterion 2 (utilisation versus choice) is stated only on `procurement-packages`. The per-home `resident-choice` view says nothing about offered capacity, so the choice-first side of the resolution is not shown where the resident choice is read.
* Smallest slice: one text panel on the per-home `resident-choice` view after the choice, withdrawal and service request panels, a source-level test, trace doc update. Web edit is minimal (one panel). Focused tier; no security, infrastructure, SQL or deployment change; the gate is not run here.
* Cannot be proven by this slice: rendered behaviour, same-home fixture EX-HOME-901 and stage 1 screen, WCAG 2.2 rendered or assistive-technology evidence (#151), component verification (#150), user validation (#155), deferred theme "Prevention through rehearsal".
