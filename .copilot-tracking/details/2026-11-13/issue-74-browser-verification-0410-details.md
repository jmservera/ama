<!-- markdownlint-disable-file -->
# Details: #74 home-case browser verification (issue-74-browser-verification-0410)

Plan: [plan](../../plans/2026-11-13/issue-74-browser-verification-0410-plan.md). Derived from prospective details V1 of `issue-74-building-separation-0400` (blob cf783f754a76bb03c3eacce3624e9a7aa94daf4f), browser portion only.

## Run procedure

* Runner: `run.sh` in the owned evidence directory (SHA-256 334867fb2c21e3848f3f570f6f25fda4159912007d751d1163dd2a01c6b3d74d). Command run from `src/api` under `env -i` with PATH=/usr/bin:/bin, a HOME inside the owned directory, LANG, `PYTHONDONTWRITEBYTECODE=1`, `PLAYWRIGHT_BROWSERS_PATH` to the existing cache, `ZF_BROWSER_SCRATCH` in the owned directory and `ZF_AXE_JS` set to the owned axe copy: `<owned venv>/bin/python -m checks.home_case_browser_check`.
* Run 1 used the owned venv before installing anything (selected validation). Run 2 followed the declared-dependency install.
* Records to capture: preflight, exit codes, assertion lines, counts, installed versions, hashes, cleanup.

## Out of scope

Outcome fields, G5, V2 mapping, unit tests, building route, any criterion tick.
