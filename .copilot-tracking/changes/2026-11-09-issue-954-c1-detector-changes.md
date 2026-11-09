# Changes: issue 954 C1 checker detector correction (2026-11-09)

Implement phase after the prospective commit `88371a5e8` (research, plan, details, critique committed before the checker edit; parent `e9fbcaf05`, tree `8431f506`).

## Chronology

The original lane's disclosed scratch-before-plan ordering and every earlier failure (lock-busy attempts, interrupted retry loop, the 503 detector failure) are unchanged. C1 is a new prospective cycle and does not repair that ordering.

## Changes

* `src/api/checks/photo_flag_stale_browser_check.py` only (git blob `ab8fadcca0a12365d5ad5cf8fcd26ed1730029e3`): the detector now evaluates rendering (CSS, `hidden`, box), flags visible severe overlays even when empty, flags ordinary `role=alert` only with meaningful content, sweeps all candidates on every mutation and every 50 ms, records outerHTML at hit time, and receipts ignored alerts (`ignored_empty_alerts`). Added an in-checker detector self-test (13 cases) run in the same browser launch.
* No product, API or web asset change. Console recording and native-diagnostic classification are unchanged and unfiltered; page-error and native dialog assertions are unchanged.
* Budget: one C1 cycle spent after the source edit; four of five remain; no reset or extra grant.

## Validation (DEMO targeted tier; worktree-first PYTHONPATH)

* ruff 0.17.1 (pinned in `src/api/pyproject.toml`, installed in an owned scratch venv): check and format check pass.
* One nonqueued holder check/admission at 2026-11-09T16:18:01Z (`flock -n /tmp/ama-rpi-heavy.lock`, lock free): exit 0. Self-test 13 of 13 pass, 503 and 403 each pass every behavioural assertion and quiet classification. Receipt: 503 and 403 each 2 native `Failed to load resource` diagnostics, 2 console events, no page errors, no dialogs, no disruptive nodes, the empty `#account-error` receipted as ignored (`not-rendered`), `quiet_per_owner_definition` true, `literal_no_console_event` false (informational).
* `test_photo_availability`: 1 test, exit 0. Core `test_scenario_manifest` plus `test_needs_inventory`: 19 tests (8 plus 11), exit 0.
* Raw outputs, exits and SHA-256 manifest: session files `evidence-954-c1/` (outside the repo).

## Skipped

SQL, cloud, live, model, credentials, full or `--changed` gate, repeated browser campaign. Hosted CI and independent exact-head review are pending.
