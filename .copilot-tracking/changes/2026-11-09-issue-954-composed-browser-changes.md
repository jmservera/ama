# Changes: issue 954 composed-source browser validation (2026-11-09)

Implement phase after prospective commit `7f435fc43` (research, plan, details and critique committed before the holder check and the run; parent `271ea1440`).

## Changes

* No source, test, config, product, API or UI change. The only artifacts are these tracking records; raw evidence is in the session directory `evidence-954-composed-browser/` (outside the repository).
* Checker `src/api/checks/photo_flag_stale_browser_check.py`: SHA-256 before and after `620301300f3f3dc541e2d1bb577e5331a89e2e440c6a56466a62bd19f324a6db`, git blob `4767591f42be97e1d14932d08d8d805b31131a62` (equal to the blob at `271ea1440`); worktree clean before and after the run.
* Budget: no correction cycle spent; C1, C2, C3 spent, two of five remain; no reset or grant.

## Validation (DEMO focused tier)

* Holder check 2026-11-09 (`holder-check-time.txt`): `fuser -v /tmp/ama-rpi-heavy.lock` reported no holder (exit 1, no output). ONE nonqueued admission `flock -n -E 99`, started and ended per `admission-start.time` and `admission-end.time`: exit 0 (not 99), so it was admitted; stderr empty.
* Interpreter `python3` 3.12.3 with worktree-first `PYTHONPATH`; Playwright and the chromium-1248 asset were already present; nothing installed or restored.
* Output: 83 `PASS` lines and exactly one `FAIL` line, the expected negative control (`FAIL 503: client applied the served false (actual client flag false after refresh)` followed by `PASS negative control: ignored false response fails the client-flag assertion`). Stdout is byte-identical (`diff` exit 0) to the pre-typing C2 run `evidence-954-c2/browser.out`; 13 detector fixtures plus `empty alert receipted` pass.
* Receipts (`obs/photo-flag-stale-console.json`), both 503 and 403: photo requests 2 with served statuses `[503, 503]` and `[403, 403]`; actual client flag `me_flags` `[true, false, true]` (true, false after the served-false refresh, true on the later true refresh); no page error, dialog or disruptive node; one ignored not-rendered empty `#account-error` alert; 2 native `Failed to load resource` diagnostics; no other or unexpected console event; `quiet_per_owner_definition` true; `literal_no_console_event` false (informational, owner definition unchanged).
* Raw commands, stdout, stderr, exits, tool versions, git identities, checker SHA before and after and `MANIFEST.sha256` (14 files) retained in the session directory; no cleanup.

## Main and comparison base

* Fetched `origin/main` `2b6d80a2580444751d4b85fc8eaa2c15f367855d`. The comparison base for the earlier hosted and gate evidence is `3a9767d5c`; the current target is `2b6d80a25`. Between them only the rubric score (`700bf11e1`) and pure documentation (`2b6d80a25`, PR 1317) landed; `git diff --name-only` shows no `src/`, `infra/`, `tools/` or workflow path, so base and target have no runtime-source delta. This is not a claim that the committed `.github` rubric score equals the new main. The tested head is `3a9767d5c` merged with the checker change; it is not merged with `2b6d80a25` (no source delta, no unnecessary merge); a trial `git merge-tree` was clean.

## Skipped

SQL, cloud, credentials, models, private data, full and `--changed` gates, global installs, mypy and Ruff reruns (unchanged source; C3 results stand and are not re-claimed here). Hosted CI, functional f41 current-head qualification, one batched push and independent exact-head review are pending with the coordinator.
