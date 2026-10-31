<!-- markdownlint-disable-file -->
---
title: Resident Survey check phase details - Refs #571
description: Execution targets, boundaries and completion evidence
ms.date: 2026-10-31
---

## Metadata

Task 571, resident-survey-check-571. Plan and research use that slug in dated
2026-10-31 tracking folders. Source base: 5666bd33. No runtime edits planned.

## Phase Index

| Phase | Intent | Status |
| --- | --- | --- |
| P01 | Fresh positive/refusal browser evidence | Complete |
| P02 | One independent Review and gated publication | Pending P01 |

<!-- rpi:phase id=P01 -->
## P01: Preserve and strengthen the browser contract

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add fresh obsolete-prompt refusal coverage and guide

Research C1-C5 proves the correction is already delivered. In the browser
check, after the detailed positive document loop and its reflow/source checks,
send `documents help` and `forms help` using existing `ask_chat`. Each new
article must contain explicit task refusal, housing-officer help and rules
metadata, with no Survey, R-SURVEY, D-EPC or AI-suggestion leakage. Preserve
all positive checks and later behavior. Update the related README explanation.
No unit changes, helpers, runtime changes or unrelated cleanup. Completion:
scoped diff conforms to the coverage lock.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Execute local validation and record evidence

Depends on P01-T01. Use a task-owned pip environment after the observed missing
distribution failure; avoid changing shared editable environments. Run from
`src/api` with
`PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests`.
Run existing document/form/refusal HTTP units, complete resident browser with
installed Chromium and hash-verified axe, then exact `python3 -m unittest
discover -s tests -q`, `ruff check .`, `ruff format --check .`. Heavy commands
share `/tmp/ama-rpi-heavy.lock`; no bypass. Store heavy outputs externally;
changes record retains exact outcomes, counts, hashes and unproven boundaries.

<!-- rpi:phase id=P02 -->
## P02: Independent assessment and gated publication

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run one independent post-implementation Review

Depends on P01-T02. Fresh independent reviewer reads frozen diff and canonical
artifacts, writes only dated Review; no implementation or repeat Review.
Assess evidence honestly, including already-merged fix and out-of-scope
acceptance. Parent records outcome and routes findings.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Commit evidence, full gate, exact-head assessment, push/PR

Depends on P02-T01. Resolve `gh api user` id/login and repository-local
privacy-safe email for author/committer. Commit only scoped files and original
dated evidence, with required trailer and Refs-only text. Fetch main and run
`python3 tools/rpi-checks.py --all --base <current-main-sha> --out <fresh-external>`.
Verify receipt against newly fetched current main immediately before exact-head
assessment and push. Later commits/source/base/input drift invalidate receipt.
No cloud fallback, skips, fabricated receipt, force-push or merge. If blocked,
preserve actual failure externally and commit an honest blocker record; do not
push or create a PR. Human/hosted approval remains independent.

## Implementation Current State

P01-T01 matches the coverage lock. Complete updated Chromium/axe and focused
HTTP/Ruff checks passed. Full discovery first timed out on lock admission;
the admitted retry failed two imports because the existing Event Hub dependency
was missing. Task-owned pip environment now has all existing API/core extras
and dev dependencies; `pip check` passes, both affected modules pass (64 tests).
Third full discovery uses the exact requested unittest command, extending only
shared-lock queue allowance to `flock -w 1800` to avoid another contention-only
failure. No bypass, pin/source change or new critique. Outputs are external.
Required capacity preflight currently admits one worker.
Final discovery passed: 1430 tests, 515.446s, 320 explicit discovery skips.
No skip is counted as execution or as real SQL/browser/live acceptance.
Freshly fetched main is `1330869ea675ff019958846330108b4f45e163ce`;
the user-supplied base remains `5666bd33`. Publication ancestry reconciliation
is outside current explicit base direction. Preserve branch history, run one
Review, commit original evidence and record actual full-gate rejection if it
cannot validate this candidate; no push without a valid receipt.
P02-T01 executed exactly once, Complete / Residual work. Original implementation
and RPI evidence committed as `437965cb`. Actual `--all` attempt on a clean
detached exact-commit candidate was refused on current-main ancestry (exit 1),
before checks/receipt creation. P02-T02 local-commit portion complete; full gate,
verification, exact-head publication assessment and push/PR remain blocked.
