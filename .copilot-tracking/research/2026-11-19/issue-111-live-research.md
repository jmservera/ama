# Issue 111 live research (2026-11-19)

Task: issue-111-live. Disposition: executed. Planning Readiness: Ready.

* Issue #111 has three criteria; the first two are ticked. The only unmet one is "R1 to R3 complete before a derived measure is used beyond an exercise rule".
* Plan R2 (docs/reference/research/iot-sensor-analytics-research-plan.md line 730) requires sign-off by a competent building-physics reviewer and Asset; R3 limits need agreed false-alert and miss limits. These are human approvals.
* Code gate already exists: `AnalysisPolicy.validate` raises RESEARCH_GATE_REQUIRED for a SOURCED threshold without a `ResearchGate`; review tasks need a named `RuleApproval`.
* Existing test run: src/core test_sensor_analysis, 46 tests OK (11 skipped, 1 expected failure).
* Owner waivers (2026-11-18) cover billing, DPO/Legal and assistive-technology testing, not R2 reviewer sign-off.
