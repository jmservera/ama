---
title: Employee acceptance browser gate research for 570
description: Focused follow-up to the unresolved PR 601 receipt coverage thread
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Research Brief

Date: 2026-10-31. Researcher: RPI Agent / rpi-research.
Status: Complete. Output mode: convergence.

Investigate the mandatory post-install employee acceptance CLI missing from
local browser execution and receipt verification. Audience: PR #601 maintainers.
Scope: tools/rpi-checks.py, tools/test_rpi_checks.py, pinned src-ci.yml and
the maintained API acceptance CLI. Non-goals: app/UI changes, live identity
acceptance, receipt-format redesign, unrelated threads or historical evidence.
Criteria: default browser execution and full receipt requirements include the
exact CLI, test import paths and zero-skip integration contract.

## Research Parameters

Focused posture selected from the named bounded caller scope. Evidence root:
.copilot-tracking/research/2026-10-31/. External scope: PR #601 review metadata
only, retrieved 2026-10-31; no public research or private datasets.
Research edits are limited to evidence and lifecycle tracking.

## Extension Registry and Provenance

Repository instructions apply to all inputs; RPI research supplies the evidence
protocol. Web skills are skipped because no web source changes are planned.
Research specialists are skipped because this is one continuous code trace.
Non-interactive intake is adequate: exact thread and acceptance criteria supplied.

## Direction Controls

Owner selected PRRT_kwDOUU8JX86yRJOA on tools/rpi-checks.py. Pull and merge
completed on the existing clean topic branch; no merge conflicts occurred.
Use pip only, no secrets, no force push. Owner requests focused unit validation
and hosted CI rather than waiting for the full gate; repository publication
requirements must be reconciled before publishing, not silently waived.

## Research Questions

* Q1: Which exact command, cwd, environment and skip contract match pinned CI?
* Q2: How do execution and verification share required browser identities?
* Q3: Which regression proves default coverage without extra selectors?

## Prior Knowledge Gate

Read the case study, addendum, knowledge-base index, memory, sector primer,
source gate guide and parent gate-bootstrap state. Parent adverse full-gate
evidence is historical, not a current success. Verify supplied thread claims
against current source rather than assuming its workflow pin is sufficient.

## Research Cycle Log

Cycle 1 Wider: workflow, browser runner and receipt matrix traced inline.
Reflection: the workflow hash is current but does not add commands to the matrix.

Cycle 1 Deeper: inspected shared test-path helpers, skip parsing, runtime row
accounting, receipt verification and both receipt fixtures.
Reflection: suite/integration flags reuse the existing parser; the SQL-only
non-applicability exception means the employee CLI needs an explicit three-test,
zero-skip result bound as well as its own fail-closed exit status.

Cycle 1 Contrarian: considered extra selectors and relying on discovery alone.
Both fail the default-coverage requirement. Considered command flags alone;
they would leave the SQL skip exception available during receipt recomputation.
Reflection: retain unrelated SQL/discovery semantics and add an optional expected
suite count used only for this mandatory CLI.

Parent synthesis: focused questions answered; no further cycle required.
Single continuous trace handled directly; no worker execution implied.

## Evidence Log

* C1: .github/workflows/src-ci.yml:97-99 installs Chromium then invokes
  python -m checks.employee_acceptance_check with
  PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
* C2: tools/rpi-checks.py:704-714 and :1629-1644 omit that CLI from both
  required_checks and Gate.browser while requiring the chat-panel selector.
* C3: src/api/checks/employee_acceptance_check.py:472-485 runs exactly three
  named Chromium tests and exits nonzero for failure, changed count or any skip.
* C4: tools/rpi-checks.py:941-953 and :1307-1319 recompute suite evidence through
  check_skips; :1034-1073 allows one exact SQL-only integration exception.
* C5: tools/test_rpi_checks.py:27-87 demonstrates dispatch contract testing;
  :114-190 demonstrates rehashed adverse receipts; :358-409 and :723-740
  build scoped/full fixtures that need the new successful suite count.
* C6: tools/rpi-checks.py:505-513 and :1379-1382 expose reusable absolute
  test paths, but the literal pinned CLI paths also include source directories.
* W1: https://github.com/jmservera/ama/pull/601#discussion_r4431854464,
  retrieved 2026-10-31, unresolved thread PRRT_kwDOUU8JX86yRJOA confirms scope.

## Alternatives and Decision State

Select an unconditional post-install CLI command in the browser group, with
shared module/path constants in runtime and trusted matrix, suite/integration
flags and optional expected_count=3 in both result parsers (C1-C4).
Reject --extra-test dependence and discovery-only coverage (C1-C3).
Do not change workflow/hash, receipt schema, SQL exception or app sources.

## Open Questions, Risks and Residual Uncertainty

Live employee expected-object attestation remains outside this tooling change.
Full local publication evidence and hosted/human approval are separate gates.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready.
Self-check: all questions answered, three waves complete, evidence mapped,
alternatives disposed and residual acceptance/publication gates explicit.
