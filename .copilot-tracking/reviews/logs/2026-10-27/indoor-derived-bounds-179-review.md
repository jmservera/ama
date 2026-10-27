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

## Correction Cycle 1 Independent Review - 2026-10-27

### Opening Review State

* Goal: assess the complete user-authorized PR #502 / #179 correction once,
  independently of implementation, preserving the original Review above.
* Scope: current working-tree diff against a06c2063, containing-pack version
  correction, version-bound golden and compatibility tests, and reconciliation
  with the original synthetic-model acceptance evidence.
* Evidence readiness: canonical research, plan, details, critique, changes and
  durable state supplied; final core validation reported complete, awaiting
  independent inspection. PR #502 is open on feat/indoor-derived-bounds-179
  targeting main.
* Acceptance basis: all three #179 criteria at the synthetic exercise boundary,
  published snapshot version convention, PC-C1-001 and preserved original
  adverse validation evidence.
* First comparison boundary: implementation/test diff and historical/current
  replay distinction, then plan markers, critique dispositions and evidence.
* Read-only boundary: only this appended record may change. Existing dirty
  implementation/planning files belong to the correction and are not moved,
  committed or modified by this Review. No subagents.
* Initial blockers: none identified; publication gates are outside this review.

### Independent Validation Checkpoint

The independent 22-test selector ran in 3.622 seconds: 13 methods passed,
nine methods errored. All ten canonical projection tests, the versioned golden,
multi-shard determinism and default current admission passed. The nine errors
are destination-policy refusals, not assertions about changed behaviour:
project-local scratch conflicts with the existing stock/fault writer's
requirement that its output be outside a checkout. The stale default subcase
passed; the stock subcase failed at fixture creation. The reviewer did not
disable that guard, redirect writes outside the permitted project boundary,
or count the nine errors as passes. Scratch was removed.

The supplied external final core log was read directly: it explicitly records
all nine affected methods as `ok`, including both new stale-version tests,
and ends with 1,437 tests in 433.719 seconds, OK (skipped=186).
This is implementation-run evidence, not an independent full-suite rerun.

Independent configured core static checks passed: `python -m ruff check .`,
`python -m ruff format --check .` (100 files) and
`python -m mypy --no-incremental` (153 files). An earlier explicit-path format
probe failed because it overrode the existing format exclusions for migrated
sensor_backfill.py and test_synthetic_provenance.py. The project configuration
explicitly excludes those files; the exact CI-format command passes. Neither
probe justifies source changes or a new format-conformance claim for excluded
files. `git diff --check` passed.

### Execution Status and Assessed Boundary

* Review execution: Complete. This is the single independent Review of the
  complete current correction boundary, not a second assessment of the
  original delivery. No subagents were used.
* Source base: a06c2063; all 18 pre-existing modified files were inspected
  against HEAD, including source, tests, documentation and dated evidence.
  The original model and canonical tests were also read. Their SHA-256 values
  still match the original assessed fingerprints above.
* The earlier original Conformant outcome is preserved, alongside its limited
  targeted coverage and the subsequently discovered hosted failure. Neither
  that failure nor either independent probe failure is retrospectively green.
* No source, test, plan, details, research, critique, changes or durable-state
  edit was made by this reviewer. Only this record is appended.

### Plan-to-Change and Completion Reconciliation

| Scope | Implementation and evidence | Assessment |
| --- | --- | --- |
| P03-T01 | sensor_backfill.py declares default v3, stock v2, fault snapshot v2 and integrated v2; writers and current loaders use the same constants. | Complete and reconciled. Model equations/RNG and reading schemas do not change in this correction. |
| P03-T01 | Fault snapshots separately record sensor-fault-packets-v1; evaluator truth remains v1. Composed output takes integrated v2, including fault-enabled composed output. | Snapshot identity is distinct from unchanged packet mechanics and schemas. No new loader path is implied. |
| P03-T01 | privacy.py recognizes historical stock-v1 and current STOCK_VERSION in both fabric-file selection and the empty-register exception. | Historical audit compatibility is retained without granting historical loader admission. |
| P03-T01 | Literal-version default golden, strengthened stock/integrated/fault manifest assertions, both stock privacy layouts, two isolated stale-version methods. | Existing tests remain; one method is renamed, two added, within the four-addition budget. Current positive loader/consumer controls remain. |
| P03-T02 | Core README, existing synthetic-data synthesis, reference index and append-only log explain the deliberate baseline change and immutable historical bytes. | Complete; old SHA and original adverse outcomes remain in dated evidence. No published dataset is modified in the diff. |
| P03-T02 | Final exact core discovery log and configured static checks. | Complete for the stated local core boundary; optional skips and independent environment limitations remain explicit below. |
| P04-T01 | Independent correction Review followed by commit/same-PR publication. | This Review is complete. Publication and parent-owned evidence/state reconciliation remain pending; the combined P04 marker must not imply publication is complete. |

Original P01/P02 completion statements describe the earlier delivery; the
appended correction sections explicitly identify current P03 completion and
P04 pending. Plan, details, changes and durable state agree on that active
handoff. No stale historical header is used as current publication evidence.
The branch includes the rubric-bot a06c2063 commit without rewriting it.

### Implementation-Time Decisions and Critique Disposition

The containing-version change is supported by C8/C9, the existing pack-version
convention and the user-authorized correction, not an unexplained golden
replacement. The refresh-policy defaults are described as proposed in the
synthesis; this code correction follows the selected version convention
without treating it as owner approval to refresh any published or live data.
Model v2 remains intentional; restoring v1 clips would contradict #179.

PC-C1-001 is resolved. The two new tests construct current fixtures, mutate
only manifest version and preserve current revision/hashes/parameters. They
assert the early specific private provenance/composed-version refusal rather
than accepting a later manifest mismatch, and patch the replay writer and
downstream schema/SQL/consumer effects. Default and stock admission refuse;
composed admission also proves no temporary context allocation. Existing
successful current default, stock and authoritative-consumer tests are the
positive controls. The final implementation-run log contains all these passes.

The legacy-scratch clarification is accurate and compatible: load_into()
already opens an empty temporary context before _verify_snapshot(), so the
legacy tests promise no replay writer/output/schema/SQL, not zero context
allocation. load_with_consumer() checks version before its temporary context,
as directly asserted by the composed test. Details and changes preserve this
distinction; no unrelated loader-control-flow refactor or unaccepted material
decision is concealed. Original critique verdicts remain Complete / Revise
with their later direct dispositions, not rewritten as original approvals.

### Independent Golden Legitimacy and Acceptance Audit

A separate reviewer-executed measurement independently reconstructed the
original v1 baseline, schedule, loss, fixed floor/RH clips and two Gaussian
draws using the old source as the reference. Only an in-memory patch of
project() was used for this measurement; no legacy implementation was added
to production. Fresh project-local synthetic outputs were discarded afterward.

For seed 183, 12 homes, three days and the default window, it reproduced:

* v1 SHA: `657ff373107807b34bd4bb6720dec534fcef13134292c5d753ef24bdbd723549`.
* Current v2 SHA: `25bb5259d89554560e179ae5412f3148595c47a87def9ee2fca61518e18ded5b`.
* Exactly 861 rows in each; one temperature and four RH field changes;
  every other row field and sensors.csv bytes identical.

This independently confirms the recorded causal evidence. The new golden
asserts literal snapshot v3, literal model v2 and manifest model v2; unchanged
scale/register goldens remain pinned. It supplements independent semantic
tests rather than using deterministic repetition as proof of model correctness.
Historical snapshots require their original revision/runtime, are not
relabelled for admission and are not overwritten by this correction.

| #179 criterion | Review assessment and evidence |
| --- | --- |
| 1. Documented/versioned inputs, equations and parameters | Supported: unchanged model-v2 declarations, README equations, manifest/fingerprint binding and now coherent containing versions. Canonical fingerprint and literal-version golden passed independently. |
| 2. Every parameter sourced or labelled exercise | Supported: explicit exercise classification for coefficients, domains, noise scales and tail cap; RH 0..100 is physical saturation, not an empirically validated indoor threshold. No new calibration claim. |
| 3. Outdoor-record-derived plausible indoor bounds | Supported only at the authorized synthetic-model boundary: B/V depend on each paired outdoor record and dwelling/household/dated inputs; capped residuals produce derived envelopes. Independent tests cover supported endpoints, both exact equations/RNG states, two-call tails/saturation, sensitivity and all 70,176 nominal paired-history rows with replay. |

Nonnegative vapour and increasing saturation pressure make the RH interval's
endpoint order valid; the supported indoor temperature interval remains inside
the helper's guarded domain. Fault-corrupted packets are intentionally outside
nominal bounds. Rounded CSV comparisons retain the explicit 0.005 tolerance.
Closes #179 remains supportable at this narrow exercise boundary, not parent
#177, live PRD AC-066--068, empirical building physics or operational acceptance.

### Validation Evidence and Limits

All commands below use the supplied existing core-venv Python; no dependency
install was performed. Independent unit selection ran from src/core with
PYTHONPATH=tests, PYTHONDONTWRITEBYTECODE=1 and project-local TMPDIR.

| Validation | Status and attribution |
| --- | --- |
| Supplied final `python -m unittest discover -s tests -v` | Implementation-run evidence inspected directly: 1,437 run, 1,251 passes, 186 optional skips, zero failures/errors, 433.719 seconds. Not rerun by reviewer. External file: core-unit-correction1-final.log under the supplied session files directory. |
| Independent `python -m unittest -v` selection | 22 methods, 13 passed and nine destination-policy errors in 3.622 seconds. Full explanation preserved in Independent Validation Checkpoint. No failed method is counted as a pass. |
| Independent causal reference measurement | Passed: both exact hashes, 861 rows, permitted 1+4 field changes only and identical sensor register. |
| Independent `python -m ruff check .` | Passed under configured full-core CI rules. Explicit changed-path lint also passed. |
| Independent `python -m ruff format --check .` | Passed: 100 files. Earlier explicit-path probe failed on existing excluded migrated files; not silently discarded. |
| Independent `python -m mypy --no-incremental` | Passed: 153 source files, under existing exclusions, not a claim that migrated ignored modules are fully typed. |
| Independent `git diff --check` | Passed. |
| Heavy gate, API rerun, hosted rerun, live SQL Server/blob/browser/cloud, calibration and human approval | Not performed; outside this authorized bounded Review. Existing optional core skips are not live/platform acceptance. |

The exact independent unit selector comprised:

* All ten methods in test_indoor_projection.ProjectionTests.
* SyntheticDeterminismTests.test_versioned_payload_goldens and
  test_sensor_all_shards_reproduce_and_date_and_seed_change_readings.
* SensorPrivacyTests.test_stale_snapshot_versions_refuse_before_replay_or_sql,
  test_valid_synthetic_receipt_is_counts_only_and_idempotent and
  test_stock_requires_explicit_matching_selection.
* HistoricalBackfillTests.test_stale_composed_version_refuses_before_scratch_replay_or_consumer,
  test_verified_writer_load_uses_real_consumer_and_replay and
  test_compressed_bytes_repeat_and_manifest_binds_all_models.
* PrivacyMutationTests.test_register_backed_sensor_snapshot_is_checked.
* SensorFaultTests.test_writer_truth_positions_cross_sensors_shards_and_hashes
  and test_loader_refuses_new_schema_before_database_changes.
* SensorStockTests.test_all_excluded_is_explicit_empty_output.

The supplied final log is located at
/home/azureuser/.copilot/session-state/9b4f81eb-34a4-420a-bd8a-6c799d50f583/files/core-unit-correction1-final.log.
Its exact affected-method `ok` entries and terminal summary were inspected,
not inferred from the handoff. No external receipt, complete local gate,
exact published-head assessment or hosted success is established here.

### Findings, Follow-Ups and Outcome

* Findings: none. RV-C1 severity counts: Critical 0, High 0, Medium 0, Low 0.
  No substantive implementation defect, unaccepted decision or material
  in-scope research gap was found; no RV-C1 identifier is fabricated.
* Review execution: Complete.
* Outcome: Conformant within the explicitly synthetic exercise boundary.
* Independent integration rerun limitation: nine methods could not reach
  their assertions because of the reviewer-local output restriction. This is
  disclosed validation coverage, not an observed model/admission defect.
  Direct source inspection and inspected final full-suite evidence support
  the verdict without bypassing the destination guard or claiming a fresh
  independent 22-test pass.
* Blockers to this Review: none. No approval or permission to publish is
  granted by this verdict. P04 publication, owner review/merge, hosted checks
  and all applicable exact-head/publication prerequisites remain parent-owned.

| Finding class | Destination and smallest next action |
| --- | --- |
| Implementation defect | None; no rpi-implement correction routed. |
| Decision gap or invalid assumption | None; no rpi-plan revision routed. |
| Material in-scope evidence gap | None; no rpi-research restart routed. |
| Non-blocking follow-up: building-physics calibration | Distinct future live-use research; Assets/Building Safety commission competent calibration before making empirical claims. Not an active P03/P04 requirement or a closed acceptance item. |
| Non-blocking follow-up: OD-43 activation | Assets/Building Safety/DPO/data owners resolve real monitoring and activation approvals separately. No resident consent, safety authority or operational approval follows from synthetic tests. |

The unchanged plan Follow-Up Items and durable-state priority retain those
owners/next actions and exclusions; they are not defects or newly active plan
tasks. This single correction Review stops here. A later routed implementation
would not require another Review by this record.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/reviews/logs/2026-10-27/indoor-derived-bounds-179-review.md](.copilot-tracking/reviews/logs/2026-10-27/indoor-derived-bounds-179-review.md) | Original Review preserved; this dated correction record appended |
| [.copilot-tracking/research/2026-10-27/indoor-derived-bounds-179-research.md](.copilot-tracking/research/2026-10-27/indoor-derived-bounds-179-research.md) | C1--C9 and correction causal/versioning research |
| [.copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-plan.md](.copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-plan.md) | P03 complete, P04 publication pending |
| [.copilot-tracking/details/2026-10-27/indoor-derived-bounds-179-phase-details.md](.copilot-tracking/details/2026-10-27/indoor-derived-bounds-179-phase-details.md) | Correction contract and legacy-scratch clarification |
| [.copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-critique.md](.copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-critique.md) | Original critique and PC-C1-001 preserved |
| [.copilot-tracking/changes/2026-10-27/indoor-derived-bounds-179-changes.md](.copilot-tracking/changes/2026-10-27/indoor-derived-bounds-179-changes.md) | Final implementation/test evidence and prior failures |
| [.copilot-tracking/rpi-sessions/2026-10-27/indoor-derived-bounds-179-state.json](.copilot-tracking/rpi-sessions/2026-10-27/indoor-derived-bounds-179-state.json) | Parent-owned current handoff and distinct follow-ups |
| [docs/reference/research/retrofit-synthetic-data/README.md](docs/reference/research/retrofit-synthetic-data/README.md) | Version/refresh convention and historical immutability |
| [src/core/README.md](src/core/README.md) | Model equations, containing versions and literal hashes |

## Next Steps

Return this Complete / Conformant, zero-finding result to the active parent.
The parent should reconcile P04/state with this record, then perform only its
authorized same-branch PR #502 publication steps when independently eligible.
No source correction, second Review, merge, live activation or user decision
is requested by this Review.
