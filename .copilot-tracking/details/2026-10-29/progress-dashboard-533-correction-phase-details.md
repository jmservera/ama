---
title: Progress dashboard correction phase details
ms.date: 2026-10-29
---

Task 533-correction-2026-10-29; plan:
.copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction-plan.md.
Research C1-C7/W1 is sufficient. Initial direction: guard once at lifecycle
entry and use structured metadata, never infer field invalidity from HTTP failure
alone. No unresolved design decision. Missing requested venv is a disclosed
environment deviation, not an excuse to use another worktree's source.

## Current Completion and Evidence

P01-T01 and P02-T01 complete: guard, typed scoped metadata, inline field errors,
README and canonical regressions implemented. P03-T01 complete under caller's
lock-busy fallback: 35 targeted tests pass and targeted progress browser/axe
passes, 11 states with zero violations. Full discovery not run. Ruff, configured
mypy (102 files), JavaScript syntax, diff and all four scenario pins pass.
The targeted browser is not a full suite and ran separately after the full-suite
nonblocking admission was denied. P03-T02 remains pending only for independent
Review and local commits; no implementation work remains. Full-suite scheduling,
human accessibility/contrast assessment and publication remain later work.

<!-- P01 -->
## P01: Backend

<!-- P01-T01 -->
### P01-T01

Read history to a local; return None unless list. Keep [] behavior unchanged.
Add a dedicated DateRangeError(ValueError) used only for reversed or oversized
dashboard and reversed archive ranges. Catch it before ValueError at these two
endpoints and add reasons.fields for start/end; existing app.js already forwards
this channel. Do not change global error serialization.

Add inherited semantic regression with null, string, mapping, numeric and boolean
history, checking valid siblings are unaffected and unknown closures remain
visible unbounded but excluded with date filters. Extend HTTP test for both
range endpoints and an unrelated paging/unknown-parameter 400. Assert inclusive
366-day dashboard acceptance, 367 rejection and no archive 366-day cap.
Completion requires direct regression failure before fix and passing after.

<!-- P02 -->
## P02: Native form errors

<!-- P02-T01 -->
### P02-T01

In shared load catch, require 400 plus structured date field metadata. Attach
existing .field-error paragraphs by each date input, unique stable IDs and
aria-describedby/aria-invalid; render controls then override show() focus with
the first affected field. Do not move focus or add invalid fields on actual
read failures; retain alert/retry and cancellation/session safeguards. Fresh
controls naturally clear submitted errors after correction.

Expand existing real loopback browser check: reversed dashboard, oversized
dashboard, reversed archive (form submit); linked invalid URL with defaulted
end; inclusive max and valid wide archive. Assert text/IDs/focus and retained
values before axe; successful correction has no stale invalid attributes/errors.
Mock 503 and unrelated 400 to ensure service errors do not mark dates.
README briefly documents error behavior and malformed-history unknown policy.

<!-- P03 -->
## P03: Validation and review

<!-- P03-T01 -->
### P03-T01

Use /tmp/ama-533-venv, since caller path is absent, with absolute current src
api/core/agents paths before test fixture paths in PYTHONPATH. Verify imports.
Take flock -n /tmp/ama-rpi-heavy.lock before full API discovery and browser
run; release immediately after heavy work. If busy, no waiting or full suites:
run selected progress tests/check only and report reduced coverage.
Pinned axe asset from previous evidence must pass existing SHA-256 guard.
Write logs/reports only in a new external evidence directory. Run existing Ruff,
mypy, node --check and git diff --check; verify manifest pins without changing
them if no pinned target changed. No complete publication receipt claimed.

<!-- P03-T02 -->
### P03-T02

Reconcile plan checkmarks/details/changes and actual validation before Review.
Dispatch one independent read-only assessment of the exact correction diff,
with artifact-only write authority. Record execution separately from outcome;
route findings to later work, no repeat Review or in-task review/fix loop.
Configure local privacy-safe Git identity from authenticated account and commit
implementation plus original evidence with Conventional Commit/trailer. A later
evidence-only commit is permitted; never push or mutate PR.
