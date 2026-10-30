---
title: Sensor mean-step boundary correction original Review
description: Independent original assessment for PR 587, Refs #188
ms.date: 2026-10-30
---

## Scope and Evidence

* Task ID: 188-pr587-mean-step-boundary
* Review date: 2026-10-30
* Review scope: complete bounded source correction and requested local validation
  for PR #587, Refs #188. P02-T01 post-Review reconciliation and local commit
  remain parent-owned, not completed by this assessor.
* Assessed boundary: formula, inclusive decision, report behavior, external
  regression, types, locked source ownership, critique dispositions,
  implementation updates, validation truthfulness and follow-up separation.
* Plan: .copilot-tracking/plans/2026-10-30/sensor-mean-step-boundary-188-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/sensor-mean-step-boundary-188-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-30/sensor-mean-step-boundary-188-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-30/sensor-mean-step-boundary-188-changes.md
* Research: .copilot-tracking/research/2026-10-30/sensor-mean-step-boundary-188-research.md
* Source evidence: actual working diff and current contents of
  src/core/src/zava_forward/core/synthetic/sensor_consistency.py,
  src/core/tests/test_sensor_handover.py and src/core/README.md.
* Supporting contracts: src/core/pyproject.toml,
  src/core/src/zava_forward/core/sensor_consumer.py and
  src/core/tests/test_sensor_privacy.py.
* Authorized external evidence root:
  /home/azureuser/.copilot/session-state/451e3ac2-96a7-4da9-a4ad-5f807e8aad8a/files/.
  Read mean-step-red.log, mean-step-green.log, core-validation.log,
  core-validation-final.log and core-install.log.
* Read-only branch inspection: feat/sensor-ingestion-consistency-188;
  HEAD 2b7aec802f98338805e32421c5291b3caf7ec866 has
  18602ae7103ceee89fa4c87ca312b04a57ca0dba as an ancestor.
  No remote PR lifecycle or exact-candidate publication assessment was rerun.
* Project context was read; owner memory is context, not acceptance evidence.

## Opening Review State

* Interpreted review goal: independently assess exact inclusive comparison, nonconstant-reference
  regression, preserved report semantics and truthful validation boundaries.
* Review scope: P01 completed correction and validation, plus P02 handoff fidelity.
* Evidence readiness: assessor has read the five named task artifacts and
  inspected the three-file working diff on feat/sensor-ingestion-consistency-188.
  P01 is marked complete; authorized external red/green and validation logs
  were the next comparison boundary at opening.
* Acceptance basis: current plan criteria and passing one-time critique.
* First comparison boundary: mean-step arithmetic and regression against the actual diff.
* Active read-only boundaries: source, tests and original artifacts; only this canonical
  Review record may be written.
* Initial blockers: none for assessment. One opt-in local SQL skip, unrun full
  publication gate and live/hosted/human acceptance remain explicit limitations.

## Execution Status

* Execution status: Complete.
* Review execution evidence: this is the task's one independent original
  post-implementation assessment, completed on 2026-10-30. All supplied artifacts,
  the actual diff and five authorized logs were inspected. A read-only in-memory
  evaluation of the current arithmetic AST matched an exact Fraction oracle;
  existing test ownership was independently checked against HEAD.
* This execution status describes Review execution. The full plan still has
  parent-owned P02-T01 reconciliation and local persistence pending.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Nonconstant-reference red-to-green correction | Reconciled | Current diff implements the specified numerator, scaled inclusive limit and report-only division; external red/green logs agree. |
| P01-T02 | Typed Decimal sums and final requested validation | Reconciled | Final log supersedes, but does not erase, the original typing failure. The declared skip is identified in both source and final output. |
| P01 | Complete correction and validation | Reconciled | Plan checked markers, details completion state and changes evidence agree. |
| P02-T01 | Original Review then local commit | Reconciled as pending | Pending marker is intentional; no local commit or clean candidate is claimed. Parent owns the next action. |
| Follow-Up Items | Publication, hosted/human and live evidence | Reconciled as outside scope | Open items are mirrored in changes, not promoted into correction acceptance or claimed complete. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/synthetic/sensor_consistency.py | Replace rounded-mean decision with reference-adjusted side sums | Actual diff and exact oracle | 24 in-memory cases passed; red-to-green method evidence | Conforms to requested formula and inclusive boundary |
| P01-T01 | src/core/tests/test_sensor_handover.py | Add one nonconstant-reference method, 24 subcases | AST comparison with HEAD confirms one added method and unchanged existing methods | Original four boundary failures; corrected method passed | Required reproducer, signs/channels, counts and isolation covered |
| P01-T01 | src/core/README.md | Explain comparison before division | Three-file diff | Documentation and contract inspection; diff check passed | Accurate, directly related, preserves synthetic-only acceptance caveat |
| P01-T02 | src/core complete configured surface | Validate sensors, lint, formatting and typing | Supplied final execution output | 142 tests, one declared skip; ruff and mypy passed | Requested evidence is supported, within stated configuration and skip limits |

### Arithmetic and Report Contract

Let B be before_count, A be after_count and D_before/D_after be the
actual-minus-reference sums. The implemented decision uses
N = abs(D_after * B - D_before * A) and S = B * A.
N/S is exactly the magnitude of the reference-adjusted difference of means.
The check uses N <= Decimal(str(limit)) * S before division.
Both counts are positive because existing validation requires at least two
samples per side.

For the required B=A=3 positive example, D_before=0.00 and D_after=0.30.
N=0.90 equals the scaled limit 0.9; the report returns 0.1.
Independent in-memory reconstruction of the old divided-mean calculation gave
0.100000000000000000000000003, incorrectly above 0.10.
For B=2, A=3 with common offset 0.02, D_before=0.04 and
D_after=0.06 plus three signed steps. At either signed 0.10 step,
N=0.60 equals 0.6; 0.09/0.11 yield 0.54/0.66.

The admitted NUMBER shape allows at most two fractional digits and small
bounded values. These fixture sums and integer cross-products fit exactly
within the default 28-digit Decimal context. The decision no longer introduces
recurring division. No claim is made for arbitrarily mutated ambient precision
or unbounded sample counts exceeding the context's capacity.

The independent check evaluated the actual current AST expressions for
step_numerator, step_scale, the mean_step check and step_error, not merely a
separate proposed formula. All 24 signed/channel/count/delta cases agreed with
a Fraction oracle and the expected report magnitudes.
Explicit Decimal(0) sum starts keep numerator typing Decimal without casts,
ignores, precision changes, quantization or epsilon.

Report version, keys, units, counts and tolerance representation remain
unchanged. Means and standard deviations still use the previous computations;
point/stddev checks remain independent. Only mean_step_error now divides the
decision numerator, so report rounding cannot drive the decision. Float report
metrics remain representations, not exact threshold oracles.

### Regression and Source Ownership

The required zero-offset three-prefix fixture has exactly
10.00/10.00/10.00 before and 9.99/10.00/10.00 in the reference suffix.
Its fourth-slot boundary selects three samples on each side; it does not
incorrectly reuse the full-window HANDOVER constant.
The second variant retains two prefix and three suffix samples and applies
0.02 to both sides, detecting missing prefix subtraction and equal-count
assumptions. Both channels and signs cover 0.09/0.10/0.11.
Assertions inspect aggregate pass, all target-channel check flags, counts and
reported error. Generous point/stddev limits isolate mean-step behavior;
the untouched sibling channel retains zero tolerance.

The tracked diff is exactly three named files: 56 insertions and four replaced
lines. There are no test removals, changed existing test methods, packaged tests,
new production modules, dependency/configuration changes or generated targets.
Untracked task artifacts belong to the supplied parent workstream and were not
discarded, moved or committed. This assessor wrote only this Review path.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T02 | Add explicit Decimal zero starts to sums | Original mypy run inferred object and reported two operator errors; no new user decision needed | Current source, details completion state, changes update and final validation agree | Original critique Pass retained; no material direction change | Supported local implementation correction, not a divergence or unresolved failure |
| P01/P02 handoff | Mark validated work complete, retain Review/commit pending | Final successful component checks | Plan markers, details index, remaining work and changes handoff agree | No significant revision or fresh critique required | Preserves caller intent and stage ordering |

## Critique and Material Revision Assessment

* Latest critique dispositions: one original critique, execution Complete,
  verdict Pass, no actionable PC findings. Its formula, fixture, typing and
  evidence-boundary rationale match the implementation.
* Material revisions: none. Decimal sum starts are within the approved formula
  and strict-typing requirement, not a new architectural decision.
* Dependent-work pause assessment: supplied artifacts record P01 after Research
  and critique, with P02 pending final validation. No contrary evidence supports
  premature publication or a repeated critique/Review.
* Justification assessment: supported. Original red and failed typing evidence
  remain preserved and are not treated as current unresolved defects.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Exact-candidate publication gate, hosted checks and human approval | No push authorized; focused checks are not the complete gate receipt | Coordinator, separately authorized publication work | Open, distinct follow-up RV-001 |
| Actual Hub/Azure SQL handover evidence | Synthetic arithmetic correction is not live transport, SQL or sensor acceptance | Coordinator, separately authorized live-evidence work | Open, distinct follow-up RV-002 |

These follow-ups remain outside active implementation and correction acceptance.
The existing local-SQL opt-in skip is disclosed, not silently waived into live
SQL acceptance.

## Findings

No implementation defects, material decision gaps or material research gaps
were found in the assessed correction. The complete actionable finding set is
the following two non-blocking, coordinator-owned follow-ups.
Severity counts: Critical 0; High 0; Medium 0; Low 2.

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Publication eligibility remains unproven

* Related scope: plan Follow-Up Items; outside P01 correction acceptance.
* Evidence: plan and changes explicitly exclude a full publication receipt,
  push and hosted/human acceptance. Current worktree is uncommitted; component
  logs do not establish an exact-head gate.
* Impact: this correction must not be described as publishable or whole #188
  acceptance solely from focused local checks.
* Destination: distinct follow-up, coordinator-owned publication work.
* Smallest useful next action: after parent reconciliation and privacy-safe
  local commit, retain no-push status. If separately authorized to publish,
  obtain the required complete exact-candidate gate and receipt verification,
  independent exact-head assessment, hosted checks and human approval.
  This is not a request to repeat this original Review.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Live sensor and actual Hub/Azure SQL acceptance remains separate

* Related scope: plan Follow-Up Items; outside local correction acceptance.
* Evidence: src/core/README.md retains synthetic-only limitations; final
  sensor output explicitly skips
  test_sensor_privacy.SensorPrivacyTests.test_actual_owned_mssql_admission_and_idempotency
  for "opt-in own local SQL". No live evidence is supplied or claimed.
* Impact: model/ingestion parity does not prove physical accuracy, real
  transport, actual Azure SQL handover or whole #188 completion.
* Destination: distinct follow-up, coordinator-owned live-evidence work.
* Smallest useful next action: retain these unmet boundaries under Refs #188;
  separately scope and authorize actual sensor/Hub/Azure SQL evidence with
  the relevant operational and human approvals. Do not activate private
  datasets, SQL opt-in or Azure as part of this correction.

## Defects

* None within the assessed boundary. No later rpi-implement correction is
  recommended by this Review.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | Distinct publication follow-up | Coordinator; separately authorized exact-candidate gates | Outside correction acceptance, not an implementation defect |
| RV-002 | Distinct live-evidence follow-up | Coordinator; separately authorized actual handover proof | Outside synthetic correction acceptance, not a research blocker for this formula |

No finding is routed to rpi-plan or rpi-research. Later work does not require
this original Review to run again.

## Residual Work

* RV-001 and RV-002 preserve the existing distinct follow-up boundaries.
* P02-T01 post-Review reconciliation and local commit are ordinary parent
  continuation, not defects and not falsely marked complete here.

## Blockers and Remaining Work

* Blockers: none for the completed assessment or bounded source correction.
* Remaining active work: parent records this original result, reconciles
  P02-T01 and commits explicit candidate paths locally using authenticated
  privacy-safe author/committer identity and the required Copilot trailer.
* Publication and live acceptance remain unproven. No push, Azure operation,
  source/test fix, artifact mutation outside this path or nested Review was
  performed by this assessor.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Original selected unittest method; mean-step-red.log | Required regression before correction | Failed, intentionally preserved | One method, four positive exact-boundary failures across channels/counts; 0.018s |
| Corrected selected unittest method; mean-step-green.log | Same external regression | Passed | One method, all subcases; 0.018s |
| First combined unittest discovery; core-validation.log | test_sensor_*.py plus test_resident_sensors.py per changes record | Passed with declared skip | 142 tests, 17.213s, skipped=1 |
| First ruff check and format check; core-validation.log | Full configured core | Passed | All checks passed; 115 files already formatted |
| First mypy; core-validation.log | Full configured core | Failed, subsequently resolved | Two object/Decimal operator errors, 168 files; explicit sum starts resolve inference |
| Final combined unittest discovery; core-validation-final.log | Same requested sensor surface | Passed with declared skip | 142 tests, 17.474s, 141 passed; one named pre-existing dedicated-local-SQL opt-in skip |
| Final ruff check .; core-validation-final.log | Full configured core | Passed | All checks passed |
| Final ruff format --check .; core-validation-final.log | Full configured core | Passed | 115 files already formatted; existing exclusions unchanged |
| Final mypy; core-validation-final.log | Full configured core | Passed | No issues in 168 source files; existing strict settings and overrides unchanged |
| pip install -e 'src/core[dev]'; core-install.log | Parent isolated environment | Reported passed; raw log empty | Changes records exit 0 and Python/tool versions. Empty quiet-install output alone does not prove installation details; subsequent actual tooling output supports usability |
| python3 -B in-memory AST/Fraction assessment | Current mean-step expressions and test ownership | Passed, independently executed | 24 cases agree with exact oracle at precision 28; required old error reproduced; one added method, existing method ASTs unchanged |
| git diff --check, diff/stat and ancestry inspection | Current working candidate | Passed, independently executed | Three named tracked source/test/doc files only; expected base is an ancestor |
| Complete publication gate and receipt | Exact committed publication candidate | Unavailable, not run | Outside authority; focused evidence is not a receipt |
| Live sensor/Hub/Azure SQL, hosted and human approvals | Operational/issue/publication acceptance | Unavailable, not run | Separate coordinator-owned follow-ups |

The changes record and caller specify flock -w 600 /tmp/ama-rpi-heavy.lock
for the implementation's install and heavy runs. Raw logs contain result output,
not shell command/lock metadata; lock acquisition and exact wrapper commands
are supplied execution provenance, not independently witnessed by this assessor.
No heavy suite or install was rerun, and no lock or other external file was
created here. This assessment independently checks source, arithmetic and
ownership while transparently retaining that provenance limit.

Research's missing-package failure and earlier oracle experiments were reviewed
as recorded research evidence, not newly observed executions. The independent
current AST/oracle check corroborates the material arithmetic conclusion.
Failed original outputs are historical red/typing evidence, not unresolved
final validation failures.

## Outcome

* Outcome: Conformant.
* Outcome rationale: the bounded implemented correction satisfies the specified
  sum formula and inclusive comparison before division, reproduces the original
  failure, adds the locked count/sign/channel regression, preserves report and
  independent-check semantics, and has supported final component validation.
  No material divergence or defect was found. The two outside-scope follow-ups
  do not negate correction conformance.
* This outcome does not accept the full plan's unperformed local commit, whole
  #188, publication eligibility, live sensor accuracy or operational activation.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No source correction required by this Review |
| Decision gap or invalid assumption | None | No rpi-plan handoff |
| Material evidence gap within correction | None | No rpi-research handoff |
| Non-blocking residual work | RV-001 publication follow-up | Coordinator; separately authorized exact-candidate/hosted/human gates |
| Non-blocking residual work | RV-002 live-evidence follow-up | Coordinator; separately authorized actual sensor/Hub/Azure SQL evidence |

* Execution status: Complete.
* Outcome: Conformant.
* Validation coverage: supplied final 142-test sensor run with one disclosed
  opt-in skip, configured core ruff/format/mypy, and independent arithmetic,
  test-ownership and diff checks.
* Blockers: none for this assessment. Parent reconciliation and local commit
  remain pending; publication/live acceptance remain distinct follow-ups.
* Original assessment is final and preserved; do not repeat Review.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/sensor-mean-step-boundary-188-plan.md](.copilot-tracking/plans/2026-10-30/sensor-mean-step-boundary-188-plan.md) | Assessed plan and follow-ups |
| [.copilot-tracking/details/2026-10-30/sensor-mean-step-boundary-188-phase-details.md](.copilot-tracking/details/2026-10-30/sensor-mean-step-boundary-188-phase-details.md) | Assessed execution details |
| [.copilot-tracking/reviews/plans/2026-10-30/sensor-mean-step-boundary-188-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/sensor-mean-step-boundary-188-plan-critique.md) | Original Pass critique |
| [.copilot-tracking/changes/2026-10-30/sensor-mean-step-boundary-188-changes.md](.copilot-tracking/changes/2026-10-30/sensor-mean-step-boundary-188-changes.md) | Preserved implementation and validation evidence |
| [.copilot-tracking/research/2026-10-30/sensor-mean-step-boundary-188-research.md](.copilot-tracking/research/2026-10-30/sensor-mean-step-boundary-188-research.md) | Arithmetic and boundary research |
| [.copilot-tracking/reviews/logs/2026-10-30/sensor-mean-step-boundary-188-review.md](.copilot-tracking/reviews/logs/2026-10-30/sensor-mean-step-boundary-188-review.md) | One complete original independent Review |
| [src/core/src/zava_forward/core/synthetic/sensor_consistency.py](src/core/src/zava_forward/core/synthetic/sensor_consistency.py) | Assessed evaluator |
| [src/core/tests/test_sensor_handover.py](src/core/tests/test_sensor_handover.py) | Assessed external regression |
| [src/core/README.md](src/core/README.md) | Assessed contract documentation |

## Next Steps

The active parent retains this original Complete / Conformant result,
reconciles P02-T01 and makes the authorized privacy-safe local commit with the
required Co-authored-by trailer. No user action, peer-stage invocation, push
or repeated Review is required. RV-001 and RV-002 remain distinct
coordinator-owned follow-ups, not whole #188 or publication acceptance.
