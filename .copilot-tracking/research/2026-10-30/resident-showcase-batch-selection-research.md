<!-- markdownlint-disable-file -->
---
title: Resident showcase batch selection research
description: Focused research for the PR 590 regression-test correction
ms.date: 2026-10-30
---

## Research Brief

Correct stale SQL view batch selection in the resident showcase tests. Audience:
PR 590 reviewers. Refs #521. Output mode: convergence, preparing planning.
Scope: the named test module, its SQL input and local validation contracts.
No Azure access, push, production SQL change, issue closure or unrelated work.

## Research Parameters

Focused posture, selected from the caller's narrow correction and supplied
failure evidence. Evidence root: `.copilot-tracking/research/2026-10-30/`.
Questions: which indexed selections are stale; how to select the view by
content; how to prove sensor-table projection rather than fallback execution?

## Direction Controls

Use the existing branch and PR 590. Commit locally with Conventional Commits
and the required Copilot trailer. Use Refs only. Run the file's unit tests and
Ruff check/format from `src/core`; serialize heavy runs with the shared lock.

## Extension Registry and Provenance

Repository instructions and RPI skills selected for evidence and local workflow.
Research-specialist delegation skipped: one tightly coupled test/SQL trace.
Web, regulatory and Azure extensions not applicable to this test-only change.
Prior-knowledge gate: caller's defect report awaits source verification;
recent branch session lookup returned no reusable research.

## User Participation and Research Decisions

The user explicitly requested the complete loop; no routine phase questions
are necessary. Automatic execution is bounded to this correction and local
commit, not publication or a new follow-up.

## Research Cycle Log

Cycle 1, Wider: inventoried the full named test module, renderer and SQL batch
boundaries. Exactly two `script.render(USER)[N]` calls exist, both index 2
inside the empty-sensor test; both are stale (C1-C2).

Deeper: setup initially creates the no-sensor fallback view. The optional-table
branch sets `sensor_home_id` from case stock ID, whereas the fallback emits NULL.
Both branches emit `[]` for empty history. Reflection: assert both the home ID
and empty JSON to distinguish real projection without populating empty tables (C3).

Contrarian: a new fixed index 3 would fix today's layout but repeat the defect
after another batch insertion. Selecting the unique batch by the exact view
definition marker and testing reordered batches avoids that dependency.
Zero/multiple matches should fail explicitly, not select an arbitrary batch.
Other migration tests already select by content, not position (C4).
Reflection: no production change or broad suite is needed for this correction.

## Evidence Log

* C1: `src/core/tests/test_resident_showcase_sql.py:357,373` are the only fixed
  indexed renderer calls; both attempt to rebuild the view.
* C2: `infra/sql/resident-showcase.sql:24-45` adds the constraint migration at
  index 2; the view-containing batch follows at index 3.
* C3: `infra/sql/resident-showcase.sql:49-54` distinguishes NULL fallback home ID
  from projected `$.home.stock_id`; existing assertions check only `[]`.
* C4: `src/core/tests/test_resident_showcase_sql.py:663` selects the migration by
  content, establishing the small single-match list-unpacking pattern.
* C5: `src/core/pyproject.toml:15-17` pins dev tools; direct focused discovery
  failed with missing `zava_forward`, and Ruff was absent (2026-10-30).
  Existing manifests may be restored with pip; no dependency change is needed.

## Findings Mapped to Questions and Evidence

All three questions answered by C1-C4. Use a private test helper selecting the
unique view-containing batch. Replace both calls; assert `("HOME-A", "[]")`.
Add always-run helper tests for order independence and missing/duplicate markers.

## Alternatives and Decision State

Selected content matching plus a semantic projection assertion. Rejected another
fixed index and a mere `[]` assertion: neither prevents recurrence (C1-C3).
Rejected inserting sensor data: the test must retain genuinely empty tables.

## Open Questions, Risks, and Residual Uncertainty

SQL-backed tests are explicitly loopback opt-in. Ordinary discovery reports
these skips honestly; no cloud fallback is authorized. No material source gaps.
Another research cycle is unnecessary: remaining uncertainty is execution.

## Planning Readiness

Research disposition: executed, complete. Planning Readiness: Ready.
Self-check: three ordered inline waves, source evidence, alternatives, constraints
and implementation direction recorded. No research worker or external source used.
