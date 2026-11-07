---
title: Issue 80 r13 details, owned installed environment and schema download browser run
description: Step details for environment preparation, nonqueued browser run and evidence capture
ms.date: 2026-11-06
---

* Plan: [plan](../plans/2026-11-06-excel-transition-80-r13-installed-browser-run-plan.md). Research: [research](../research/2026-11-06-excel-transition-80-r13-installed-browser-run-research.md).

## Phase 1: external area

* `R=/mnt/ama-gates/e80-r13-r67-1106`; refuse if it exists. Subdirectories: `venv`, `tmp`, `pipcache`, `xdg`, `ruffcache`, `mypycache`, `pyc`, `scratch`, `wheels`, `src-archive`, `logs`.
* Environment for every command: `TMPDIR`, `PIP_CACHE_DIR`, `XDG_CACHE_HOME`, `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `RUFF_CACHE_DIR`, `MYPY_CACHE_DIR`, `PYTHONPYCACHEPREFIX`, `PYTHONDONTWRITEBYTECODE=1`, `ZF_BROWSER_SCRATCH=$R/scratch`, `PIP_DISABLE_PIP_VERSION_CHECK=1`. `PLAYWRIGHT_BROWSERS_PATH` is left unset so the existing cache in the home directory is read, and the cache is verified, not written.

## Phase 2: provenance and install

* `python3 -m venv $R/venv`; first record the venv interpreter and `pip list`, then try `python -c "import aiohttp, playwright, zava_forward.api"`; record the failures verbatim.
* `git archive HEAD src/core src/agents src/api` into `src-archive`; build wheels with `pip wheel --no-deps` for core, agents and api into `wheels`; install the pinned hash manifests with `pip install --require-hashes -r` for each component (api requirements include core and agents pins as the manifest declares), then `pip install --no-deps` the three candidate wheels, then playwright pinned by the dev extra if absent.
* Record `pip list --format=json`, `pip show -f` for the three candidates, `importlib.metadata` origins, `zava_forward.*.__file__` for each package, and sha256 of each wheel and each installed module file compared with the checkout file at the same relative path.

## Phase 3: browser run

* Immediately before: re-read `/proc/meminfo`, root and `/mnt` free space, and `lsof`/fuser view of the lock. Python wrapper stored in `$R`: open the lock file, `flock(LOCK_EX|LOCK_NB)`, import `tools/rpi-checks.py` unmodified through importlib and call `worker_limit(1)`, then start the command as a subprocess from `src/api` with stdin `/dev/null`, `cwd=src/api`, stdout and stderr to new files, record exit; hold the lock until the subprocess has exited. A busy lock or GateError is recorded and stops the run.
* Command: `PYTHONDONTWRITEBYTECODE=1 $R/venv/bin/python -m checks.schema_download_browser_check`. Expect 21 PASS lines and COMPLETE.

## Critique amendments (see plan)

* Set `PLAYWRIGHT_BROWSERS_PATH=$HOME/.cache/ms-playwright` explicitly (read only) while `XDG_CACHE_HOME` is external; `unset PYTHONPATH PYTHONHOME PYTHONSTARTUP PYTHONUSERBASE` and `PYTHONNOUSERSITE=1` in the parent; assert `__file__` of concrete modules lies under `$R/venv`.
* Candidate wheels are installed explicitly; the api manifest does not contain them. Compare playwright's installed version with 1.64.0.
* Preconditions before building: tracked status empty, ignored status empty, HEAD equals the execution commit; record fixture hashes.
* Wrapper runs the subprocess in a new process group, and on any exception or signal terminates and waits for it before the lock is released.

## Phase 4 and 5

* `git status --short --ignored` before and after; `git diff --stat a6bc5af2` over `src` empty; hashes of the check, harness and `role-screens.js` before and after.
* Changes, then a separate later author Review, state after Review, validated JSON and links, commit. The execution HEAD (a6bc5af2 plus the prospective commit) and the final record HEAD are both stated, with proof that runtime and check files hash identically.
