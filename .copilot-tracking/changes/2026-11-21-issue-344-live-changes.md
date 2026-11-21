# Changes: issue 344 live (2026-11-21)

Tier: FULL (src change); local commit only; `rpi-checks.py --all` not run. The implement-start witness noted the source was already dirty: the one-line edit landed in the same tool batch as the witness call.

## Files

* src/core/src/zava_forward/core/workflows.py: `unaccepted_handoffs` skips a handoff that `handoff_ageing` cannot age (naive or missing offered_at) instead of failing with 500.
* src/core/tests/test_handoff_escalation_83.py: regression test (JSON and SQL stores); 2 errors without the fix, passes with it.
* docs/reference/research/public-browser-access-live-r8-2026-11-21.md, docs/reference/README.md, docs/reference/log.md: evidence note, index, log.
* .copilot-tracking/evidence/2026-11-21/issue-344-live/: probe script and outputs (no credentials).

## Validation

* `src/core`: test_handoff_escalation_83, test_handoff_lifecycle, test_exception_feeds: 44 OK. ruff check clean. mypy: 3 errors, none in the changed files (missing opentelemetry stubs in telemetry.py; unused ignore in synthetic/device_provision.py); pre-existing and environmental.
* Hosted CI for the exact head: not observed (nothing pushed).
* Not run: api suite (no api file changed), full gate.

## Per-criterion table

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Landing, Entra sign-in, anonymous API 401 not redirect | Partly proven | Landing, sign-in, curl 401 proven; browser fetch redirects; needs owner Return401 infra decision |
| 2 | Edge follows #143 | Proven (already ticked) | External Container Apps environment |
| 3 | /healthz public; anonymous API 401 | Proven | curl 200 and 401 on 2026-11-21 |
| 4 | SQL private, public Disabled, no bypass | Proven | Disabled, 0 firewall rules, 0 policy assignments |
| 5 | Parity with matrix | Unproven | 33 of 36 swept paths 200; 3 Blocked matrix rows; handoff 500 fixed locally, not deployed; no full walk-through |
| 6 | Browser sign-in smoke | Proven (already ticked) | Playwright sign-in reached /app |
