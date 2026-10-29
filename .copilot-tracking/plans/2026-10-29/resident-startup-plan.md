---
title: Resident image startup plan
description: Document and test the resident SQL projection deployment prerequisite
ms.date: 2026-10-29
---

## Task Metadata

* Task ID: f568fbf4-e1b7-45d5-ae08-d7034d24a85b
* Task slug: resident-startup
* Date: 2026-10-29
* Planning status: Ready; original Complete / Revise critique disposed
* Details: .copilot-tracking/details/2026-10-29/resident-startup-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/resident-startup-plan-critique.md

## Executive Summary

The same unmodified main image fails against the old SQL projection and serves
successfully after the local view update. Document the #525 SQL prerequisite
and preserve this compatibility contract with a real SQL regression. No new
required app setting or production-code defect was demonstrated. Do not mask
missing document facts, change startup admission or expand resident grants.
Actual Azure causality remains unconfirmed because its console was unavailable.

## User Decisions and Requirements

* Complete the full ordered RPI loop with dated artifacts.
* Read the named prior deployment evidence/logs first; use Docker and the repo locally.
* Never read .env/secrets/private data; settings use constructed dummy values.
* No az, Azure mutation, push or live SQL. Use fix/resident-startup from origin/main.
* Fix a demonstrated code bug with regression or document required configuration.
* Run ruff, mypy and relevant unittests; commit locally with mandated Copilot trailer.

## Goals

* Explain the observed local startup failure without overstating historical Azure proof.
* Make the SQL-before-image dependency discoverable to the next authorized operator.
* Preserve explicit refusal on incompatible view shape and prove the current template restores it.

## Scope and Non-Goals

In scope: src/api/README.md, src/core/tests/test_resident_showcase_sql.py,
dated task artifacts, local synthetic SQL and Docker verification.
Non-goals: runtime fallbacks, production behavior changes, schema/allowlist/expiry
changes, Azure, real datasets, browser redesign, deployment and publication.

## Functional Requirements

* Explain that `documents_json` is required at startup even without active chat/AI.
* Describe no new mandatory agenda/model setting, existing port/probe behavior,
  failure sequence and separately authorized SQL prerequisite.
* Regression must reproduce incompatible SQL projection and prove current SQL
  template restoration, preserving view-only principal permissions.

## Non-Functional Requirements

* No credential/raw config logs in git; no private data/model calls.
* Tests use the existing opt-in loopback SQL harness and clean database lifecycle.
* No production startup or resident access semantics are weakened.
* Preserve original critique and one Review outcomes; gate limits reported honestly.

## Acceptance Criteria

* Same main image: old view exits 2, current view health 200 on 8089,
  shell 200, unsigned protected view 401, wrong Host 403 (research C9).
* Regression executes against task-owned SQL Server without skips in the opted-in suite.
* Ruff lint/format and mypy pass for relevant projects; affected resident unit/SQL suites pass.
* One final-candidate critique and one independent post-implementation Review retained.
* Local commit contains intended source/tests/docs and dated artifacts only;
  no push and no publication-gate success claim.

## Sources

* .copilot-tracking/research/2026-10-29/resident-startup-research.md, C5-C9.
* src/api/src/zava_forward/api/resident_demo/__main__.py.
* src/core/src/zava_forward/core/resident_showcase_sql.py.
* infra/sql/resident-showcase.sql and its pre-#525 version.

## Test Ownership and Change Budget

Owner: src/core/tests/test_resident_showcase_sql.py, existing SqlBoundaryTests.
Removals: none. Maximum additions: one SQL compatibility test. Canonical targets:
that test file and src/api/README.md. Generated targets: none.
Semantic coverage: document facts remain required/unknown, never fabricated.
Regression coverage: stale view fails SELECT before server bind; current template
restores reader and view-only access. Validation uses actual local SQL, not mocks.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve startup prerequisite

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Document SQL-before-image ordering and local diagnosis limits

Explain required view column, no new mandatory setting, port/probe and authorized
operator action without providing/performing a live apply. Dependency: C5-C9.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add SQL compatibility regression

Temporarily remove/rename the document projection in the task-owned view,
assert the reader refuses it, reapply current template in finally, and prove
the fixture is readable with unchanged restricted access. Dependency: C6-C7.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and review

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute static, unit, real SQL and image checks

Use isolated installed distributions and existing suites; retain commands,
exit codes/skips and external local probe evidence. Depends on P01.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: One independent Review and local commit

Reconcile plan/details/changes/state; preserve Review outcome and route findings
without a second Review. Resolve GitHub account read-only for privacy-safe local
author/committer identity. Commit with mandated trailer. No publication.
Depends on P02-T01.

## Dependencies and Publication Boundary

Local Docker and owned SQL container must be available; heavy checks use
nonblocking shared lock. Ruff/mypy were initially missing and were installed
with declared pinned dev dependencies into an external isolated venv.
No full gate is claimed: user prohibits az and push; the full gate includes
offline Azure CLI/Bicep commands. Publication remains blocked until a separately
authorized complete external gate/receipt and exact-head/human review.

## Critique Disposition

Exactly one critique executed Complete / Revise. Original is preserved.

| Finding | Disposition | Evidence / response |
| --- | --- | --- |
| PC-001 Medium | Rejected, unsupported premise | The critique asserts this execution forbids /tmp file operations, but no such prohibition appears in the supplied user/developer/repository instructions. src/README.md explicitly requires the actual shared /tmp/ama-rpi-heavy.lock. Nonblocking flock already admitted the research builds/SQL probes. Continue that actual lock; never substitute a task-local lock or bypass/interrupt a foreign holder. No scope or safety boundary change. |

## Follow-Up Items

* Separately authorized live view/schema, auth and secretRef verification before
  any retry; local reproduction is not proof of the historical cloud cause.
* Preserve prior rollout executor secretRef/deadline findings as separate work.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-29/resident-startup-changes.md.
Ready; critique finding disposed. Parent proceeds to Implement without another critique.

Pre-Review status: P01 and P02-T01 complete. P02-T02 remains open solely for
the single independent Review and requested local commit; no further source
implementation remains. Validation evidence:
.copilot-tracking/changes/2026-10-29/resident-startup-evidence.json.
