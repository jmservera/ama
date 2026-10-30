---
title: Workspace script retry 524 phase details
description: Execution boundaries and completion evidence
ms.date: 2026-10-30
---

## Metadata

Task ID: 524. Slug: workspace-script-retry-524.
Plan: .copilot-tracking/plans/2026-10-30/workspace-script-retry-524-plan.md.
Research: .copilot-tracking/research/2026-10-30/workspace-script-retry-524-research.md.
Starting state: merged runtime present; verify before making any change.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01 |
| P02 | Complete implementation; Review ready | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Verify current implementation

Context: research C3-C7 establishes existing issue coverage at the supplied base.
Intent: fresh evidence of exact behavior without redundant source changes.
Boundary: no package/test edits, no private data/cloud/credentials.
Targets: existing workspace unit/browser suites; caller's full API/static checks.
Dependencies: existing `/tmp/mv` interpreter and installed source packages; use
explicit source paths so another worktree's editable distribution cannot mask code.
Completion: captured current-run output, request bounds, readiness/error messages,
local static HTTP headers/bytes, scoped pinned axe results with limitations.
Unresolved: actual historical live failure cause and owner acceptance.

Completion evidence: full API discovery 1370 tests/318 existing skips; workspace
unit owner 3 tests; Ruff/60-file format/mypy 116 files passed. Existing real
Chromium suite passed on second bounded lock admission. Pinned axe found zero
violations in loading/recovered/exhausted scopes with reduced motion; recovered
map has 21 color-contrast incomplete nodes, not manual acceptance.
See the changes record and its external evidence root for original output.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Execute local checks and record current results

Use exact full API discovery selector and existing Ruff/mypy commands. Acquire
`flock -w 600 /tmp/ama-rpi-heavy.lock` for the heavy API/browser batch. External
caches and disabled bytecode avoid introducing ignored inputs. Browser suite
starts its own synthetic loopback app, checks health, aborts nonlocal requests,
injects transport/503 failures and stops its exact server PID. Supplemental axe
scans only recovery-relevant states with the existing integrity-pinned version;
do not infer whole-site WCAG conformance from zero scoped violations.
Preserve failures and report unchanged baseline problems without unrelated fixes.
No new regression tests are justified unless fresh execution demonstrates a
specific missing behavior, in which case stop affected planned source changes
and record the divergence rather than silently expanding this plan.

PC-001 layout: use existing `/tmp/mv/bin/python` read-only and place new runner,
axe, caches/logs and fresh `full-gate` child beneath the session-owned external
`files/issue-524/` directory. Probe executable/write access before running.
No actual parent rule prohibits temporary-path reads; no location bypass is
needed. Avoid repository caches with environment flags. For the existing helper
subprocess, add `-B` in memory to its exact Python argv; do not mutate source or
shared interpreter. Preserve helper-owned scratch cleanup and inspect candidate
ignored files rather than broadly deleting anything.

<!-- rpi:phase id=P02 -->
## P02: Reconcile evidence and hand off

Intent: make current evidence durable and exact scope clear.
Boundary: existing API guide and new dated artifacts only.
Dependency: P01 completed or explicit evidence blocker.
Completion: issue acceptance table, original one-pass Review, local commit and
external complete-gate result. No publication or live approval claimed.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Update API guide and reconcile RPI evidence

Update the existing workspace-recovery section with the current local evidence
and cause/live limitations. Do not copy tracking paths into production docs.
Keep earlier #524 artifacts untouched, including adverse reviews.
Run git diff/link review. Request a fresh independent reviewer to activate
rpi-review once against the implementation/evidence boundary and retain findings.
Resolve authenticated GitHub login/id only for privacy-safe local commit identity.
Commit with Refs #524 and the required Co-authored-by trailer. Run complete local
gate only after commit, recording its authoritative receipt externally. Any gate
failure remains a blocker for the coordinator, not a fabricated passing receipt.

Completion evidence: existing API recovery section now records actual 2026-10-30
local results and the exact unknown/live/accessibility boundary. No runtime or
test delta. Plan, details and changes agree on completed implementation scope.
Independent Review, local commit and complete gate are subsequent lifecycle/
publication steps, not already executed implementation claims.
