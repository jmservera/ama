<!-- markdownlint-disable-file -->

# Task Research: sensor-scenarios-190

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher | RPI Agent, rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/sensor-scenarios-190-research.md |

## Research Brief

Research #190 and children #192, #193, #194 against the merged simulator.
Audience: maintainers and downstream #111/#133 evaluators. Scope: synthetic
scenario inputs, isolated truth, deterministic checks and simulator documentation.
Non-goals: deployment, real devices/data, operational thresholds, completing
unrelated live-streaming or aftercare features. Output mode: convergence.
Acceptance requires per-check evidence; unmet dependencies must remain explicit.

## Research Parameters

Focused posture, selected for the caller's bounded internal task. Initial
internal areas: src/core simulator and tests, linked PRD/BRD/ADRs, research plan
and data dictionary. External areas: named GitHub issues only; no new regulatory
claims. Evidence root: .copilot-tracking/. Source edits prohibited in Research.
Caller limits: local tests only; at most one scoped changed gate for large
changes under /tmp/ama-rpi-heavy.lock, timeout 0; no full gate, secrets, private
datasets, uv or deployment.

## Extension Registry and Provenance

| Kind | Candidate | Provenance and disposition |
| --- | --- | --- |
| Instruction | Repository instructions | Selected: src layout, KB maintenance, safe branch/publication |
| Skill | rpi-research | Selected: three-wave evidence and readiness |
| Specialist | RPI Researcher | Skipped: one tightly coupled code/contract trace, direct investigation |
| Skill | Web/design skills | Skipped: no web changes |

## User Participation and Research Decisions

The explicit full-loop request authorizes automatic progression for this task.
No interaction is needed for routine choices; unresolved Legal/DPO/Compliance
authority will be recorded, never inferred.

## Scope and Success Criteria

Read all four requested issues and linked requirements. Verify reusable
generation/schema/fault/check APIs, truth separation, outcome semantics and
downstream test surfaces. Every result needs a stable evidence pointer or an
explicit gap. No acceptance criterion is ticked without proof.

## Task Research Requests

Deliver one PR to main on the provided clean feat/sensor-scenarios-190 branch,
including dated Research, Plan/details, changes and independent Review.

## Direction Controls

Caller selects #190/#192/#193/#194, existing src/core backfill, pip only and
local validation. Keep workflow/check names unchanged. #191 is already closed.
Live #184, #111 and #133 remain open and must not be represented as delivered.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What generator/check contracts can scenarios reuse? | depth | Open |
| Q2 | How can truth and expected outcomes stay separate from inputs? | depth | Open |
| Q3 | What live and downstream surfaces exist versus remain blocked? | depth | Open |
| Q4 | What provenance and documentation are missing? | straightforward | Open |

## Prior Knowledge Gate

Read requested issues, #191, #111, #133, #177, #184, KB index opening,
memory, original case study and addendum context. Verify source claims against
current code rather than historical "not started" issue text.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Mapped generator, existing fault-packet schema, projection, dated loss model,
plausibility tests and paired ERA5 packet. Issue text saying "not started"
is stale for these delivered components. Reflection: reuse generation and
observation normalization; do not build a parallel ingestion or device client.

#### Wave 2: Deeper

Verified `sensor_backfill.readings()` accepts an explicit outdoor sequence,
`sensor_faults.observation()` removes embedded labels, and existing snapshot
conventions separate analysis/truth. `retrofit_effects.Measure` only models
beneficial fabric-loss multipliers; adverse effects cannot honestly be passed
off as a sourced physical effect. Reflection: overlay explicit exercise
temperature/RH profiles on clean backfill rows, retaining identity/schema and
labeling every magnitude. Retrofit scenarios use identical paired diurnal
cycles and noise, a completion instant, delayed activation and a matched
no-effect counterfactual, not an asserted causal evaluation.

#### Wave 3: Contrarian

Searched runtime/tests for `sensor_analysis`, `SENSOR_REVIEW_DUE` and aftercare.
No delivered #111 deterministic analytics or #133 evaluator contract exists.
Live #184 has only schema #186 closed. A runnable live simulator command would
be fabricated. Air temperature/RH alone cannot establish surface condensation
or mould. Reflection: provide an explicitly exercise-only comparator and
confusion/sensitivity report; do not activate tasks or call the comparator an
approved R2 method. Keep #193 downstream-use criterion and #190 closure unmet.

#### Parent Synthesis and Disposition

Accept separated, deterministic packs and per-check exercise reporting.
Reject adding real analytics/aftercare or live streaming in this task, which
would widen scope and assume undecided authority. Accept documentation of the
live contract and explicit missing runner, not invention of a command.
No second cycle needed: material APIs, requirements and limitations are known.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Clean provided topic branch, no existing PR | git status / branch / gh pr list, 2026-10-27 | High |
| W1 | Parent requires child disposition and per-check validation | https://github.com/jmservera/ama/issues/190, retrieved 2026-10-27 | High |
| W2 | Seven named damp scenarios, separated truth, confusion support | https://github.com/jmservera/ama/issues/192, retrieved 2026-10-27 | High |
| W3 | Retrofit directions and downstream test use required | https://github.com/jmservera/ama/issues/193, retrieved 2026-10-27 | High |
| W4 | Both-stage docs and climate licence/provenance required | https://github.com/jmservera/ama/issues/194, retrieved 2026-10-27 | High |
| C2 | Clean seeded generation accepts explicit outdoor/window | src/core/src/zava_forward/core/synthetic/sensor_backfill.py:95 | High |
| C3 | Shared observation normalization excludes fault truth | src/core/src/zava_forward/core/synthetic/sensor_faults.py:116 | High |
| C4 | Dated effect is a loss multiplier, not guaranteed outcome | src/core/src/zava_forward/core/synthetic/retrofit_effects.py:1 | High |
| C5 | Projection is uncalibrated exercise math | src/core/src/zava_forward/core/synthetic/indoor_projection.py:10 | High |
| C6 | R3 needs confusion/sensitivity and agreed exercise limits | docs/reference/research/iot-sensor-analytics-research-plan.md:454 | High |
| C7 | AC-067/068 require approved signals and evidence, not diagnosis | docs/prds/zava-forward-retrofit-programme-demonstrator.md:2163 | High |
| C8 | OD-43 blocks real use, not simulator exercise | docs/brds/agentic-retrofit-programme-brd.md:2161 | High |
| C9 | Existing snapshot helpers refuse nonempty destinations | src/core/src/zava_forward/core/synthetic/provenance.py:33 | High |
| C10 | ERA5 packet records retrieval, hashes, CC BY and limited approval | docs/reference/research/climate-paired-source-178/open-meteo-era5-durham-2023-2024-metadata.json:1 | High |
| C11 | Existing #191 checks cover bounds, structure and rates | src/core/tests/test_sensor_plausibility.py:1 | High |
| C12 | Shared schema delivered, live transport unavailable | docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:71; src/core/README.md:23 | High |
| C13 | ADR 0006 requires packaged src and external tests | docs/adrs/0006-src-layout-and-cutover.md:58 | High |

## Findings Mapped to Questions and Evidence

Q1 answered by C2-C5/C9/C11. Q2 answered by C3 and the existing sibling
analysis/truth convention. Q3 answered by C7/C8/C12 and runtime search:
downstream integration remains future work. Q4 answered by C10 and the stale
dictionary Sensor data section (claims no composed/datestamped effects).

## Alternatives and Decision State

Selected: bounded standalone `synthetic.sensor_scenarios` CLI, exercise
comparator and per-check report, tests outside the package, extend existing
README/dictionary/research synthesis. Compared with modifying default backfill
(rejected: would change seeded compatibility) and building #111/#133 now
(rejected: unrelated authority/product scope). No new dependencies needed.

## Open Questions, Risks, and Residual Uncertainty

The live stage cannot be run yet. #193's actual use by #111/#133 tests remains
unmet; downstream-ready fixtures are not integration acceptance. #190 remains
Refs until all child criteria are proven or explicitly owner-deferred. R3
outputs are engineering evidence, not competent-reviewer R2 approval or agreed
false-alert limits. No new Legal/DPO decision is necessary for independent
synthetic-only fixture work. Python cannot import core in this worktree yet;
create an external virtualenv and pip-install editable packages for validation.

## Potential Next Research

Only re-enter if the code contradicts the selected scenario or evidence design.

## Planning Readiness

Ready for bounded independent implementation. Research disposition: executed.
Self-check: three waves completed in order, sources/limits mapped, no fabricated
live capability or acceptance, source unchanged during Research.
