# Research: issue 233 stage map drift check

Date: 2026-11-03. Disposition: executed. Planning readiness: Ready.

* Already merged (not redone): #671 trace and checker, #713 status drift, #767 guardrails, #815 and #838 withheld panels, #935 stage map, #970 utilisation rule.
* Gap: the stage map in `role-screens.js` (#935) duplicates the walkthrough table; nothing detects drift between them.
* Smallest slice: extend the offline checker in `src/core`. No screen, security, infrastructure, SQL or deployment change. Focused tier.
* Not implementable without owner input: the deferred theme "Prevention through rehearsal", stage 1 source-account screen, EX-HOME-901 fixture, rendered WCAG evidence (#151), component verification (#150), user validation (#155).
