---
title: Role task queues 76 phase details
ms.date: 2026-10-16
---

## P01

Evaluation clock: dataset Store.as_of, normalized to UTC midnight for date-only
snapshots. Publish it; this is a reproducible snapshot, not a live service
clock. New: stage_since age inclusive 0..7 days. Stale: last supplied EPC/Survey
document `at`, strictly greater than 30/180 days; absent, invalid or future
observations are Unknown. Reassessment is explicitly stale. Deadline overdue:
strictly before snapshot; timezone required for time-valued deadlines.
Offered/Received/Escalated handoffs are pending; Accepted/Completed/Declined/
Withdrawn are not unowned. Only pending handoff due_at is overdue.
Case resident_update remains independent of handoff lifecycle; completed_at
suppresses its deadline. Hazard response/update deadlines are checked against
responded_at/resident_updated_at, independently; released holds do not erase
outstanding external commitments. Missing completion is "Not evidenced".

Structured blockers: funding confirmation uses case owner; hazards use
accepted_by/sender or explicitly recorded legacy owner; stock queries use
query_owner; technical missing_items uses responsible role and named owner
Unknown; resident checks use case owner for obtaining supplied evidence, not
authority to consent; building blockers retain owner Unknown. Do not parse
display prose to invent assignments. Label final-check prerequisites separately
from safety/stock/building stops. Stable ordering: safety, stock, building,
then final-check funding/resident/technical prerequisites. Current next action:
first active stop, pending handoff action, current-stage return action,
then first final-check prerequisite only at that stage; otherwise ask case
owner to record a next action. Human free text is role-projected before
serialization, including source/reason aliases. Each item carries origin,
version and snapshot; source-trace rendering reuses this same object.

Validation oracles include >50 mixed cases across two pages, exact expected
IDs/count/order for JSON/SQLite/CSV, nondefault sort and compound filters.
Unknown queue yields 400 on both endpoints; unavailable approved priority
returns an empty set with visible policy explanation. Sentinel free text
must not escape via new context, list/detail or CSV. Browser reset is tested
with alternate server-defined order to distinguish contract use from hardcoding.

P01-T01 starts from research C4-C7. Add a typed pure derived read model in
core; reuse existing reasons and accountability metadata. Store summaries
and detail must use the same context. SqlStore's optimized pagination must
not silently bypass queue filters. Dynamic filters may use the existing
in-memory fallback before slicing. No SQL schema changes.

P01-T02 exposes the versioned definitions/default in authenticated metadata
without adding privileges. Keep contractor outputs unchanged. Free-text
context must follow the existing need-to-know rules; safe unknown labels must
remain available. Direct API tests include forged role/perspective query
values, invalid queues, non-staff reads, contractor field isolation and denied
controlled actions. Compare list/detail context and CSV membership.

## P02

P02-T01 depends on P01. Extend existing filters with one queue selector and
visible definitions; no second reset. Use server default metadata, retain
existing first-page/no-selection semantics and cancellation. Show current
shared context near case heading, history and suggestion panels; do not
rewrite historical event snapshots as current ownership.

P02-T02 runs /tmp/zf164/bin/python and absolute PYTHONPATH for current-worktree
package source and shared fixtures from each project. Run each project's
ruff and mypy with its existing configuration. Node syntax-check changed JS.
Extend existing real synthetic loopback Playwright check for semantic queue
membership, visible definitions, consistent context, reset and responsive UI.
Record failures, corrections, skips and unexecuted external gates honestly.

## P03

P03-T01 depends on P02. Document the audit, definitions and operational limits
in API README, update parity matrix/reference routing and append reference log.
Run one final post-implementation acceptance review and record findings.
Do not claim all #76 acceptance complete while owner approvals are open.

P03-T02 depends on P03-T01. Confirm only intended source/docs/tracking changes,
configure the GitHub-verified privacy email locally, commit with Refs #76 and
the required trailer, push without force, create main-targeted PR. No merge.
