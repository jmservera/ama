<!-- markdownlint-disable-file -->
# Changes: issue #80 current-main export audit

Status: prospective, written before any check runs. Updated in place when implementation finishes.

## Planned changes (tracking only)

* Added `.copilot-tracking/audits/2026-11-10/issue-80-main-export-audit-1110-matrix.md`: acceptance and inventory matrix.
* Added `.copilot-tracking/reviews/2026-11-10/issue-80-main-export-audit-1110-review.md`: single Review.
* No source, test, fixture, endpoint, workflow or documentation change. Raw check logs stay outside the worktree under the Root evidence folder `checks-80-main-export-audit-1110/`.

## Planned checks (outcomes recorded verbatim below once run)

* Owned venv and import-origin verification.
* API: `test_list_export_api`, `test_role_endpoint_inventory`, `test_form_staging_api`.
* Browser, one non-queued `flock -n` each: `schema_download_browser_check`, `progress_browser_check`.

## Outcomes

* Added the matrix `.copilot-tracking/audits/2026-11-10/issue-80-main-export-audit-1110-matrix.md`.
* Owned venv `/tmp/ama-80-audit-venv-1110`: pip install exit 0 (dependency need: system python resolved another checkout); imports resolve to this worktree.
* API: `test_list_export_api` 11 OK, `test_role_endpoint_inventory` 24 OK, `test_form_staging_api` 14 OK.
* Browser: `schema_download_browser_check` exit 0 (21 PASS). `progress_browser_check` attempt 1 failed to start (pre-created `--out` directory, `FileExistsError`); attempt 2 exit 0, 58 PASS, 0 FAIL. Both under `flock -n`; none BUSY; no skips.
* Source worktree stayed clean of non-tracking changes.

## Amendments and divergences

* Progress browser check ran twice because attempt 1 never started (my argument error). Both logs preserved.
* Web guidelines fetch was truncated at 6,000 characters; no UI review finding made.
