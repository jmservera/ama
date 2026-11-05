---
title: Gate Chromium prerequisite changes (#1208)
description: Implemented changes, commands and results for the Chromium ordering repair
ms.date: 2026-11-05
ms.topic: reference
---

## Changes

* tools/rpi-checks.py: new Runner.install_chromium; Runner.run calls it right after the api venv install when project-api is selected (before plan_shards and schedule); required_checks adds the identical command to the project-api contract; Runner.browser reuses the helper (same argv and 900 s timeout, so its contract is unchanged).
* tools/test_rpi_checks.py: three regressions: contract order, receipt rejected without the install, runner order and PLAYWRIGHT_BROWSERS_PATH.
* No change to EXPECTED_SKIP_REASONS, check names, SQL, security, human or closure gates.

## Commands and results

* Red reproduction on base ead177e with the new tests: 1 failure and 2 errors (no Chromium install in contract or runner).
* python3 -m unittest tools.test_rpi_checks: 85 tests OK after the change (a printed KeyboardInterrupt line comes from an existing timeout fixture).
* ruff check and ruff format --check (isolated, line length 100, E,F,I,B,UP, py312) on both files: pass.
* mypy --strict on both files: no issues.
* Not run: full gate, SQL, image and browser groups; no full-suite receipt for tooling.

## Native validation status (qualified)

* Nonqueued probe of /tmp/ama-rpi-heavy.lock on 2026-11-05 reported HELD (holder #96, PID 1232396, rpi-checks --all, --lock-timeout 0).
* The small native-browser check was therefore not run. Native execution of test_resident_summary_ai_ui with the installed browser is UNPROVEN. No sleeping or polling; no shared cache mutation.

## Preserved adverse evidence

* /tmp/rpi188-full-20261105T0740/receipt.json (SHA256 72b69ac4d11d7215b3d8c583385c98c6a807d59740cc82a4287000189e399ef8) and 0051-project-api.log are untouched and not used as evidence for this head.

## Freeze correction (appended 2026-11-05; originals above unchanged)

* Discrepancy: the earlier reported clean freeze at 92210ae5260fe2b8b068b51dc0b50198c0a7ff93 was verified only against tracked status. Under `git status --short --ignored` it was not clean: `.mypy_cache/`, `.ruff_cache/` and `tools/__pycache__/` were present. The original review outcome above is unchanged; no source behavior changed.
* Disposition: 25 own-generated, untracked, non-symlink files (created 2026-11-05 08:53-08:54 by this task's lint, type and unit runs; none tracked, none referenced by sources or receipts) were archived outside the checkout at `~/.local/share/ama/tracking-archives/2026-11-05-issue1208-gencache/` (`caches.tar.gz` SHA-256 cf0dab8fc72747dee0452a22c74ae19aaa5b0ba1d4ae96993f91366647d61175, `manifest.txt`, `sha256.txt`), restored into `restore/` with 0 hash mismatches, then removed individually (`removed.log`, 25 entries) and the emptied directories removed with `rmdir`. No glob, recursive or foreign deletion.
* Historical disclosure retained: an earlier artifact was authored through a bash printf redirect, contrary to the file-creation rule; it is not rewritten here.
* Native browser evidence remains pending: heavy lock held by #96 (PID 1232396). No browser, SQL, build or full-gate run. Not all acceptance criteria are proven; Refs, not Closes.
* Later probes use PYTHONDONTWRITEBYTECODE=1 and external Ruff/mypy cache directories.
