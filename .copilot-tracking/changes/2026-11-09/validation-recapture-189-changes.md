<!-- markdownlint-disable-file -->
# Issue 189 validation recapture changes (2026-11-09)

Plan: [plan](../../plans/2026-11-09/validation-recapture-189-plan.md). Refs #189 only. Nothing pushed. Validation only: no source file edited.

## Binding

* Frozen record commit `e0f657f01` (child of `d985f149590f83a50a6d9db08312f21ecf7bc01b`) committed before any capture. Tested head is `e0f657f01`; its `src` tree `ff5046c4ec3b5425462a198559e867007916755a`, `infra` `b0969f8b...`, `tools` `8ccabea4...` and `.github` `7eba9cba...` equal those of `d985f1495`. A content hash of tracked `src` was identical before and after the capture (`57a38688...979d`) and `git status --short` was empty before and after.
* Fetched `origin/main` `ef28d4da42d83b111d48f14df9b70e3c4932a477`; `git diff 8d6f029ca origin/main -- src infra tools` is empty (the one later main commit changes only `.github/rubric/scores/latest.json`).
* Environment: Python 3.12.3 (worktree `.venv`), Playwright 1.64.0 with Chromium 1248, Node v24.21.0, axe 4.10.3 sha256 `880970c0...8a68bb` (verified), `ZF_*` variables 0 and the four SQL/Azure opt-ins unset. Every test module resolved under this worktree (`env.txt`). Nothing queued; only the run's Chromium and an ephemeral loopback port; no leftover process.

## Retained raw capture (outside the repository, never deleted)

`/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/capture-189-validation-recapture/`: 70 files, per producer `.cmd`, `.stdout`, `.stderr`, `.exit` (written by `run.sh`, no pipe), plus `identity.txt`, `env.txt`, `run.sh`, `hashes.sha256` (68 entries, `sha256sum -c` all OK) and `hashes.sha256.sha256` = `6a0d3cabea36b8c8b29253d6eaa408ae50cbeef4e26715d2ff7e27e63e76ea93`. Raw logs are not committed. `unittest -v` writes to stderr.

## Results (single capture, in `run.sh` order)

| Producer | Exit | Result |
|---|---|---|
| api test_simulator_admin | 0 | Ran 27, OK, 0 skips |
| api test_live_control | 0 | Ran 34, OK, 0 skips |
| api test_entra_authoritative | 0 | Ran 36, OK, 0 skips |
| api test_auth | 0 | Ran 41, OK, 0 skips |
| api test_content_standard | 0 | Ran 18, OK, 0 skips |
| api test_design_system | 0 | Ran 8, OK, 0 skips |
| api test_workspace_scripts | 0 | Ran 5, OK, 0 skips |
| api test_case_journey | 0 | Ran 31, OK, 0 skips |
| core test_priority_order | 0 | Ran 142, OK, 77 ok, 65 skipped |
| core test_resident_decisions | 0 | Ran 256, OK, 163 ok, 93 skipped |
| browser simulator_control_browser_check `--axe` | 1 | FAILED (see below) |
| node --check app.js, simulator-control.js | 0, 0 | syntax OK |

Verbose lines ending in `ok` (pattern `ok$`) equal each API run count. In `test_auth`, `test_live_control` and `test_simulator_admin` some tests print to stderr mid-line, so a strict ` ... ok$` pattern gives 39, 25 and 26; the `Ran` and `OK` summaries are authoritative. Core reconciles as 77+65 and 163+93.

## Browser failure (not waived)

The capture exited 1: `AssertionError` at `checks/simulator_control_browser_check.py:156` (`json.loads(control.read_text())["enabled"] is False` after the first Stop click). States passed before it with 0 axe violations: unavailable, rejected start, permitted. The later states (stopped, permitted stop, expired, invalid window, already stopped, stale, write error, manual route, view-only default-deny) did NOT run in this capture, so none of them is evidenced by it.

Diagnostic reruns of the identical command, retained as `diag-browser-axe-rerun1..3` (not a replacement for the failed capture and not a new pass): rerun 1 exit 0, rerun 2 exit 0, rerun 3 exit 1 at the same line 156. Two failures in four runs: an intermittent defect, not an environment fluke. Passing reruns show 0 axe violations in every state, but are retained as diagnostics only.

Hypothesis (read-only, not instrumented): the check waits with `get_by_text("Stopped", exact=False).first` after the first Stop click; non-exact matching is a case-insensitive substring and the always-present paragraph at `simulator-control.js:116` contains "already stopped", so the wait can return before the stop POST has written the file. The BrokenPipe warning in stderr follows the check aborting while the response was being written. Scope if confirmed: one check-side wait in `src/api/checks/simulator_control_browser_check.py`. No product defect is shown. A correction would be the next scoped cycle (C2); none is authorized or made here. C1 remains one of five spent, four remain.

## Skips and denials (unverified, not passed)

* 156 skips `'opt-in owned loopback SQL Server'` (65 priority_order, 91 resident_decisions), 1 `'JSON file rollback only'`, 1 `'Explicit isolated synthetic Azure SQL database required'`. Total 158 skipped, 0 actual SQL or Azure execution.
* Observed refusals are only offline unit tests of the guard (for example `test_symlinked_manifest_is_refused`, `test_remote_docker_engines_are_refused_before_any_inspection`), which pass; no live SQL admission was attempted, so there was no actual denial of an attempted SQL connection. Skips come from decorators before any guard runs.

## Not run

Whole API suite (historical capture `8ab64519c`: 2105 tests, 365 skips, producer 0, preserved and not rerun), `rpi-checks --all`, SQL Server, Azure, models, deployment, assistive-technology acceptance, web-guidelines refetch, ruff and mypy.

## Adverse loss retained

The raw logs of `sql-main-integration-189` were removed after that run (its handoff says so). Its summaries are not current evidence and are not reconstructed. Unchanged: the invented `--out` browser invocation (exit 2), the first merge command failure, original adverse reviews, C1 records, approve 0 on `8ab64519c`, F3 cause UNKNOWN.
