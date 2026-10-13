<!-- markdownlint-disable-file -->
---
title: Five Retrofit Assistants Phase Details
ms.date: 2026-10-13
---

Task: five-retrofit-assistants-2026-10-13

<!-- rpi:phase id=P01 -->
## P01: Specify the five bounded assistants

Existing source: mvp/zavaforward_mvp, mvp/web, mvp/tests. Existing SQL driver
persists recommendation bodies transactionally with optimistic row versions.
Generic review is requester-only; funding_draft mutates case state. Neither
can be called unchanged for proactive role-owned proposals.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Requirements and architecture

PRD: docs/prds/zava-forward-retrofit-programme-demonstrator.md.
ADR: docs/adrs/0002-pilot-readiness-architecture.md.
Retain historical approval and proposed production boundaries. Map stock to
data owners/Assets, assessment to separate competent sign-off, funding to
Finance, coordination to resident choice/Programme, quality to independent QA.
The shared service and SQL-owned work lifecycle amend the lean exercise
realization, not the deferred premium topology's approval status.

<!-- rpi:phase id=P02 -->
## P02: Implement the specified assistants

Depends on completed P01. Write boundary: mvp/ runtime, UI, tests and README.
No parent docs, infrastructure, data, credentials, platform or Git writes.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Implementation

Capture permitted immutable evidence and canonical hash before invoking AI.
Use stable task/trigger identifiers and persisted state to deduplicate scans.
Claims must be atomic across SQL replicas with recoverable bounded leases.
Do not count templates as inference. Retain visible failure and manual paths.
Review rechecks snapshot, case access and registered reviewer roles; no actor
impersonation or cross-role data exposure. Disabled assistance never blocks
ordinary case access. Proactive evaluation must not invoke the old funding
method, change rank/queues, release work or modify quality states.

Apply accepted PC-001 to PC-008 from the plan: fenced lease CAS and lookup
recovery, distinct attempt liability reservations, compatible source/reviewer
audiences, dependency-complete signature rechecks, inference outside locks,
additive migrations and retained-data rollback. Record independent-connection
race/restart tests and each capability's exact trigger/source/output contract.

UI: integrate the case card and owned review work without a new application.
Expose invocation mode, sources, unreviewed/stale/failure states and separate
proposal review. Build and test existing clients and APIs consistently.

<!-- rpi:phase id=P03 -->
## P03: Validate and deliver the existing-platform version

Depends on P02. Parent owns this phase.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Validation and delivery

Use existing unittest/Node/browser/container patterns. Test JSON/SQLite and
MSSQL adapter behavior, authority and unchanged controlled state, stale review,
deduplication, competing claims, crashes, failures and bounded calls. Add no
unrelated lint framework or dependency.

Build a tagged image via existing ACR/container tooling; retain data and SQL.
Do not provision another estate. Verify existing deployment privileges/config
before an externally visible rollout. Record exact image/revision and real
SQL/model evidence; keep acceptance Blocked if essential evidence cannot be
obtained, rather than claiming local tests satisfy CON-009.

Publish on #68, no merge/amend/force-push. Dynamically resolve GitHub identity,
use its noreply email locally and include the required co-author trailer.

Capture private existing config, identity, domain/data fingerprints and rollback
digest before rollout. Build exact source; verify serving revision/digest and
unchanged SQL/AI/auth references. Demonstrate a registered deployed assistant,
provider usage and independent SQL task/audit before/after/restart. Missing
authority or live evidence remains blocked, never substituted with old results.
