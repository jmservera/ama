---
title: Issue 223 research, meaningful human-review effectiveness harness
ms.date: 2026-11-17
---

## Scope

Deterministic synthetic harness only. No real reviewers, no approvals invented, desktop demo only. Tier FOCUSED. Refs #223 (all five criteria stay unticked: no competent real participants, no appointed OQ-017 holders).

## Research disposition: executed

Evidence read: issue 223 and its three comments (closure audits 2026-10-31, 2026-11-05, 2026-11-16), `src/agents/src/zava_forward/agents/review_effectiveness.py`, `src/agents/tests/test_review_effectiveness.py`, `src/agents/evals/review_effectiveness_golden.json`, `src/agents/README.md` review-effectiveness section.

## MEASURE (baseline, base eb51af5c)

Run with worktree sources on PYTHONPATH. The installed `zava-forward-agents` in user site-packages shadows the worktree and has no `evals/` file, so the CLI fails with FileNotFoundError unless PYTHONPATH points at `src/agents/src`; this is an environment issue, not a repository defect.

* `python3 -m unittest test_review_effectiveness -q`: 34 tests OK.
* CLI: competent 4 of 4 detected, gate PASS; default_accept 0 of 4, FAIL; automation_bias 0 of 4, FAIL; workflow-only effort 24 vs competent 23; all 9 checks PASS.

Probe of extra scripted panels against the real `Store.ai_run` and `Store.review_ai` path:

| Panel | Gate | Detected | Note |
| --- | --- | --- | --- |
| reject everything with a resolving source | FAIL | 0 of 4 | two controls falsely rejected |
| competent but accepts exactly one defect (each of the four classes in turn) | FAIL each time | 3 of 4 | gate refuses the accepted defect |
| competent but accepts one control | PASS | 4 of 4 | correct, controls may be accepted |

## Finding

No gate defect reproduced. The gate already refuses each adversarial panel above, but the committed report never measures them: `run_review_test` reports only competent, default-accept, automation-bias and unauthorised panels. The criterion "seeded critical defects are detected and prevented from satisfying a controlled gate" is evidenced for a reviewer who misses all defects, not for one who misses exactly one defect class or who over-rejects. Leave-one-class-out sensitivity and an over-rejecting panel are the smallest missing measurement.

## Planning readiness: Ready

Add leave-one-class-out and over-rejecting scripted panels to `review_effectiveness.run_review_test`, two new checks, a report `sensitivity` section, regression tests and a README note. Evidence boundaries unchanged: scripted panels are not people; OQ-017 stays open.
