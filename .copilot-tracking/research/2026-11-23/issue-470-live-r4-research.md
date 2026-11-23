# Research, issue 470 live r4 (2026-11-23)

Opening: only criterion 4 is unticked ("Measured full-run time before and after is recorded in the PR"). Criteria 1, 2, 3 and 5 stay ticked; 129 gate tests passed in r3.

Findings:

* Measurement needs two matched `--all` runs per arm and a PR; `--all` and publication are forbidden here, so the measurement itself cannot be proven for the demo.
* The comparison tool `tools/rpi-gate-timing.py compare` exists and refuses non-comparable arms, but emits JSON only. Recording the result in a PR needs a hand-built table, which is a tooling gap.
* Buildable slice: a `--markdown` option on `compare` that renders a PR-ready table (spans, medians, delta, per-group medians) and refuses to render anything for a NONCOMPARABLE verdict beyond its reasons.

Planning Readiness: Ready. Research disposition: executed.
