<!-- markdownlint-disable-file -->
---
title: Workspace script retry implementation evidence
description: Changes and validation for issue 524
ms.date: 2026-10-28
---

# RPI Changes: workspace-script-retry-524

## Metadata

* Task ID: 524
* Plan: .copilot-tracking/plans/2026-10-28/workspace-script-retry-524-plan.md
* Details: .copilot-tracking/details/2026-10-28/workspace-script-retry-524-phase-details.md
* Implementation date: 2026-10-28

## Execution Status

Partial; full plan scope. P01/P01-T01/P01-T02 and P02-T02 complete; P02/P02-T01
remain incomplete because required heavy validation could not acquire the shared
lock. Source boundary: app.js, API README and two approved regression files.
Research complete, plan originally Ready after one Revise critique with direct
dispositions. Source is stable for an explicitly incomplete-evidence Review.

## Execution Summary

Implemented targeted error-only retries, terminal timeouts/load-without-global,
shared page budgets and route cancellation. Lightweight validation passed;
heavy validation was blocked before execution. No Azure, private data, secrets,
.env or deployment.

## Completed Work

### Targeted dependency recovery (P01-T01)

app.js now shares per-path retry promises, performs two delayed load-error-only
attempts with five-second timeout/cleanup, rechecks route globals and awaits
readiness before rendering. Existing terminal error text and native controls
are unchanged. Route abort check follows the wait; no views are invoked for a
superseded route. Source implementation complete; regression validation pending.

### Regression and operator coverage (P01-T02)

Added test_workspace_scripts.py using actual app.js in Node VM and
workspace_scripts_browser_check.py using the existing synthetic server lifecycle.
Unit coverage includes request limits, delays, timeout cleanup, HTTP load without
readiness, every existing role/route predicate, shared promises, stale routes and
sign-out. Browser coverage owns actual script evaluation, retry HTTP failures,
exhaustion/native keyboard reload, no document refresh, delayed lexical evaluation
and local HTTP status/size/headers. README documents bounds and live limitations.

## Implementation-Time Plan and Detail Updates

None beyond final planning dispositions. No second critique.

## Validation Record

Node syntax, 32 lightweight workspace/role/navigation/design/content/accessibility
unit tests, package-wide Ruff and mypy (92 source files) passed. Explicit
100-character validation of both new Python files passed after wrapping four
browser-check lines. Initial mypy run caught
an unnecessary incorrectly typed Browser event listener; it was removed and the
next targeted type check passed. API discovery and Chromium did not execute:
nonblocking flock exited 1 because another process holds /tmp/ama-rpi-heavy.lock
(observed PID 4061333). No lock bypass, blocking wait or alternate lock used.
Dependencies
installed from existing manifests in /tmp/ama-524-venv after system import failure.

## Pre-Review Reconciliation

P01 and source summaries reconcile with plan/details. P02-T01 remains unchecked;
P02-T02 handoff reconciles the known missing evidence. Independent Review receives
the stable source once with API/browser validation unavailable, not a purported
passing candidate. Full publication gate remains required after commit.

## Blockers

Heavy validation is temporarily blocked by the required shared lock. Live cause
unresolved; deployment verification pending owner. Publication gate unexecuted.

## Remaining Work

P02-T01 (API discovery and browser fault injection), final exact-head gate and
receipt verification, then publication only if all required gates pass.

## Generated-output preservation

The finite 41 task-generated egg-info/cache/bytecode files were archived, readback
verified, restored and hash-compared before individual removal. The entire
3206-file tracking snapshot was also archived and checked unchanged.
External selection, protected hashes, archive, restored files and prune journal:
/tmp/ama-524-generated-archive-20261028. No historical tracking records were
removed. This keeps gate inputs clean without discarding original RPI evidence.

## Committed-candidate publication attempt

Candidate 464558bb was committed with the authenticated account's privacy-safe
noreply email for both author and committer and the required Copilot trailer.
After fetching origin/main, the complete gate was attempted against the reviewed
base 413ccaf253fce4566e855bae9d0a924b2a82b506:

```bash
python3 tools/rpi-checks.py --all \
  --base 413ccaf253fce4566e855bae9d0a924b2a82b506 \
  --out /tmp/ama-524-final-464558bb --lock-timeout 0 --jobs 1
```

Result: exit 1, `BLOCKED: Global heavy-resource lock timeout`. No gate group
started, no passing receipt exists, and receipt verification was therefore
unavailable. External output/log remain preserved. This adverse attempt does not
supersede the missing API/Chromium evidence or original Not accepted Review.
The branch was not pushed and no PR was opened: required publication gates are
unmet. No force push, main write, Azure action or issue-closure claim occurred.

## Follow-Up Items

RV-001/RV-002 route to a later rpi-implement invocation: session-ended
post-await guard and deterministic late-delivery assertions. RV-003 routes
missing API/Chromium evidence to bounded later collection under the shared lock.
These are not marked closed or added to completed P01/P02 claims.
Owner live response/cold-start/auth correlation and post-deployment check.

## Return-to-Caller State

Implementation execution Partial. The one independent Review execution is
Complete and outcome Not accepted; its original record is
.copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-review.md.
RV-001 reproduced same-document session-ended stale status/view dispatch;
RV-002 found non-deterministic/incomplete late-delivery proof; RV-003 records
mandatory API/Chromium non-execution; RV-004 preserves owner-pending live work.
No findings were silently fixed or marked closed after Review. Required
API/browser checks and publication remain blocked; full receipt unavailable.
Commit this local candidate and original dated evidence only. Do not push or
open a PR without required publication gates. No issue closure is claimed.
