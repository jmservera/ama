<!-- markdownlint-disable-file -->
# RPI Changes: Nonblocking regulatory usage refresh

## Metadata

* Task ID: reg208-pr506-usage-refresh-2026-10-29
* Task slug: regulatory-usage-refresh
* Related plan: .copilot-tracking/plans/2026-10-29/regulatory-usage-refresh-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/regulatory-usage-refresh-phase-details.md
* Implementation date: 2026-10-29
* Baseline: 7e8ab4d5290177ef48b17d27ea8d64a4f39e8c73

## Execution Status

* Status: Complete, full plan.
* Completed markers: P01, P01-T01, P01-T02, P01-T03.
* Remaining active implementation markers: none.
* Critique: one independent execution, Complete / Pass, no findings.

## Execution Summary

Implement only the lookup lifecycle, one test method and the API usage guide.
Start with P01-T01 red evidence. Then remove the secondary await and validate.
No push, az, other-worktree operation or rubric edit is authorized.

## Completed Work

### Dependency restoration

The chosen baseline unittest failed importing zava_forward under system Python.
Created the initially empty current-worktree .venv and installed editable
src/core[sql,blob], src/agents, src/api, plus pinned Ruff 0.17.1.
No manifest change, private data or other worktree was used.

### Deferred usage regression proves the baseline defect

P01-T01: added exactly one test method to
src/api/tests/test_case_journey.py using the existing DOM and shipped_helpers
plus real chat.js. Four delayed outcome/input scenarios assert recovery before
usage settlement and preserve answer/dirty-field state afterward.
Node --unhandled-rejections=strict and timeout=30 are explicit.

The focused command failed as intended on unchanged production source:
AssertionError: usage must not keep lookup disabled (actual true, expected
false). One test, 0.039s, one failure; no dependency error.

### Answer completion no longer waits for usage

P01-T02: in src/api/src/zava_forward/api/web/chat.js the unchanged submitted
question is cleared before void refreshUsage(). The existing helper owns usage
errors; the existing finally immediately restores the button and focus.
src/api/README.md now documents independent background usage/failure behavior.
No other shipped functionality or copy changed.

### Focused checks pass

P01-T03: from src/api:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_case_journey test_chat_panel test_regulatory_chat_api test_regulatory_ux_check -q
```

69 tests passed in 34.616s, including the new four-scenario regression.
Existing synthetic missing-law-store/provider fallback warnings were logged;
the test runner completed OK with no skips or failures.

From the worktree root:

```bash
node --check src/api/src/zava_forward/api/web/chat.js
.venv/bin/ruff check src/api/tests/test_case_journey.py
.venv/bin/ruff format --check src/api/tests/test_case_journey.py
git diff --check
```

All commands exited 0; Ruff reports all checks passed and one file already
formatted. No new tools, manifest edits or generated checked-in assets.

## Implementation-Time Plan and Detail Updates

No material divergence; dependency restoration was already anticipated.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| System-Python baseline selected unittest | Existing raw-question regression | Failed prerequisite | ModuleNotFoundError: zava_forward; restored local dependencies |
| Local dependency installation | Current-worktree distributions and Ruff | Passed | pip exit 0 |
| Focused deferred-usage regression against original chat.js | P01-T01 red | Failed as expected | Button still disabled while usage pending; 1 test, 0.039s |
| Selected four unittest modules | P01-T01/T03 green | Passed | 69 tests, 34.616s, OK |
| node --check chat.js | Shipped changed JavaScript | Passed | Exit 0 |
| Ruff check and format --check | Touched test_case_journey.py | Passed | All checks passed; one file already formatted |
| git diff --check | Current implementation diff | Passed | Exit 0 |

## Pre-Review Reconciliation

Ready: all plan and detail markers match completed evidence; handoff prose,
validation state and remaining work agree. Exactly one test method was added,
none removed. No material divergence, active implementation blocker or
follow-up was discovered. One independent Review is pending; no browser,
whole-suite, publication, hosted or human acceptance is implied.

## Blockers

None after dependency restoration.

## Remaining Work

No active implementation work remains. Parent owns independent Review and
local commit. No push or publication is authorized.

## Follow-Up Items

None.
