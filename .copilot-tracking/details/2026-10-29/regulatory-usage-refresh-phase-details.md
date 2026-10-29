<!-- markdownlint-disable-file -->
# RPI Phase Details: Nonblocking regulatory usage refresh

## Metadata

* Task ID: reg208-pr506-usage-refresh-2026-10-29
* Task slug: regulatory-usage-refresh
* Related plan: .copilot-tracking/plans/2026-10-29/regulatory-usage-refresh-plan.md
* Research: .copilot-tracking/research/2026-10-29/regulatory-usage-refresh-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Prove and fix answer-completion lifecycle | Complete | P01-T01 through P01-T03 |

<!-- rpi:phase id=P01 -->
## P01: Prove and fix answer-completion lifecycle

Context: C1-C5 identify a secondary await extending both manual control disable
and submit-handler busy state. Boundaries are the named behavior fix, existing
test module and owning API guide. No service, role, safety, legal or data-model
change. Completion requires red/green executable evidence and focused checks.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add deferred usage regression and capture red result

Use DOM plus shipped_helpers from test_case_journey.py and load real chat.js.
Stub admission/history so they cannot overwrite answer state during the test.
Defer the answer, then resolve it with a synthetic reply. Hold usage unresolved.
After a deterministic event-loop turn, assert answer and question rendered,
button enabled, unchanged input blank/clean, input focused, and submit promise
settled. Include a changed-input scenario to preserve its dirty state. Then
resolve valid usage or reject with an Error. Under Node
--unhandled-rejections=strict, assert usage-only result/error text and unchanged
answer status, available button and input. Retain the existing tests for pending
duplicate prevention and failed answer/thread. Use subprocess timeout=30.
Run the new method first against unchanged chat.js; record assertion failure
before applying the fix.

Test ownership: one new method in the existing case-journey class; removals
none; no generated assets or copied production logic.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Decouple refresh and update owning guide

Depends on P01-T01 red evidence. In the success branch, preserve answer/status,
move clearSubmittedQuestion before a nonawaited refreshUsage invocation.
Use explicit void if it improves intentional-fire-and-forget clarity, with no
new catch because refreshUsage owns request/render error handling.
The existing finally remains the only control/focus recovery owner.
Update the audit-only usage paragraph in src/api/README.md to explain that
refresh latency/failure does not hold lookup open and failures remain explicit.
No other code, visuals, copy or dependency-manifest changes are planned.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Validate and reconcile implementation evidence

Depends on P01-T02. From src/api, with installed current-worktree source
distributions and tests:../core/tests:../agents/tests in PYTHONPATH, run
test_case_journey, test_chat_panel, test_regulatory_chat_api,
test_regulatory_ux_check. Execute node --check on chat.js and Ruff check plus
format --check on test_case_journey.py. Keep generated outputs external;
record commands/counts/outcomes in changes. No full-suite or browser acceptance
is implied by targeted tests. Reconcile plan markers/details and record any
remaining publication/human boundaries before a single independent Review.

## Completion Evidence

* P01-T01 complete: deferred regression failed on original chat.js with the
  expected disabled-button assertion.
* P01-T02 complete: submitted-field cleanup now precedes void refreshUsage;
  existing caught refresh and finally cleanup retained; API guide updated.
* P01-T03 complete: all 69 selected tests passed, including the four deferred
  usage/input scenarios; Node syntax, focused Ruff lint/format and diff checks
  passed. See the changes artifact for commands/results.
* No active implementation markers, blockers, divergence or follow-ups remain.
  Independent Review and local commit are parent-owned next actions; no
  publication, browser/human acceptance or hosted check is claimed.
