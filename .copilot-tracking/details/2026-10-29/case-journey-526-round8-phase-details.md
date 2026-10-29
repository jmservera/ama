---
title: Case journey round eight phase details
description: Implementation context and completion evidence
ms.date: 2026-10-29
---

Task 526-round8. Research C1-C6 and W1 are sufficient. No unresolved design
decision. Full-loop continuation selected explicitly; no remote writes.

<!-- rpi:phase id=P01 -->
## P01: Correct and exercise shared state

<!-- rpi:task id=P01-T01 -->
### P01-T01

Implement one persistent mutation map in app.js, at the transport used by api.
Key endpoint plus action/task/kind and resource identifiers, not note, reason,
source, dates, revision or other editable content. Raw resident/challenge
forms must call the same guarded JSON transport and preserve their existing
structured refusal/history feedback. Lock release occurs in finally after
response JSON or failure, never during GET recovery or rendering.
Raw resident/challenge JSON parsing remains strict on 2xx/409/503. Parsing
failure releases the lock but preserves uncertain-outcome history barriers.
Extend existing raw matrices and browser feedback coverage for malformed JSON.

For queue drafts, reuse capture/restore/reconcile helpers with an explicit
queue session. Capture on response completion before replacing cards, not only
when the listing starts. Preserve revision identity, read-only recovery,
later edits, successful submitted-field consumption and explicit discard.
Retain failed queue DOM and make refresh retry available. Reset queue state
at authenticated-session and explicit leave/discard boundaries.

Audit every employee web mutation: app, panels, ops, assistants, chat and
timecapture share the guarded API transport; role-screens and case-workspace
have no mutation owner. Preserve existing post-outcome generation barriers.
Completed: two raw transports migrated; resident template and timecapture
callbacks surface newly possible pending-lock errors rather than unhandled
event promises. No visual or authorization change.

<!-- rpi:task id=P01-T02 -->
### P01-T02

Unit tests execute shipped JavaScript. Extend held raw-form matrix with actual
reconstruction and changed note; add shared transport lock semantics, fieldless
reconstruction and queue preservation coverage within four added methods.
Browser journey holds POST across refresh for fieldless advance, resident update
and challenge; assert one dispatch then refusal retry/history behavior.
Assistant browser matrix asserts reason/JSON across old and failed listing,
fresh same revision and changed/missing revision copy recovery. Axe scans
each new reachable state. No test removal or synthetic acceptance shortcut.

<!-- rpi:phase id=P02 -->
## P02: Validate and independently assess

<!-- rpi:task id=P02-T01 -->
### P02-T01

Use worktree src roots in PYTHONPATH and this worktree's .venv interpreter.
Focused test_case_journey and test_workspace_scripts, related API/web tests,
JS syntax and Ruff line length 100. Journey and assistants checks use the
existing pinned axe 4.10.3 asset. New external output directories, preserved
failures, exact command/results and source hashes in changes evidence.
Acquire /tmp/ama-rpi-heavy.lock using flock -n; retry up to 40 minutes,
without inspecting foreign outputs or invoking az.
Completed: full API discovery 1,208 tests/316 skips; focused 27 tests, Ruff,
format check, mypy 99 source files; journey 319 assertions/57 axe states and
assistants 206 checks/56 axe states, zero violations/page errors. Commands and
external evidence hashes are retained in the changes record.

<!-- rpi:task id=P02-T02 -->
### P02-T02

Fresh independent reviewer reads complete correction diff, audit siblings,
regressions and evidence; fetches current Web Interface Guidelines; writes
only the dated Review. Parent preserves outcome and routes any finding as a
distinct correction task rather than rewriting Review. A conformant bounded
Review is not publication or human acceptance. Commit source and dated evidence
locally using authenticated privacy-safe identity and required trailer.
