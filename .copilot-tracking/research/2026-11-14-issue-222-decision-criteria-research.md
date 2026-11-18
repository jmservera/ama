---
title: Issue 222 decision criteria research
ms.date: 2026-11-14
---

## Question

Does the repository already evaluate continue, narrow, pause or retire per AI feature against
safety, accuracy, reviewer effort and cost thresholds?

## Evidence

* `src/core/src/zava_forward/core/ai_registry.py`: `chat_entry` holds only proposed, unapproved
  safety-style thresholds (critical_failures, pass rates) with no outcome mapping, and no cost or
  reviewer-effort criteria. Other tasks carry no thresholds.
* `rai_metrics.py` reconstructs invocation, override, human_review and token counts from audit events;
  these can feed observed values but nothing decides on them.
* `cohort_eval.py` and tests (`test_rai_threshold_live_approval_guard.py`) gate activation on
  named-human approval of constructed thresholds; the same boundary is reused here.
* `docs/reference/research/rai/project-rai-review.md` B05/B06 list #222 as needing reviewer-burden and
  missed-safety evidence and named approval.

## Finding

No deterministic decision module exists. Planning Readiness: Ready. Research disposition: executed.

## Decisions and boundaries

* Recommend only; a named accountable person decides. Unapproved criteria are advisory.
* Missing, malformed or under-sampled evidence fails closed to pause.
* Threshold values in tests are illustrative; real values need owner approval (open item).
