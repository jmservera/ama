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

Current evidence: P01/P02 complete; corrected runtime bf383c4 and local image
d3e652ce verified. Validation source 560c30c / CI 38461679776 passes 379
discovered tests and all 69 actual SQL tests, including 43 assistant tests.
47 local assistant and 19 Chromium checks pass. The completed runtime
follow-up fixes the shutdown/rendering defects and disposable SQL coverage.
Historical Reviews remain unchanged. P03 remains unchecked until actual
changed-platform provider/SQL/restart proof exists.

Owner explicitly authorized retained-data rollout and bounded QA on
2026-10-13: 10 calls, 126000 reserved tokens, one-hour authority, proactive off,
up to USD 5 incremental target. No exact billing guarantee, tenant changes,
new estate, data reset or PR merge. Later child five-assistant-live-delivery
owns the remaining P03 implementation and its new evidence.

The owner subsequently authorizes a fresh synthetic exercise database instead
of migrating the old database. Stop migration and revoke QA authority first.
Enrich the existing generator through the explicitly requested dataset agent,
including booked visits and other empty operational sections. Preserve
authentication and private tenant staff bindings. The new database must retain
the current ledger-enabled architecture: create assistant evidence as an
append-only ledger table, not an unsupported trigger on an updatable ledger
table. Fresh domain becomes the independent before/after/restart baseline.

Current execution: latest sourcecd14b3b/image05 locally ready, deterministic
generator, discovery389/316passed/73SQLskips,21browser regressions and21exact
generated-data image UI/API/local-restart checks pass. Last backendec7721b
actualSQL73pass and canonical7c4eb18test/image/mssql CI are historical.
Current source/learning published at e5567f9; CI38481199508test/mssql/image
all pass. The actual deletion was cancelled;
no alternate destructive route was used. Reset confirmation unavailable.
Image02/revision11 remains healthy with assistance authority removed, zero
modelcalls and oldretrofit retained. P03 remains unchecked until confirmed
reset, seeding and actual registered provider/SQL/restart proof are complete.

Local image04 populated-data browser check exposed API38/UI0 visits because
show filtered out arrays of day-group elements. Sourcea76d281 flattens before
node filtering; two-day/case-link regression and rebuilt image05 prove all38
visits render. This directly required UI correction is not new acceptance or
permission to bypass the cancelled reset.

Capture private existing config, identity, domain/data fingerprints and rollback
digest before rollout. Build exact source; verify serving revision/digest and
unchanged SQL/AI/auth references. Demonstrate a registered deployed assistant,
provider usage and independent SQL task/audit before/after/restart. Missing
authority or live evidence remains blocked, never substituted with old results.
