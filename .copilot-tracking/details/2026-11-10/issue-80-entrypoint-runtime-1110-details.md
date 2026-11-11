# Details: issue 80 entrypoint runtime check

* Date: 2026-11-10
* Task: `issue-80-entrypoint-runtime-1110`
* Plan: `.copilot-tracking/plans/2026-11-10/issue-80-entrypoint-runtime-1110-plan.md`

## Phase 2 details (corrected observation, only if Root admits)

* Working directory: `src/api` of the worktree. Environment: `EP_OUT` (new run directory, must not pre-exist for this driver's output), `EP_WT` (worktree), `ZF_BROWSER_SCRATCH` (new absolute path outside the checkout), `PYTHONPATH` with the worktree `src/api`, `src/api/tests`, `src/core/tests`, `src/agents/tests`, and the three `src/*/src` paths, `PYTHONDONTWRITEBYTECODE=1`.
* Interpreter: existing owned venv `/tmp/ama-80-audit-venv-1110` (Playwright and Chromium already present). Install only after an actual missing-dependency failure, into a new owned venv with pip from `src/api/requirements.txt`.
* Admission: `timeout 300 flock -n /tmp/ama-rpi-heavy.lock <python> <driver>`. If the lock is busy the exit is non-zero; record BUSY and stop. Never queue, wait, spin or touch the holder.
* Driver edits (external file only): wait on `a[download='cases.csv'][href]`; save `errors` and non-GET requests inside `save()`. No other change.
* Expected assertions already in the driver: role Retrofit Programme Manager; no `report` in `work_queues.default`; the `cases.csv` href has no `report`; the capacity screen shows package "SYN north wave" and at least one `WO-` work order; `ZF_DATA` inside the owned scratch and not under `~/.zava-forward`.
* Outputs to capture per stage: URL, h1, every anchor and `[download]` (href, text), button and option texts matching `csv|excel|download|export`, `.csv` network requests, and the click-captured download URL and filename for each located control.
* Failure handling: a fixture, harness or driver failure is the result. Preserve the log and exit code; do not repair again within the same admission.
* Cleanup: remove the owned scratch; confirm no `zava_forward.api.server` or Chromium helper owned by the run remains.

## Phase 4 details (only after Root consumes real evidence)

* Candidate change sites, named only so Root can scope them: `src/api/src/zava_forward/api/web/ops.js` `capacityView` render block (Packages and Work orders sections). The anchor pattern to copy is the existing one at `web/ops.js:246` (checklists) and `web/panels.js:575` (finance).
* Role and contract: unchanged; the routes and `LIST_EXPORTS` already exist (`server.py:172-173`). The manager-only screen already matches the JSON role limits.
* Validation if later admitted: the existing `api/tests/test_list_export_api.py` targeted run plus one existing browser check that renders `#/capacity` (for example `checks/capacity_browser_check.py`, which imports `SqlStore` and so may be blocked without SQL; otherwise the disposable driver) and the web-guidelines review. None of this is run now.
* Risk: adding a visible control is not evidence that rows are correct, authorised or immutable; those remain covered by the preserved API observations only (historical 11, 24, 14 at an earlier pin).
