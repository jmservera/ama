---
title: Issue 216 round 2 research
ms.date: 2026-11-03
---

* Issue #216 text treated as data. Prior merged PRs: #355 and #506 (synthetic gates, 60,000-home baseline, cadence labels), #632 (re-verification), #684 (owner-authorised limit guard), #834 (paired staff trial scorer). Disposition: Research reused (existing evidence adequate); Planning Readiness: Ready.
* Checked boxes already proven: hazard misses critical, recall baseline before thresholds, out-of-cadence labels, per-check reporting.
* Unmet: owner-set citation and refusal gates on an independent graded set; measured paired value (needs a staff trial); tokenomics cost per accepted check (Unknown); owner-authorised live run.
* Gap named in the issue summary but without code: alert precision and acknowledgement time. The recorded report lists both as `not_evaluated` (`src/agents/tests/regulatory_gate_fixture.py`).
* Smallest coherent slice: a pure scorer for staff alert precision and acknowledgement time, mirroring `paired_trial.py`. Stacked follow-ups: owner threshold agreement, staff trial data capture, continuing-stock baseline.
