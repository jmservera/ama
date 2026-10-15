---
title: Issue 122 service continuity research
---

Task: issue #122 (parent #113). Disposition: executed. Planning Readiness: Ready.

## Evidence

* Acceptance: disable mechanism and tested manual fallback; versioned, evaluated, reversible model/rule/config changes; export retaining evidence independent of the AI supplier; RAI suspension and restart controls.
* Pattern: `mvp/zavaforward_mvp/governance.py` (breach and restart), `controls.py` helpers, `assistants.py` independent SQL connection runtime, `sqlstore.py` `DOCS` meta persistence.
* Owner rules: ADR 0005 synthetic-labelled fixtures only; Azure-only deployment; AI stays in prototypes.

## Decisions

* One new `ContinuityMixin` document persisted with existing meta docs; epoch-based suspension; quarantine of late results.
* No supplier-specific code in the export.

## Unknowns (open, not invented)

* Witnessed drill, recovery and response limits, supplier terms, Azure SQL drill evidence, interface identifier mapping, named restart authority.
