---
title: Chat review fixes 157 phase details
description: Task boundaries and completion evidence
ms.date: 2026-10-29
---

Task: `157-chat-review-fixes-2026-10-29`.
Plan: .copilot-tracking/plans/2026-10-29/chat-review-fixes-157-plan.md.
Research C1-C9 resolves readiness; no open design decision.

<!-- rpi:phase id=P01 -->
## P01: Correct callbacks and consumption
<!-- rpi:task id=P01-T01 -->
### P01-T01: Safe admission and completion failures

Catch ordinary callback exceptions at the two adapter admission boundaries,
log only the exception class, and raise ModelUnavailable from None with safe
outcomes admission-check-failed / completion-check-failed. The former retains
default zero calls; the latter includes the provider envelope's calls/usage.
Explicit activation-not-approved/revoked behavior stays unchanged.
Do not expose provider text when completion authorization is unknown.
Test pre-dispatch provider-not-called, completion usage, disabled completion,
safe errors and panel audit/receipt propagation.

<!-- rpi:phase id=P02 -->
## P02: Correct bounded role-scoped history
<!-- rpi:task id=P02-T01 -->
### P02-T01: Budget dispatched block

Build each candidate history block using the actual block helper with the
full candidate length; retain only candidates <=4000 characters and append
the already expanded block to the prompt. Assert the exact emitted block,
not the stored history or total prompt as a substitute.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Persist per-message actor role

Append actor_role to MESSAGE_COLS to preserve evidence's positional index.
Fresh SQLite/MSSQL DDL adds non-null actor_role default empty. SQLite schema
setup and MSSQL transactional chat migration add missing columns idempotently.
chat_add_message derives actor_role from user.role for every message.
Panel requires matching actor_role and excludes unknown legacy rows.
The existing regulatory service bypasses ChatMixin for atomic paired writes:
set actor_role on those new records and preserve unknown roles on copied
historical messages. This is required persistence compatibility, not a feature.
Shared storage tests cover A/B/A role roundtrip, restart and migration;
existing SQL Server shared suite inherits role coverage but is not claimed run
without an approved disposable local service.

<!-- rpi:phase id=P03 -->
## P03: Validate and review
<!-- rpi:task id=P03-T01 -->
### P03-T01: Regressions and component checks

Restore isolated dependencies after observed missing interpreter/package.
No private datasets or cloud clients are needed for fixture-based validation.
Record exact commands, counts and skips; preserve red results.
Update owning core and agents READMEs for behavior changes.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Independent Review and local commit

Dispatch one fresh independent Review after reconciliation of tasks and checks.
Do not loop back to implementation on Review findings; route any new findings.
Use authenticated GitHub account's local noreply author/committer identity,
Conventional Commit and supplied trailer. No push. A complete publication
gate incompatible with owner constraints stays blocked, not skipped-as-passed.
Required human review remains unchecked.

## Completion

P01/P02 and P03-T01 passed the focused regressions, complete component suites
and requested static checks recorded in the changes artifact. The single
independent Review is Complete / Conformant with justified divergence for
bounded implementation, with no implementation defects. P03-T02 concludes
with the local commit containing this original evidence. SQL Server and
publication/hosted/human/activation gates remain residual, not claimed passed.
