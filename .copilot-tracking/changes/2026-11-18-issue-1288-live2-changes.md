# Changes: issue 1288 live run 2 (2026-11-18)

Refs #1288. Docs and evidence only; no `src/` edit. Tier FOCUSED.

## Files

* `docs/reference/research/issue-1288-live-r2-quality-sensor-evidence-2026-11-18.md` (new note with per-criterion table).
* `docs/reference/README.md`, `docs/reference/log.md`.
* `.copilot-tracking/evidence/2026-11-18/issue-1288-live2/` (probe script, `live_probe.json`, `run.txt`, two screenshots).
* Phase artifacts and state under `.copilot-tracking/`.

## Per-criterion table (criteria 1, 2, 9 ticked; not reopened)

| # | Criterion | Proven? | Basis |
| --- | --- | --- | --- |
| 3 | Quality AI snapshot uses UI reading IDs and values | Local only (mock provider); live unproven | PR 1971 browser check and tests; live release null |
| 4 | Release-admitted proactive durable bounded flag | Unproven | Live `proactive: false`, `call_allowance: 0`, no approved release (OQ-017) |
| 5 | Visible finding, cited IDs, source time, model, unapproved status | Local only; live unproven | PR 1971 browser check |
| 6 | Explicit missing, stale, unavailable states with human route | Proven locally; unavailable observed live again (stale seen in run 1, fresh now) | live_probe.json invoke and sensors |
| 7 | Focused SQL, API, browser correlation tests | Proven as local engineering evidence (PR 1971; not re-run, no source change) | PR 1971 outputs |
| 8 | Finite live walkthrough with actual model | Unproven, cannot be proven for the demo | No admitted #1288 run, no release record, no model call |

## Validation

* Live read-only probe via Playwright Chromium at 13:08Z (credentials read at run time, not printed). Local suites not re-run: no source change.
* Adverse/unintended: probe wrote a second retained denial proposal (metric invocation 6 to 7), a persistent synthetic record on the demo that was not removed; research-open witness was recorded after the probe ran, not before; screenshots do not show the sensor panel.
* mypy, ruff, web tests not applicable. No Azure resource created or modified.

## Unmet

Criteria 3 to 8 stay unticked. Hosted CI and independent exact-head review outstanding.
