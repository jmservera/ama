<!-- markdownlint-disable-file -->
# RPI Changes: Loading startup correction

## Metadata

* Task ID: 531-correction-2026-10-29
* Task slug: loading-startup-correction-531
* Related plan: .copilot-tracking/plans/2026-10-29/loading-startup-correction-531-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/loading-startup-correction-531-phase-details.md
* Implementation date: 2026-10-29

## Execution Status

Complete, full plan. All P01/P02 task markers complete.
Write boundary: planned src web/tests/browser/API README and dated evidence.
No blockers; canonical heavy lock admission succeeded for required runs.

## Execution Summary

Complete pre-edit audit and one critique retained. PC-001 law initial failure
and PC-002 execution-time guideline requirements applied directly. PC-003's
parent filesystem premise contradicted by actual host access; defensive
busy/inaccessible prerequisite distinction retained. No re-critique.

Pre-edit web-design-guidelines activated and full current text/plain source
successfully retrieved 2026-10-29. Native/Fluent/ASCII/plain-language repository
standards take precedence over generic aesthetics. Scope is lifecycle fixes,
not styling or design acceptance.

## Completed Work

### P01-T01: Helper-owned notice disposal

async-action.js retains a WeakMap of control-owned notice disposers. Pending
guard stays first; a new task disposes the earlier notice before execution.
Success/abort removes its own node, failure remains until next attempt.
VM regression proves original failure, then reject/succeed, succeed/fail,
repeat/sync failure, sync success, abort, explicit region placement and
same-control/independent/null-control overlap with timer and inline-error checks.
Handler-owned busy/disabled behavior retained.

### P01-T02: Main completion and law sibling

app.js workspaceReady() independently removes startup in login, authenticated
start and terminal errors, preserving the ready event for timer cancellation.
Shared watchdog uses the startup region's display name. law.html reuses the
watchdog with its own static region; law show/fail independently settle it,
retaining prior reference content and All sources/search retry.
Browser matrix passed: blocked watchdog signed-out/authenticated/503, all
remaining index companion failures, optional plain-case fallback, failed law
entry/native keyboard reload and initial 503/rejection with/without watchdog.
All previous helper/law/HAX/async action/browser assertions also pass.
API README documents these boundaries and nonqueued heavy-lock behavior.

### P02-T02: Local Candidate and Original Independent Review

* Implementation/original evidence committed locally as
  7ed914c99d384b297a7c2e5c70a07c475ae174f8, Conventional Commit with Refs #531
  and required Copilot coauthor trailer. GitHub-authenticated privacy-safe
  repository-local address used for both author and committer.
* Exactly one fresh independent Review assessed
  4c586a762eea71faeb193bd75f16abdebbeaf330..7ed914c99d384b297a7c2e5c70a07c475ae174f8.
  Execution Complete / original outcome Conformant. Zero substantive findings.
  Canonical record: .copilot-tracking/reviews/logs/2026-10-29/loading-startup-correction-531-review.md.
* Reviewer independently refreshed current web guidelines and assessed all five
  changed web files against all fetched categories. Independently ran four
  focused VM tests, JS syntax/whitespace, baseline negative control, budget,
  source-byte and pin checks. Broader external full/strict/browser logs were
  parent-reported to that reviewer, not independently opened or rerun.
* No source edits after Review. Original critique and Review outcomes retained.
  Final artifact-only bookkeeping resolves temporal research question labels,
  current lock wording and completion markers; does not change original Review.
* Caller explicitly requested stopping with local commits and summary. No
  follow-up task starts; automatic session stops at this authorized endpoint.

## Implementation-Time Plan and Detail Updates

No source/requirement amendments after critique dispositions; approved law
sibling covers initial API failure as well as downloaded-entry failure.
Validation recipe correction uses normal pip build isolation instead of
assuming setuptools exists in the shared runtime. This is local execution
judgment, not a new dependency or material divergence.

## Validation Record

* Original reproduction: helper VM failed, exit 1, connected stale notice
  expected 0 / actual 1 after successful retry.
* After correction: 4 helper/loader VM tests pass; JS syntax and git diff
  whitespace checks pass.
* Scenario manifest: all four pinned source hashes match; no pinned files edited.
* Nonblocking heavy lock admitted using flock -n /tmp/ama-rpi-heavy.lock.
* First full evidence directory: /tmp/issue-531-startup-20261029-validation.
  Editable setup with --no-build-isolation failed because /tmp/mv lacks
  setuptools. Preserve log and repair with standard build-isolated pip.
* Despite setup failure, explicit source-first paths loaded this worktree.
  API mypy (101 files), Ruff lint/format (53 files), API full units
  (1219 tests, 316 opt-in skips), full loading browser and core mypy
  (157 files), Ruff lint/format (104 files) and core full units
  (1463 tests, 190 opt-in skips) passed.
* Browser Chromium 156.0.8078.4; pinned axe 4.10.3, expected SHA-256 verified
  by entry point; all new and existing scenarios passed. No Azure/live AI/data.
  Four retained briefing axe states have zero violations; the new failure
  states are DOM/keyboard checks, not independent full WCAG acceptance.

### Setup Repair and Final Validation State

* Each full run and shared-environment mutation held the exact canonical
  flock -n lock. No lock replacement, queue, busy-lock bypass or az operation.
* /tmp/issue-531-startup-20261029-validation-repair/editable.log records
  successful `/tmp/mv/bin/python -m pip install --no-deps -e src/core -e src/agents
  -e src/api` using build isolation. No application manifests changed.
* The first provenance wrapper failed because source-first PYTHONPATH caused
  importlib.metadata to select local egg-info without direct_url.json. This
  was a verification-command issue, not a package or source failure. Preserved
  original attempt; retried metadata verification without PYTHONPATH.
* /tmp/issue-531-startup-20261029-postinstall/package-provenance.log verifies
  editable=True and exact file URLs for this worktree's core, agents and api.
  All six required API/core strict commands and four targeted VM tests pass
  again after installation. No source changes between full suites and repair.
* Full command environment, from the repository root:
  `PYTHONDONTWRITEBYTECODE=1`; API PYTHONPATH is absolute api/src, core/src,
  agents/src, api/tests, core/tests, agents/tests. Core uses core/src,
  agents/src, api/src, core/tests, agents/tests, api/tests.
  Each project runs `/tmp/mv/bin/mypy`, `/tmp/mv/bin/ruff check .`,
  `/tmp/mv/bin/ruff format --check .`, and
  `/tmp/mv/bin/python -m unittest discover -s tests -q`.
  Browser runs from src/api:
  `/tmp/mv/bin/python -m checks.loading_briefing_browser_check --axe
  /tmp/issue-531-correction-20261029-validation-final/axe-4.10.3.min.js --out
  /tmp/issue-531-startup-20261029-validation/browser`.
* All requested checks have passed at stable source, not a blanket successful
  claim for the first wrapper (exit 1 for setup) or first provenance wrapper
  (exit 1). Existing opt-in SQL/integration skips remain skips, not passes.
  No full tools/rpi-checks.py publication receipt or human approval claimed.

## Pre-Review Reconciliation

At Review handoff, plan/details reconciled P01 and P02-T01 complete, with only
parent-owned commit/Review/finalization in P02-T02. Current changes and all
validation outcomes agreed. The sole Review completed on the committed boundary;
its original outcome and limitations are retained. Final bookkeeping now
reconciles all completed markers, evidence and stopped-session endpoint.
No source changes or review repetition. No source blockers.

## Blockers

None known.

## Remaining Work

None in accepted correction scope. Final artifact-only local evidence commit
is the delivery action for this record; no publication is authorized.

## Follow-Up Items

Owner retains screen-reader/voice, real-staff and hosted/live acceptance.
No publication or complete publication receipt requested or claimed.
