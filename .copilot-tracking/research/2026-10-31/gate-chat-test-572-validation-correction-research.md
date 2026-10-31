<!-- markdownlint-disable-file -->
# Research: gate-chat-test-572-validation-correction

## Brief and Prior Knowledge

Date: 2026-10-31. Focused convergence research for the caller-selected child
correction of issue 572. Parent research, changes and original Review remain
unchanged. Goal: obtain actual execution and current exact-head publication
evidence, not redesign the already reviewed parser. Explicit automatic
continuation and publication authority are supplied by the caller.
Evidence root: `.copilot-tracking/`. No interaction is available or needed.
Repository, RPI and pip-only constraints selected; web skills skipped because
no web edit/review is proposed. No Azure, secrets or private datasets.
The original/addendum, reference index, memory and sector primer were consulted.

## Questions and Ordered Focused Cycle

Wider: inspect prior Review RV-001/RV-002 and changes. Both are missing execution
evidence, not source defects. Reuse the parent's exact-case source research.
Reflection: no further parser, workflow or skip-allowlist change is justified.

Deeper: fetch origin/main and perform the requested non-rewriting merge.
It reports Already up to date; 1330869e is an ancestor of 11829dbd.
The restored external venv contains the existing API/core/agents distributions,
Ruff 0.17.1, Playwright 1.64.0 and azure-eventhub 5.15.1.
Reflection: no dependency install or conflict resolution is currently needed.

Contrarian: an outer file-based flock around this self-locking gate opens a
second file description; its own exclusive flock cannot acquire until the
outer command finishes. That would create a self-deadlock, not useful waiting.
Use the caller's `flock -w 1800 /tmp/ama-rpi-heavy.lock <command>` for the
actual focused Chromium command. For the complete gate use its documented
internal lock with `--lock-timeout 1800`, retry once only on admission timeout.
Both use the same lock and 30-minute admission bound. No bypass, foreign-process
interruption or runner modification. API discovery and Ruff need no outer lock.
Reflection: preserve the runner's existing safety contract rather than add
lock inheritance merely to match a wrapper spelling.

## Evidence

| ID | Finding | Pointer |
| --- | --- | --- |
| C1 | Original Review preserves two execution gaps, not a parser defect | .copilot-tracking/reviews/logs/2026-10-31/gate-chat-test-572-review.md:168 |
| C2 | Prior gate executed no groups after lock timeout | .copilot-tracking/changes/2026-10-31/gate-chat-test-572-changes.md:143 |
| C3 | Runner opens and exclusively locks its own file description | tools/rpi-checks.py:2309 |
| C4 | Gate validates clean input before admission and verifies inside its lock | tools/rpi-checks.py:2351 |
| C5 | Guide explicitly forbids outer flock for the self-locking gate | src/README.md:128 |
| W1 | Four issue acceptance criteria still need current execution evidence | https://github.com/jmservera/ama/issues/572, retrieved 2026-10-31 |

## Disposition and Readiness

Research disposition: reused parent source evidence plus executed focused
three-wave correction investigation. Planning Readiness: Ready.
Selected: validation/evidence-only child loop, preserve every original adverse
outcome, one correction critique and Review, then commit and full exact-head
gate before independent publication assessment and push/PR.
Rejected: lock bypass, self-deadlocking outer wrapper for the gate, workflow/hash
edits, unnecessary source changes, premature issue closure.
Actual execution and future main drift remain uncertainties, not successes.
No further research cycle is justified; runtime evidence belongs to validation.
