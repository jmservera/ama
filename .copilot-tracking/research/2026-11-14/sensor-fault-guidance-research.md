# Research: sensor fault guidance (Refs #111)

* Disposition: executed. Planning Readiness: Ready.
* Evidence: `sensor_view.py` had freshness only (fresh/stale/unknown); `api/sensor_badges.py` (#1650) added Offline/Stale/Unavailable badges but no fault or out-of-range state and no operator next action; consent-withheld shared the Unavailable badge.
* Issue #111 criteria are not proven by this slice; it is demo UI guidance only, not an operational rule.
* Physical limits (0-100 %RH, -40 to 60 degC) are labelled exercise plausibility values, not a sourced standard.
