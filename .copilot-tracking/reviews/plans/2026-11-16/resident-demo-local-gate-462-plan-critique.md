---
title: "Plan critique: resident-demo-local-gate-462"
description: "Single-pass critique of the Issue #462 local candidate plan"
ms.date: 2026-11-16
---

Execution: single pass, one final-candidate critique, performed by the RPI agent against the plan, details and research. Verdict: Revise (0 Critical, 1 High, 2 Medium, 1 Low). Corrections were applied directly to the plan and details; no repeat critique.

## Findings

| ID | Severity | Finding | Disposition |
|----|----------|---------|-------------|
| PC-001 | High | The gate invalidates on any later commit, but the plan did not say what happens when the gate fails or when the state file must record `commit-complete` (needs the commit sha). | Applied: state file is finalised before the single candidate commit with a "gate pending" next action; the witness log and receipt live outside the repository so they do not dirty the tree. If the gate needs a fix, the fix is a new commit and the gate is re-run in a new output directory; no receipt is reused. |
| PC-002 | Medium | Phase 3 did not say what counts as "SQL Server parity": the browser check creates its own database, but the SQL unit suite and the view template must also run against the same container. | Applied: run `test_resident_showcase_sql` and apply `infra/sql/resident-showcase.sql` through the check's fixture on the same throwaway container; record the image and version. |
| PC-003 | Medium | Docker non-root proof relied on the Dockerfile text. | Applied: assert the running container's effective uid with `docker inspect` and `docker exec id -u`, not only the `USER` line. |
| PC-004 | Low | Dependency check could be read as claiming the historical rubric failure is resolved. | Applied: the plan records state only and routes the judgement to review as a coordinator matter. |

## Conflicts with confirmed decisions

None. No advice was rejected. No significant or divergent issue needed a user decision.

## Verdict basis

The plan is bounded, local only, and keeps every unmet cloud criterion explicit. Remaining risk is environmental (container image pull, Chromium), recorded as a blocker if it occurs, never bypassed.
