<!-- markdownlint-disable-file -->
# RPI Plan: employee-skills-chat-530

## Task Metadata

* Task ID: 530
* Task slug: employee-skills-chat-530
* Plan date: 2026-10-30
* Planning status: Ready; compatible critique PC-001 applied directly.
* Details: .copilot-tracking/details/2026-10-30/employee-skills-chat-530-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-30/employee-skills-chat-530-plan-critique.md

## Executive Summary

Preserve the delivered skills chat and strengthen local evidence with two
shared storage regressions. Four JSON/SQLite cases, eight targeted HTTP contracts
and API/core static gates pass. Full API/browser/actual SQL execution is blocked
by the shared heavy lock; no runtime behavior was duplicated.

### What You May Not Know

Seven issue criteria are checked upstream, but original Review RV-003 left
whole API and actual SQL evidence missing. Local success does not prove live
employee-site/model or human acceptance. The complete publication matrix invokes
Azure CLI, prohibited in this run; no full receipt will be claimed.

## Sources

* .copilot-tracking/research/2026-10-30/employee-skills-chat-530-research.md: C1-C6, W1-W2.
* src/api/README.md: existing design note and commands.
* src/core/tests/test_chatthreads.py: shared JSON/SQLite/MSSQL behavior suite.
* src/api/tests/test_mssqlstore.py: MssqlChatThreads reuses that suite.

## User Decisions and Requirements

* Complete research, plan, implement, review in order on the supplied branch/base.
* Implement exactly #530; one agent/five skills, projected sources, no added authority.
* Use src, tests outside packages, pip only, native Fluent/WCAG/plain language.
* Run requested API discovery, Ruff, formatting, mypy, local Playwright/axe and SQL.
* Hold flock -w 600 /tmp/ama-rpi-heavy.lock for heavy checks.
* No Azure, deployments, live sign-in, credentials, secrets or push.
* Commit locally with required coauthor; Refs #530 only; report unmet acceptance.

## Goals

Collect reproducible local acceptance evidence, including actual SQL Server,
without replacing the existing implementation or claiming operational approval.

## Scope and Non-Goals

In scope: two storage contract tests, relevant component documentation and dated
RPI evidence. Non-goals: runtime redesign, router, new UI, regulatory changes,
live names/site/model acceptance, full publication receipt or remote writes.

## Functional Requirements

* All five explicit skills and general work help return bounded, cited answers.
* No selected skill bypasses owned threads; model failure remains workflow-only.
* Stored questions/answers, citations and minimal skill/outcome audit survive reopen.

## Non-Functional Requirements

* Constructed data and synthetic model only; no external model or credential files.
* Exact evidence: six selections per store, one call per answer, no case changes,
  audit references without duplicated question/contact text and a valid chain.
* Actual SQL must run in a newly owned, labelled, bounded loopback container.
  Remove only that exact container; retain external logs.

## Acceptance Criteria

* AC1-AC7: existing runtime evidence plus current regression/browser checks mapped
  separately to issue criteria, without treating doubles as live model evidence.
* AC8-local: requested API suite/static checks, employee browser/axe and actual
  SQL selectors pass. If any fail, preserve the failure and qualify evidence.
* AC8-whole: explicitly unmet without separately authorized live verification.

## Test Ownership and Locked Boundary

* Canonical target: src/core/tests/test_chatthreads.py, ChatBehaviour.
* Removals: none. Maximum additions: two test methods and needed imports.
* Existing JSON, SQLite and MssqlChatThreads reuse; no duplicate test harness.
* Semantic coverage: six selections, fallback, owner denial, cited sources,
  minimal audit and restart. Regression coverage: prior missing actual SQL proof.
* Generated targets: none in git; logs/axe reports external only.
* Documentation target: src/api/README.md; no web source changes planned.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Storage acceptance contract

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add two cross-store skill regressions

Use the existing factory/cleanup conventions; assert persisted cited turns,
audit minimization, model-call count, unchanged case and rejected foreign user.

<!-- rpi:phase id=P02 -->
### [ ] P02: Local evidence and documentation

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Execute bounded local gates

Run focused tests first, then requested API discovery, component lint/format/types,
employee Playwright/axe and owned actual SQL MssqlChatThreads. Heavy checks under
the requested lock, no foreign resource access or cloud fallback.
Current result: focused JSON/SQLite and eight HTTP tests pass; API/core static
checks pass. Heavy lock acquisition timed out at 600 seconds, exit 1, before
execution. Full discovery/browser/actual SQL remain not run, not successful.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Document outcomes and acceptance boundaries

Update the API guide and dated changes with actual commands/exits/skips, external
paths, identities and unresolved full/live gates; reconcile plan/details.

<!-- rpi:phase id=P03 -->
### [ ] P03: Independent Review and local handoff

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Review once and commit locally

Obtain independent exact-diff Review; preserve findings without a second Review.
Record state and evidence, configure authenticated privacy-safe identity and
commit with the required trailer. No push or PR. Attempt only authorized local
publication checks; a full receipt remains blocked by the no-Azure boundary.

## Dependencies

P02 follows P01; P03 follows P02 or an explicitly recorded validation blocker.
PR #529 is merged. Docker, local SQL image and mssql_python are available.

## Critique Disposition

One final-candidate critique executed: Complete / Revise, PC-001 High.
Resolved directly in P02-T01 details: isolated SQL environment, positive
ownership/binding/resource admission, stdin-only password bootstrap, bounded
execution and exact-ID cleanup. No user decision needed, no repeat critique.
Original verdict is preserved.

## Follow-Up Items

* Owner/coordinator: separately authorized live site/name acceptance and complete
  publication gate. Outside this run's explicit no-live/no-Azure/no-push scope.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-30/employee-skills-chat-530-changes.md.
P01 and P02-T02 complete; P02-T01 blocked on heavy-lock admission. Proceed to the
single independent Review with the validation gap explicitly unresolved, then
local commit only. This is not a publication-ready candidate.
