---
title: Approved sensor backfill integration plan critique
description: Single final-candidate assessment for the owner-approved continuation of Refs 177
ms.date: 2026-10-27
---

## Metadata

* Task ID: 177-approved-integration-2026-10-27
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/sensor-backfill-177-approved-integration-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/sensor-backfill-177-approved-integration-phase-details.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique; no implementation or additional review launched.

## Inputs and Criterion Boundary

* Caller requirements: owner-approved continuation of Refs #177 on parent feat/sensor-backfill-177 / PR #486, integrating children #481-#485. Owner key owner-approvals-2026-10-27-b approves candidate climate reuse for synthetic demonstration, canonical existing stock home IDs, child merges and aggregate validation.
* Primary inputs: the plan and phase details above, plus .copilot-tracking/research/2026-10-27/sensor-backfill-177-approved-integration-research.md, including C1-C8, W1-W3 and its decision record.
* Supplied evidence pointers followed: current sensor_stock, sensor_backfill, sensor_faults and SensorConsumer contracts; the consumer's directly related SQLite/SQL Server case schemas; the climate adapter at candidate 72f52358; component interfaces at the exact #482-#484 heads recorded in .copilot-tracking/changes/2026-10-27/sensor-backfill-177-changes.md. These are bounded contract checks, not a new research cycle.
* Context read: docs/case_study_48_original.md; relevant opening context in docs/case_study_48_addendum.md; docs/reference/README.md; docs/reference/memory.md; src/README.md local gate; docs/reference/method/tracking-retention-policy.md. Memory supplies preferences, not evidence.
* Locked implementation boundary: no test removals; at most four new test modules and 45 new methods; intentional stock identity/version expectation changes only. Findings below must fit that budget and do not authorize a wider test or source programme.
* Publication boundary: one foreground parent --changed gate, --lock-timeout 0, fresh external --out, following authorized archive/restore-verified git clean -fdxq. This owner-specific instruction supersedes --all. No uv, private dataset reads, secrets, main push/merge, closing keywords, repeated gate or repeated Review.
* Branch inspection: feat/sensor-backfill-177 at d906de31b00006b4dbc811edf21d9e03066eb103. The supplied plan, details, research and continuation state were already untracked. They were not altered, committed, cleaned or moved. No remote lifecycle changes were made.
* Assessment boundary: planning credibility, dependency/interface fit, acceptance evidence and safe sequencing. This critique cannot establish successful source acquisition, test results, runtime scale, live approval, current remote heads or hosted check results.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner decisions / W1-W3 | Covered | Approved demo reuse, canonical identities and integration are prospective; prior adverse outcomes remain preserved. No renewed source approval requested. |
| Q1 / P01-T01 | Covered | Genuine contiguous two-year paired acquisition, UTC alignment, strict validation, hashes, derived bounds and attribution are required. Retrieval failure blocks rather than authorizes repetition or filling. |
| Q2 / C1, C3-C4 / P01-T02 | Partial | Canonical identity and independent availability/control checks are explicit, but the actual SQL cases.id ceiling and its acceptance consequences are unspecified: PC-001. |
| C5 / P01-T02 / P02-T02 | Partial | Fault truth separation is covered; the new sensor-ID bound does not account for the existing unmapped transformation: PC-002. |
| Q3 / P02-T01 | Partial | Opt-in integration is correct, but supplied component APIs do not expose a compatible composition seam: PC-003. |
| Q3 / C2, C7 / P02-T02 | Covered | Public generated 60,000-home stock, complete window, declared supported cadence, streaming, measured hourly estimate, actual rows/bytes/hashes and bounded deterministic replay. Lower cadence is explicitly not hourly validation. |
| Functional requirements / acceptance criteria | Partial | Climate, exclusions, dated boundaries, manifest binding and actual consumer tests are named. PC-001 through PC-003 need explicit resolving assertions within the locked budget. |
| Dependencies / P01-P02 | Covered | Separate child implementation worktrees, committed delivery before normal merges, all five child heads in parent ancestry and retained overlapping README sections. No squash, rebase or force push. |
| Q4 / C6 / P03 | Covered | Original independent Review precedes commit/gate; exactly one scoped gate and partial-scope receipt verification; failures block readiness. No post-gate source commit. |
| Related documentation / P03-T02 | Partial | GitHub blocker updates are required, but current knowledge-base status and its index/log reconciliation have no assigned task: PC-004. |
| Locked tests / regression requirements | Covered with corrections | Existing tests remain, intentional expectation changes are bounded, and legacy byte/RNG coverage is required. Findings do not require new tooling or extra modules beyond the cap. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 2 High, 2 Medium, 0 Low.
* Rationale: the approved direction is credible, but the supplied source contracts expose an unresolved SQL availability boundary, a fault-ID length interaction and incompatible projection/composition interfaces. These should be resolved in the plan before implementation, not hidden by changing home IDs, bypassing availability or relabelling test success.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Specify the actual SQL case-availability identity boundary

* Related IDs: Q2, C1, C3-C4, P01-T02, canonical-ID/SQL-parity acceptance.
* Evidence: src/core/src/zava_forward/core/synthetic/sensor_stock.py select accepts preserved IDs up to 128 UTF-16 units. src/core/src/zava_forward/core/mssqlstore.py TABLES defines cases.id as NVARCHAR(64) with binary collation; SQLite cases.id is unrestricted TEXT in src/core/src/zava_forward/core/sqlstore.py. src/core/src/zava_forward/core/sensor_consumer.py _quality requires that exact home to exist in cases. Phase details acknowledge unspecified store availability limits, but name only consumer/helper/test changes.
* Concern: widening observation/control admission to the stock contract does not make a 65-128-unit canonical home representable in the existing SQL case store. Fresh stock-reading NVARCHAR(128) DDL does not fix that independent dependency. Merely promising SQL parity and documenting unspecified limits leaves the success boundary ambiguous.
* Impact: SQLite fixtures or short generated IDs could pass while a claim of full stock-ID compatibility is false on SQL Server. Truncating/aliasing IDs, or dropping availability checks, would violate approved decisions.
* Smallest useful change: explicitly name the existing 64-unit SQL cases ceiling in P01-T02. Separate canonical export support from store-representable consumer admission; specify unchanged-ID refusal/unavailability for homes that cannot exist in that store and qualify the acceptance claim. Do not silently widen the shared case/audit identity model. If universal 128-unit SQL case admission is necessary for the claimed outcome, record that as an unresolved dependency rather than imply it is covered by consumer-only edits.
* Action owner: planning parent; P01-T02 implementer supplies the proof.
* Exact resolving evidence: revised P01-T02 and acceptance wording naming both supported domains; a bounded fixture matrix covering 64, 65 and 128 UTF-16 units, case-distinct and non-ASCII keys, with unchanged exported IDs; actual SQLite/SQL Server results showing supported exact-key admission and explicit unsupported/unavailable behavior without truncation, substitution or unrelated case mutation. Tests must use the existing selectors/budget and retain missing-case refusal.
* Decision route: Direct planner correction to expose and qualify the existing store boundary. Owner approval of canonical IDs is already settled. Broad shared-schema expansion, if subsequently proposed instead of bounded support, is a significant scope/design decision and must not be inferred from this critique.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Budget sensor-ID length for the existing unmapped fault transformation

* Related IDs: C1, C3, C5, P01-T02, P02-T02, fault-rejection acceptance.
* Evidence: phase details require compact uppercase sensor IDs, while SensorConsumer _shape retains the 20-character sensor limit. src/core/src/zava_forward/core/synthetic/sensor_faults.py packets implements the unmapped fault as "UNMAPPED-" + sensor_id, adding nine characters. Existing consumer tests expect UNMAPPED for that fault.
* Concern: a valid compact ID of 12-20 characters becomes an invalid observation identity under this transformation. The supplied plan tests bounded IDs and generic fault rejection but does not require the intended fault to reach the independent mapping check.
* Impact: an unmapped test can pass as a generic rejection while actually exercising IDENTITY, losing the intended mapping/fault semantic coverage after the ID change.
* Smallest useful change: add the fault namespace to P01-T02's identifier design. Either reserve sufficient length in integrated sensor IDs or define a separate bounded, deterministic, guaranteed-unregistered fault ID without changing canonical home IDs. Retain collision detection and legacy behavior.
* Action owner: planning parent; identity/consumer implementer coordinates with the aggregate-test owner.
* Exact resolving evidence: a named maximum-length generated-ID case passed through the real fault packet writer and actual consumer, yielding UNMAPPED rather than IDENTITY; a neighboring valid packet remains accepted and duplicate replay remains unchanged. Record the namespace/collision rule and fit this assertion inside the locked modules/methods.
* Decision route: Direct planner correction. No new user decision or relaxation of the 20-character consumer limit is needed.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Define an opt-in composition seam instead of assuming the component APIs compose

* Related IDs: P02-T01, P02-T02, projection/dated-measure/household functional requirements, legacy byte/RNG acceptance.
* Evidence: at #482 head c74a1015bf5f6f0af10c002faada72c50b4364b1, indoor_projection.project accepts the legacy sensor mapping, RNG, UTC instant and outdoor pair only. Its construction_loss is restricted to a fixed whitelist between 0.75 and 1.2; its heating patterns are all_day, morning_evening and low. At #483 head c969eae53d3d348cbe68f1f95ce90159cea7fed2, retrofit_effects returns an arbitrary product of active dated loss multipliers. At #484 head e0491c441de0386cec5077e3c9e5e34ccbe1787a, household_conditions returns explicit setpoint, ventilation and moisture values, and profiles include extended_day/evening schedules.
* Concern: the phase currently says to apply these components but does not define the new projection inputs or their composition. Multiplying retrofit effects into construction_loss can violate the whitelist; copying household schedule names can fail validation; setpoint, ventilation and moisture have no existing project arguments. Successful standalone child tests cannot establish the integrated behavior.
* Impact: implementation could fail on valid dated histories, silently ignore household outputs, or alter the legacy path/RNG while claiming all components are integrated.
* Smallest useful change: name the opt-in projection interface and its owning source boundary in P02-T01. Specify how baseline fabric loss, active measure multipliers, supplied household setpoint, ventilation and moisture enter the exercise equations, their validation domains and neutral/default behavior. Keep the current legacy projection path unchanged; do not smuggle new model values through incompatible legacy enum/whitelist fields. Version and fingerprint the composed model.
* Action owner: planning parent; parent integration implementer owns the new composition contract.
* Exact resolving evidence: revised phase details with the input/composition contract; aggregate assertions proving each supplied household field affects its intended term, valid combined measures below the legacy construction whitelist are supported, completion activates at the exact instant, other homes/no-history remain neutral, excluded households emit nothing, and the untouched default still matches legacy bytes/RNG. Manifest evidence must identify the composed model and bound input histories. Use the existing locked test allocation, not additional unbounded suites.
* Decision route: Direct planner correction within the already approved synthetic opt-in integration. It does not require calibrated physics, production authority, a new framework or renewed user approval.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Assign durable knowledge-base reconciliation before Review and the one gate

* Related IDs: W1-W3, P01-T01, P02-T01, P03-T01-T02, related-documents scope.
* Evidence: docs/reference/README.md currently introduces #177 as five unmerged children with source/identity owner blockers and no integrated historical delivery. The indexed synthesis is docs/reference/research/iot-sensor-analytics-research-plan.md. P03-T02 assigns GitHub issue/PR updates, and child integration retains component README sections, but neither phase assigns the knowledge-base status update and required index/log maintenance.
* Concern: successful approved integration would leave the project's durable entry point describing the superseded current state, even if PR bodies and issue comments were corrected. A blanket related-documents scope does not identify who reconciles this before the immutable candidate is reviewed and gated.
* Impact: later work may rediscover resolved blockers or mistake historical partial evidence for the new aggregate outcome. A post-gate documentation fix would invalidate the sole receipt.
* Smallest useful change: assign a bounded P02 closeout/P03 pre-Review step to append the prospective owner decision and actual implementation/evidence status to the existing synthesis, reconcile the index introduction, and append the required knowledge-base log entry. Preserve all original blocked/Residual work outcomes; do not modify memory or immutable source snapshots.
* Action owner: planning parent; parent integration/documentation owner executes before P03-T01.
* Exact resolving evidence: phase checklist identifies the existing synthesis, docs/reference/README.md and docs/reference/log.md, with pre-Review/pre-commit ordering and factual status conditional on actual results. The final candidate diff distinguishes original evidence from the approved continuation and links its aggregate evidence without claiming production/full-hourly/private-stock acceptance.
* Decision route: Direct planner correction under existing knowledge-base conventions, with no new user decision.

## Strengths and Residual Risk

* The source approval is correctly limited to synthetic demonstration. Genuine second-year retrieval, not repetition or relabelling, is required; underlying terms and scientific qualification are not falsely declared verified.
* Canonical stock home IDs remain untouched. Independent case availability, consent, calibration, mapping intervals, ordering, schema and replay controls are explicitly preserved.
* Public generated stock avoids private reads and does not claim equality with an unseen private register.
* The full-stock exercise uses the complete two-year window at a declared supported cadence, with hourly volume estimated separately. This is an explicit acceptance boundary, not a missing requirement to force billion-row hourly generation.
* Original child/parent adverse outcomes are retained, and normal child merges preserve ancestry. Integrated behavior, rather than five isolated component passes, is the intended acceptance target.
* Exactly one Review and one scoped parent gate are explicit. Acquisition, lock, SQL/browser/scanner and hosted-check failures remain genuine blockers; this critique does not authorize retries, fallback, protection changes or manufactured success.
* Production physical/source/regional qualification, real monitoring authority and legal/professional activation remain outside this exercise. None is reopened as a prerequisite to the owner's approved bounded demo.

## Questions or Blocking Evidence Gaps

* No user question is needed for the four direct planning corrections.
* Full 128-unit SQL case support cannot be inferred from the existing schemas. A proposal to expand the shared case model would need its own explicit design/scope disposition; bounded honest support can be planned without that expansion.
* Runtime retrieval, aggregate volume/results, exact child delivery heads and final publication evidence are implementation obligations, not facts established by this critique.

## Limitations

* No network acquisition, private dataset access, installation, test execution, cleanup, gate, commit, push or GitHub mutation was performed.
* Remote PR/check state is the supplied dated research state, not a fresh hosted verification. Current source evidence was read only.
* This is the complete actionable finding set from this one bounded assessment. It is not a request for another critique or a second independent Review.
* The only written artifact is this critique. Supplied plan/details/research remain unchanged; their SHA-256 values at assessment were respectively e66a551742e9bc3ea6e0c6b3d25d1fdfc744477c350c327a2b974810fc0c8db0, cecb8e67009533d84cff20305859b956199831ddb69ac6d3e8232e284f211335 and 194cb7d5e893b92f8bc9f50668f8d7cb23d28c002e225363c1fdac09a129118f.

## Recommended Next Action

* Highest-impact finding: PC-001, the SQL case-availability identity boundary; PC-003 also blocks a credible integrated implementation contract.
* Action owner: planning parent.
* Smallest next action: directly revise the named phase details/acceptance statements and record dispositions for PC-001 through PC-004, retaining the locked tests/removals/maximum additions and owner approvals.
* User response required: No for these corrections. Do not infer approval for a later shared-schema expansion.
* Handoff: return this Complete / Revise result to the active parent for direct disposition and finalization without another critique. This critique performs no implementation.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/sensor-backfill-177-approved-integration-plan.md](.copilot-tracking/plans/2026-10-27/sensor-backfill-177-approved-integration-plan.md) | Assessed final-candidate plan; unchanged. |
| [.copilot-tracking/details/2026-10-27/sensor-backfill-177-approved-integration-phase-details.md](.copilot-tracking/details/2026-10-27/sensor-backfill-177-approved-integration-phase-details.md) | Assessed phase details; unchanged. |
| [.copilot-tracking/research/2026-10-27/sensor-backfill-177-approved-integration-research.md](.copilot-tracking/research/2026-10-27/sensor-backfill-177-approved-integration-research.md) | Supplied bounded research and owner decisions; unchanged. |
| [.copilot-tracking/changes/2026-10-27/sensor-backfill-177-changes.md](.copilot-tracking/changes/2026-10-27/sensor-backfill-177-changes.md) | Original child-head evidence and preserved historical outcome. |
| [.copilot-tracking/reviews/plans/2026-10-27/sensor-backfill-177-approved-integration-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/sensor-backfill-177-approved-integration-plan-critique.md) | This single Complete / Revise critique. |

## Next Steps

The active planning parent should resolve PC-001 through PC-004 directly, record
their dispositions, and finalize without another critique. No user action is
required. Implementation remains outside this critique and may start only
after the parent's disposition.
