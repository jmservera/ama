# Research: staff time capture gated on DPIA (#120)

Disposition: executed. Planning Readiness: Ready.

* Existing `mvp/zavaforward_mvp/timecapture.py`: flag, `DPIA_APPROVED`, `ZF_TIME_CONSULTATION`, per-person notice acknowledgement (audited), min-group suppression in `report()` (floor 2, default 5).
* Gaps against #120 criteria: notice approval not recorded; enabling was env-only with no audited admin action; no screens.
* Constraints: ADR 0005 synthetic only; OD-36 DPIA and approvals are owner decisions, so no real references are invented (tests use labelled fixtures).
