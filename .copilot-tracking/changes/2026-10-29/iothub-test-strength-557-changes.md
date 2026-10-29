---
title: IoT Hub test strength changes
description: Implementation, validation and review handoff for PR 557
ms.date: 2026-10-29
---

Task: pr-557-test-strength / iothub-test-strength-557.
Scope: full approved test-only plan, with Review and commit handled by the
parent after implementation. Status: P01, requested validation and independent
Review complete; local commit remains.

## Canonical Inputs

* Research: .copilot-tracking/research/2026-10-29/iothub-test-strength-557-research.md
* Plan: .copilot-tracking/plans/2026-10-29/iothub-test-strength-557-plan.md
* Details: .copilot-tracking/details/2026-10-29/iothub-test-strength-557-phase-details.md
* Original critique: .copilot-tracking/plans/2026-10-29/iothub-test-strength-557-critique.md
* State: .copilot-tracking/rpi-sessions/2026-10-29/iothub-test-strength-557-state.json

## Baseline and Boundaries

Initial `git pull --rebase`: already up to date. Clean topic branch:
feat/iot-hub-live-140, matching open PR #557.
Pre-change HEAD: 2926a0afa1f81b85cfd23166262ec49a7361ca37.
Observed origin/main: 129808b3d0a2a5ab88bdcf631d2722362de9e857.
No push, Azure service access, production edits or score edits.

## P01: Implementation

P01-T01 complete: extracted assert_live_sku_guards(template), preserving
no-hub-PUT, constraints, original SKU/unit mismatch matrix and consumer-group
coverage. Both named reference fixtures assert the exact fixture hub ID before
returning synthetic SKU/capacity or location.

P01-T02 complete: assert_live_diagnostics now pins to-log-analytics. Existing
diagnostic mutation coverage retains scope/workspace cases and adds name-only
wrong-setting. One new method independently mutates SKU, units and location
references, verifies the expression changed and verifies failure identifies
both intended and wrong hub IDs. No test coverage removed or production file
changed. Candidate lock met: one new method, one extracted assertion helper,
two named local reference fixtures, zero generated targets.

## P02-T01: Validation

Pre-change baseline, from infra:
`python3 -m unittest discover -s tests -p 'test_iothub*'`.
Result: 22 tests, OK, no skips, 13.166 seconds.

Missing Ruff confirmed on PATH and system Python. Restored pinned Ruff 0.17.1
in external /tmp/ama-iothub-557-ruff-20261029, no dependency manifest change.
Local Bicep compilation verified SKU/unit inputs are value dictionaries while
location is a whole parameter-object expression; mutations must retain these
compiled shapes.

Final post-format command, from infra:
`python3 -m unittest discover -s tests -p 'test_iothub*'`.
Result: 23 tests, OK, no skips, 16.780 seconds.
The first post-edit run also passed 23 tests in 12.836 seconds.

Ruff 0.17.1, from repository root with executable
`/tmp/ama-iothub-557-ruff-20261029/bin/ruff`:

* `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_iothub_module.py`: All checks passed.
* `ruff format --isolated --line-length 100 --check infra/tests/test_iothub_module.py`: 1 file already formatted.
* `git diff --check`: passed.
* `git diff --exit-code -- .github/rubric/scores/latest.json`: passed; unchanged.

Initial lint found E501 on a new 101-column assertion. Ran the existing Ruff
formatter, then both lint and format check passed. No unrelated formatting.

### Counterfactual mutation sensitivity

Ran a local, in-memory AST counterfactual of the test module, removing only the
two new reference-ID assertions and the new live diagnostic-name assertion.
Asserted exactly three statements removed. Executed only the wrong-reference
and live-diagnostic mutation methods in that counterfactual namespace. Required
exactly four failures, zero errors and zero skips, identifying SKU, units,
location and diagnostic name individually.

Result: sensitivity verified; exactly four expected failures. Thus the new
mutations fail if their corresponding pins are removed, rather than passing
because of an unrelated pre-existing assertion. Counterfactual source was never
written to disk. All compilation was local Bicep; no Azure service operation.

## Amendments and Divergences

Ordinary implementation judgment: mutation code must account for the two
existing compiled parameter shapes. This preserves the approved expression-only
mutation and is not a scope or behavior change.
No material divergence or new user decision.

## Blockers, Remaining Work and Follow-ups

No implementation or Review blocker. P01, P02-T01 and P02-T02 complete.
P02-T03 local commit remains. No automatic follow-up session or publication
authorized. No new in-scope follow-up discovered.

## Review Handoff

Ready: plan markers, details, changes, blockers and validation reconciled.
Assess the named test file against C1-C6 and AC1-AC5, with original critique
preserved. Exactly one Review; material open criteria block successful closeout
and route to later work, not a second Review or implementation loop here.
Local commit is pending until Review completes. No full exact-head gate,
publication readiness, hosted/human approval, Azure acceptance or issue closure
is claimed for this deliberately local-only test change.

## P02-T02: Independent Review Result

Original record:
.copilot-tracking/reviews/logs/2026-10-29/iothub-test-strength-557-review.md.
Execution: Complete. Outcome: Conformant for the assessed implementation and
Review boundary. Findings: none; no routed correction or residual work.
Reviewer independently corroborated 23 tests/no skips, Ruff check/format,
22-to-23 method preservation and exactly four in-memory sensitivity failures.
AC1-AC4 proven; AC5's Review obligation met and local commit still pending.
No second Review or post-Review source edit.

## P02-T03: Local Persistence

Ready to commit the reviewed test file and this task's seven dated artifacts.
Repository-local privacy-safe identity derives from fresh gh api user:
8036360 + jmservera. No publication, push or approval claim. Persist completion
state only after the actual local commit succeeds; preserve the original Review.
