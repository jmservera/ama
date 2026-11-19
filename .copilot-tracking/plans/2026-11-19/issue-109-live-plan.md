# Plan: issue 109 live (2026-11-19)

* [x] 1. Add `ResearchGate` (R1 source review, R2 reviewer sign-off, R3 synthetic validation references) and optional `AnalysisPolicy.research_gate` in `src/core/.../sensor_analysis.py`.
* [x] 2. `AnalysisPolicy.validate` raises `RESEARCH_GATE_REQUIRED` for a `SOURCED:` label without a gate; exercise labels unchanged.
* [x] 3. Include the gate in `policy_digest` only when present so existing digests stay stable.
* [x] 4. Targeted tests in `src/core/tests/test_sensor_analysis.py`; mypy and ruff format on src/core.

Details: .copilot-tracking/details/2026-11-19/issue-109-live-details.md
Critique: .copilot-tracking/plans/2026-11-19/issue-109-live-critique.md
