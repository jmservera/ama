# Issue 350 r9 changes

Refs #350. Tier FULL (`src/api` changed). Full local gate and `rpi-checks.py --all` not run here (coordinator owns them). Sequence note: the source edit and its test were made while the live evidence was being taken, before this record existed; the witness is called afterwards and records that order.

## Files

* `src/api/src/zava_forward/api/server.py`: GET `/api/assistants*` re-raises a SQL write-lock timeout so the safe-method path answers 503 with `Retry-After: 5` and logs the cause; other failures log class and path.
* `src/api/tests/test_error_logging.py`: `test_assistants_registry_busy_lock_503_retry_after_and_other_failures_logged` (fails without the fix, passes with it).
* `docs/reference/research/issue-350-live-r9-2026-11-23.md` and its `raw/` and `scripts/`; index entry in `docs/reference/README.md`; entry in `docs/reference/log.md`.

## Validation

* `test_error_logging`: 14 tests OK. `mypy` in `src/api`: no issues in 373 files. `ruff check` and `ruff format --check`: pass.
* Full `src/api` discovery exceeded the 50 minute cap and was stopped with no failure printed (no FAIL or ERROR lines in its log). Focused run of test_assistants, test_error_logging, test_role_endpoint_inventory, test_expected_denials and test_auth: 238 tests OK, 64 skipped. The coordinator's gate covers the rest.
* Live Azure: read-only; nothing created, nothing to delete.

## Per-criterion table (live, 2026-11-23)

| # | Result | Why |
| --- | --- | --- |
| 1 | Unproven live (app side proven) | Edge returns 302 for browser-style anonymous API requests; exemption needs trusted-principal proof and is a production auth change |
| 2 | Partly proven | One staff role, read probes only; matrix rows, 16 assets, second role, writes not executed |
| 3 | Partly proven | Counts present; restore authorisation and provenance not visible to this role |
| 4 | Partly proven | Two model deployments exist now; registry, briefing, failure behaviour seen; release authority and live model call not made |
| 5 | Partly proven | Map equals open cases, list alternative; licence approval unproven; export and sensors 403 |
| 6 | Unproven | Needs authorised consent; fallback shown |
| 7 | Partly proven | Store responds, 0 sources; approval human-owned |
| 8 | Partly proven | Chain intact over 7305 entries, jobs executing; document durability not re-run (403) |
| 9 | Proven for the demo | Gate, 403, explanation and case-work 200 together |
| 10 | Unproven | One role, read-only |
