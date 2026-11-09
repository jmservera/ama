# Changes: issue 954 C3 strict mypy on the photo-flag checker (2026-11-09)

Plan `.copilot-tracking/plans/2026-11-09-issue-954-c3-types-plan.md`. Refs #954 only. Prospective commit `efb236103` precedes the merge, validation and the source edit. Merge `2d9c14952` (ordinary `--no-ff`, no conflicts) integrated `origin/main` `3a9767d5cf728c5e3be76813ce0bfdac4c06841e` (after PR 1240). The shared remote ref has since advanced (`700bf11e188a9fce05177385019b3d10ba5bb92f` observed locally); it was not merged here.

## Source change (one file, +17/-5): `src/api/checks/photo_flag_stale_browser_check.py`

* Typed module aliases `principal_header`, `make_provider`, `make_app` (`Callable`, `Mapping`) for the untyped `test_auth.principal`, `TrustedProxyProvider` and `App`; call sites use them.
* Named typed callback `on_dialog(dialog: Dialog) -> None` (append message, then dismiss; same order and effect) replaces the tuple lambda.
* `count = int(page.evaluate(...))` in the detector helper (runtime conversion of a JavaScript length; no cast).
* No `Any`, `cast`, `type: ignore`, `pyproject.toml`, workflow, `test_auth`, product UI or API change. The standalone 189 checker is not imported. Detector, expected negative control, 503/403 behavior and receipts, and the owner quiet definition are untouched.
* Delta versus the merged main base: the checker plus tracking only.

## Validation (owner-selected demo focused tier; raw files outside the repository in session `files/evidence-954-c3/`, raw manifest `MANIFEST.sha256`)

| Check | Exit | Result |
|-------|------|--------|
| mypy 2.4.0 from `src/api` before the fix (fresh session venv, CI install profile `pip install -e ../core -e ../agents -e ".[dev]"`, fresh cache) | 1 | exactly the five hosted errors (lines 162, 214, 232, 387 x2) |
| same mypy after the fix | 0 | no issues in 200 source files |
| Ruff 0.17.1 `check .` and `format --check .` | 0 and 0 | passed, 125 files formatted |
| Ruff format check on the file (project and `--isolated`) | 0 and 0 | formatted |
| `test_photo_availability` | 0 | 1 test OK |
| Core `test_scenario_manifest` and `test_needs_inventory` | 0 | 19 tests OK |
| ONE actual synthetic Chromium run (status receipts, 13 detector fixtures, negative control) | 1 (unadmitted) | `flock -n /tmp/ama-rpi-heavy.lock` was held by a prior 1292 original-load diagnostic; checker not run; no waiter, poll or kill; NOT claimed passed |

Notes: the first reproduction in the existing `ama462` venv (stale editable installs) and a stale-cache rerun showed unrelated import errors; both are retained as `mypy-before.*` and `superseded/`, and the authoritative reproduction is the fresh-venv, fresh-cache run. Isolated Ruff `E,F,I,B,UP` finds I001 and E501 that the project config already exempts for `checks/*.py` (pre-existing, not touched). Not run: SQL, cloud, credentials, models, full or `--changed` gates, web guidelines review (no web UI file changed).

## Cycle ledger

C1, C2 and C3 spent; two of five remain; no reset or grant.
