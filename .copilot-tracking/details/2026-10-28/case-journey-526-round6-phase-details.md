---
title: Case journey sixth correction phase details
description: Implementation tasks and evidence boundaries
ms.date: 2026-10-28
---

Task 526-pr529-round6-20261028. Evidence C1-C4/W1-W2 in primary research.
No implementation blocker; complete publication gate blocked by no-az direction.

## P01

### P01-T01

Use caseFieldEntries semantic keys, raw immutable snapshots and owning session.
Compare current controls independently from original references. Recovery
checkboxes preserve checked semantics despite textarea display. Retire only
equal cache entries and consumed recovery controls; no stale saved array may
restore retired text after a delayed loader. Keep ordinary external draft text
separate from AI review when the review does not submit that control.

### P01-T02

Validate missing Reason before JSON; parse separately before request dispatch.
Associate/focus malformed JSON editor, clear stale validity on correction/retry.
API/reload failure is status feedback without false Reason invalidation.
Pending review state follows proposal ID/revision across refreshed cards,
excludes duplicate action and restores readiness after failure/success.
Quality Save pending guard must not stop measure switching or later text input.
Proposal state is shared by ID/revision in case cards and the sessionless queue,
not scoped to a required caseSession. Queue malformed JSON and pending refresh
must preserve working review actions and exclude duplicate dispatch. Successful
mutation consumes its revision even if reload fails; retryable rejection restores
readiness, uncertain transport keeps review unavailable until authoritative
refresh. Quality confirmed success with failed redraw stays unavailable until
current case state loads. Neither failure path falsely invalidates a field.
Audit sibling draft review and quality remediation errors for the same false
invalidity/stale invalid state; keep uncertain committed forms disabled.

### P01-T03

Extend test_case_journey executable shipped-JS harness for keyed live/recovery/
cache-only comparisons, later values, checkbox/file identity and isolated errors.
Extend existing browser fixtures, not a new server/tool. Journey quality pending
measure-switch matrix adds no scan count; existing restored-quality scan covers
the resulting controls. Assistants error and pending-refresh matrix uses held
synthetic response routes plus real proposal mutations where feasible.
Include success followed by reload failure, definitive refusal and queue rows.
Document dispatch/recovery/error behavior in existing API README.
No removals, new dependencies or generated artifacts.

## P02

### P02-T01

Run API test_case_journey and test_workspace_scripts, Ruff line limit 100,
owning format/type checks and JavaScript syntax. Both browser suites use pinned
axe 4.10.3 and constructed local data only. Acquire /tmp/ama-rpi-heavy.lock
using flock -n; deadline 2400 seconds, no Azure fallback. Preserve failed run
logs external to worktree. Record browser assertions, scan counts/violations,
page errors and exact evidence paths. Review all PR-changed web paths for
error routing, aria-invalid clearing, pending guards and recovery lifecycle.

Completed: 21 requested plus 22 related unit tests, owning Ruff/format/mypy,
JavaScript parsing, journey 231 assertions/38 axe scans and assistants 141
checks/32 axe scans. Both have zero violations/page errors; contrast incomplete
results remain manual work. Exact runs, hashes and failed attempts are recorded
in the changes artifact. Browser-only synchronization corrections followed the
final production/unit bytes; no source mutation invalidated those earlier runs.

### P02-T02

Reconcile plan/details/changes and actual checks before one independent Review.
Do not silently fix/re-review findings in this task after Review; route later work.
Record original execution/outcome and assessed boundary. Resolve authenticated
GitHub identity for local privacy-safe author/committer. Commit source and dated
evidence with required trailer and Refs #526. No push or thread mutation;
coordinator owns full-gate publication and human/hosted gates remain open.

Review executed once, Complete / Not accepted. Both primary fixes supported;
Medium RV-001 routes upload uncertainty/retry safeguards to later rpi-implement.
No source fix or repeat Review after this outcome. The task completes its
requested phase execution and local retention, not acceptance. Seven original
dated phase/state artifacts accompany the eight changed API files in the
local-only commit; full gate and publication remain unperformed.
