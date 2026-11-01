# Issue 167 research: generator coverage baseline and gap closure

* Date: 2026-11-01
* Task: issue-167-generator-coverage-baseline (branch feat/generator-coverage-baseline)
* Research disposition: executed
* Planning Readiness: Ready

## Findings

* Criterion 1 (each need has a child story or deferral): proven by needs-inventory v1.2.0 and
  `zava_forward.core.synthetic.coverage` (route shape only, 13 needs: 2 covered, 11 partial, 0 missing).
  Ticked on the issue.
* Criterion 2 (reuse seed, identifier, is_synthetic conventions): open. The README (retrofit-synthetic-data,
  gap closure section) says per-record `is_synthetic` is proven for the scale fixture (v1.3.0) but not for the
  SN-01 stock register or other child outputs; `generator_output_conformance` is reported `not-assessed`.
* The committed register header has an `is_synthetic` column; no tool checks it per row.
* Owner confirmation of the mapping and deferrals cannot be supplied by an agent; it stays an open item.

## Smallest deliverable slice

Add a read-only, per-row `is_synthetic` conformance check for any explicitly supplied CSV register to the
existing coverage tool (no second generator, no dataset reads by default). Tests use wholly fictional rows.
Aggregate counts only may be recorded from a local run on the register.

## Constraints

* Source in `src/core`, tests outside the package, no mvp/ or prototype/ code, pip only, no secrets.
* Closing keyword only if every criterion is proven: owner confirmation is missing, so use `Refs #167`.
