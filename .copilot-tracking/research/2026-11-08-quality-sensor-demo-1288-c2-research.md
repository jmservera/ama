# Research: #1288 correction 2 (C2)

Written 2026-11-08T20:19Z, before any C2 product or test edit. Session 7442ea61 resumed.
Start head 7d2dcc0891bb6d49e739f33e96473381c6be06f1, tree 025bf08b05db6b3c541f399747a5f3c74bdabefd, tracked clean. Fetched origin/main 6354b13f; this branch keeps its c50 merge ancestry and is not rebased or merged here (coordinator merges after #184 lands).
Preserved unchanged: original and C1 research/plan/details/changes/reviews, the original and C1 state files. C1 chronology is uncertain per the independent reviewer (its files may be post hoc); C2 does not rewrite it.

Evidence read: the complete independent findings JSON (4 High, 1 Medium), sensor_view.py, assistants.py (signature, eligible, review_flag, snapshot, _enqueue, claim, complete, _view, _withhold_sensors, _scrub_events, export, scan, forecast, review), sensor_consumer.py (_schema, configure, home_consent), index.html.

## Findings and root causes

1. Same-bucket reuse. `assistants.signature` replaces the sensor source by a coarse six-hour value and drops `sensor:` and `source:sensors` citations. The same value is task id, staleness test and scheduling key, so a new reading or context row in the bucket reuses an older immutable snapshot and the proposal stays non-stale beside a different visible latest. Fix: identity and staleness use the exact capture (clock-free, includes IDs, values, context, composite citations). The coarse value becomes a separate scheduling key stored in the existing `signature` column, used only by scan and forecast, so proactive cost stays rate limited. Manual invocation always captures exact evidence.
2. Withheld leak. `_withhold_sensors` blanks output only when a finding cites `sensor:`, and `_scrub_events` checks only `output`, so uncited text and `edited_output` can carry withdrawn values. Fix: when the stored capture held values and consent is not granted now, replace the whole output and every output-bearing event field (`output`, `edited_output`) with the withheld stub, on detail, list, export and raw JSON.
3. Manual relabelled autonomous. `review_flag` looks for any proactive invocation in history. Fix: at claim, record `dispatch={trigger, fence}` on the task and in the claimed event from the invocation events that existed at that moment (any person request makes it `requested`); the returned output keeps that attribution; later invocations never change it. Legacy tasks without a dispatch record are treated as not proactive.
4. Sampled-sensor consent. `_controls` looks only at sensors named by selected rows plus two guessed IDs. The authoritative `home_consent` gives any declined control for the home precedence but scans the fleet. Fix: a small indexed table `sensor_consumer_control_home (home_id, sensor_id)` maintained by `configure` and backfilled once when created, read by `sensor_view.consent` with a bounded fetch, decline precedence, and fail closed (unknown) when a named sensor's control is not indexed, an indexed control is missing, or the table is absent.
5. Future and unbounded time. Newest and context queries have no as-of bound, so a future-dated row can win latest and be called fresh. Fix: capture takes the store clock as an as-of filter only (the capture records no clock), excludes rows after as-of, records a stable `future_dated_excluded` flag, and applies finite horizons (window lookback 366 days; anchor context 30 days each side, both capped at as-of). `view` also never reports negative age as fresh. Model rules text states readings are bounded by request time and no current freshness is asserted.

Accessibility: the whole-page axe `label-content-name-mismatch` is on `summary[aria-label="Your account"]` in index.html:25. Cause to confirm in the plan phase from the visible summary text; smallest fix is an accessible name that contains the visible text.

## Constraints and risks

* SQLite and Chromium runs are light; actual SQL, Docker and browser checks are PENDING until a separate coordinator admission (#184 has first access to `/tmp/ama-rpi-heavy.lock`). Nothing here may be reported as passed until it runs.
* #184 also edits `sensor_consumer.py`; the C2 touch there is only the new table in `_schema` and `configure`. Not stacked; semantic integration is a later merge task.
* The rules/registry hash changes again; no release, attestation, allowance or live Quality activation is granted.
* Human notes are human-authored, not model-derived, and are not stubbed.

Planning Readiness: Ready.
