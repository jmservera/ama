---
title: Issue 149 parent main e2ec integration changes
ms.date: 2026-11-08
---

## Changes

Merge commit cbb9fdcf (tree 0e756d0b) of main e2ecee25 into f8c1be6c; parent ancestors 4d95, 153/233 inputs and all earlier RPI records preserved. No source edit by this continuation. Main-relative delta: 99 files (the 14 non-tracking paths named in the phase details).

## Validation (focused, CI-first; archive and venv /tmp/zf149-e2ec-merge-1108)

* pip-installed core, agents, api, Playwright 1.64.0, ruff 0.17.1, mypy 2.4.0 (non-editable); 212 installed production files equal the archive. Test-helper PYTHONPATH only.
* 76 API tests OK (AI state, exception-register screen, atlas checker, content standard, document controls, role screens); 19 Core tests OK (needs inventory, scenario manifest).
* ruff check clean and canonical format clean for api (121) and core (216) once the scratch pip `build/` dirs were removed from the archive; the first run's lint and format noise came from those build dirs, not source. mypy strict: api 195 files, core 269 files clean. Configured checker format exclusions are unchanged.
* Browser under `flock -n` from the archive with Chromium 1248 and required axe 4.10.3 (SHA 880970c0...8a68bb): atlas exit 0, 194 PASS, no axe step; data operator exit 0, 100 PASS, required axe on the queue page and per-home view with no violations and incomplete []. Not complete coverage, WCAG or AT acceptance. The harness supplies archive source paths to its child server, so this is not exclusively installed-runtime proof.
* Raw out hashes equal the earlier correction 3 runs (08093407..., 042fb269...); this run is a fresh execution on merged source and the equality is not the witness. Checker and role-screens.js bytes equal the pre-merge head.
* Not run: FULL, SQL, scanners, images, `--changed` and `--all`.

## Pending

Coordinator exact-head assessment, hosted checks, human, AT and whole-issue acceptance. Refs #149 and #229 only.
