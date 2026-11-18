# Changes: issue 1288 live verification (2026-11-18)

Refs #1288. Docs and evidence only; no `src/` edit. Tier FOCUSED (no source, SQL schema, infra or deployment change; the throwaway SQL container was local only). `rpi-checks.py --all` not run.

## Files

* `docs/reference/research/issue-1288-live-quality-sensor-evidence-2026-11-18.md` (new research note).
* `docs/reference/README.md` (index entry), `docs/reference/log.md` (appended entry).
* `.copilot-tracking/evidence/2026-11-18/issue-1288-live/` (live probe script and JSON, two screenshots, focused test, browser check and SQL outputs including adverse runs).
* Phase artifacts under `.copilot-tracking/` (research, plan, details, critique, changes, review, state).

## Per-criterion table (criteria 1, 2 and 9 already ticked, not reopened)

| # | Criterion | Proven? | Basis |
| --- | --- | --- | --- |
| 3 | Quality AI snapshot uses UI reading IDs and values | Proven locally only (mock provider); unproven live | Browser check 33 passed; focused tests 497 OK |
| 4 | Release-admitted proactive durable bounded flag | Unproven for the demo | No approved release record (OQ-017); live invoke `release: null`, no call. Local dedup/bounds proven |
| 5 | Visible finding, cited IDs, source time, model, unapproved status | Proven locally only; unproven live | Browser check attributed unapproved flag |
| 6 | Explicit missing/stale/unavailable states and human route | Proven locally; stale and unavailable observed live | Live `/sensors` stale; live invoke disabled with manual route |
| 7 | Focused SQL/API/browser correlation tests | Proven as local engineering evidence | 497 OK (179 skipped), browser 33 passed, SQL Server 2022 classes run with one harness-hygiene failure (note 1) |
| 8 | Finite live walkthrough with actual model | Unproven, cannot be proven for the demo | No simulator job, no release record, no model authority |

## Validation

* `python3 -m unittest <seven quality sensor modules>` from `src/api`: OK, 497 tests, 179 skipped.
* `python3 -m checks.quality_sensors_browser_check` from a short directory: exit 0, 33 checks.
* SQL Server 2022 local container: `MssqlReadModel` and `MssqlHttp` 93 of 94 pass (inherited memory canary test fails on a reused database, passes on a fresh one); first run had login errors (preserved).
* mypy, ruff and web tests not applicable: no source or web file changed.
* Container `ama1288-mssql` removed. No Azure resource created. Live probe wrote one denial proposal.

## Unmet

Criteria 3 to 8 stay unticked. Hosted CI and independent exact-head review outstanding.
