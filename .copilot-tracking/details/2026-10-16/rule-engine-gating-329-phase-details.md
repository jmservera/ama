---
title: RPI Phase Details - Rule engine gating regressions
description: Test ownership and execution boundary for issue 329
ms.date: 2026-10-16
---

## Metadata

* Task ID: 329
* Task slug: rule-engine-gating-329
* Plan: .copilot-tracking/plans/2026-10-16/rule-engine-gating-329-plan.md
* Evidence: issue 329; rule_engine.py; test_rule_engine.py; core README; ADR 0006.

<!-- rpi:phase id=P01 -->
## P01: Pin behavior and publish verified evidence

Initial direction: keep the current rule engine unless new regressions expose
a real defect. Existing source assertions are permissive and same-episode
deduplication can conceal broken shared throttling. No open product decisions.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add focused regressions and repair a demonstrated defect

* Tighten consultation/historical/future source expectations to exactly not
  applicable; partial/unreviewed/stale/missing remain exactly unknown. Retain
  citation status and verify no alert rows, not just the filtered open view.
* Use a long synthetic clock so attention remains attention beyond 24 hours.
  Write another case for the same home and alter awareness/due time on the same
  case. Assert distinct checkpoint/check IDs, revisions and due times as
  applicable, with no new publication during the shared window.
* Assert just before 24 hours is suppressed and exactly 24 hours publishes.
  Every attempt must retain its check/checkpoint. Force schedule evaluations
  or revisions so retries do not merely return the original checkpoint.
* Cover independent home/card/step/item keys and breach bypass after an
  attention publication on another case.
* Test owner: src/core/tests/test_rule_engine.py; no removals; at most six new
  methods. Extend fixture card ID only as needed. No real datasets or services.
* Completion evidence: new tests pass; any original-code failure has a minimal
  root-cause fix and a mutation that restores the defect.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Validate, document and deliver

* Depends on P01-T01. Install src/core[dev] editable with pip in a session venv
  after the initial missing-package failure. Run core unittest discovery,
  ruff check ., ruff format --check . and mypy from src/core.
* Mutate citation consultation and historical guards independently, and disable
  the shared throttle without removing episode deduplication. Load mutations
  in memory and require the intended assertion failure; never persist broken
  package files. Record exact failed tests and baseline results.
* If core behavior changes, add relevant installed-package downstream suites;
  otherwise the full core suite covers the test-only change.
* Update src/core/README.md, docs/reference/README.md routing and append only
  docs/reference/log.md. One post-implementation rpi-review; no review loop.
* Authenticate GitHub identity; set local privacy-safe author/committer email,
  Conventional Commit plus Copilot trailer. Push without force, open PR to main
  with Refs #329 and no issue-closing keyword. No merge.
* Completion evidence: changes/review artifacts, passing validation, mutation
  assertion failures and remote branch/PR URL. Hosted checks are separate.

## Unresolved Items

* None. Additional legal, human and live-platform acceptance is outside this
  regression-only slice, not approval granted by synthetic tests.

## Current Execution Evidence

* P01-T01 complete: three new tests and one tightened source-gating test. Original
  implementation passes unchanged; no root-cause production fix was needed.
* P01-T02 code/docs and local validation complete: 20 targeted tests; 466 full
  core tests with one explicit Azure opt-in skip; Ruff lint/format and mypy
  passed; nine in-memory mutations rejected by intended assertions.
* Implementation evidence:
  .copilot-tracking/changes/2026-10-16/rule-engine-gating-329-changes.md.
* One post-implementation Review complete, Conformant, no findings:
  .copilot-tracking/reviews/logs/2026-10-16/rule-engine-gating-329-review.md.
* P01-T02 complete: commit f5b297b, non-forced branch push and open
  https://github.com/jmservera/ama/pull/334 to main. Verified references-only
  body and empty closingIssuesReferences. No source or validation blocker.
* Hosted checks were queued/running at publication. Owner retains merge decision.
