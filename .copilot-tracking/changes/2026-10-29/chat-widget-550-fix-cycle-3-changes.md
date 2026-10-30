---
title: Chat widget fix cycle 3 changes
description: Implementation and validation evidence for issue 550 and PR 556
ms.date: 2026-10-29
---

## Context and Scope

Task ID: issue-550-pr-556-fix-cycle-3. Full plan scope, P01/P02 first,
then one independent Review and local persistence in P03.
Plan/details use chat-widget-550-fix-cycle-3 under their dated 2026-10-29 folders.
Exactly one original critique: Revise; PC-001 resolved directly in reconciled
plan/details before source edits. Source scope includes guarded loading, status
and error layout mutations and both widget adapters' status writes.
No push, az, latest.json edits, generated targets or unrelated work.

## P01 Implementation

Complete. chat-widget.js extracts following() and preserveBottom(), preserving
the current <=1 px bottom eligibility and history-focus exclusion across loading
show/hide, status updates and error changes. message() uses the same predicate.
No sticky state, new listeners, observers, copy or focus changes.

Both employee chat.js and resident assistant.js route only their widget status
writes through setStatus(). Other callback/regulatory status is untouched.
README documents current-intent preservation and the regression.

Existing test owners retained, no removals or new test files. One unit method
covers seven modes: following, upward before/after loading, log focus before,
Sources focus before/after and returning to bottom. Geometry models status
wrapping, loading shrink, long reply, error sizing and completion/disposal
cancellation. Existing focus/lifecycle coverage remains.

reply_scroll adds two before-loading negative modes. Its positive mode positions
only before send, asserts bottom after send/status and loading, then fulfills a
long reply and checks <=2 px final distance without any post-send repositioning.
Resident begins that case after a completed answer with empty status.
All negative modes preserve <=1 px position and exact focus. The existing
Playwright clock now starts before reply_scroll, pauses throughout controlled
interaction and advances 200 ms for each reveal, then resumes. Later 199/200 ms
checks reuse the clock with a future pause target.

## P02 Validation

Complete. Evidence root:
/home/azureuser/.copilot/session-state/84897398-9719-4cb4-b217-1a3237c9cbe4/files/fix-cycle-3.

| Check | Result | External evidence |
| --- | --- | --- |
| Exact requested chat discovery | 109 tests, OK, one existing opt-in Chromium skip | chat-tests.log |
| Final discovery with ZF_BROWSER_TESTS=1 | 109 tests, OK, zero skips | chat-tests-browser-enabled.log |
| Ruff check and format --check | Passed, 59 formatted project files | static-final.log |
| Explicit isolated browser-harness Ruff/format | Passed, one formatted file | static-final.log |
| node --check, all three changed JS files | Passed | static-final.log |
| Existing mypy | Passed, 112 source files | static-final.log |
| Two-site constructed-data Chromium/axe | Passed, including both new pre-send/pre-loading cases and retained semantics/focus/consent/stale checks | browser-attempt2.log; browser-attempt2/results.json |
| Original widget and two focused mutations | All three rejected with bottom-follow assertion, not missing-method error | negative-controls.log; negative_checks.py |
| git diff --check | Passed | command output |

Commands ran from src/api with
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests:

```bash
/tmp/mv/bin/python -m unittest discover -s tests -p 'test_*chat*' -q
ZF_BROWSER_TESTS=1 /tmp/mv/bin/python -m unittest discover -s tests -p 'test_*chat*' -q
/tmp/mv/bin/ruff check .
/tmp/mv/bin/ruff format --check .
/tmp/mv/bin/ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 checks/chat_widget_browser_check.py
/tmp/mv/bin/ruff format --isolated --line-length 100 --check checks/chat_widget_browser_check.py
node --check src/zava_forward/api/web/chat-widget.js
node --check src/zava_forward/api/web/chat.js
node --check src/zava_forward/api/resident_demo/web/assistant.js
/tmp/mv/bin/mypy
/tmp/mv/bin/python -u -m checks.chat_widget_browser_check --axe <evidence-root>/axe-4.10.3.min.js --out <evidence-root>/browser-attempt2
```

Pinned axe-core 4.10.3 fetched from cdnjs; existing checker verifies its hash.
No dependencies installed. Browser check confirmed owned loopback server
responsiveness and cleaned up its applications. Unit warning/trace output
belongs to expected fail-closed synthetic fixtures; unittest outcome is OK.

### Adverse attempt and correction

browser-attempt1.log preserves an actual failure: employee checks passed, but
resident startup stayed at Loading because adapter cleanup removed the local
status alias while leaving status.id. Corrected to ui.status.id; no behavior
assertion removed or weakened. Deterministic clock handling was added to prove
before-loading negative cases truly precede reveal, not depend on execution speed.
Final browser attempt 2 and static/type checks pass after the correction.

### Sensitivity

An external temporary copy runs the new unit script against baseline 34f7f8fc
and two focused mutants of current source. Original and unguarded-status fail
after status insertion; unguarded-loading fails after the 200 ms reveal.
Temporary copies are scoped and auto-cleaned, tracked source never replaced.
This proves independent sensitivity to both PC-001 and the requested defect.

## Amendments and Divergences

PC-001 status prerequisite applied before implementation; original critique
preserved. No significant/divergent user decision required.

## P03 Review and Persistence

Pre-Review reconciliation: P01/P02 markers and details complete; six source
files within reconciled scope, all required checks pass, no implementation blocker.

Exactly one independent Review completed, outcome Conformant, zero substantive
findings. Review record:
.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-fix-cycle-3-review.md.
It preserves original Revise critique, accepts PC-001 resolution and validates
the scoped six-file boundary, current guidelines and supplied positive/negative
evidence. Independently rerun five focus methods and three JS syntax checks pass.
No correction or second Review performed.

Final P01-P03 markers/details/state are reconciled. The containing local commit
persists source and all original dated RPI evidence; its hash and clean-tree
verification belong to external command evidence, not a self-referential tracked
receipt. GitHub API resolved id 8036360/login jmservera; repository-local
8036360+jmservera@users.noreply.github.com is used for author and committer.
Required Copilot co-author trailer is included. No push or az command, and
latest.json unchanged.

Publication and its complete local gate, exact-head assessment, hosted/human
approvals remain separate. This local review is not publication approval,
whole-issue closure, real-user/live-model or accessibility-conformance acceptance.
