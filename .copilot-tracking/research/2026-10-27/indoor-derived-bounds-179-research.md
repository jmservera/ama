---
title: Indoor derived bounds research for issue 179
description: Focused evidence for outdoor-record and dwelling-derived synthetic bounds
ms.date: 2026-10-27
---

## Research Brief

Issue #179 criterion 3 requests indoor temperature and humidity bounds derived
from the outdoor record and dwelling model, replacing the fixed exercise floor
and humidity clips. Re-evaluate all three criteria. Audience: implementer and
PR reviewer. Output mode: convergence preparing planning. Evidence root:
`.copilot-tracking/research/2026-10-27/`.

## Research Parameters and Direction Controls

Focused posture, selected for a bounded internal defect with named sources.
Read issue #179 and its comment, parent #177 and dependencies #168/#178 before
implementation. Preserve exercise labels, synthetic provenance, consent and
human authority. No private data, secrets, Azure, uv or full gate. Only relevant
local tests; at most one locked scoped gate for a large change. One existing
branch and one PR, closing only fully evidenced issues.

## Extension Registry and Participation

Repository instructions and ADR 0006 apply. RPI research selected; domain web
skills skipped because this is backend synthetic modelling. Inline research:
one continuous model/caller trace does not justify delegated research.
No interaction required: the owner explicitly requests the full ordered loop
and the derived-bounds alternative. Phase advancement is authorized by that
request, without implying live, legal or scientific approval.

## Questions and Candidate Areas

1. What outdoor records and dwelling parameters reach each projection path?
2. Which model-derived bounds constrain both normal and composed histories?
3. What documents/tests prove every #179 criterion without claiming calibration?

Starting areas: indoor_projection, sensor_backfill, sensor_stock, outdoor
climate adapters, their tests/READMEs, PRD AC-066--068, ADR 0002 sensor section,
ADR 0006, BRD OD-43 and the sensor research synthesis.

## Research Cycle Log

### Cycle 1: Wider

Read the current model, generator, stock adapter, project commands, linked
PRD/ADR/BRD and existing tests. C1 confirms both legacy and composed paths
still impose 8 C and 15..98% independently of outdoor records. C2 confirms the
writer already passes paired outdoor rows to both paths; no second source or
stock generation is needed. Reflection: share the bound calculation, not the
input-validation/household policy, and preserve the existing ingestion policy.

### Cycle 1: Deeper

C3 establishes the approved public, hash-pinned 17,544-hour Durham ERA5 pack.
It is safe for offline regression; no network or private dataset is necessary.
C4 shows explicit composed setpoint, ventilation and dated loss inputs.
Independent temperature bounds can be derived from the noiseless equation
per outdoor row and dwelling, with an explicit bounded exercise-noise margin.
RH follows outdoor vapour plus model moisture divided by saturation at the
derived temperature range, with physical 0..100% saturation limits.
Reflection: bound Gaussian residuals, not outdoor records; preserve two RNG
draws in their original order. Test whole paired records and forced tail draws.

### Cycle 1: Contrarian

Checked the supported outdoor endpoints (-80..60 C), maximum dwelling/age/
construction loss, composed setpoint/moisture/ventilation endpoints, explicit
retrofit multiplier and the old fixed-bound/equality tests (C1, C4, C5).
Unbounded Gaussian noise prevents a deterministic finite envelope, so merely
replacing fixed temperature/RH clips with new constants is rejected.
No calibration data exists: a model-consistent envelope is not a verified
healthy-home, design-weather or risk threshold. RH at saturation may reach
100%; preserving 98% would reintroduce the defect. Fault packets intentionally
leave nominal envelopes and must not be used as evidence of nominal failure.
Reflection: keep physical saturation, label the 3-sigma tail policy exercise,
version both models, and distinguish nominal from injected-fault output.

### Parent Synthesis and Disposition

Accept a per-record causal envelope: deterministic indoor temperature baseline
+/- three temperature-noise standard deviations; humidity bounds derived from
outdoor vapour and model moisture at those temperature endpoints +/- three RH
noise standard deviations, intersected with 0..100%. Clamp the two Gaussian
draws through that envelope. Reject fixed exercise output clips, global
outdoor min/max alone (ignores pairing/schedule), and scientific calibration
claims. Defer real building-physics validation and OD-43 activation decisions.
One completed cycle covers the bounded scope; another cycle would repeat the
same model/caller evidence rather than resolve calibration outside scope.

## Evidence Log

| ID | Finding | Workspace-relative source |
| --- | --- | --- |
| C1 | Two versioned projection functions and fixed floor/clips | `src/core/src/zava_forward/core/synthetic/indoor_projection.py:10`, `:115`, `:159` |
| C2 | Writer passes outdoor pairs unchanged before explicit faults | `src/core/src/zava_forward/core/synthetic/sensor_backfill.py:100`, `:118`, `:331`, `:365` |
| C3 | Public paired hourly source, pinned raw/metadata hashes and exact subsampling tests | `src/core/tests/test_climate_history.py:16`, `:59`; `src/core/src/zava_forward/core/synthetic/climate_history.py:290`; `docs/reference/research/iot-sensor-analytics-research-plan.md:311` |
| C4 | Household domains and effective dated loss reach composed projection | `src/core/src/zava_forward/core/synthetic/indoor_projection.py:148`; `src/core/src/zava_forward/core/synthetic/household_conditions.py:43` |
| C5 | Existing reference equation, provenance and exercise plausibility regressions | `src/core/tests/test_indoor_projection.py:16`; `src/core/tests/test_sensor_plausibility.py:68` |
| C6 | PRD live ingestion/analysis criteria differ from this indoor model story; OD-43 does not block synthetic exercise | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:2162`; `docs/adrs/0002-pilot-readiness-architecture.md:825`; `docs/brds/agentic-retrofit-programme-brd.md:2161` |
| C7 | Existing docs explicitly state the unmet criterion and unchanged default bytes | `src/core/README.md:2147`, `:2293` |

No external sources newly fetched; committed public climate evidence is used
only under the existing synthetic-demo source approval. No new legal claim.

## Findings, Alternatives and Current Decisions

Q1 answered by C1--C4: the existing writer already carries all necessary
inputs. Q2 answered by the algebra and endpoint review above (C1/C4/C5).
Q3 answered by C5--C7: add forced-tail, parameter/domain sensitivity,
paired-history, RNG/determinism/provenance tests and a per-criterion audit.
The existing baseline passed four projection tests after isolated editable
package installation; the initial uninstalled command failed explicitly.

No owner/Legal/DPO decision is needed for this exercise-only change. Actual
calibration, operational monitoring and whole PRD acceptance remain unavailable.
All #179 criteria must be assessed after implementation; none is newly ticked
by this research.

## Planning Readiness

Ready. Research disposition: executed, complete. Handoff: implement the
per-record shared envelope and v2 parameters, preserve validation/RNG order,
prove nominal outputs on the pinned public history, and document limitations.
Self-check: all questions mapped to C1--C7, all three waves completed inline,
alternatives and residual uncertainty explicit; no source files edited.

## Correction cycle 1 intake (2026-10-27, PR #502)

Focused, parent-authorized ordered Research/Plan/Implement/Review continuation.
Investigate the hosted historical sensor SHA-256 regression before choosing
compatibility gating or an intentional versioned golden update. Append evidence
to the existing dated artifacts; preserve their original outcomes. Starting
sources: issue #179 and PR #502, determinism tests, projection/writer versions,
snapshot documentation and the exact `src-core` CI commands. No external
research, private data, cloud, heavy gate, secret reads or workflow changes.
Repository instructions and RPI phase skills apply; UI skills are inapplicable.
Inline investigation is appropriate for this single tightly coupled trace.
No new acceptance checkbox or historical golden changes without proof.

### Correction cycle 1: Wider

C8: `src/core/tests/test_synthetic_determinism.py:94` pins the old sensor
reading digest independently of the model version. Hosted run 40577511316
ran 1,435 tests, one failure and 186 skips; its exact mismatch is reproduced
locally on Python 3.12.3 after installing missing core/dev dependencies with
pip. Old digest: `657ff373107807b34bd4bb6720dec534fcef13134292c5d753ef24bdbd723549`;
current: `25bb5259d89554560e179ae5412f3148595c47a87def9ee2fca61518e18ded5b`.
Reflection: the first delivery omitted this canonical regression from its
selected tests; the original green targeted result did not prove full core CI.

### Correction cycle 1: Deeper

C9: `docs/reference/research/retrofit-synthetic-data/README.md:157` documents
row-changing refreshes bumping the pack version, exact replay requiring the
same revision/runtime/parameters, and writing a new destination rather than
overwriting published records. `src/core/README.md:2197` and the existing PR
already explicitly intend changed v2 values. Model versions are v2, but
`sensor_backfill.py:33`, `:344`, `:355`, `:364` still use the old snapshot
versions in default, stock, fault and composed modes. Read/replay and privacy
classification use those version identifiers (`sensor_backfill.py:464`,
`:518`; `privacy.py:228`, `:256`). Reflection: an unqualified hash replacement
is insufficient; pack version bumps must reach writers, readers and privacy.

### Correction cycle 1: Contrarian

Considered gating the old default at v1. This would preserve its SHA, but
would intentionally retain fixed 8 C / 15..98% clips for one supported path,
contradicting #179's requested correction and the already documented v2
decision (C1, C7, C9). No source requires a changed generator revision to emit
old values. Rejected changing RNG order, weakening bounds tests, overwriting
published outputs, or bumping unchanged fault/schema/stock-fabric algorithms.
Snapshot versions and model versions are distinct; fault packet mechanics
can stay v1 while their containing generated snapshot advances.

### Correction cycle 1 synthesis and readiness

Research disposition executed; Planning Readiness Ready. Intentional v2 model
change is legitimate for new snapshots; historical published bytes remain
immutable and require their original revision for replay. Follow the documented
version convention: default snapshot v3, stock snapshot v2, integrated snapshot
v2, and a distinct fault-snapshot v2 with fault-packet algorithm still v1.
Pin the new default golden with literal snapshot/model version assertions,
preserve unchanged scale/register digests and record the old digest here and
in the changes artifact. Prove the cause using the independent old equations
and exact seeded reference, then run all three core CI commands unchanged.
No new operational approval or dataset refresh is requested. One inline
three-wave cycle suffices; no unresolved owner/Legal/DPO decision.
Upstream contains only rubric-bot commit a06c2063 beyond local HEAD; retain it
by fast-forwarding before publication, without rewriting history.
