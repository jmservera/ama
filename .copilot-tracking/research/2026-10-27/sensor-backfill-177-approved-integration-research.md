<!-- markdownlint-disable-file -->
# Task Research: sensor-backfill-177-approved-integration

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/sensor-backfill-177-approved-integration-research.md |

## Research Brief

* Research the approved climate integration, canonical stock home IDs, child integration and aggregate validation for Refs #177.
* Audience: implementer, independent reviewers and parent PR #486 coordinator.
* Scope: children #481-#485, existing paired climate candidate #425, core synthetic generator and authoritative #110 consumer.
* Non-goals: private datasets, operational monitoring, production acceptance, main push/merge, uv, secrets.
* Criteria: repeatable two-year history on generated 60,000-home stock, truthful provenance, reused consumer validation and evidence-bound acceptance.
* Output mode: convergence, preparing planning.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Source extension; canonical identity compatibility; streaming scale; integration/gate boundaries |
| Codebase scope | src/core, relevant tools, docs and dated RPI records |
| External scope | Existing candidate public climate endpoints and attribution sources only |
| Initial internal candidate areas | synthetic/sensor_backfill.py, sensor_stock.py, sensor_consumer.py; child diffs; paired climate candidate |
| Initial external candidate areas | Existing Open-Meteo/NASA POWER candidate |
| Research posture | focused |
| Posture provenance | Default for bounded caller-directed integration |
| Explicit limits | Exactly one changed parent gate, foreground lock timeout 0, fresh external output, git clean -fdxq first |
| Completion basis | Answer material contract and scale questions with wider/deeper/contrarian evidence |
| Edits allowed | Research evidence and workflow state only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance and scoped authority | Disposition |
| --- | --- | --- | --- |
| Instruction | Repository instructions | All paths; branch, privacy-safe identity, retention and gates | Selected; owner scoped gate supersedes --all |
| Skill | rpi-research | Three-wave evidence contract | Selected |
| Skill | rpi-plan / rpi-implement / rpi-review | Later canonical phases | Deferred until respective phase |
| Specialist | Research worker | Registered independent investigation | Skipped: one tightly coupled code/identity/data trace |
| Skill | Web/design skills | Backend-only task | Not applicable |

## User Participation and Research Decisions

The explicit full-loop request is consent to automatic progression for this new
continuation, not a mode change of the historical completed task. Owner decisions
are supplied directly in the 2026-10-27 request under
`owner-approvals-2026-10-27-b`: candidate source reuse approved for synthetic demo;
existing stock IDs canonical; child integration/aggregate validation authorized.
No additional ordinary approval question is needed or possible in this host.

## Direction Controls

* Preserve original completed RPI evidence and adverse outcomes.
* Reuse current parent and child branches, all currently open draft PRs.
* Use Refs only; mark criteria only on proof; resolve issue blocker comments.
* Mark #486 ready only after checks and independent Review pass; never merge it.
* Clean worktree verified at intake; current branch feat/sensor-backfill-177.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | How can approved paired records support two years without fabricating climate? | depth | Open |
| Q2 | How can stock identities remain canonical while consumer controls stay enforced? | depth | Open |
| Q3 | How can all components generate and validate 60,000-home history locally? | depth | Open |
| Q4 | What exact integration, review and scoped publication gates apply? | straightforward | Open |

## Prior Knowledge Gate

Prior parent PR #486 and issue #178/#183 comments inspected on 2026-10-27.
Their owner-decision blockers are prospectively superseded by the request,
not retrospectively erased. Existing source #425 is one-year modelled climate;
two-year coverage and consumer identity remain technical questions.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inspected all five child diffs and source #425, public stock/fabric/backfill
contracts, faults and consumer. Child source interfaces are independent modules;
their README additions overlap. Candidate climate is one calendar year.
Reflection: reuse approved candidate source with its provenance, but acquire
actual second-year records rather than repeating or relabelling one year.

#### Wave 2: Deeper

Verified stock IDs accept <=128 UTF-16 units with case preserved, while the
consumer restricts uppercase IDs and home length 12. Sensor hashes are 73
characters; bounded uppercase sensor IDs can be derived with collision checks,
without modifying canonical home IDs. Consumer checks home availability against
cases independently of controls. Its SQL stock DDL already allows home
NVARCHAR(128). Explicit fixture case binding is needed for actual admission
tests; no observation may manufacture availability, consent or calibration.
Reflection: identity adaptation must preserve those gates and SQL parity.

#### Wave 3: Contrarian

Challenged scale and scientific claims: 60,000 * 17,520 hourly slots is
1,051,200,000 nominal rows, far beyond the 14 GiB root filesystem free space.
The existing cadence parameter permits a declared lower-frequency full-window
exercise; full hourly volume must still be estimated. Existing private stock
files were identified by names only and were NOT opened. Generate an explicit
public synthetic 60,000-home fixture; do not claim its exact ID set equals the
unread private register. Household and retrofit components are not yet wired;
empty history must not invent completion dates. No model is calibrated physics.
Reflection: aggregate validation must declare cadence, stock fixture lineage,
actual row count and exclusions instead of overstating full-hourly acceptance.

#### Parent Synthesis and Disposition

Accept approved Open-Meteo paired temperature/RH reanalysis with a genuinely
retrieved two-year window and retained hashes/attribution. Retain the NASA
candidate cross-check evidence without pretending it is station truth. Adapt
the writer to canonical stock home IDs, bounded derived sensor IDs and existing
consumer controls; test actual consumer acceptance/rejections and replay.
Integrate all components opt-in to preserve legacy deterministic defaults.
Use gzip-capable deterministic shards if needed for full-stock local validation.
Reject altering home IDs, reusing private datasets, source-year repetition,
automatic consent/calibration, and calling partial gates full-tier validation.

#### Cycle Re-entry Evaluation

No further research cycle required: interfaces and material risks are located;
retrieval and runtime behavior are implementation verification obligations.
Source access failure would block climate implementation, not justify fallback.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/pull/486, retrieved 2026-10-27 | Parent draft; five unmerged children and historical partial gate |
| W2 | https://github.com/jmservera/ama/issues/178, retrieved 2026-10-27 | Existing candidate reuse approval was missing |
| W3 | https://github.com/jmservera/ama/issues/183, retrieved 2026-10-27 | Existing stock observation rejected by consumer identity limits |
| C1 | src/core/src/zava_forward/core/synthetic/sensor_stock.py:63 | Per-ID fabric and preserved opaque stock home IDs; sensor hashes too long |
| C2 | src/core/src/zava_forward/core/synthetic/sensor_backfill.py:195 | Streaming sharded writer, pre-generation estimate, optional fault truth |
| C3 | src/core/src/zava_forward/core/sensor_consumer.py:379 | Closed schema and identity admission; availability and controls remain separate |
| C4 | src/core/src/zava_forward/core/sensor_consumer.py:510 | A control alone does not establish available case/home |
| C5 | src/core/src/zava_forward/core/synthetic/sensor_faults.py:19 | Existing 13-field consumer input and evaluator-only truth contract |
| C6 | src/README.md:48 | Scoped changed-path selection can include transitive images/SQL |
| C7 | src/core/src/zava_forward/core/synthetic/stock_fabric.py:153 | Deterministic fabric attaches to supplied canonical IDs |
| C8 | .copilot-tracking/changes/2026-10-27/sensor-backfill-177-changes.md:23 | Prior exact child heads and focused test evidence retained |

## Findings, Alternatives and Decision State

Selected opt-in integration with canonical home identity and strict input
provenance. Production calibration, real resident consent, regional source
representativeness and exact private-stock coverage remain outside this
synthetic exercise. No source implementation changed during Research.

## Planning Readiness

Ready. Research disposition: executed. Wider, deeper and contrarian completed
inline because this was one coupled contract trace. All Q1-Q4 answered above.
Self-check: named boundaries, source evidence, alternatives, risks and
parent-owned disposition recorded. Parent may transition to Plan.
