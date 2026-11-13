<!-- markdownlint-disable-file -->
# Details: #74 buildingView operational observation (issue-74-building-observation-0420)

Plan: [plan](../../plans/2026-11-13/issue-74-building-observation-0420-plan.md).

## Interaction

Owned driver `observe.py` (absolute path in the owned output directory) imports `checks.design_system_browser_check.main` and `checks.home_case_browser_check.home_case_data` unchanged and supplies its own browser callable. Journey: sign in as `pam@example.test`, then request listeners (request/response) attach; navigate to `#/case-home/ZF-2`; click the existing link `Open full building context`; wait for the heading `Fictional exercise block (SYN-B1)`. No other click, no control is activated, nothing is filled after sign-in.

## Recorded (bounded only)

Route hashes, HTTP status of `/api/buildings/*` responses, h1, h2 names, per h2 section booleans for a fixed list of synthetic IDs, labels and amounts (SYS-1, WORK-1, HOLD-1, DEP-1, COST-1, GBP 12000.00, GBP 6000.00, ZF-2, ZF-3, home-only document and quality labels, "Affected homes"), count of controls in `main`, non-safe request methods after sign-in (list), count of non-loopback-origin requests, page JavaScript errors, browser version. No DOM, headers, cookies, tokens or messages.

## Isolation

`env -i` with PATH, HOME in an owned new directory, LANG, `PYTHONDONTWRITEBYTECODE`, `PLAYWRIGHT_BROWSERS_PATH` (existing read-only cache), `ZF_BROWSER_SCRATCH` and `OBS_OUT` in the owned directory. No `ZF_DATA` is set by the caller; the harness sets it to its own temp file. Interpreter: frozen b0e venv. Not set: any model, provider, deployment or auth variable.

## Cleanup

The harness terminates the exact Popen server PID in `finally` and the driver closes the browser in `finally`. Afterwards a process snapshot confirms nothing of this task remains. No name-based kill, no prune, nothing else is removed.

## Resource

`flock -n` on `/tmp/ama-rpi-heavy.lock` held by the runner through cleanup; regular non-symlink file, owner and inode recorded; MemAvailable at least 4 GiB; no queue or retry; 10 minute total.
