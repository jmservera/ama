<!-- markdownlint-disable-file -->
# Historical climate source: issue 178

## Research brief

Compare candidate historical outdoor climate sources for North East England,
record the owner-directed source choice and licence gate, and derive bounds
only from retrieved observations. Audience: synthetic-data maintainers and the
exercise owner. Output mode: audit. Posture: focused, selected from the bounded
issue and explicit offline-only instruction.

## Scope, controls and extensions

Code, if needed, is limited to src/ and infra/. No Azure, remote climate
retrieval, private datasets, legacy trees, environment files, or Entra script
edits. GitHub issue inspection and requested PR publication are authorized.
Repository instructions, ADR 0006 and rpi-research selected. No specialist
delegation: the evidence fits direct reading. No legal approval inferred.
No interaction is available; missing records cannot be invented.

## Questions and evidence

* C1: Issue 178 and its owner comment, read through `gh issue view 178
  --comments` on 2026-10-16: choose Met Office (UKCP18) and Environment
  Agency open data under OGL where available; otherwise labelled synthetic
  data. Licence and retrieval dates are required per dataset.
* C2: `src/core/src/zava_forward/core/synthetic/sensor_backfill.py:6`:
  external climate data have not been retrieved; the source is synthetic.
* C3: `src/core/tests/test_sensor_plausibility.py:3`: outdoor ranges are
  exercise values, not retrieved observations.
* C4: `docs/reference/research/iot-sensor-analytics-research-plan.md:15`:
  sensor methods and operational thresholds remain review-only/open.
* C5: `docs/adrs/0006-src-layout-and-cutover.md:45`: all new executable
  work belongs under src/.

No W evidence IDs: no external climate or licence page was retrieved.

## Cycle 1

### Wider

Read issue, owner comment, source research plan, source generator and existing
plausibility tests. Candidate list includes HadUK-Grid, MIDAS Open, historic
stations, ERA5, CIBSE and the owner's UKCP18/Environment Agency direction.

### Deeper

The only available outdoor series is a deterministic constructed model.
Neither an observation archive nor a dataset-specific licence is identified
by the current evidence. Source choice and completed retrieval must be
separate states; no observed bounds can honestly be calculated.

### Contrarian

A candidate name, provider homepage or OGL assumption is not dataset-level
reuse evidence. A future projection cannot silently substitute for historical
observations. Synthetic fixture extrema cannot establish North East climate
bounds. Building a new importer would not close missing retrieval or approval
and would widen this source-selection issue unnecessarily.

## Parent synthesis and dispositions

Accepted: retain the owner-directed synthetic fallback, record candidate
evaluation gaps and exact evidence needed in the existing research synthesis.
Rejected: fabricated retrieval dates, licence confirmation, climate figures,
and relabelling exercise limits as sourced values.
Deferred: verified historical source comparison, dataset selection and measured
bounds until approved records and licence evidence are supplied locally or
remote retrieval is authorized. No runtime changes are appropriate.

## Readiness and disposition

Research disposition: executed. Planning Readiness: Ready for the bounded
offline documentation/evidence audit; blocked for full issue acceptance.
One complete cycle suffices within the offline boundary: no additional local
source can resolve the missing external records.

## Self-check and handoff

C1-C5 support the audit, not external climate claims. No unverified source is
treated as retrieved. Plan must preserve every unmet criterion explicitly,
update the index and append the log, and keep issue checkboxes unchanged.
