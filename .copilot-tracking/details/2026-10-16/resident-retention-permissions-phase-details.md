---
title: Resident retention and permissions details
description: Evidence and completion contract for the issue 86 follow-up
ms.date: 2026-10-16
---

Task: issue-86-resident-retention-permissions. Research C1-C5 and W1-W3 apply.
No unresolved product decisions; explicit delivery request permits parent continuation.

<!-- P01 -->
## P01: Implement and prove locally

<!-- P01-T01 -->
### P01-T01

Use first recorded contact, not decision/withdrawal/design/file dates.
Persist marker on log_call and retain earliest historical contact in schedule.
Calendar anniversary handles February 29 by February 28. Unknown remains unknown.
Retention list/delete reuses manager and legal-hold controls. Remove resident
decision/authority/wishes/contact-reference payloads only; complaint outcomes
and unrelated contact history are not silently put on this schedule.
Expired decisions cannot release dependent work, whether or not purged.
Purge inventory: resident_scopes, measure_decisions, representative_authorities,
resident_safe_contact, resident_contact_history, resident_reviews; reset legacy
decision; remove service request representative_ref and resident.representative.
Keep first_contact_at and purge metadata, general contacts and complaint outcomes.
New legacy audit records contain status only. Old immutable audit content,
backups and ledger row history are outside current-payload deletion claims.
Safe-contact confirmations are also evidenced contact events. Ignore malformed
or future dates; preserve Unknown if no usable date. authority_for denies
retention-expired reliance even when records remain under legal hold.

<!-- P01-T02 -->
### P01-T02

Existing Liaison Officer covers Neighbourhood/Resident Engagement, Coordinator
covers Retrofit. Manager and Programme Support are read-only for resident data.
Require registered identity equality, not caller-supplied role alone.
Preserve independent named reviewer actions only for eligible recorder roles.
Keep vulnerability permissions separate from resident-decision field rights.
Authorized resident subtrees survive recursive unrelated-note redaction.
Contractor flags reuse resident_gate, with conservative Hold on missing context.
AI prompt/citation tests must prove private authority/wishes/safe-route exclusion.
No new task-approval mechanism or role taxonomy is implied.
Separate complaint/redress service actions preserve the prior named-owner
permissions, including manager complaint closure. UI hides only resident
recording forms from managers, not their independent service route.

<!-- P01-T03 -->
### P01-T03

Update obsolete role expectations and prove new failures on original code.
Run core/API existing suites, project ruff/mypy, local HTTP fixture that starts
ThreadingHTTPServer and verifies health/app/authenticated reads and mutations.
Use python3 and existing dependencies; missing ruff/mypy allow installation.

<!-- P02 -->
## P02: Azure, evidence and delivery

<!-- P02-T01 -->
### P02-T01

After local green: existing SQL server in ama/uksouth, isolated new test DB,
Entra token from already signed-in az. Seed only constructed DATA; never read
existing application database or properwarm. Same MssqlStore inherits SqlStore
behavior. Verify decisions, first-contact schedule, permissions, restart,
retention purge and audit chain against real Azure SQL.

<!-- P02-T02 -->
### P02-T02

Owner explicitly permits full group wipe. Delete ama after evidence and verify
az group exists false. Record only resource identifiers and assertions,
no tokens/secrets. Cleanup also runs on failed verification.

<!-- P02-T03 -->
### P02-T03

Update core/API README and reference index/log. Record commands/results and
remaining human acceptance boundaries. One independent post-implementation
Review; route its findings, no repeated review loop. Confirm gh identity,
configure local requested email, commit trailer, push topic, PR Refs #86.

## Current Evidence

P01-T01/T02/T03 completed: 401 core, 517 API, 70 agents tests plus targeted
retention/privacy and local HTTP; component ruff/format/mypy passed.
P02-T01 completed: isolated Azure SQL Basic database, real MssqlStore,
reopened scoped decisions and purge, first contact preserved, intact audit,
ledger off; no private inputs. P02-T02 teardown running with no remaining SQL,
storage, AI or application resources in the latest inventory.
P02-T03 documentation ready; one Review and git delivery remain.
