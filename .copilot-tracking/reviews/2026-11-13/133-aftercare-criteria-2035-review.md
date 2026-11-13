---
title: Issue 133 aftercare criteria review
task_id: 133-aftercare-criteria-2035
date: 2026-11-13
---

Execution: one self-review of the final diff after validation. Outcome: conformant for software scope, with human gates open. No independent exact-head review or hosted CI was performed.

| Criterion | Software status | Evidence |
| --- | --- | --- |
| 1 Accessible and non-digital route | Staff-assisted phone, in person, paper and assisted visit with representative basis proven. No resident self-service portal exists. Human assistive-technology sign-off remains | `test_non_digital_route_needs_staff_and_channel`, `test_every_channel_is_accepted_and_digital_is_not`, browser check |
| 2 Owner, outcome, remedy kept | Proven at register, service and restart level; restore refuses unevidenced closed remedies | new closure tests in `test_aftercare*.py` |
| 4 Evaluator view | Payload and rendering show baseline, outcomes, unresolved fractions, households fraction, scope and unknowns | `test_aftercare_screen.py` |
| 5 No causation, blame, savings | Guard widened for templates, packs, notices and web strings; the lexical guard is best effort | `test_aftercare.py` phrasing tests |
| 6 Optional AI pack | Registered, disabled, unapproved; owner review only; no API route; proposing leaves the record equal | pack tests |

Open items routed to later work: human assistive-technology sign-off, evaluator role access, DPO position, resident self-service route decision, partial-baseline display choice. The lexical guard cannot prove the absence of all causal language, so human review stays required. Criteria are not ticked and issue #133 was not edited.
