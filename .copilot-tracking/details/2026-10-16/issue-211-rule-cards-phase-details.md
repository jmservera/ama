---
title: Issue 211 phase details
ms.date: 2026-10-16
---

Task: 211 / issue-211-rule-cards. Final critique corrections:
one shared adapter RLock and outer source transaction, with non-committing
review helper; write lock precedes state reads; derived index retries independently
and immutable orphan blobs are not deleted. Rule capabilities need a unique
provisioned oid, never email fallback or a reserved-claim workbench mapping.
Test legacy history, rollback recovery and portable SQL contracts. Any material
post-implementation Review finding blocks acceptance and makes the PR draft;
do not restart implementation in this one-pass lifecycle.

Completion: P01/P02 and P03 all delivered. One Review completed, Conformant
within the local labelled exercise boundary; commit 2678443 pushed to the
requested branch and PR #324 opened to main. Commands, results, final
publication and residuals are recorded in the changes artifact. No human
card approval or live-platform acceptance is inferred.

Parent plan:
.copilot-tracking/plans/2026-10-16/issue-211-rule-cards-plan.md.

<!-- P01 -->
## P01: Core reuse and persistence

<!-- P01-T01 -->
### P01-T01

Use the lawstore SqliteDb/MssqlDb adapters, retaining direct SQLite construction
compatibility for existing tests. Initialize append-only rule tables for either
dialect. Remove identity-dependent inserts and SQLite-only pagination from shared
queries. Serialize complete writes using SQLite BEGIN IMMEDIATE or the existing
SQL Server application-lock transaction. Roll back failed mutations, including
superseding versions. Keep the immutable version schema compatible.

<!-- P01-T02 -->
### P01-T02

Validate nonempty identifiers, text, provision lists, ISO dates and retirement
after effective date. Owner hold needs a reason. Source ingestion adds review
items only after the first source version, within its transaction. Existing
exercise seeds stay draft and owner-unassigned; no automatic approvals.

<!-- P02 -->
## P02: Authenticated API

<!-- P02-T01 -->
### P02-T01

Recognize ZavaForward.RuleAuthor and ZavaForward.RuleOwner separately from the
existing single workbench app role. Only validated, provisioned trusted-proxy
identities carry these capabilities; ignore staff-file capability fields.
Use canonical staff email for author/approver, not mutable display names.
Dual capability holders still cannot approve their own versions.

<!-- P02-T02 -->
### P02-T02

Use /api/law/cards collection and /api/law/cards/{id} history;
POST collection drafts new immutable versions; POST
/api/law/cards/{id}/{version}/{approve|activate|hold|release|retire} changes state.
GET /api/law/cards/reviews reads retained source review records. Reject
client-supplied actor/role/author/date/exercise overrides. All writes require
appropriate server capabilities and existing CSRF; reads follow staff law access.
Resolve owner email to an existing staff identity before drafting. Initialize
rules only when a law store is configured; missing stores return 503.

<!-- P03 -->
## P03: Evidence and delivery

<!-- P03-T01 -->
### P03-T01

Extend existing tests, plus at most one typed API lifecycle harness. Cover real
TrustedProxyProvider principal parsing with synthetic claims, spoofed body and
headers, self-approval under dual roles, unassigned seeds, hold/release/retirement,
retained approvals, persistence/reopen, source change and transaction failures.
No test removals. Add new routes to the existing endpoint inventory.

<!-- P03-T02 -->
### P03-T02

Run full core/API suites with absolute PYTHONPATH, mypy and ruff per touched
project. Use /tmp/zf164 tools, installing with pip only if missing. Start a
loopback app with temporary synthetic fixtures, verify health/auth/card lifecycle
over HTTP, stop its exact process and clean up temporary files. Record commands,
counts, skips and failures, including corrected intermediate failures.
Update core/API READMEs, knowledge-base index and append-only log.

<!-- P03-T03 -->
### P03-T03

Run one independent rpi-review after implementation reconciliation; route any
findings as follow-ups rather than restarting this loop. Verify authenticated
GitHub account, set local privacy-safe email, commit scoped files plus all
dated RPI artifacts with required trailer, push the topic and create PR to main.
PR uses Refs #211 and records unmet human/platform acceptance honestly.
