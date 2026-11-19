---
title: Issue 223 first buildable demo criterion (run 3)
description: 2026-11-19 check of whether any unticked criterion on issue 223 can be built or proven for the synthetic demo with new code, with a per-criterion table
author: AMA RPI agent
ms.date: 2026-11-19
ms.topic: reference
keywords:
  - issue 223
  - human review
  - automation bias
  - OQ-017
estimated_reading_time: 3
---

Refs #223. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18. No Azure resource was created or touched; the earlier [run 2 note](./issue-223-live-r2-2026-11-18.md) holds the live retention proof from 2026-11-18, which this run did not repeat.

## Method

* `src/core`: `PYTHONPATH=src:tests python3 -m unittest tests.test_human_review_effectiveness_223` ran 6 tests, OK.
* `src/agents`: `PYTHONPATH=src:../core/src python3 -m zava_forward.agents.review_effectiveness --json` returned `passed: true` with every check true; `tests.test_review_effectiveness` ran 37 tests, OK.

## Result

Every part of #223 that can be built offline already exists and passes: seeded wrong, stale, unsupported and incomplete defects with valid citations, a gate that rejects default acceptance, citation-only and unauthorised review, retained reviewer, source and reason, and scripted effort against workflow-only. The one remaining buildable-looking gap is a live seeded-defect set in the deployed app. That would need a defect-injection route in production code on a review and approval path, which weakens the control the issue exists to test and moves the change into the FULL tier. It was not built.

| Criterion in #223 | Result for the demo | Limit |
| --- | --- | --- |
| Seeded critical defects are detected and prevented from satisfying a controlled gate | Proven offline with a scripted panel; unproven with people or live | Needs competent human reviewers or a production injection route |
| Reviewer, source and reason are retained | Proven offline; live route proven in run 2 | Not re-run here |
| Detection, corrections and total review effort are reported against the same workflow-only scenarios | Proven as scripted reporting; unproven as measurement | Measured effort needs a person to complete the worksheet |
| Default acceptance and citation validity alone cannot pass | Proven offline | Not shown with human reviewers |
| Automation-bias test included; reviewer authority and evidence defined (OQ-017) | Test proven offline; authority unproven | No OQ-017 holder is appointed |

Every remaining criterion is human-only or production-only, so no box is ticked and no source change was made.
