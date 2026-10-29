---
title: Chat receipt audit locking phase details
description: Task-level implementation and validation expectations
ms.date: 2026-10-29
---

Task ID: `157-pr503-audit-locking-2026-10-29`.
Plan: `.copilot-tracking/plans/2026-10-29/chat-audit-locking-157-plan.md`.

<!-- rpi:phase id=P01 -->
## P01: Regression, implementation and validation

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add regression coverage

Use the existing JSON fixture and injected model in core test_chat_panel.
Coordinate concurrent entry construction after capturing predecessor values.
Verify all chain links with store.verify_audit, counts, receipt outcomes and
metadata, no dispatch for rejected turns and no lost events. Exercise completed
turns too, because their indirect message events currently leave repo.txn before
auditing. A model callback must allow a different thread to take store.lock and
append an ordinary event. Cover nested JSON and SQLite calls with genuine audit
flushes. Test ownership/removal/addition limits are locked in the plan.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Demonstrate original failure

Run only the concurrent rejected-turn test on unchanged production code.
Record nonzero exit and the failed genuine chain assertion. Do not retain
temporary mutation files or alter historical evidence.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Apply small lock sections

Wrap finally's receipt append with self.iso.store.lock. Wrap question persistence
with store.lock so chat.message.added also serializes. In finish, hold store.lock
through assistant-message persistence and chat.answer append. Leave model call,
prompt construction and ordinary read operations outside these sections.
Reentrant locks avoid introducing a second lock or conditional ownership probes.
Update the existing per-user chat storage README section; do not add KB pages.

<!-- rpi:task id=P01-T04 -->
### P01-T04: Validate

From src/core, run /tmp/mv/bin/python with
PYTHONPATH=src:tests:../api/src:../api/tests:../agents/src:../agents/tests.
Core selectors: test_chat_panel, test_chatthreads, test_chat_privacy,
test_chat_memory; sibling isolation/model/provenance selectors where applicable.
Because both core and API use test_chat_panel, run API's panel from its own
project directory with API source/tests first. Ruff check and format --check
cover the changed Python files. Use the existing mypy configuration if practical.
No live data, model or SQL Server/Azure actions.

P01 completed: four added regression methods, original rejected-chain failure
reproduced, three short lock sections applied, focused suites and Ruff checks
passed. Commands and original adverse evidence are preserved in changes.

<!-- rpi:phase id=P02 -->
## P02: Independent Review and local closeout

<!-- rpi:task id=P02-T01 -->
### P02-T01: Review once

Independent reviewer assesses actual diff, tests and acceptance evidence,
including SQL queued-audit behavior. Preserve original result. Route material
open findings to later work; do not rerun Review within this task.

Completed once: original execution Complete / outcome Conformant, no findings.
Reviewer independently passed 26 core panel tests, changed-file Ruff lint and
format checks and whitespace review. No source changes followed this Review.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile and commit

Update all task markers, changes, critique/Review outcome and durable state.
Resolve GitHub account using gh api user and configure its privacy-safe email
repository-locally before committing. Use a fix(chat) subject, Refs #157 and
the requested coauthor trailer. No push. A complete external publication receipt
and hosted/human approval are deferred publication prerequisites, not local
validation successes.

P02 completion is bound to the local commit containing this evidence and the
reviewed implementation. No later source correction or second Review is part
of this task. Original adverse results and review limitations remain intact.
