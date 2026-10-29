<!-- markdownlint-disable-file -->
# RPI Phase Details: Loading startup correction

## Metadata

* Task ID: 531-correction-2026-10-29
* Task slug: loading-startup-correction-531
* Related plan: .copilot-tracking/plans/2026-10-29/loading-startup-correction-531-plan.md
* Research: .copilot-tracking/research/2026-10-29/loading-startup-correction-531-research.md
* Initial readiness: source audit complete, no material evidence gap.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Correct lifecycles and regressions | Complete | P01-T01, P01-T02 |
| P02 | Validate, commit and review | Active | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Correct lifecycles and regressions

Context: research C1-C9 demonstrates stale helper status and watchdog-only
startup removal. Law is the only sibling page loading the shared helper.
No redesign, broad status selectors or new dependency framework.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Per-control feedback cleanup

Keep pending deduplication first; then dispose previous helper notice before
task invocation. Store helper notices weakly by control without changing the
public API. Notice disposal cancels timers and removes only its own node.
Successful/abort completions remove their current node. Retained error remains
until that control tries again. Distinct controls and null-control reads do
not share cleanup keys. Preserve existing observer/disabled/busy restoration.

Likely targets: async-action.js and test_loading_feedback.py.
Validation: rejection-success and success-failure, repeat rejection, sync
throw/sync success, abort, same-control overlap, out-of-order independent
controls/null reads, timer cancellation, inline error survival.
Completion evidence: focused VM and full required checks.
Unresolved: none.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Independent startup completion and law watchdog

App completion removes #startup itself and still dispatches workspace-ready
to cancel watchdog timers. Replace each existing dispatch in login/start/error,
not route semantics. law.html nests static startup under law-out so normal
show() replaces it even if watchdog fails. Shared watchdog reads startup
display name (default workspace); law completion also cancels timer events.
Preserve native retry and existing thresholds.

Likely targets: app.js, workspace-shell.js, law.html, law.js, existing loader
VM and loading browser check. No index change needed unless evidence requires.
Validation: blocked watchdog with login, signed-in workspace and 503 error;
remaining eight companion scripts each blocked with explicit exhausted reload
or case tab fallback; app failure already covered; law entry failure and
watchdog failure separately, native keyboard reload. No raw default dataset.
Completion evidence: literal DOM outcomes, bounded request counts, no pageerror.
Unresolved: none.

<!-- rpi:phase id=P02 -->
## P02: Validate, commit and review

Dependency: P01. User-required strict/unit/browser checks, existing synthetic
fixtures and nonblocking lock admission. Never queue or inspect private data.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Validation

Use source-first PYTHONPATH with owning tests before other project tests.
Install core/agents/api editable in /tmp/mv while holding heavy lock; do not
mutate a shared venv if admission is busy. Targeted Node/unittest checks are
independent. Full API/core units may enumerate opt-in skips; record count and
do not equate them to integration passes. Run exact required Ruff commands
and mypy in each folder. Full relevant browser entry point verifies pinned
axe, real Chromium and owned synthetic loopback app. Verify manifest hashes
without altering unrelated files. Update API guide for actual behavior.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Commit and independent Review

Resolve gh api user and configure repository-local privacy-safe identity for
both author/committer. Conventional Commit, refs only, exact requested trailer.
Commit implementation/original research/plan/critique/change evidence before
one independent Review; write Review outcome honestly and commit final local
tracking. No push, az, publication gate or human approval claim.

## Critique Corrections and Execution Requirements

* PC-001: law fail() must independently remove static startup and signal
  completion, just like show(), without replacing prior reference content.
  Browser parameters cover initial 503/rejection with and without watchdog,
  advance beyond deadlines, preserve the error and retry via All sources.
* PC-002: P01 uses activated web-design-guidelines/current source fetched
  before edits. The sole P02 independent reviewer separately refreshes the
  source and assesses every changed web file with file:line findings,
  repository precedence and missing-check disclosures.
* PC-003: alleged parent filesystem restriction is unsupported by actual
  Bash access to /tmp/mv; original finding retained, premise rejected.
  Actual canonical lock/tool accessibility still must be recorded. Busy or
  inaccessible lock blocks full suites distinctly; never substitute a lock.

## Completion Evidence and Reconciliation

P01 complete: helper VM fails against the old implementation for the exact stale
notice assertion and passes after correction. Four helper/loader VM tests pass.
Real loading browser matrix passes every new blocked-watchdog, required/optional
companion and law entry/initial-service-failure case, plus all existing cases.
No test methods removed or added; three new parameterized browser functions.
Only existing planned targets changed; no amendment or significant divergence.
P02-T01 complete: API full 1219 / 316 opt-in skips, core full 1463 / 190 opt-in
skips, required strict lint/type/format and full loading browser all pass.
Initial editable setup lacked setuptools; normal isolated pip install succeeded.
Distribution direct_url metadata verifies all three packages point at this
worktree. Post-install helper/loader units and all strict checks passed again.
Original setup and provenance-wrapper failures are retained in changes.
P02-T02 remains only for commit, sole Review and final evidence.
