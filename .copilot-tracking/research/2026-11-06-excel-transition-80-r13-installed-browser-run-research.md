---
title: Issue 80 r13 research, owned installed environment and schema download browser run
description: Prospective research for running the prepared schema download browser check in an owned pip-installed external environment
ms.date: 2026-11-06
---

* Task: excel-transition-80-r13-installed-browser-run, parent r12 test isolation. Intake HEAD a6bc5af2ff91817c1568826d166c7454da56b8a0, tree 750e73a7dc3231dafca6a4b216d9f5c0c7b3b18d, origin/main bb3a3b03, parent ead177ef unchanged. Ignored-inclusive status is empty and the repo-root `.venv` is absent.
* Disposition: executed (read-only). Planning Readiness: Ready.
* Qualifications carried from r12 (not rewritten there): r12 Research, Plan and Details were serial before edits, but its critique was self only and not an independent critique; its checks started in parallel with edits (13:59:41.435-.438) and commit calls ran in parallel with record writes. Root's sequential final-head rerun (4 tests, Ruff, format, mypy, all 0) resolves the current-test-execution concern, not the past chronology. The r12 cleanup (4 roots, 75 members, 1901524 logical bytes) was root-authorised and is done; it grants no further removal.

## Facts from source and guides

* Command (`src/api/README.md` line 1302, module docstring): from `src/api`, `PYTHONDONTWRITEBYTECODE=1 <python> -m checks.schema_download_browser_check`. The module registers a synthetic schema through the real `POST /api/form-schemas` as the Retrofit Programme Manager, opens the Funding screen, tabs to `a[href="/api/form-schemas.csv"]`, presses Enter, and reads the actual CSV; `support@example.test` and `grants@example.test` are denied by `forms._actor` (403, no CSV, no attachment). The r10 run printed 21 PASS lines; the expectation here is 21 PASS and COMPLETE.
* Harness `checks/design_system_browser_check.py`: the child server is started with `sys.executable -m zava_forward.api.server` and a `PYTHONPATH` of the worktree `src/{core,agents,api}/src`. That child source override is the reviewed harness behaviour (the r12 `child_env()` passes only PATH, HOME, LANG and the bytecode controls), so the parent interpreter must itself be correctly installed; the child override is not evidence of the parent installation.
* `scratch_parent()` honours an absolute `ZF_BROWSER_SCRATCH` outside the checkout, else `ROOT/.venv`.
* Dependencies (`src/api/pyproject.toml`): aiohttp 3.14.5, azure-identity 1.26.0, azure-eventhub 5.15.1, azure-iot-device 2.14.0, zava-forward-core[sql,blob] (mssql-python 1.15.0, azure-storage-blob 12.31.0), zava-forward-agents; dev extra playwright==1.64.0 (also ruff, mypy). `requirements.txt` files hold the pinned hash sets.
* Guides prescribe editable installs (`pip install -e ../core -e ".[dev]"`). An editable or in-tree build writes egg-info or build directories beside the checkout sources and would create new ignored inputs. Chosen alternative: build wheels from a `git archive` of the exact HEAD into an external directory and pip-install those wheels into a new external venv. This still installs the candidate's own distributions (imports resolve to the venv site-packages, with versions and hashes recorded) without writing to the checkout. This is a stated deviation from the guide's editable wording.
* Global editable `zava-forward-*` installs point at `/home/azureuser/source/ama` (another checkout) and must not be used. The system Python plus PYTHONPATH of r10 was not an installed environment.
* Playwright 1.64.1 and Chromium revision 1248 exist under `~/.cache/ms-playwright` (r11 environment notes). Compatibility with playwright 1.64.0 pin is verified by the run itself, not assumed.

## Resource state at intake

* Root filesystem is 100% used (about 1.9 GB free); `/mnt` has about 129.6 GB free. Every new venv, pip cache, TMPDIR, browser profile and log must live under new `/mnt/ama-gates/e80-r13-r67-1106/`. Memory available about 6 GB at intake; to be rechecked immediately before the browser.
* The shared lock `/tmp/ama-rpi-heavy.lock` has no holder at intake; it is acquired nonqueued (`LOCK_EX|LOCK_NB`) only for the browser and `tools/rpi-checks.py` `worker_limit(1)` is called unmodified. Busy lock or capacity refusal means a blocked handoff, no waiting.

## Limits

* Local synthetic fixture, loopback server only. No WCAG, assistive technology, Fluent, concurrency, every-list, owner-threshold or live acceptance. No FULL, SQL, container, scanner, cloud or model call. No production, harness or check byte change from a6bc5af2.
