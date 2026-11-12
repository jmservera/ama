# Plan: add source-completeness dimension to paired_equity (Refs #128)

Research: [research](../../research/2026-11-12/issue-128-cohort-trace-1112-research.md). Details: [details](../../details/2026-11-12/issue-128-cohort-trace-1112-details.md). Critique: [critique](issue-128-cohort-trace-1112-critique.md).

* [x] Phase 1: failing-first tests (source pair fixture, seeded source defect, required dimension, confounded source pair)
* [x] Phase 2: add `source_completeness` to `DIMENSIONS` and `CONTRASTS` (`source_record`: complete -> missing)
* [x] Phase 3: focused validation (test_paired_equity, ruff, mypy, test_journey_register)
* [x] Phase 4: README and equity test plan wording; KB log entry

Tier: focused (constructed-fixture diagnostic only; no security, infrastructure, SQL, deployment, workflow or dependency change). No full gate, no push, PR or merge.

Behaviour note: the new dimension is required like the others, so a caller supplying no source pair now gets a `source_completeness:no_pairs` blocker. Only tests call `evaluate`.

Process disclosure: the failing tests were written and run red before the production edit, but the independent critique ran on this plan plus the draft candidate, not before any code existed.
