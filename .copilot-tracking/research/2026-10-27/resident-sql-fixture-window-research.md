---
title: Resident SQL fixture authorization window research
description: Focused research for PR 479 shared browser and image fixture correction
ms.date: 2026-10-27
---

## Research brief

Correct the shared SQL fixture without extending SQL authorization or changing
the application cap. Audience: implementer and PR 479 reviewer. Output mode:
convergence. Posture: focused, selected from the named defect and owner scope.
Research root: `.copilot-tracking/research/2026-10-27/`.

## Direction controls and extensions

The owner requests the complete RPI loop, dated evidence, local unit tests,
Docker checks where available, normal commit/rebase/push and review-thread
resolution, explicitly no merge, uv or secrets. This is explicit authorization
to progress all four phases; no broader automatic follow-up session is assumed.
Repository instructions and RPI skills apply. No web edits, regulatory changes,
cloud changes or private datasets are in scope. Research stays inline because
the fixture, schema and consumers form one bounded trace.

## Questions and candidate areas

1. Where is AUTHORITY_END reused in SQL fixtures, tests and checks?
2. Which SQL constraint and check execution paths govern the shared fixture?
3. What regression evidence can establish separation without widening authority?

## Research cycle log

Cycle 1, Wider: searched `src/` and `tools/` Python/SQL/Markdown for
`AUTHORITY_END`, `ck_allowed_case_window` and the November timestamp, then
`infra/` and workflow consumers. One SQL-bound use of AUTHORITY_END exists:
the shared browser fixture. Reflection: image checks inherit this defect;
sensor browser fixtures are in-memory and should retain the application cap.

Cycle 1, Deeper: traced fixture inserts, SQL renderer, constraint and image
imports. Reflection: an explicit UTC November endpoint converted to naive UTC
for DATETIME2 fixes the insert without changing application configuration.
Core SQL test fixtures already retain November 1.

Cycle 1, Contrarian: considered extending the SQL constraint (rejected by
owner scope), reusing the application cap (the defect), and choosing a shorter
dynamic end (unnecessary churn). The existing current-time start is valid on
the requested October 27 exercise date; after SQL expiry these checks must
fail closed rather than invent extended authority. Reflection: preserve
current application expiry tests and explicitly regress the actual insert
parameters with a fake SQL boundary, not a source-string proxy.

## Evidence and findings

| ID | Source | Evidence-backed finding |
| --- | --- | --- |
| C1 | src/api/checks/resident_demo_browser_check.py:104-109 | allowed_case inserts application AUTHORITY_END as valid_to |
| C2 | infra/sql/resident-showcase.sql:21 | SQL requires valid_to <= November 1, independently of application cap |
| C3 | src/api/checks/resident_demo_image_check.py:26-33 | image check imports the same database fixture |
| C4 | src/core/tests/test_resident_showcase_sql.py:263-270 | core SQL fixture already uses November 1 |
| C5 | src/api/checks/resident_sensors_browser_check.py:27-45 | in-memory sensor rows do not write SQL |
| C6 | src/core/tests/test_resident_showcase.py:423-434 | December application cap and expiry behavior have existing coverage |
| C7 | src/README.md:48-52 | current small-issue policy allows planned unit/focused checks; full gate is for broad feature/release/infra/SQL/security changes |

PR 479 thread PRRT_kwDOUU8JX86wuntn confirms the exact C1/C2 failure.
Docker 29.9.0 is responsive and SQL Server image is cached. System Python lacks
Playwright/Ruff/mypy; SQL driver is installed. Tool restoration is needed.
No independent research lanes were warranted; all three waves ran inline.

## Alternatives and decision state

Select one SQL-only November 1 constant in the shared fixture and regress both
resident inserts while substituting a later application cap. No SQL or runtime
source changes. No further research needed: scope and consumers are covered.
Original resident-live-acceptance Review and its live dependency blockers are
preserved; this child correction does not renew live authorization.

## Planning readiness

Research disposition: executed, complete. Planning Readiness: Ready.
Self-check: questions answered with C1-C7; no unsupported live acceptance claim.
