---
title: Indoor derived bounds review
description: Single post-implementation Review for issue 179
ms.date: 2026-10-27
---

## Scope and Evidence

Task 179 / indoor-derived-bounds-179. Date: 2026-10-27. Assessed boundary:
completed model/test/documentation changes against every #179 criterion at
the explicitly synthetic exercise boundary; no physical calibration or live
PRD acceptance claim. Source base: 0ded682bab690d24eb59b78e704be82d337bf6cd.

* Research: .copilot-tracking/research/2026-10-27/indoor-derived-bounds-179-research.md.
* Plan: .copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-plan.md.
* Details: .copilot-tracking/details/2026-10-27/indoor-derived-bounds-179-phase-details.md.
* Critique: .copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-critique.md.
* Changes: .copilot-tracking/changes/2026-10-27/indoor-derived-bounds-179-changes.md.

## Opening Review State

Goal: assess the record/dwelling-derived envelopes, both callers, independent
tests, exercise labels/provenance and the three-criterion audit.
Evidence readiness: implementation, ten canonical tests and relevant core
regressions/static checks complete. P01/P02-T01 reconciled. Supplemental API
discovery is still running; P02-T02 remains unchecked, and P02-T03 publication
is pending. First comparison: mathematical envelope against actual validated
domains, then tests and claims. Review is read-only except this one record.
No source fixes or repeated Review are authorized. Publication cannot claim
the still-running API check has passed.

## Execution Status

Independent source/test assessment: Complete; Conformant at the synthetic
exercise boundary, no substantive findings. A fresh read-only reviewer examined
the exact diff, callers, parameters, plan/PC-001 and criterion claims and reran
nine non-writing canonical tests (5.053 seconds, all passed). The writer/
fingerprint test was inspected and its parent-run pass retained.

The supplemental API discovery completed with four import errors (missing
declared azure SDK), not a green run: 1,058 tests in 830.173 seconds, 310 skips,
744 executed passes and four failed-test import entries. Restore the API's
declared dependencies into the isolated session venv, then retry only the four
affected modules; no source change or repeated Review is needed. Publication
remains held until that validation disposition is recorded.

## Independent Mathematical and Criterion Assessment

The reviewer confirmed the shared B/V equations, nonnegative vapour and
monotonic saturation envelope, bounded residuals and exactly two ordered
Gaussian calls in both paths. Conservative supported indoor temperatures
1.3096..38.3 C stay inside the saturation helper's guards. PC-001 is resolved
by independent composed numeric/state and recording Gaussian-call tests.
The 70,176 nominal record rows/replay, domain/tail/sensitivity coverage,
versioned parameter manifests, fingerprints and documentation support all
three #179 criteria. Closes #179 is justified at this exercise boundary,
not empirical calibration, parent #177 or live PRD acceptance.

## Findings

None. No corrective source/plan/research route. The missing dependency is
an execution-environment prerequisite with an explicit bounded restoration
and test retry, not an observed model defect.

## Plan-to-Change and Critique Reconciliation

| Scope | Evidence and assessment |
| --- | --- |
| P01-T01 | Shared typed math preserves validation/noiseless model and RNG order; both model versions advance to v2 and manifests carry exercise noise/bounds policy. Conformant. |
| P01-T02 | Independent numeric/envelope, two-call/state, domain/tail/saturation/sensitivity tests and actual paired-history/replay prove the intended behaviour. Six new methods; two existing references amended; no test removed. Conformant. |
| P02-T01 | README and dated synthesis/index/log consistently describe model-consistent exercise envelopes and changed seeded values while preserving original historical adverse outcomes. Conformant. |
| P02-T02 | Core/static/local link checks passed. Original API import failure is retained, with successful dependency restoration/retry below. No unresolved validation error. |
| P02-T03 | One independent Review executed; commit/push/PR is the remaining parent-owned publication action, not an unmet source requirement. Human/hosted approval is not inferred. |
| PC-001 | Original critique remains Complete / Revise; direct compatible disposition explicitly required composed numeric and RNG tests and implementation provides them. No second critique. |

No material implementation divergence or unaccepted user decision exists.
Marker-format reconciliation and environment restoration preserve the approved
intent; no source correction followed this Review. Read-only independent
assessment covered mathematical and acceptance uncertainty. The parent
reconciles this one complete finding set rather than running another Review.

## Acceptance Audit

| #179 criterion | Result | Resolving evidence |
| --- | --- | --- |
| 1. Inputs, equations and parameters documented/versioned | Supported | v2 PARAMETERS/COMPOSED_PARAMETERS and core README; generator source-revision and manifest binding tests; existing composed manifest tests. |
| 2. Every parameter sourced or labelled exercise | Supported | Broad model classification, explicit noise/tail-cap exercise classification and docs; physical 0..100% RH domain separated from an empirical threshold. No fabricated physical source. |
| 3. Indoor series inside plausible outdoor-record-derived bounds | Supported at synthetic exercise boundary | Temperature baseline B and vapour V derive from each actual pair and dwelling/household/dated effects. Tests cover 70,176 nominal record rows, exact repeats, analytic envelopes and adversarial extremes, without the former floor/clips. |

## Validation Evidence

| Check | Result and boundary |
| --- | --- |
| Relevant core combined suite | 142 run; 141 passed, one existing opt-in own-local-SQL skip. |
| Dependent resident sensors | 9 passed. |
| Final canonical suite after formatting | 10 passed; included in combined suite, not extra unique coverage. |
| Independent canonical rerun | 9 non-writing tests passed; no extra unique coverage claimed. |
| Changed-file ruff, format check and strict mypy | Passed, two changed Python files. |
| Git diff whitespace and three new relative links | Passed. |
| API discovery | Original run: 1,058 entries; 744 passed, 310 skipped, four missing-azure import errors. This failed result is preserved. |
| Four affected API modules after declared dependency restoration | 67 run; 61 passed, six existing optional SQL skips, no errors, 37.650 seconds. Only the affected modules were rerun, not a second monolithic discovery. |
| API coverage reconciled across discovery/retry | 805 passes and 316 skips over 1,121 actual tests after replacing the four import-error entries with their 67 real tests. No known unresolved test failure; not described as one green full-discovery run. |
| Heavy gate, Azure, real data/platform, human acceptance | Not run. No --all allowed; --changed reserved for large work, not this small correction. No cloud substitute or claim. |

Restoration used pip on the existing API manifest, in the isolated external
session venv only. No dependency manifest or source was changed.

## Plan Follow-Up Assessment and Routing

Competent real-building calibration is separate research for a later live-use
work item; Assets/Building Safety should commission competent review.
OD-43 requires Assets, Building Safety, DPO and data-owner decisions before
real monitoring. They remain outside #179 exercise acceptance, not silently
checked tasks, defects or blockers created for this synthetic story.
Parent #177 and live PRD AC-066--068 need their own evidence/approval.

No implementation defect, plan decision gap or material in-scope research gap
needs routing. No repeat Review is required or planned. Future live-readiness
work remains a distinct owner-selected follow-up.

## Outcome

Execution: Complete. Outcome: Conformant within the explicitly synthetic
exercise boundary. Findings: none. Closes #179 is justified, while owner PR
review/merge and hosted checks remain separate.

## Blockers and Remaining Work

No source or validation blocker. Parent owns P02-T03 commit/push/one PR to main.
Required human approval is not completed by this Review:

* [ ] Owner reviews and decides whether to merge the PR.
* [ ] Any future real-use calibration, OD-43 and operational approvals.

## Assessed Source Fingerprints

No source or test edits followed the independent assessment. SHA-256:

* src/core/src/zava_forward/core/synthetic/indoor_projection.py:
  `39de567d601f12767c579c885b3114c9ff1a531820ffd3bdbc30788097b38c11`
* src/core/tests/test_indoor_projection.py:
  `14a5164bacb7a6c6d9fdb581c92aeee55d1387e75b2c6b7efe7eb6cf280df3c8`

Final publication bookkeeping must preserve these exact assessed source bytes.
