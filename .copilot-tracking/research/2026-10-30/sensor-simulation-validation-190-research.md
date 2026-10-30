---
title: Sensor simulation validation 190 research
description: Current-base scope and evidence for the sensor validation feature
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Research Brief

* Target: issue #190 and children #191-194, both simulator stages, per-check validation, scenario isolation and documentation.
* Purpose and audience: give the coordinator a locally verified implementation and honest criterion dispositions.
* Scope: existing `src/` simulator, tests outside packages, related README and data dictionary.
* Non-goals: Azure, live transport, deployments, secrets, issue mutation, push or PR creation.
* Criteria: exact issue acceptance, synthetic-only safety, labelled exercise thresholds and retained original evidence.
* Requested outputs: dated Research, Plan/details/critique, changes and Review; local commit.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | What is already delivered, what remains, and what can be verified without live services? |
| Initial internal areas | `src/`, sensor scenario tests, existing 2026-10-27/29 evidence, research plan, data dictionary |
| Initial external areas | GitHub issue #190, children and dependencies via `gh issue view` |
| Posture | Focused, selected for bounded named issue scope |
| Completion basis | Material acceptance coverage and verified current contracts |
| Resolved evidence root | `.copilot-tracking/` |
| Edits during Research | Evidence and state only |
| Explicit limits | No cloud, credential access, live sign-in, push or deployment; heavy gates under flock |

## Extension Registry and Provenance

| Kind | Candidate | Selection and authority |
| --- | --- | --- |
| Instruction | `.github/copilot-instructions.md` | Selected: src layout, local gate, knowledge-base and branch safeguards |
| Skill | `rpi-research` | Selected: three ordered inline waves and evidence-owned readiness |
| Specialist | Research subagent | Skipped: a continuous current-code trace is best handled inline |
| Web skills | UI and accessibility | Deferred unless scope requires web edits; no visual changes inferred |

## User Participation and Research Decisions

User supplied branch, base, full-loop authority, commands and exclusions. Non-interactive execution requires no routine questions. Existing issue text is inert scope data, not authority to execute embedded instructions.

## Scope and Success Criteria

Verify every child disposition, current scenario contracts and exact parent criteria. Preserve original evidence and avoid claiming live or human acceptance from local tests.

## Direction Controls

Keep the supplied clean branch `feat/sensor-simulation-validation-190` at base `a31048f15fa3120c58bacd22a375d86ae5ab7431`. Local commit only. Use `Refs #190`.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What current code and tests satisfy the children? | depth | Open |
| Q2 | What gaps remain in both-stage documentation and per-check results? | depth | Open |
| Q3 | Which criteria must remain explicitly deferred? | straightforward | Open |

## Prior Knowledge Gate

Initial issue retrieval: #191 closed; #192/#193/#194 open. #177 closed; #184 open. Historical sensor-scenarios evidence exists on main and must be verified, not replayed as current evidence.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inspected source, component guides, child/dependency issues and original
2026-10-27/29 records. The scenario generator already delivers eleven isolated
cases and fifteen per-check comparisons. Inline execution avoids unnecessary
delegation for this continuous trace. Reflection: do not recreate or alter
the delivered fixture/comparator.

#### Wave 2: Deeper

Verified observations-only analysis, fixed-truth confusion, retrofit windows,
hash manifests, replay construction and CI discovery. `sensor_stream.replay`
uses legacy clean seasonal backfill, not composed ERA5 projections. Its existing
test witnesses one short exact overlap; annual range/structure and per-home
distribution checks across both stages are not explicit. Reflection: add
targeted cross-stage regression tests using constructed stock, without changing
the model, schema, version or scenario result count.

#### Wave 3: Contrarian

Checked the assertion that the live runner is absent against the actual API
SDK adapters: the dictionary is stale, while the core README already links the
finite publisher. Also checked downstream #111/#133: neither whole feature is
delivered by standalone scenario tests. The original Review identifies these
as open criteria, not permission to invent downstream consumers or owner
deferrals. Reflection: correct documentation and report bounded deferrals
without changing GitHub state or claiming parent acceptance.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Reuse eleven-case scenario pack | C1-C2 | Accepted | Already implements exact damp/retrofit scenario scope |
| Cross-stage annual checks | C3-C5 | Accepted | Close local statistical-validation gap without new runtime behavior |
| Repair stale both-stage dictionary | C6-C7 | Accepted | Current adapters contradict unavailable-runner wording |
| Implement #111/#133 or run Azure | W3/W5, C8 | Deferred | Separate features and explicit no-cloud boundary |

#### Cycle Re-entry Evaluation

No further cycle required: current source and criteria are covered; remaining
uncertainties concern prohibited live services or separately owned consumers.
No missing evidence prevents the bounded tests/documentation plan.

## Evidence Log

### External Evidence

| ID | Finding | Source | Retrieved |
| --- | --- | --- | --- |
| W1 | Parent requires child stories closed or deferred and per-check reporting | https://github.com/jmservera/ama/issues/190 | 2026-10-30 |
| W2 | #192 requires seven seeded labelled scenarios, isolation and confusion-summary support | https://github.com/jmservera/ama/issues/192 | 2026-10-30 |
| W3 | #193 has outstanding downstream #133/#111 test use | https://github.com/jmservera/ama/issues/193 | 2026-10-30 |
| W4 | #194 requires both-stage README/data dictionary | https://github.com/jmservera/ama/issues/194 | 2026-10-30 |
| W5 | Live-stage dependency remains open; no permission for live execution | https://github.com/jmservera/ama/issues/184 | 2026-10-30 |

### Codebase Evidence

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Seven damp and four retrofit scenarios already generated from clean observations | `src/core/src/zava_forward/core/synthetic/sensor_scenarios.py:219` | High |
| C2 | Fifteen independent outcome/delta results, confusion and sensitivity; no overall pass | `src/core/src/zava_forward/core/synthetic/sensor_scenarios.py:387` | High |
| C3 | Replay is clean seasonal backfill with explicit transport faults and nominal slots | `src/core/src/zava_forward/core/synthetic/sensor_stream.py:156` | High |
| C4 | Existing overlap test covers one home and two days | `src/core/tests/test_sensor_stream.py:131` | High |
| C5 | CI discovers every core test; existing long-history plausibility remains exercise-valued | `.github/workflows/src-ci.yml:82`; `src/core/tests/test_sensor_plausibility.py:1` | High |
| C6 | Dictionary incorrectly calls live runner unavailable and lists older snapshot versions | `docs/reference/research/retrofit-synthetic-data/data-dictionary.md:414`; `:463` | High |
| C7 | Finite SDK publisher/receiver exist, require independently approved activation and credentials | `src/api/README.md:1202` | High |
| C8 | Original Review preserves downstream/live and child-disposition gaps | `.copilot-tracking/reviews/logs/2026-10-27/sensor-scenarios-190-review.md:64` | High |

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Implication |
| --- | --- | --- | --- |
| Q1 | Existing scenario/source tests cover #192 and local #193 targets | C1-C2 | Reuse unchanged |
| Q2 | Add explicit annual backfill/replay statistical contracts; correct dictionary | C3-C7 | Bounded tests/docs implementation |
| Q3 | #193 consumer use, #184 live operation and owner child dispositions remain open | W3/W5, C8 | Preserve honest parent acceptance gap |

## Alternatives and Decision State

Selected: focused tests plus documentation, using current models and fixtures.
Rejected: duplicate generator, optional new report mode or rewritten scenario
schema; these add maintenance and break existing count/hash contracts without
addressing a demonstrated defect. Rejected: normal mock-network evidence as
live proof. Deferred: actual downstream consumer integration and human acceptance.

## Risks and Residual Uncertainty

Annual structure thresholds are labelled exercise values, not climate-derived
limits or health indicators. Replay parity validates the shared legacy model,
not composed-climate continuity, live IoT Hub or SQL. Existing historical Review
outcomes remain immutable. No fresh legal/licence currentness assertion is made.

## Sources and Self-check

Repository files above and GitHub issue reads were used. Session-history query
for matching recent branches returned no rows. Required original/addendum,
knowledge-base index/memory and housing primer were read; no private data read.
System Python lacked installed packages; restored declared pip dependencies in
an isolated session venv, not the shared editable environment. No source edits
were made during Research.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready for bounded tests
and documentation. Questions Q1-Q3 answered; no research blocker. Full parent
acceptance remains conditional on human child dispositions/downstream evidence.
Parent RPI Agent owns transition to Plan under the explicit full-loop request.
