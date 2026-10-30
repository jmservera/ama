---
title: Workspace script retry 524 plan
description: Current-main local verification and evidence reconciliation
ms.date: 2026-10-30
---

## Task Metadata

* Task ID: 524
* Task slug: workspace-script-retry-524
* Planning status: Ready; one critique dispositioned
* Details: .copilot-tracking/details/2026-10-30/workspace-script-retry-524-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-30/workspace-script-retry-524-plan-critique.md

## Executive Summary

Verify the already merged retry implementation at the caller's exact main
baseline and reconcile the existing API recovery guide with fresh local results.
Do not duplicate working runtime code or rewrite historical RPI evidence.

### What You May Not Know

PR #527 already delivered automatic retry. The issue's unchecked live acceptance
cannot be performed under the explicit no-deploy/no-live-sign-in boundary.
Historical transport cause remains unresolved, an outcome permitted by AC1.
The existing local suite already exercises real failed-first-load recovery.

### Unresolved Decisions or Blockers

No planning blocker. Runtime behavior is implemented, not newly authored here.
Live verification remains owner-pending; full publication gates may expose
environment prerequisites and must not be reported as passed if blocked.

## User Decisions and Requirements

* Run research, plan, implement, review in order with dated artifacts.
* Address exactly #524 on fix/workspace-script-retry-524 at supplied main
  5634f9a077d175a931c15e3400114665d8c071ee; use Refs #524 only.
* Run full API unittest discovery, Ruff, format and mypy locally.
* Preserve native semantics, non-colour signals, reduced motion and current
  Fluent-derived/plain-language controls.
* Hold `/tmp/ama-rpi-heavy.lock` with `flock -w 600` for heavy validation.
* No Azure, deploy, live sign-in, credentials, private data, secrets or uv.
* Commit locally with the required trailer; never push or open a PR here.

## Goals

Establish current local acceptance without speculative changes or overstating
live delivery, root cause, accessibility, human or hosted acceptance.

## Scope and Non-Goals

Included: existing retry tests/browser checks, supplemental external scoped axe
evidence, API guide update and new dated RPI records.
Excluded: runtime changes absent a demonstrated #524 defect, new test ownership,
visual redesign, infrastructure, deployment and historical artifact changes.

## Functional Requirements

* Missing required scripts recover automatically within the existing finite
  page-lifetime budget, without document refresh.
* Exhaustion retains the exact error, live status and native reload action.
* Healthy dependencies do not reload; stale routes/sessions do not render.

## Non-Functional Requirements

* Existing two automatic attempts, 250/500ms delays, 5s timeout and stop after
  ambiguous execution remain unchanged.
* No secrets/private datasets or external browser network; constructed loopback
  data only. Preserve existing controls and all approval boundaries.

## Acceptance Criteria

| ID | Issue criterion | Planned evidence |
| --- | --- | --- |
| AC1 | Cause identified or unresolved with checked items | Current server source and HTTP status/size/MIME/cache assertions; explicit no live evidence |
| AC2 | Missing script retries and loads without refresh | Existing Node owner and real Chromium recovery with one document |
| AC3 | Existing message after bounded retries | Exact unit/browser message and request-count assertions, native keyboard reload |
| AC4 | Failed first load followed by successful retry test | Existing test_workspace_scripts and browser recovery owner executed afresh |
| AC5 | Live verification recorded or marked owner-pending | Explicit owner-pending record, no claim of live acceptance |

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-30/workspace-script-retry-524-research.md.
Changes: .copilot-tracking/changes/2026-10-30/workspace-script-retry-524-changes.md.
Review: .copilot-tracking/reviews/logs/2026-10-30/workspace-script-retry-524-review.md.
Automatic parent continues after one critique is dispositioned.

## Sources

Current research C1-C8/W1, actual workspace unit/browser owners and
src/api/README.md workspace recovery contract; original artifacts are preserved.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Verify current implementation

Dependencies: completed Research and dispositioned one-pass critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Execute local checks and record current results

Use the existing `/tmp/mv` validation interpreter (confirmed imports), selected
through PATH so the user command remains `python3`. Set source/test PYTHONPATH,
`PYTHONDONTWRITEBYTECODE=1`, and external Ruff/mypy caches. Execute from src/api:
`python3 -m unittest discover -s tests -q`, `python3 -m ruff check .`,
`python3 -m ruff format --check .`, `python3 -m mypy`.
Run existing workspace unit selector and real browser suite under the heavy lock.
Use pinned, hash-verified axe 4.10.3 for a scoped external browser scan of loading,
recovered and terminal retry states. Reuse the owned synthetic-server callback.
Record exact results and limitations, never synthesize success.

<!-- rpi:phase id=P02 -->
### [x] P02: Reconcile evidence and hand off

Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update API guide and reconcile RPI evidence

Add a short current-main local verification record to the existing #524 guide.
Preserve the historical-cause and owner-live gaps; document no runtime delta.
Reconcile plan/details/changes and run one independent post-implementation Review.
Commit implementation and original evidence; attempt complete local gate with a
fresh external directory. The gate already locks internally: run its admission
using its own bounded lock, not nested flock. No remote writes.

## Locked Test Ownership and Targets

Canonical regression owner: src/api/tests/test_workspace_scripts.py.
Semantic end-to-end owner: src/api/checks/workspace_scripts_browser_check.py.
Exact removals: none. Maximum additions: zero production/test files.
Canonical changed documentation: src/api/README.md, plus dated RPI evidence.
Generated output: new external session/temp directories only; no historical
cleanup authorized. Supplemental axe runner/report remain external, not a new
repository test suite. Existing browser helper may create `.venv` scratch;
its own context manager removes its named temporary data.

## Dependencies

Existing API/core/agents distributions, Node, Chromium and pinned dev tools.
Missing prerequisite failures permit isolated pip setup, not pin changes or uv.
Full-gate failure is a publication blocker, not permission to skip or use cloud.

## Critique Disposition

Original independent critique: Complete / Revise, one Medium PC-001.
Disposition: resolved directly by recording concrete interpreter/output layout
and executable/write probes. The reviewer's claimed general temporary-directory
prohibition is not present in the parent execution contract; do not infer one.
Existing `/tmp/mv/bin/python` is used read-only (no shared environment mutation).
All newly authored supplemental runner, pinned axe, caches and logs go under
`/home/azureuser/.copilot/session-state/4a9b9792-8318-4a58-b3a9-dd143fec4f16/files/issue-524/`.
The post-commit gate receives a new `full-gate` child there, outside the worktree.
Check interpreter executability and create/check writability of this owned
directory before execution. The caller-prescribed lock is unchanged.
The existing browser helper owns its narrow `.venv/zf-browser-*` scratch and
removes it itself; disable bytecode for its subprocess through interpreter
`-B` using a supplemental in-memory Popen wrapper, without editing the helper.
Inspect ignored/untracked candidate inputs before the gate; never delete
historical or unrelated material. No second critique.

## Follow-Up Items

* Owner: live response/cold-start/auth correlation and post-deployment check.
  Excluded by caller boundaries; no deployment or sign-in authorization inferred.

## Handoff

P01/P01-T01 and P02/P02-T01 implementation complete. Ready for the one independent
Review; local commit and external complete-gate attempt follow that Review.
The original critique remains Complete / Revise, directly dispositioned.
Final receipt remains external. The coordinator owns publication and exact-head
assessment. No runtime, style or test changes were needed.
