# Issue 188 plan: self-contained handover demo (2026-11-03)

Details: [details](../details/2026-11-03-issue-188-demo-self-contained-details.md)

## Stacked slices

* Slice 1 (this PR): demo finds its fixtures; shorter documented command. [x]
* Slice 2 (owner-gated): Azure SQL verifier run after a live Hub stream (#110, #140, #184).
* Slice 3 (blocked): real pinned climate in the demo once the climate source blocker clears.

## Critique (single pass, self)

Verdict: proceed. Alternative of moving fixtures into the package was rejected as larger, riskier and not criterion-advancing. Path bootstrap is limited to the checks script; tests are unchanged.

## Validation (focused)

* Demo run with package paths only (pass and seam failure exit codes).
* `test_sensor_handover_demo` and `test_sensor_consistency`, ruff, mypy with `--cache-dir=/tmp/mypy-188`.
* Gate, benchmarks and full suites not run.
