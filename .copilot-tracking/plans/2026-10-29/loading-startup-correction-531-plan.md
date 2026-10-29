<!-- markdownlint-disable-file -->
# RPI Plan: Loading startup correction

## Task Metadata

* Task ID: 531-correction-2026-10-29
* Task slug: loading-startup-correction-531
* Planning status: Complete; original critique Revise preserved, dispositions complete
* Plan date: 2026-10-29
* Phase details: .copilot-tracking/details/2026-10-29/loading-startup-correction-531-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/loading-startup-correction-531-plan-critique.md

## Executive Summary

Clear only the previous helper-owned feedback when a control starts a fresh
attempt. Preserve pending duplicate suppression and independently overlapping
reads/actions. Make app.js remove startup itself on every existing ready/error
path while keeping the watchdog for a missing app.js.
Implementation and required checks are complete. The original independent
Review is Complete / Conformant at implementation commit 7ed914c9.

### User Decisions and Requirements Highlights

* One complete pre-edit loading audit, regression checks, full RPI evidence and
  local Conventional Commits on the existing PR branch. No push or az.

### What You May Not Know

The only other helper-loading page, law.html, also hangs if its entry script
fails. Reuse the existing watchdog with a named law startup region; law show()
replaces that region independently and signals completion. No new framework.

### Unresolved Decisions or Blockers

None at planning. Heavy validation admission depends on the shared lock; busy
means targeted-only checks and an explicit recorded limitation.

## User Decisions and Requirements

* Fix both supplied findings and audit all sibling loading surfaces first.
* Test reject/succeed, succeed/fail and overlapping attempts.
* Block workspace-shell.js in an actual browser regression.
* Run full Research, Plan, Implement and independent Review with dated artifacts.
* Run git pull --rebase first; keep the existing topic branch and all commits local.
* Use src, no closing keywords, Conventional Commits and required Copilot trailer.
* Install required editable src packages in /tmp/mv; run API/core mypy, Ruff lint/
  format, unit tests with this worktree's source/fixture paths and relevant browser check.
* Hold flock -n /tmp/ama-rpi-heavy.lock for full suites; targeted-only if busy.
* Update scenario-manifest SHA-256 pins if pinned files change.

## Goals

Fresh attempts cannot display previous helper failures. Every audited script
failure has a usable terminal outcome without losing manual case work.

## Scope and Non-Goals

In scope: async-action.js, app.js, shared watchdog, law startup markup/completion,
existing helper/loader units and loading browser check, API README and dated RPI.
Not in scope: resident apps, redesign, hosted checks, deployment or publication.

## Functional Requirements

* Starting a fresh run clears its previous helper-owned feedback before task
  invocation, including sync success, sync throw and abort cases.
* Same-control overlap retains the same promise and one active notice.
* Distinct controls/null controls keep independent progress/errors.
* Login, authenticated startup and terminal errors independently remove startup.
* Missing app/law entry points retain native timed reload; missing watchdog does
  not leave stale startup after the main entry completes.
* Law initial service failure removes startup and cancels watchdog timers
  without clearing prior rendered reference content on later action errors.
* Preserve script retry counts, route/session guards, optional plain-case
  fallback, disabled-state ownership and human approval controls.

## Non-Functional Requirements

No dependency additions or type suppressions. Native controls, polite status,
200ms spinner delay and reduced motion remain. Current web guidelines apply
with Fluent/native/ASCII/plain-language repository precedence.

## Acceptance Criteria

* Helper tests assert zero connected stale notices after rejection then success,
  one current failure after success then failure, no duplicate attempt/status
  and independent out-of-order settlement across controls/null reads.
* Browser blocks watchdog for signed-out, authenticated and 503 outcomes;
  startup is removed even after simulated watchdog deadlines.
* Browser blocks every other index script individually and checks the existing
  bounded terminal recovery or explicit optional fallback.
* Browser blocks law.js and verifies timed native keyboard reload; also blocks
  law watchdog and verifies main completion removes startup independently.
* Law initial 503/rejection, with and without watchdog, stays terminal after
  both deadlines and recovers via All sources.
* Required strict and unit/browser checks pass, or lock/prerequisite blockers
  remain explicit. No claim of full publication or human acceptance.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-29/loading-startup-correction-531-research.md
(executed, Ready, C1-C10/W1). Changes record:
.copilot-tracking/changes/2026-10-29/loading-startup-correction-531-changes.md.
No evidence gap. Parent executes task-scoped automatic loop, then stops as requested.

## Sources

* Research C1-C10: full startup/helper inventory and existing regressions.
* User request 2026-10-29: exact branch, correction and validation boundaries.
* src/api/README.md and src/README.md: package validation and gate limits.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct lifecycles and lock regressions

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Per-control feedback cleanup

Add a WeakMap of helper-owned notice disposers; clear before fresh task starts.
Keep pending guard first. Cover sync/async/abort and overlap without DOM-wide
selectors or clearing inline errors.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Independent startup completion and sibling law recovery

Add app-owned completion helper at all current ready dispatch sites. Reuse
workspace-shell for law static startup, with per-region display name. law
show() replaces its startup region and notifies the watchdog. Expand existing
browser matrix to all listed dependency failures. Law fail() independently
removes startup/notifies too, retaining prior content for subsequent errors.
Use already activated web-design-guidelines and freshly fetched current source
before web edits; independent Review must refresh separately and report scoped
file:line findings with explicit limits.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and review local candidate

Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Strict, unit and browser validation

Targeted reproduction first. Install editable packages under nonblocking lock
before full suites. Run API/core mypy, ruff check ., ruff format --check .,
both full unit discoveries with owning test path first and shared source/test
paths, then full loading browser check with pinned axe. Busy lock means no full
suite or shared-venv mutation, targeted checks only. Record all outcomes.
If the lock or tools are inaccessible, record that distinct prerequisite
blocker rather than substituting another lock or implying a full pass.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Local commits and one independent Review

Update README and implementation evidence, commit source/original artifacts,
then obtain one fresh task-wide independent Review, record its original
outcome and commit final evidence locally. Blocking findings prevent a complete
correction claim; do not loop Review. Human/hosted approval remains unchecked.

## Dependencies

* Existing /tmp/mv Python/mypy/Ruff, installed source packages and Chromium.
* Local pinned axe 4.10.3, isolated constructed loopback fixture.
* Heavy lock nonqueued admission for full suites.

## Test Ownership and Change Budget

Canonical behavior: helper and loader VM units plus real loading browser check.
No test removals. At most two new helper unit methods, one loader unit method
and three new parameterized browser functions; existing tests may be extended.
No generated tests. Semantic coverage is explicit DOM notice ownership and
terminal startup outcome; regression coverage includes real blocked downloads.
Scenario manifest pins checked; no planned pinned-file changes.

## Critique Disposition

Original critique execution Complete / verdict Revise is preserved in
.copilot-tracking/reviews/plans/2026-10-29/loading-startup-correction-531-plan-critique.md.

| Finding | Disposition | Resolving plan/evidence |
| --- | --- | --- |
| PC-001 High | Applied directly | P01-T02 and acceptance require initial law failure completion, deadline stability and All sources retry |
| PC-002 Medium | Applied directly | P01 pre-edit source use and P02 sole independent Review fresh retrieval/file:line reporting explicitly assigned |
| PC-003 Medium | Unsupported premise rejected; defensive requirement accepted | Parent successfully read /tmp/mv tools using the host Bash tool; no workspace-only filesystem restriction applies to parent. User explicitly authorized /tmp/mv and canonical lock. Actual nonblocking admission will be recorded; busy and inaccessible remain distinct blockers |

## Follow-Up Items

* Owner retains screen-reader/voice, real-staff and hosted/live acceptance.
  Publication separately requires its original exact-head gates; no push is authorized.

## Handoff

All P01/P02 markers complete. Implementation/original evidence committed in
7ed914c99d384b297a7c2e5c70a07c475ae174f8. Sole independent Review Complete /
Conformant, no substantive task findings. Final local evidence prepared for
commit; no source changes after Review. Stop at caller-requested local-only
endpoint. No second critique, repeat Review, push or approval claim.
