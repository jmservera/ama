---
title: Issue 93 live plan (2026-11-23)
ms.date: 2026-11-23
---

* [ ] P1 Register the #2312 eval files in the provenance register and add a schema description.
* [ ] P2 Run test_form_review_pack, test_synthetic_provenance, test_eval_harness, then re-run the 12-module offline set.
* [ ] P3 Write docs/reference/research/issue-93-criteria-recheck-live-2026-11-23.md, index row, log entry.
* [ ] P4 Changes record with per-criterion table, review, one local commit.

Tier: FULL classification (src/agents/evals touched, test-gate semantics); only targeted checks run locally; coordinator runs the gate. Regression test: the existing registration test is the regression test (it failed before, passes after).
