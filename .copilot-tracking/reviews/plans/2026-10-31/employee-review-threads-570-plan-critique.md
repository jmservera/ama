---
title: RPI Plan Critique - Employee acceptance review threads
description: Single final-candidate credibility assessment for the issue 570 follow-up on PR 601
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 570-review-threads
* Task slug: employee-review-threads-570
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/employee-review-threads-570-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/employee-review-threads-570-phase-details.md
* Critique execution status: Complete
* Branch: fix/employee-identity-check-570
* Existing PR: #601
* Reviewed origin/main: e64c6e6c9da407682de59b926944424f94f50671
* Execution count: one final-candidate critique; no delegation or implementation.

## Inputs and Criterion Boundary

* Caller requirements: repair the two selected review threads only; small
  absolute floating tolerance for cluster containment; reproduce the 501-home
  producer failure at (54.9, -1.6); keep strict points, coordinate validity and
  geographic bounds; preserve missing-Chromium discovery qualification.
* Hosted requirement: add `python -m checks.employee_acceptance_check` after
  Chromium installation in src-ci.yml using the documented import environment;
  update its exact-byte SHA-256 WORKFLOW_HASHES pin in the same commit.
* Supplied research: .copilot-tracking/research/2026-10-31/employee-review-threads-570-research.md,
  including C1-C7 and the two supplied review-comment pointers W1-W2.
* Source evidence read: src/core/src/zava_forward/core/insights.py;
  src/api/checks/employee_acceptance_check.py;
  src/api/tests/test_employee_acceptance_check.py;
  src/api/tests/test_employee_identity_check.py;
  .github/workflows/src-ci.yml; tools/rpi-checks.py;
  tools/test_rpi_checks.py; src/api/README.md; src/api/pyproject.toml.
* Both named GitHub review comments were retrieved directly and agree with
  the supplied research and caller requirements. Repository index, memory and
  relevant case-study context were also consulted.
* Decisions and dependencies: existing branch/PR; main merge reported Already
  up to date and origin/main matches the caller's SHA; maximum two new test
  methods, zero removals, existing acceptance module owns producer and negative
  regressions, no core edits. P01 precedes validation/Review in P02; P03 requires
  P02 completion and no material publication defect.
* Validation boundary: relevant acceptance/identity tests, API discovery,
  configured Ruff/format/mypy, strict changed-adapter checks, requested
  `python3 -m unittest discover -s tools -p 'test_rpi_checks.py' -q`,
  workflow structure/digest verification and maintained Chromium CLI execution.
* The caller explicitly chooses CI as the gate and no full local gate wait.
  This assessment accepts that direction; it does not introduce an overriding
  local-gate demand or relabel prior gate failures.
* This is a plan assessment, not implementation verification, a fresh code
  Review, hosted CI acceptance, live identity attestation or issue closure.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C2; P01-T01; producer regression | Covered | Producer sums coordinates and divides at insights.py:143-179, while bounds use original extrema. Details require 501 uniquely identified fictional homes, default cap 500, cluster/count assertions, nonzero overshoot and successful projection through the real producer. |
| P01-T01; cluster-only tolerance | Covered | Exactly 1e-9 degrees absolute containment slack on all four cluster edges; no relative tolerance or core change. Existing validity checks remain before containment. |
| P01-T01; strict negative contracts | Covered | Details require both axes/sides, inside/outside tolerance, exact points, geographic limits, booleans, nonfinite coordinates/bounds and ordered bounds. Existing count/schema/duplicate-link checks remain intact. |
| P01-T01; test ownership and budget | Covered | At most two new methods in the existing acceptance module: producer regression and table-driven negatives; existing malformed cases may be extended, zero tests removed. No new harness. |
| C3-C5/C7; P01-T02; hosted browser execution | Covered | Current discovery precedes browser installation and the browser step omits this CLI. Details explicitly insert the CLI after installation with PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests from src/api. |
| C3-C4; P01-T02; no skipped acceptance | Covered | Missing-executable discovery qualification remains unchanged. Existing CLI at employee_acceptance_check.py:469-482 requires successful execution, exactly three tests and zero skips. |
| C6; P01-T02; workflow integrity | Covered | Same-commit exact-byte SHA-256 update affects only src-ci.yml in WORKFLOW_HASHES. Existing test_matrix_drift_and_unreviewed_extra_commands_refuse checks each workflow digest against source bytes. |
| P01-T02; documentation | Covered | API guide update records tolerance and hosted enforcement while preserving synthetic/non-live and discovery qualification boundaries. |
| P02-T01; requested validation | Covered | Component tests, Ruff/format/mypy, strict adapter/tool checks, requested gate-tool tests, real Chromium CLI and command order/environment/digest checks are specified. Missing Chromium blocks integration validation, not converted to success. |
| P02-T02; independent Review | Covered | One fresh independent Review of current artifacts and source diff, dated outcome retained, genuine residual work routed without a second Review of this task. |
| P03-T01; publication and thread disposition | Covered | Existing PR/branch, same-commit workflow/pin/evidence, privacy-safe authenticated identity, required trailer, non-force push and remote/thread verification. Resolve only addressed findings; no PR merge or issue closure claim. |
| Caller decisions; scope and dependencies | Covered | No secrets, live sign-in, private datasets, UI or core edits. Hosted CI and owner merge approval remain distinct from local checks; live #570 criteria remain unclaimed. |

## Verdict

* Verdict: Pass
* Rationale: The supplied final candidate covers both verified review requests
  at their producer/consumer and discovery/integration boundaries. Its bounded
  numerical change, producer-derived regression and negative matrix preserve
  the existing strict contracts. Hosted invocation, import environment and
  workflow pin are planned together with the requested validation.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

No actionable PC-xxx findings were identified within the supplied criterion
boundary. The complete actionable finding set is empty; no discoverable
concern is withheld for a later critique. There is consequently no finding
owner, resolving-evidence request or direct/decision disposition to assign.

## Strengths and Residual Risk

* The regression must demonstrate nonzero producer overshoot, preventing an
  inert hand-authored fixture from claiming to cover the actual defect.
* The selected slack is approximately 0.11 mm in latitude. It is bounded,
  cluster-only and unrelated to raw coordinate/geographic validity.
* The two-method budget can accommodate the full negative matrix through
  subtests without removing existing tests or changing browser method names.
* The CLI already fails on skipped browser tests, so reusing it after install
  enforces execution rather than creating a second acceptance harness.
* Source/hash drift is covered by an existing requested gate-tool regression.
* Implementation results and hosted CI are still pending. The caller accepts
  the CI-only direction; a planning Pass is not a passing publication check.
* Synthetic browser success will not prove live expected identity, deployed
  chat/map/case acceptance or operational privacy approval. The plan preserves
  these limitations and historical outcomes.
* Publication remains conditional on no material defect. Any changed reviewed
  scope during non-force push recovery must not inherit stale validation or
  Review claims; the plan's residual-work route remains available.

## Questions or Blocking Evidence Gaps

* None for this bounded planning assessment. No significant or divergent user
  decision is needed.

## Limitations

* No implementation, test, lint, type-check or browser command was executed by
  this critique; those are P02 execution evidence, not plan-credibility inputs.
* No full local gate was run or requested.
* Only the named review comments and relevant source evidence were inspected;
  this is not an open-ended repository or PR audit.
* Existing untracked research, plan, details and session-state inputs were
  observed and left untouched. Only this caller-authorized critique artifact
  was written; no plan, source or state was edited.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: planning parent.
* Smallest next action: record this Pass disposition and continue P01 under
  the supplied test budget and scope, without another plan critique.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/employee-review-threads-570-research.md](.copilot-tracking/research/2026-10-31/employee-review-threads-570-research.md) | Supplied bounded research and evidence |
| [.copilot-tracking/plans/2026-10-31/employee-review-threads-570-plan.md](.copilot-tracking/plans/2026-10-31/employee-review-threads-570-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-31/employee-review-threads-570-phase-details.md](.copilot-tracking/details/2026-10-31/employee-review-threads-570-phase-details.md) | Assessed task-level details |
| [.copilot-tracking/reviews/plans/2026-10-31/employee-review-threads-570-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/employee-review-threads-570-plan-critique.md) | This single completed critique |

## Next Steps

No user action is required. Return Complete / Pass to the active planning
parent for finalization and P01 continuation. This critique worker stops here;
it does not implement, delegate, run Review or perform another critique.
