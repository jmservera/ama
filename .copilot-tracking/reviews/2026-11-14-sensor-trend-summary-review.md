# Review: 7-day sensor trend summary (Refs #1288, Refs #111)

Date: 2026-11-14. Review execution: executed once, self-review of the working diff. Outcome: conformant for the stated scope; no material findings open.

Reviewed: [changes](../changes/2026-11-14-sensor-trend-summary-changes.md), [plan](../plans/2026-11-14-sensor-trend-summary-plan.md).

## Checks

* Advisory provenance: `trend.advisory_only` and `provenance.advisory_only` are true, `affects_stage_gates` false, uncalibrated. Pass.
* No gate mutation: read-only SELECTs; trend absent from `capture_source`, so snapshot digest, signature and model request are unchanged. Pass (test and existing Quality sensor suites).
* Bounds: at most 24 rows per request, 7-day window, one sensor. Pass.
* Fail-closed: consent withheld, unavailable, no readings, few readings, short span and unusable values give `insufficient`, never zero or steady. Pass.
* Validation: new tests 10 OK; ruff check, ruff format --check and mypy clean in `src/core` and `src/api`; related core and API sensor suites OK.

## Routed follow-ups (later, user-selected)

* Render the trend in the employee Quality/case UI (not requested here).
* Advisory thresholds (0.5 degC, 2 %RH) are engineering defaults; operational thresholds need owner approval (#111).
* Hosted CI, independent exact-head review and live walkthrough (#1288 criteria) remain unproved. Not pushed.

Tier: focused (non-gate read-model change); full local gate not run.
