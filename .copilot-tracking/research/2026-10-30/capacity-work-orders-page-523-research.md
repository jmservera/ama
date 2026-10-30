---
title: Capacity and work orders issue 523 research
description: Focused local investigation of the current main baseline
ms.date: 2026-10-30
---

## Research Brief

Implement exactly issue #523, verifying the supplied main baseline
5634f9a077d175a931c15e3400114665d8c071ee on the owner's existing clean
fix/capacity-work-orders-page-523 worktree. Audience: delivery coordinator.
Output mode: convergence, preparing planning. Evidence root:
.copilot-tracking/research/2026-10-30/.

## Research Parameters and Direction Controls

Focused posture, selected for a bounded bug with named source targets.
Investigate capacity rendering, API/store contracts, seeded local SQL and other
manager pages. No Azure, deployment, live sign-in, secrets, private data,
push or issue mutation. Existing issue checkboxes are claims, not fresh proof.
Research, plan, implement and review in order is explicitly user-authorized;
automatic progression applies only to this task, with no unsolicited child work.

## Extension Registry and Participation

Repository instructions and source component guides apply. RPI research selected;
web-design-guidelines selected for any web edits/review. Fluent 2, WCAG and
plain-language standards are authoritative for UI. General research workers
skipped: the bounded continuous code trace is best handled inline. No intake
questions: scope and local-only limits are explicit and this host is noninteractive.

## Questions and Candidate Areas

* Q1: What caused the reported failure, and is the fix already in this baseline?
* Q2: Do seeded SQL manager routes, capacity empty/error/retry paths and regression
  coverage satisfy the criteria now?
* Q3: Which exact gaps, if any, need implementation without duplicating merged work?

Internal candidates: src/api web/ops.js, API routes, core SQL store, API tests,
checks/capacity_browser_check.py and prior issue evidence.
External candidates: issue #523/PR #528 and current web-interface guidelines.

## Research Cycle Log

Cycle 1 opening: prior-knowledge gate found the issue comment reporting PR #528
merged and live verification still pending. Verify this against current code;
do not assume a fresh implementation is needed or claim a live observation.
### Wider

PR #528 is merged as 1dde6a908c20358dbb3067dcdd674e5ad0bd246d, an ancestor
of this baseline. It already fixes the missing contract-version projection,
capacity-specific read errors, draft-safe retry and delayed-session failure.
The existing browser check enumerates the manager's actual navigation.
Reflection: do not reapply or redesign the merged runtime fix.

### Deeper

`_appointment_binding` now uses `p.get("contract_version")`, preserving Unknown
rather than fabricating contract authority. The HTTP regression deletes both
legacy contract metadata and resident bindings, asserts successful reads and
unchanged write denial. Fresh execution passed (one test, 0.841s).
The browser harness seeds generated data and supports owned real SQL Server,
but has no axe or keyboard-specific retry assertion.
Reflection: the remaining local delivery opportunity is scoped acceptance
coverage, not a second runtime fix.

### Contrarian

The reported AI-configuration correlation is not evidence that AI caused it:
the legacy-package regression reproduces the relevant read boundary without AI.
Live environment state is unknown and may not be inferred from local results.
Existing issue checkmarks and historical tests do not establish this candidate's
SQL/browser evidence. SQLite does not substitute for SQL Server. Local Docker,
SQL image and Playwright/MSSQL driver are available; system Python lacks
Playwright, and the shared venv lacks editable core installation. Use a fresh
external venv, pip only, and source fixtures. The shared heavy lock was free
at the read-only inspection; actual admission remains serialized.
Reflection: add optional pinned axe scans of seeded/error/empty capacity and
keyboard retry to the existing check, execute real SQL and retain residuals.
One complete focused cycle is sufficient; further code discovery is redundant.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/523, retrieved 2026-10-30 with
  `gh issue view 523` and `--comments`: scope, criteria and merged-PR claim.
* C1: src/README.md:64, local RPI gate separates focused checks from complete
  publication evidence; repository-wide instructions still require the complete gate.
* C2: src/core/src/zava_forward/core/appointments.py:97-114, null-preserving
  contract-version binding, already merged.
* C3: src/api/tests/test_procurement_api.py:127-163, legacy and empty HTTP
  regressions; fresh legacy regression passed on 2026-10-30.
* C4: src/api/src/zava_forward/api/web/ops.js:187-228, labelled load errors,
  read-only retry, route/session guards and history barrier.
* C5: src/api/checks/capacity_browser_check.py:28-51, actual manager inventory;
  :52-141 owned SQLite/MSSQL stores; :390-784 recovery/empty coverage.
* C6: src/api/README.md:659-697, existing contract and separate required browser check.
* W2: https://github.com/jmservera/ama/pull/528, retrieved 2026-10-30 with
  `gh pr view 528`: merged 2026-10-28T21:56:47Z.
* W3: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
  retrieved 2026-10-30 in full. Native actions, async announcements, empty/error
  states and reduced motion apply; repository ASCII/plain-language rules take
  precedence over generic typographic suggestions.

## Alternatives and Decision State

Select acceptance-check augmentation and fresh evidence. Reject duplicate
runtime changes: C2-C4 already satisfy that implementation. Reject deployment
or sign-in as explicitly unauthorized. No redesign or additional product scope.
Keep existing regressions, add a focused test of the new scan's failure behavior.
No separate worker was used for this tightly coupled trace.

## Current Decisions and Readiness

Research disposition: executed. Planning Readiness: Ready.
Runtime root cause is the historical missing `contract_version` lookup on
`/api/workorders`, already repaired by #528; this is not a new live diagnosis.
SQL/browser validation, live owner verification and final publication gates
remain separate. All questions answered to planning depth; no source writes
occurred in Research.
