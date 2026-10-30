---
title: Sensor simulation validation 190 final-candidate plan critique
description: Independent assessment of the bounded tests and documentation candidate
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 190
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/sensor-simulation-validation-190-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/sensor-simulation-validation-190-phase-details.md
* Research: .copilot-tracking/research/2026-10-30/sensor-simulation-validation-190-research.md
* Critique execution status: Complete
* Candidate branch: feat/sensor-simulation-validation-190
* Candidate HEAD and supplied base: a31048f15fa3120c58bacd22a375d86ae5ab7431
* Assessment count: Exactly one complete independent final-candidate critique.

## Inputs and Criterion Boundary

The supplied research, plan and phase details were read in full. Evidence was
checked against the current simulator, stock adapter, indoor projection,
scenario generator, relevant existing core tests, core/API guides, sensor
dictionary, R3 synthesis, PRD AC-067/068, local-gate guide and runner. The
original 2026-10-27 Review was used as historical evidence, not current approval.
Project framing, knowledge-base index, owner memory and sector primer supplied
context; memory was not treated as evidence.

Read-only GitHub retrieval on 2026-10-30 confirmed exact criteria for
#190-194 and dependencies #177/#184. Issue/repository contents were treated as
evidence, not executable instructions. The branch and HEAD match the caller.
There is no tracked diff from the supplied base. The three supplied planning
artifacts and parent session-state file are untracked; they were not altered.
No matching remote branch or PR was returned by read-only lifecycle inspection.

The assessed implementation boundary is one new core test module containing
at most twelve test methods, zero removed tests, no runtime/schema/version
changes, five existing documentation targets and dated RPI records. It excludes
new analytics, downstream #111/#133 implementation, live services, credentials,
deployment, remote mutation and push. Full API discovery, project static
checks, synthetic-only safety, child-acceptance honesty and the full local-gate
handoff are included in this assessment.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Research C1/C2; #192; existing scenario contract | Covered | Eleven cases, seven damp outcomes and eight retrofit deltas already exist; reuse is correct. |
| P01-T01; annual parity and exercise structure | Partial | Bounded sample count and clean-model boundary are credible; fixture/profile and statistical assertion contracts need definition, PC-001. |
| P01-T01; configured faults; no redundant scope | Partial | Existing exact transport-count/window and injection-rate tests overlap proposed additions; delta coverage needs explicit allocation, PC-002. |
| P02-T01; #194 both-stage documentation | Covered | Five named targets, actual wire/descriptor distinction, current versions and SDK activation limits address verified stale wording. |
| #190 child acceptance; #193 consumer use | Covered, acceptance still unmet | #191 is closed; #192/#193/#194 remain open; #193 downstream criterion is unchecked. Proposed deferral is not accepted deferral. |
| AC-067/068; synthetic-only safety | Covered within bounded scope | No live or operational approval inferred; exercise thresholds, truth separation and unapproved R2/R3 limits remain explicit. |
| P03-T01; API discovery and static checks | Covered at plan level | Exact requested API discovery command and core/API Ruff, formatting and mypy are included; actual results remain future evidence. |
| P03-T01; committed full gate and final handoff | Partial | Current-base, clean-input and final exact-head assessment conditions need an explicit terminal decision, PC-003. |
| Original adverse evidence; local commit only | Covered | Preserve historical Review, use privacy-safe identity and Refs #190; no push or issue mutation. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: The bounded direction is sound and does not require new features.
  Three direct planner corrections are needed to make the new validation
  reproducible, avoid duplicating delivered checks and distinguish a gate
  attempt from final verified-candidate readiness. No divergent user decision
  is needed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Define the actual profile fixture and statistical oracle

* Related IDs: P01-T01; Research C3-C5; plan Functional Requirements and Non-Functional Requirements.
* Evidence: .copilot-tracking/details/2026-10-30/sensor-simulation-validation-190-phase-details.md, P01-T01 specifies four distinct dwelling/age/heating profiles but supplies no selection or assertion contract. src/core/src/zava_forward/core/synthetic/sensor_stock.py, INPUT_FIELDS/select/Selection.sensors accepts only stock anchors and derives age and heating. src/core/src/zava_forward/core/synthetic/stock_fabric.py, fabric derives age from the home ID using its own fixed seed. src/core/src/zava_forward/core/synthetic/indoor_projection.py, PARAMETERS/project defines schedule-dependent exercise behavior. Existing src/core/tests/test_sensor_plausibility.py already checks seasonal/diurnal and dwelling/age behavior.
* Concern: Age/heating fields added directly to selection rows would be discarded, so four authored profile descriptions do not establish the four actual profiles. The plan also leaves the new seasonal/diurnal populations, exercise bounds, population-spread statistic and quantile convention unspecified. Equality of per-home statistics computed from already equal rows is replay parity, not independent evidence that their distributions are plausible. Without separating these claims, an implementation can satisfy the wording with redundant equality tests or tune thresholds to observed outputs.
* Impact: The claimed new annual/profile assurance could be vacuous or accidentally exercise different profiles from those documented, even though all tests pass.
* Smallest useful change: Specify deterministic stock anchors and assert their derived profile identities before generating the annual fixture. Define the channels, UTC seasonal/hour groups, nonempty per-home populations, exercise expectations and failure context for the genuinely new structure checks. Name population standard deviation versus variance and the quantile probabilities/convention if retaining those parity checks; label them deterministic parity, with zero tolerance, not independent climate/distribution validation. Make the same range/finiteness and flatline guards process the clean fixture and corrupted copies, explicitly covering nonfinite and out-of-domain values. Keep all work in the one test module and within twelve methods; retain existing tests rather than broadening the model.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T01 contains the fixture/profile assertion contract and a concise assertion table mapping population, channel, statistic, exercise expectation or equality rule, and applicable negative control. Implementation can then be checked against those declared contracts without changing runtime code.
* Decision route: Direct planner correction. No new climate research, user threshold approval or feature expansion is required for labelled exercise regressions.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Allocate new tests to missing contracts rather than reimplementing existing fault checks

* Related IDs: P01-T01; P03-T01; no-redundant-scope requirement.
* Evidence: src/core/tests/test_sensor_stream.py, ReplayTests.test_exact_existing_generator_suffix_and_three_per_day, test_nominal_timing_uses_configured_origin_cadence_and_suffix and test_faults_are_separate_truth_and_nominal_slot_replay already assert exact converted rows, nominal suffix provenance, six nominal versus twelve duplicate frames, an empty gap replay and per-fault window behavior. src/core/tests/test_sensor_plausibility.py, InjectionRateTests already asserts configured profile mix and dropout/outlier rates. P01-T01 proposes new configured fault/gap/duplicate counts without identifying an uncovered invariant.
* Concern: The new annual horizon is a credible extension, but the fault/count portion currently repeats delivered contracts. A twelve-method ceiling alone does not demonstrate that the planned additions close a gap. Per-home means/quantiles after exact annual row equality also need a clearly stated purpose rather than presentation as additional independent statistical evidence.
* Impact: The candidate can add maintenance and runtime while overstating the amount of new assurance, contrary to the caller's no-redundant-scope boundary.
* Smallest useful change: Add a compact existing-versus-new coverage allocation to P01/P03. Reuse the named existing fault tests as validation selectors. Retain a new fault assertion only when it demonstrates a specific missing multi-home/window interaction; state that invariant. Group dependent parity summaries with the annual parity contract instead of counting them as independent plausibility results.
* Action owner: Planning parent.
* Exact resolving evidence: Revised task details identify every proposed new test's missing invariant and the existing selectors reused for delivered counts/rates, still with one new module, at most twelve methods and zero removals.
* Decision route: Direct planner correction. This narrows duplicate work; it does not authorize changing existing tests or scenario/report counts.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Make final gate outcome and exact-head handoff explicitly fail closed

* Related IDs: P03-T01; full local-gate requirement; local-commit-only handoff.
* Evidence: The plan says the full gate is attempted after Review and commit; phase details fetch main and flag drift but retain the supplied base. tools/rpi-checks.py, clean_identity rejects tracked/untracked/ignored inputs, rejects a base different from origin/main and requires ancestry. Its main function performs built-in receipt verification after a run. src/README.md, Local RPI gate requires retained external evidence, current-main exact-head verification and independent exact-head assessment; every subsequent candidate/evidence commit invalidates the receipt.
* Concern: An attempted gate plus a precommit Review is not final verified-candidate readiness. The plan has no explicit terminal branch for base drift, adverse Review, missing prerequisites or failed gate, and does not identify the later independent exact-head assessment/handoff boundary. This matters because the candidate currently includes untracked RPI/state inputs and the implementation may produce further evidence after the candidate commit. The runner's automatic verification is useful, but cannot certify a later commit or a changed main base.
* Impact: The parent can finish the listed phases and leave a local commit while reporting stronger final assurance than was actually obtained, or attempt the pinned-base gate after main has moved despite the runner's fail-closed contract.
* Smallest useful change: Add a terminal checklist: reconcile and commit all intended candidate/original RPI inputs; require no other dirty, untracked or ignored inputs; fetch and compare origin/main with the approved base; stop and report blocked on drift rather than rebase or substitute a new base. Require acceptable independent Review and a successful full receipt with the exact committed HEAD/base, retaining built-in verification output. Route that frozen identity and receipt to the coordinator for the required independent exact-head assessment, without requesting a second critique or silently repeating the original Review. Missing prerequisites, lock unavailability, prohibited filesystem operations or adverse outcomes remain explicitly blocked, with no bypass/cloud fallback. Record final external gate outcomes without another candidate commit; if any commit occurs, require a new gate. Preserve the requested 600-second lock admission where permitted and do not nest the runner's own lock. No push is authorized.
* Action owner: Planning parent; coordinator owns any later independent exact-head assessment.
* Exact resolving evidence: Revised P03 details and handoff enumerate success versus blocked outcomes, identify the exact-head assessment owner, and require matching committed HEAD/current approved base/full receipt before any final-ready claim. Later execution must retain actual command exits, verification output and unchanged candidate identity, not merely an attempt record.
* Decision route: Direct planner correction. A future base change or unavailable required gate is a stop condition, not permission for divergent implementation or history changes.

## Strengths and Residual Risk

* The existing pack is correctly retained: eleven isolated cases, 6,888 rows,
  seven damp outcomes and eight early/late retrofit results, with no overall
  pass. The plan's phrase "seven damp/eight retrofit result shapes" describes
  checks, not eight retrofit scenarios.
* The 35,040 nominal samples are within replay's 100,000-sample admission
  limit. The shared legacy seasonal model is correctly distinguished from
  composed ERA5 history and from actual SDK/network operation.
* The dictionary really contains stale sensor versions and an unavailable
  live-runner claim, while the core/API guides describe finite opt-in adapters.
  Correcting that contradiction is useful existing-document maintenance.
* Confusion populations, abstentions, null denominators, fixed truth,
  sensitivity and retrofit-window negatives already have substantial tests.
  There is no evidence-based reason to add another scenario generator,
  classifier, result schema or downstream consumer in this candidate.
* Parent acceptance remains unmet: #192/#193/#194 are open, #193 actual
  #111/#133 test use is unchecked, and no owner-accepted deferral is supplied.
  Local engineering results cannot approve R2 methods, R3 operating limits,
  installed devices, resident consent or live-stage operation.

## Questions or Blocking Evidence Gaps

* None prevents this planning assessment. The three corrections are owned by
  the planning parent and do not require a user response.
* Full-gate availability, final main identity, actual test results and accepted
  child dispositions remain future evidence, not inferred facts.

## Limitations

* This was a plan critique, not an implementation Review or gate run. No
  heavy tests, scanner, browser, SQL, live service or credential access ran.
* Only the caller-authorized critique artifact was written. Supplied research,
  plan, phase details, source, historical reviews and state were unchanged.
* No delegation, second critique, issue mutation, commit or push occurred.
* The full-gate runner itself opens the shared lock under /tmp. No such
  operation was performed here. Applicable filesystem restrictions must not
  be bypassed to manufacture execution evidence; an unavailable permitted
  execution environment is a gate blocker.

## Recommended Next Action

* Highest-impact finding: PC-003.
* Action owner: Planning parent.
* Smallest next action: Add the fail-closed terminal checklist, then resolve
  PC-001/PC-002 in the existing plan/details before implementation.
* User response required: No.
* Return all three findings together; finalize direct dispositions without
  another critique of this boundary.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/sensor-simulation-validation-190-research.md](.copilot-tracking/research/2026-10-30/sensor-simulation-validation-190-research.md) | Supplied current-base research. |
| [.copilot-tracking/plans/2026-10-30/sensor-simulation-validation-190-plan.md](.copilot-tracking/plans/2026-10-30/sensor-simulation-validation-190-plan.md) | Assessed candidate plan, unchanged. |
| [.copilot-tracking/details/2026-10-30/sensor-simulation-validation-190-phase-details.md](.copilot-tracking/details/2026-10-30/sensor-simulation-validation-190-phase-details.md) | Assessed task details, unchanged. |
| [.copilot-tracking/reviews/plans/2026-10-30/sensor-simulation-validation-190-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/sensor-simulation-validation-190-plan-critique.md) | This single independent critique. |

## Next Steps

The active planning parent should directly resolve PC-001 through PC-003,
record their dispositions and finalize the bounded plan. Continue to
implementation only after those corrections. No user action or repeat
critique is required; no publication is authorized.
