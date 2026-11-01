---
title: "Issue 221 research: operator suspension, incident and restart record"
ms.date: 2026-11-01
---

* Disposition: executed (repo evidence review). Planning Readiness: Ready.
* Criteria 1-4 are delivered and merged (#419, #504): `src/core/src/zava_forward/core/continuity.py`, `src/api/tests/test_operator_suspension.py` (16 tests, green at baseline).
* Criterion 5: incident records carry `restart_authority`; restart requires matching `authority_ref`, distinct person and trusted `ai_restart` capability. Actual OD-35/RULE-024 appointment is a human decision, not evidenced.
* Criterion 6: constructed drill exists (`test_manual_hazard_drill`); human-witnessed drill and competent corrective-test acceptance unmet.
* Gap addressable in code: no single test tying breach record, named authority, restart denial and manual fallback together.
* Follow-ups: (1) human appointment of OD-35 authority; (2) witnessed actual drill (#122 preparation).
