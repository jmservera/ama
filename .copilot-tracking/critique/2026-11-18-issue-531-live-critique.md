---
title: Issue 531 live verification critique
description: One final-candidate critique of the live verification plan and evidence note
ms.date: 2026-11-18
---

## Execution

Executed once, by the RPI worker against the final candidate: the research note, probe script and per-criterion table. No separate agent was dispatched.

## Findings and dispositions

| ID | Finding | Disposition |
| --- | --- | --- |
| CR-001 | Simulated steps (held script, aborted `ops.js`, rewritten briefing response) could be read as live proof of cold start, retry and AI output. | Applied: every simulated row is labelled "Simulated" and the evidence limits and criterion table say so. |
| CR-002 | Deployed `app.js` and `style.css` differ from main, so "live on main" would overclaim. | Applied: asset hashes compared and the diff checked for briefing and loading code; the inference is flagged as an inference. |
| CR-003 | Recording a review live is irreversible and not needed to prove wording and reason rules. | Applied: controls opened and cancelled, zero `/api/ai/review/` requests asserted. Behaviour tests stay with the local suite. |
| CR-004 | Forcing scale to zero would be a production-style change and disturb other workers. | Applied: not done; stated as unproven. |
| CR-005 | Criterion 7 tick is the owner's call. | Applied: the note states the evidence and the open limits and does not tick the issue. |

Verdict: proceed. No finding conflicts with a confirmed owner decision.
