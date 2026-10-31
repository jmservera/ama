<!-- markdownlint-disable-file -->
---
title: Resident survey mandatory gate harness correction research
description: Exact failed full-gate evidence and bounded root causes
ms.date: 2026-10-31
---

## Research Brief and Parameters

Task `571-correction2`, slug `resident-survey-check-571-correction2`, parent
`571-correction1`. Focused convergence for mandatory local gate harness repairs
needed by the owner's required validation/publication outcome. Same branch.
Non-goals: runtime/UI/grammar changes, workflow/hash/skip-policy changes, Azure,
private data, model calls, historical rewrite or weakened assertions.
Existing correction1 Research/critique/Review remain immutable.

## Prior Knowledge and Extensions

Reuse original and correction1 source/merge/acceptance research. One new focused
cycle for actual gate defects, no specialist needed for this continuous trace.
Repository full-gate, exact-head, pip and privacy-safe git guidance selected.
No interaction available; current owner direction requires persistence through
validation/publication. Repairs are limited to required harness behavior.

## Cycle 1 Wider

Full gate ran against committed `10401c5afcf2700c473909214a2698debe048548`,
main `a75bbdffa51ae34b1fcf779250f1f553d566ee93`, native shared-lock queued
11:08:57.513113Z and admitted 11:25:33.657179Z with one worker. Passed preflight,
all five project suites and namespace. Static rejected two synthetic opt-in
Chromium transcript lines; browser rejected nine B023 closure bindings.
Dependent infra/migration/SQL/images/logo unrun; no passing receipt claimed.
Reflection: genuine full execution reached failures, not a lock blocker.

## Cycle 1 Deeper

The skip-policy unit intentionally executes a printing subprocess through real
Runner.command. Runner echoes its synthetic transcript to stdout. The enclosing
static suite parser then reads two fixture lines as actual suite skips, correctly
rejecting project-api-only browser skips in static. Capture that fixture's stdout
locally and assert it still contains the transcript; do not change real parser,
skip allowlist, command matrix or executed-test counts.
Journey route callbacks close over reassigned pending/reads/loads lists,
snapshots and change strings. Explicit default-argument binding preserves each
iteration's target and clears B023 without removing routes or assertions.
Reflection: root fixes are in two test-harness files, not runner policy/runtime.

## Cycle 1 Contrarian

Rejected suppressing real skip output, extending static skip allowlist, dropping
browser lint, pin relaxation, disabling rules or partial gate publication.
Runner requires isolated Ruff E,F,I,B,UP and whole-file format for journey
harness. Its existing style is unformatted; standard formatter is needed on
that directly affected file. Keep every synthetic scenario/assertion.
Reflection: no closure factory/refactor/framework change is needed.

## Evidence and Findings

| ID | Source | Finding |
| --- | --- | --- |
| C1 | `tools/test_rpi_checks.py:89` | Synthetic transcript emitted twice by exact skip-policy fixture |
| C2 | `tools/rpi-checks.py:1025` | Strict enclosing suite parser must remain unchanged |
| C3 | `src/api/checks/case_journey_browser_check.py:74` | Loop lists captured without binding in route lambdas |
| C4 | `src/api/checks/case_journey_browser_check.py:255` | Chat route functions capture loop change and held list |
| C5 | `src/api/checks/case_journey_browser_check.py:370` | Mutation callbacks capture per-iteration snapshot/pending |
| C6 | `tools/rpi-checks.py:1350` | Required isolated lint and format contracts |

Failed receipt `/tmp/ama-571-correction1-full-gate/receipt.json`, full output
`/tmp/ama-571-correction1-full-gate.log`; preserve both unchanged. Current main
fetched after failure still `a75bbdff`. No missing prerequisite or workflow drift.

## Synthesis, Decisions and Readiness

Selected narrow capture/binding/formatter repairs with no assertions removed.
Research disposition executed; Planning Readiness Ready. One complete cycle
answers roots and rejects policy weakening; no deeper unrelated discovery.
Future gates may expose other baseline failures; preserve and assess them
explicitly rather than assuming success. Human/AT/live and hosted/owner gates
remain separate. No Closes until exact retained evidence passes publication gates.
