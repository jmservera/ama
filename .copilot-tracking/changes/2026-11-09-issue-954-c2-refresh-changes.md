# Changes: issue 954 C2 non-vacuous false-refresh proof (2026-11-09)

Implement phase after prospective commit `40f21e542` (research, plan, details, critique and the dated original-review qualification committed before the checker edit; parent `3a1629c08`).

## Changes

* `src/api/checks/photo_flag_stale_browser_check.py` only (git blob `520e711c41d39395a0324f9c59614ca4d60f1417`, SHA-256 before `1159ab1d...b7ce`, after and executed `3e89042d...a42a`, identical).
  * `refresh()` now waits for the `me.services` object to be replaced (identity sentinel) rather than the status text.
  * New `false_refresh_proof()`: establishes and asserts client `me.services.photo` true with no extra photo request, refreshes with a served false, then asserts the ACTUAL client flag false and the inline unavailable status, then no further photo request. The served-sequence, no-additional-request, true-refresh and time-origin checks are retained.
  * Deterministic negative control `false_refresh_negative_control()`: the route records the served false but omits `services.photo` from the body the client receives; the proof must fail at the client-flag assertion (it did: its `FAIL` line in the output is the expected control, followed by `PASS negative control`). The corrected real 503 and 403 runs pass through the same helper.
* No product, API or web asset change. Actual 503/403 quiet receipts, detector self-test (13 cases) and the owner definition of quiet are unchanged.
* Original review qualified by a dated appended section (original text unchanged).
* Budget: C2 spent; three of five remain; no reset or extra grant.

## Validation (DEMO focused tier; worktree-first PYTHONPATH)

* Ruff 0.17.1 (existing pinned venv `/home/azureuser/.venvs/zf123-pinned`, read only; no install): check pass, format check pass.
* Holder check 2026-11-09T16:28:30Z (`fuser`): no holder reported. One nonqueued `flock -n /tmp/ama-rpi-heavy.lock` admission: exit 0, 83 PASS lines (13 detector self-test, negative control, 503 and 403 behavioural and quiet assertions), 1 expected control FAIL line. Both 503 and 403 receipts: 2 native `Failed to load resource` diagnostics, no page errors, no dialogs, no disruptive nodes, one ignored empty alert, `quiet_per_owner_definition` true, `literal_no_console_event` false (informational).
* `test_photo_availability`: 1 test OK. Core `test_scenario_manifest` plus `test_needs_inventory`: 19 tests OK (exit 0 each).
* Raw commands, outputs, exits, versions and manifest: session files `evidence-954-c2/` (outside the repo; C1 and original evidence retained).
* Web design guidelines: the change is a test checker, not a web UI file; no UI source changed, so no guideline refresh was applied. Declared, not claimed.

## Skipped

SQL, cloud, live, model, credentials, full or `--changed` gate, repeated browser campaign. Hosted CI and independent exact-head review are pending.
