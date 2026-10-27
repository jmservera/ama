---
title: Sensor backfill 177 independent RPI Review
description: One bounded post-implementation review of parent evidence and five unmerged children
ms.date: 2026-10-27
---

## Opening Review State

* Goal: assess #177 parent evidence and all five supplied child diffs once, without repair or integration.
* Scope: parent 6a6e5d0d0e6aebad0aa44be288a3a9ec0f3e1b1f; foundation e7d531c789dbaafafc05fb4cacf7d851e188cd58; child heads supplied by caller.
* Evidence readiness: canonical research, plan, phase details, original critique and changes located; comparison pending.
* Acceptance basis: approved exercise-only components, explicit source/identity blockers, unticked original acceptance criteria; no historical, physical, writer-integration or final-ready inference.
* First comparison boundary: reconcile original plan and critique with parent changes, then inspect each exact child diff and relevant source/tests/README/blocker evidence.
* Read-only boundaries: only this review record may be written. No source, plan, state, branch, issue, PR, integration or nested-agent actions.
* Initial blockers: historical climate reuse #178/#425 pending and stock producer IDs incompatible with #110 consumer; these limit delivery, not evidence inspection.

## Scope and Evidence

* Task: #177 / sensor-backfill-177. Review date: 2026-10-27.
* Exactly one independent post-implementation Review; no nested agents, fixes, repeated assessment or integration.
* Parent assessed: 6a6e5d0d0e6aebad0aa44be288a3a9ec0f3e1b1f.
* Common foundation: e7d531c789dbaafafc05fb4cacf7d851e188cd58.
* Canonical research: .copilot-tracking/research/2026-10-27/sensor-backfill-177-research.md.
* Plan: .copilot-tracking/plans/2026-10-27/sensor-backfill-177-plan.md.
* Details: .copilot-tracking/details/2026-10-27/sensor-backfill-177-phase-details.md.
* Original critique: .copilot-tracking/reviews/2026-10-27/sensor-backfill-177-plan-critique.md. This actual path, not the skill's default reviews/plans path, is authoritative here.
* Changes: .copilot-tracking/changes/2026-10-27/sensor-backfill-177-changes.md.
* Coordination state: .copilot-tracking/rpi-sessions/2026-10-27/sensor-backfill-177-state.json.
* Parent knowledge-base evidence: docs/reference/README.md, docs/reference/log.md and docs/reference/research/iot-sensor-analytics-research-plan.md.
* Supporting context: docs/case_study_48_original.md, relevant addendum opening, docs/reference/memory.md, docs/reference/research/sector/housing-association-primer.md and src/README.md local gate policy.

All six foundation-to-head diffs were read, including the complete changed source, tests, component README additions and child changes/blocker records. Unmerged files were read with git show/diff, not substituted with the parent's older source.

| Issue / supplied PR | Branch | Exact assessed head | Complete changed surface |
| --- | --- | --- | --- |
| #178 / #481 | docs/climate-reuse-178-stack | 8871cbd3b7704212b538d284f04668c51dbd8042 | .copilot-tracking/changes/2026-10-27/sensor-climate-178-changes.md |
| #179 / #482 | feat/indoor-projection-179-stack | c74a1015bf5f6f0af10c002faada72c50b4364b1 | .copilot-tracking/changes/2026-10-27/sensor-projection-179-changes.md; src/core/README.md; src/core/src/zava_forward/core/synthetic/indoor_projection.py; src/core/src/zava_forward/core/synthetic/sensor_backfill.py; src/core/tests/test_indoor_projection.py; src/core/tests/test_synthetic_determinism.py |
| #180 / #483 | feat/retrofit-effects-180-stack | c969eae53d3d348cbe68f1f95ce90159cea7fed2 | .copilot-tracking/changes/2026-10-27/sensor-retrofit-180-changes.md; src/core/README.md; src/core/src/zava_forward/core/synthetic/retrofit_effects.py; src/core/tests/test_retrofit_effects.py |
| #181 / #484 | feat/household-conditions-181-stack | e0491c441de0386cec5077e3c9e5e34ccbe1787a | .copilot-tracking/changes/2026-10-27/sensor-household-181-changes.md; src/core/README.md; src/core/src/zava_forward/core/synthetic/household_conditions.py; src/core/tests/test_household_conditions.py |
| #183 / #485 | docs/backfill-consumer-183-stack | 66d3833967ee8594a0fc269804c5fa7c2e31a59a | .copilot-tracking/changes/2026-10-27/sensor-writer-183-changes.md |

Supporting source inspection followed the immediate contracts in src/core/src/zava_forward/core/synthetic/sensor_stock.py, stock_fabric.py, provenance.py, sensor_backfill.py and src/core/src/zava_forward/core/sensor_consumer.py. Supporting regression selectors inspected were test_sensor_backfill, test_sensor_stock, test_sensor_faults, test_sensor_plausibility and the relevant test_synthetic_determinism context. The original source comparison and its dated licence/record limitations were read in the existing IoT research synthesis; no new climate retrieval or legal currentness claim was made.

## Execution Status

* Planned execution status: Partial. P01/P02 bounded component and blocker-evidence work is delivered at the supplied heads. P03-T01 is fulfilled by this one review; P03-T02/T03 reconciliation, committed original Review and the one subsequent parent-only gate/publication remain outside this assessment's execution.
* Review execution: Complete for the supplied full-surface bounded review. No evidence-inspection blocker prevented a credible verdict.
* Whole-original delivery: Partial; two-year source-grounded history, actual dated-source mapping and actual #110 writer integration remain Blocked / unaccepted.
* No original acceptance checkbox is completed by this review. A completed evidence inspection is not completed implementation, human approval or publication readiness.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record evidence | Reconciliation | Rationale or remaining boundary |
| --- | --- | --- | --- |
| P01-T01 | Exact common foundation recorded; git commit parents inspected | Reconciled | Each of the five child heads has the foundation as its direct parent. No ancestry repair or integration is present. |
| P01-T02 | #178 changes and parent ledger record source stop and one comment | Reconciled within evidence boundary | Existing source comparison is reused as evidence, not adopted climate input. Remote comment existence/status is reported evidence, not freshly fetched here. |
| P02-T01 | #179 source, tests, manifest and README | Reconciled | Exercise projection extraction, explicit support domain and fingerprint binding are implemented. Physical/historical acceptance remains expressly unmet. |
| P02-T02 | #180 source, tests and README | Reconciled | Independent immutable dated synthetic measures and inclusive activation, not actual #173 mapping or generated historical effects. |
| P02-T03 | #181 source, tests and README | Reconciled | Independent deterministic conditions with monitoring exclusions, not integration or inferred resident behaviour. |
| P02-T04 | #183 blocker record and actual consumer/stock contracts | Reconciled | Identity refusal is real in the inspected code; the child does not widen, remap or bypass it. |
| P02-T05 | Exact heads, draft PR ledger and child check summaries | Reconciled with validation limitation | Child-local focused results are reported; they were not independently rerun. Draft/remote lifecycle is not newly verified. |
| P03 | Review next; one documentation-only parent gate remains | Correctly pending | Current evidence makes no passing receipt, hosted-check or final-ready claim. Do not demand or run the later gate before its original Review is committed. |
| Follow-Up Items 1-3 | Parent Remaining Work and coordination blockers | Reconciled | Source, identity and owner integration work remain distinct and outside immediate component acceptance. |

## Completed Work Assessment

### #179: numerical guards, extraction and provenance

The supplied head validates supported dwelling/age/schedule factors, a boolean legacy retrofit flag, exact existing construction factors, finite outdoor temperature -80..60 C, RH 0..100 and UTC-aware time. The finite Magnus singularity is rejected by the temperature domain before evaluation. The construction support matches sensor_stock.CONSTRUCTION_LOSS.

Comparison with the foundation equation confirms the same multiplication and arithmetic order and the same two Gaussian calls for supported standard generator inputs. Normal entry points resolve UTC windows; stock sensors provide the validated factors. No change to existing stock selection, sensor identity, fault assignment or monitoring exclusion is introduced. Intentional rejection of unsupported inputs and intentional provenance changes are documented, rather than misrepresented as identical historical snapshots.

The new tests contain 1,500 independent-equation/result/RNG-state comparisons, input-domain endpoints and explicit invalid cases, construction direction, helper fingerprint sensitivity and an actual generated-manifest assertion. The legacy reference shares factor constants, so these tests do not alone prove factor values; direct comparison of those constants with the foundation closes that inspection question. They do not prove historical climate or calibrated building physics.

revision_sources includes indoor_projection.py for normal and fault-enabled generation. The changed dependency-set regression explicitly includes the helper instead of relying on the old list-length shortcut. Manifest parameters include the helper's version, equation, schedule and exercise-domain classification. The intentionally changed source hash means old snapshots are not migrated or admitted as current snapshots; the README states this limitation. No substantive extraction/provenance defect identified.

### #180: actual timing versus synthetic timing

Measure is frozen and validates measure/home IDs, supported kinds, explicitly synthetic input and UTC whole-second completion. effect validates observation time and duplicate IDs, selects only the exact home and completed_at <= observed_at, then sorts by completion and ID before multiplying. Empty or other-home history yields 1.0; apply_loss validates a finite positive baseline.

Tests directly cover one second before, exactly at and one second after completion, other-home/empty neutrality, future exclusion, order independence, cumulative factors and invalid records. These are actual timestamp comparisons in the component, not a calendar-date approximation. They are NOT evidence of actual stock retrofit completion dates, generated before/after histories or guaranteed temperature/humidity savings. The code, README and acceptance audit preserve that distinction. No substantive defect identified within the approved independent component.

### #181: per-home deterministic conditions and exclusion

Profiles depend on seed, model version and unchanged home ID, not iteration order, wall clock or demographic data. Heating/occupancy choices and continuous distributions match the documentation. Hour-specific occupancy uses an ID/seed/version/date/hour key; timestamp sorting and per-hour seeding preserve subset/window agreement. The tests exercise seed/home/order/subset differences, 3,000 profiles against declared shares/ranges, schedule endpoints and drying.

Declined/unknown returns before profile creation or any RNG call and yields no conditions. Tests explicitly mock RNG to verify this. The existing stock adapter independently excludes those choices before producing sensors; its writer exclusions are unchanged. Excluded requests intentionally return empty without inspecting timestamps; they do not produce observations from invalid time inputs. Granted requests reject invalid or duplicate timestamps. Synthetic flags and neutral output fields do not manufacture real consent or resident assessment.

No household profile is used by the current writer/projection at these heads. This is disclosed in the README and changes, not a missing integration falsely reported as complete. No substantive defect identified within the approved independent component.

### #178 and #183: blocker and unsupported-claim assessment

#178 distinguishes exact HadUK regional metadata/OGL context from unavailable paired records, unresolved owner reuse and the separate unmerged one-year #425 demonstrator. Temperature-only Durham statistics cannot supply RH or three-per-day/two-year bounds. The evidence child adopts no source or terms and makes no physical-bound claim. Dated metadata/retrieval evidence is not current legal or operational approval.

#183's stop agrees with the actual contracts: the stock adapter generates SENS-SYN- plus a 64-character lowercase hex digest; consumer _shape requires the exact fault observation fields and uppercase identities with sensor/reading/home limits 20/40/12. The recorded 73/84/23 example is incompatible even if legacy DDL is wider. The recorded valid-control/IDENTITY probe is reported validation, not rerun here. No alternate loader is offered as #110 admission.

The estimate is correctly labelled: 60,000 * 730 * 3 = 131,400,000 nominal paired observations; reported legacy-sample dropout/byte estimates are not measured private-stock coverage, an upper bound or SQL/transport/billing cost. No complete generated dataset or private source access is inferred. No substantive false claim identified.

### Parent evidence and unmerged aggregate

The parent diff contains coordination, plan/state and knowledge-base documentation only. Its index/log/synthesis additions accurately name the five children and conditional capacity/source/identity boundaries. It contains none of the new child modules. All children directly fork the foundation, and their README insertions overlap; owner integration must retain all three explanations rather than choose one side. This already-documented integration concern is residual work, not an integration defect in a deliberately unmerged parent.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | Change and trigger | Reconciliation and assessment |
| --- | --- | --- |
| P01/P02 checklist | Pending tasks marked executed after child delivery | Matches exact child diffs and ledger, within reported remote/check limits. No original issue criterion is thereby ticked. |
| Exercise-only delivery | Missing approved climate records and consumer identity compatibility prevent the requested full historical outcome | Current plan, details, research, child READMEs, changes, state and KB consistently preserve the caller-approved bounded direction and stops. No unaccepted new scope substitution found. |
| P02-T01 provenance/domain | PC-001/PC-005 require fingerprinting and supported numerical domain | Both present in exact #179 source/tests/manifest. |
| P02-T05 test assertion | New fingerprint dependency invalidated an existing exact-set assertion | The tightly coupled existing regression was updated without deletion; justified by source inspection. Reported initial mypy/lint corrections do not conceal a remaining test failure. |
| P03 cleanup/gate | PC-002/PC-007 corrections require visible selection, successful partial receipt and exact base | Details preserve these future obligations. No cleanup/gate was executed by this reviewer and no receipt is claimed. |
| State/handoff | Parent records Review as active and names all three blockers | Consistent at the supplied pre-review head; parent owns subsequent reconciliation. No state was edited here. |

No material unaccepted implementation-time decision or divergent planning assumption was found that requires a new rpi-plan route.

## Critique and Material Revision Assessment

The original critique remains Complete / Revise, with 0 Critical, 3 High, 4 Medium and 0 Low. It is not replaced, rescored or silently corrected by this Review.

| Original finding | Recorded disposition | Review assessment |
| --- | --- | --- |
| PC-001 High | Accepted | Helper source fingerprint and manifest binding implemented and tested at #179 head. |
| PC-002 High | Accepted | Current details require visible git clean -ndx, preservation/selection and a stop for unknown deletion candidates; execution remains pending. |
| PC-003 High | Rejected, erroneous premise | Preserve the rejection and original wording. The caller's gate contract explicitly selects /tmp/ama-rpi-heavy.lock and external output; this Review does not endorse the critique's invented caller/parent prohibition or create a new finding from it. No gate/lock operation was needed here. |
| PC-004 Medium | Accepted | Each exact child commit directly parents the recorded foundation. |
| PC-005 Medium | Accepted | Exercise domain excludes singular/nonfinite inputs and matches existing factor support; bounds are not claimed as physical evidence. |
| PC-006 Medium | Accepted | This record assesses exact heads, preserves adverse original evidence and separates defects, residual work, execution and acceptance. No substantive implementation defect was identified to defer or waive. |
| PC-007 Medium | Accepted | Current details name successful receipt only, --required-scope partial, fetched current base and stale-input stop. Verification is still pending, not passed. |

Dependent work proceeded only in the eligible exercise-component boundary. Source adoption and identity migration did not resume under an assumed approval. No fresh critique or repair-and-repeat Review is requested.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Disposition |
| --- | --- | --- | --- |
| F01: source/reuse and grounded validation | #178/#425 remain pending; public metadata and synthetic fallback are not paired source authority | Owner/data-licence custodian chooses authorized exact source/terms/records; then grounded projection work | Open distinct follow-up; no new defect, repeated blocker comment or rpi-research command invented. |
| F02: consumer identity and actual writer | Existing stock identities fail actual #110 admission; no migration is authorized | Owner chooses separately reviewed identity compatibility path with lineage/control/replay evidence; then writer integration | Open distinct follow-up for #183/#110/#188; not an active implementation repair. |
| F03: owner integration and aggregate validation | Caller DO NOT MERGE keeps all siblings independent; new components are not wired together | Owner reviews/selects authorized integration, retains README explanations and establishes an aggregate candidate before its own scoped validation/readiness decision | Open distinct follow-up. Neither focused child results nor a parent documentation receipt replaces it. |

Actual dated-source measures, physical/historical bounds and full-stock reconciliation remain under these follow-ups, not invented new active tasks. The parent changes record mirrors the remaining work. No formal resident, legal, professional, live or whole-issue approval is inferred.

## Findings

No new substantive RV defect, unaccepted decision gap or material evidence gap was established in the supplied approved exercise-only boundary.

Severity counts: 0 Critical, 0 High, 0 Medium, 0 Low. No RV IDs are manufactured for already-declared dependency stops or for intentionally absent integration. F01-F03 above retain their distinct owners and routes; zero findings does not mean original acceptance or final readiness.

## Defects

None identified within the assessed bounded components and evidence. This is not a scientific calibration, integrated writer test or acceptance of any later repaired/different head.

## Routed Findings

| Class | Destination | Action |
| --- | --- | --- |
| New implementation defects | None | No rpi-implement repair route established by this Review. |
| New decision gaps / invalid assumptions | None | No rpi-plan revision requested. |
| New material evidence gaps | None | No rpi-research re-entry requested for the completed bounded work. |
| Existing residual dependencies | Distinct F01-F03 owners | Preserve the source/identity/integration stops and their next actions above. |

Later authorized work does not erase this original Review or extend its exact-head coverage.

## Validation Evidence

| Command or evidence | Scope | Status | Result / limit |
| --- | --- | --- | --- |
| git status --short; git branch --show-current; git rev-parse HEAD | Current worktree | Passed | Initially clean; feat/sensor-backfill-177 at exact supplied parent. |
| git diff foundation head; git show head:path | Parent and all five child heads | Passed | Complete changed surfaces inspected without checkout, copying source or branch changes. |
| git log --format with commit parents | All five children | Passed | All five heads directly fork the specified common foundation. |
| git diff --check foundation head | Parent plus all five child heads | Passed | No whitespace errors reported. |
| Child #179 record: test_indoor_projection, test_sensor_backfill, test_sensor_stock, test_sensor_faults, test_sensor_plausibility, test_synthetic_determinism; targeted Ruff/mypy | Exact #179 child | Reported Passed; not rerun | 48 tests, including 1,500 equation/RNG cases; existing ResourceWarnings disclosed. No raw retained runner transcript was independently verified here. |
| Child #180 record: test_retrofit_effects and test_sensor_stock; targeted Ruff/mypy | Exact #180 child | Reported Passed; not rerun | 18 tests; four new semantic tests plus 14 stock regressions. |
| Child #181 record: test_household_conditions and test_sensor_stock; Ruff/format/mypy | Exact #181 child | Reported Passed; not rerun | 19 tests; five new tests plus 14 stock regressions, including 3,000 profiles. |
| #183 recorded installed-package control/stock _shape probe and estimate | Public synthetic compatibility and legacy sample only | Reported Passed; not rerun | Valid control accepted, stock observation returned IDENTITY; conditional estimate before generation. Not full consumer/writer acceptance. |
| Independent executable reruns | Child tests and compatibility estimate | Skipped | Caller expressly permits honest reported-test review. No detached worktree, installation, shared venv mutation or new scratch output was needed. |
| python3 tools/rpi-checks.py --changed and subsequent receipt verification | Future committed parent documentation candidate only | Not run | Parent owns exactly one gate AFTER committing original Review. This Review spends no gate invocation and supplies no receipt. |
| Full matrix, SQL, Docker, Azure, private datasets, .env/secrets, uv, live AI and hosted checks | Outside supplied review authority | Not run | No such acceptance or activity claimed. |
| Remote issue/PR bodies, lifecycle and blocker comments | Reported research/changes evidence | Not freshly fetched | No issue mutation or PR action. PR numbers/open-draft/base status remain reported evidence at supplied heads. |

The review reran no scientific or application tests. Reported checks and source inspection support a bounded verdict, not independent execution of those checks. Parent gate readiness, remote status and hosted approval remain separate.

## Blockers and Remaining Work

* No blocker to this evidence inspection.
* Planned P03-T02/T03 still require parent reconciliation/commit and the one doc-scoped gate with visible cleanup selection and successful exact-base partial receipt verification where possible. Do not infer completion from this review.
* Whole-original source-grounded history and consumer integration remain blocked at F01/F02. All siblings remain unintegrated under F03 because merging is forbidden.
* Any later source/head/base change is outside the exact assessment below; a passing documentation gate cannot upgrade these child-source or historical/physical boundaries.

## Outcome

* Outcome: Residual work.
* Planned execution: Partial; independent Review execution: Complete.
* Bounded component assessment: #179/#180/#181 are consistent with the accepted exercise-only direction at the exact heads inspected; #178/#183 correctly stop at their recorded blockers. No new substantive defect identified.
* Whole-original acceptance: NOT established; original criteria remain unticked. This is not Conformant full historical delivery, an integrated aggregate, a final-ready parent, hosted approval or permission to merge.
* Rationale: known external decisions, integration and subsequent parent publication remain intentionally unfinished. They are not defects in the smaller approved components and cannot be waived by focused tests.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | None | No new defect found. |
| Decision gap or invalid assumption | None | No new unaccepted divergence found. |
| Material evidence gap | None | Reported-check limits explicitly retained; no unsupported pass claim. |
| Non-blocking residual work for completed component scope | F01, F02, F03 | Source/reuse owner; identity decision owner; owner-authorized integration respectively. These still block whole-original acceptance. |
| Remaining accepted P03 work | Active parent | Reconcile and commit this original review unchanged in meaning, then the authorized single documentation-scoped gate; preserve any adverse or stale result honestly. |

## Next Steps

Return this one Review to the active parent. Continue only the already-authorized P03 evidence/publication work, preserving the exact assessed heads, original critique and F01-F03 stops. No new RPI stage, second Review, repair loop, branch change, issue mutation, PR action or merge is invoked here.
