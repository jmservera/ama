# Research: issue 109 first unmet DEMO criterion (2026-11-19)

Refs #109. Mode: automatic. Tier: FULL only if src changes (core change here; targeted tests only, no rpi-checks --all, per coordinator brief).

## Criterion inventory (origin main 05e94d303)

| Criterion | State | Finding |
| --- | --- | --- |
| #109 #440 stabilization checkpoint | Unmet | #440 is open with two unticked criteria (triage, review artifacts); owner/process outcome, not code. |
| #109 all children closed or deferred | Unmet | #111 open (one criterion), #184 and #1818 open per 2026-11-18 evidence. |
| #109 no sensor signal diagnoses... | Ticked | Existing code and tests. |
| #111 R1-R3 complete before a derived measure is used beyond an exercise rule | Unticked, code-addressable | `AnalysisPolicy.validate` accepts any `SOURCED:` label with no R1-R3 evidence. |

## Selected criterion

#111 child criterion 3. Gap: `sensor_analysis.AnalysisPolicy` lets a policy claim `SOURCED:` thresholds (beyond exercise rule) with no R1-R3 record. R1-R3 themselves remain open (R2 reviewer sign-off and agreed R3 limits, see iot-sensor-analytics-research-plan.md); the code guard enforces the "before" ordering and cannot declare them complete.

## Planning Readiness: Ready. Research disposition: executed (code inspection).
