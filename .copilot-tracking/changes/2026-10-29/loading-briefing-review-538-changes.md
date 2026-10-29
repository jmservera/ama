---
title: PR 538 citation and helper recovery changes
description: Original implementation and validation evidence, refs 531
ms.date: 2026-10-29
---

Task ID: `538-review-corrections-2026-10-29`.
Declared scope: full plan P01-P02.
Plan/details/critique: matching `loading-briefing-review-538` dated artifacts.

## P01 Implementation

Completed regression-first implementation of citation whitespace, contextual
abbreviation boundaries and helper-only pre-session recovery.
Original supplied parser reproductions both failed before source changes;
new parser/loader regressions also failed against unchanged source (exit 1).
Single critique original Revise preserved; PC-001/PC-002 direct dispositions
are incorporated in current plan/details. No significant divergence.

* `src/core/src/zava_forward/core/ai_tasks.py`: normalize only protected
  trailing citation-group whitespace, including LF/CRLF, before segmentation.
  Protect recognized contextual abbreviation periods and restore exact text.
* `src/core/tests/test_ai_statement_sources.py`: three parameterized methods
  supplement the existing regression: exact examples, whitespace/groups,
  unresolved citations, title/medial examples, same-token terminal negatives,
  independent uncited statements and explicit newlines.
* `src/api/src/zava_forward/api/web/app.js`: helper readiness is a dependency
  even before authentication; role scripts require a session. A bootstrap
  awaits readiness before registering account actions and calling start.
  Same-session null bootstrap still rechecks readiness; stale identity returns
  safely. Terminal startup dependency errors show native Reload workspace.
* `src/api/tests/test_workspace_scripts.py`: execute actual loader/bootstrap
  with controlled script outcomes. Assert helper-only pre-session selection,
  no early start/listeners, working account callbacks, bounded exhaustion,
  missing readiness and timeout, plus retained route/session matrices.
* `src/api/checks/loading_briefing_browser_check.py`: actual-browser scenarios
  abort helper once/twice, exhaust all three requests or return no readiness.
  Assert automatic recovery/no document reload, case/sign-out behavior, or
  announced terminal error and keyboard-native reload. These are unexecuted
  due to lock admission, not browser success evidence.
* `src/api/README.md`: describe bootstrap recovery and conservative parser
  boundaries. No knowledge-base file or pinned manifest input changed.

## P02 Validation

Environment: Python 3.12.3, Node 24.21.0, existing `/tmp/mv` tools. Explicit
source-first imports resolved core/API/agents to this worktree; distribution
metadata alone does not establish a fresh editable installation.

Heavy admission command:
`flock -n -E 75 /tmp/ama-rpi-heavy.lock bash` with the planned install/static/
full-unit/browser script. Exit 75 before script execution. `lslocks` identified
PID 661156 (`flock`) holding the exact shared lock. No retry, queue, owner
interruption, shared pip mutation, full suite or actual browser run followed.
Full commands remain as recorded in phase details. The explicit user fallback
permits targeted checks, not a fabricated complete/full-gate result.

Completed checks:

| Command or boundary | Actual result |
| --- | --- |
| Source-first `/tmp/mv/bin/python -m unittest test_ai_statement_sources test_workspace_scripts test_loading_feedback test_ai_tasks test_needs_inventory -q` | Exit 0; 83 tests, no skips |
| From src/core: `/tmp/mv/bin/ruff check .` | Exit 0 |
| From src/core: `/tmp/mv/bin/ruff format --check .` | Exit 0; 104 files already formatted |
| From src/core: `/tmp/mv/bin/mypy` | Exit 0; 157 source files |
| From src/api: `/tmp/mv/bin/ruff check .` | Exit 0 |
| From src/api: `/tmp/mv/bin/ruff format --check .` | Exit 0; 53 files already formatted |
| From src/api: `/tmp/mv/bin/mypy` | Exit 0; 101 source files, including browser checks |
| `node --check src/api/src/zava_forward/api/web/app.js` | Exit 0 |
| `git diff --check` | Exit 0 |

`PYTHONPATH` (root-relative):
`src/api/src:src/core/src:src/agents/src:src/api/tests:src/core/tests:src/agents/tests`.
External logs: `/tmp/ama-538-checks-SC4g3w/targeted-final.log`,
`core-static.log`, `api-static-final.log`. These are supplemental command logs,
not an exact-head gate receipt.

Original adverse attempts retained in execution history: baseline regressions
exit 1; first normalization retained newlines inside capture and failed four
assertions; flattening only captured whitespace resolved them. Initial core
format check exit 1 was resolved by existing Ruff formatter. A later test-only
bootstrap block was initially inserted into the wrong JS scope, causing syntax
and E501 failures; moving it into the async test body restored all checks.
Earlier external `targeted.log` and `api-static.log` preserve that failed run.
Final logs above, not earlier failures, describe the current candidate.

Unperformed: fresh editable installs, full core/API discovery, loading/briefing
Chromium/axe and workspace-script browser check. No Azure, private data,
live model, complete publication gate or human/hosted approval performed.

## Amendments and Divergences

Contextual abbreviation and null-session contracts are approved-plan
clarifications from the original independent critique. Extra actual-bootstrap
Node assertions are immediately relevant local test strengthening within the
same existing test method, not a scope expansion. Full validation uses the
explicitly authorized busy-lock fallback; this is a limitation, not a pass.

## Remaining Work and Review Readiness

P01/P02 complete. Candidate implementation and dated original evidence
committed locally as `0e910aa1e36c616c0b433b48e392e3ba94b97d2e`.
Original independent Review not yet executed. Source and current plan/details
agree; full/browser validation is the sole recorded local residual.
FU-001: later explicitly coordinated editable/full/browser validation after
the shared lock is free. Browser behavior remains implemented-unverified.
No new implementation defect is known; no push/cloud/child task authorized.

## Independent Review and Local-Only Closeout

The preceding implementation-readiness statement describes the pre-Review
boundary and is preserved, not converted into approval. The single independent
Review completed against source `0e910aa1` versus `204507d6` and current evidence
reconciliation. Original record:
`.copilot-tracking/reviews/logs/2026-10-29/loading-briefing-review-538-review.md`.
Execution Complete; outcome Not accepted.

* RV-001 High: terminal Sr./Jr. suffixes can merge an uncited first sentence
  into a second cited sentence. Independently reproduced; future implementation.
* RV-002 Medium: a defined but unready AsyncAction object fails in h() while
  building the new terminal reload action. Independently reproduced; future
  implementation.
* RV-003 Low: original examples are represented in regression fixtures, but
  the plan lacks their verbatim source/expected-output mapping; future planning
  evidence reconciliation.
* RV-004 Medium: actual-browser/full/editable validation remains unperformed;
  existing FU-001, at a later explicit free-lock coordination event.

Review independently passed the same 83 focused tests with no skips and JS/
whitespace checks. It did not retry the lock, install, run browser/full suites
or claim human/hosted acceptance. Its full original finding set is immutable.
No finding was silently fixed or marked closed and no second Review was run.
Task loop completed with an unsuccessful acceptance outcome; automatic session
stopped per explicit user request. Ranked future routes are in the state.
The final evidence-only commit does not change the assessed source candidate.
No push, az, force-push, closing keyword or automatic child work occurred.
