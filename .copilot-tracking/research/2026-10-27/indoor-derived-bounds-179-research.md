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
