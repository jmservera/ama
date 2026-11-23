---
title: Real-filesystem regressions for unusable ranking archive paths (#1259), run 10
description: Adds regular-file ancestor, symlink loop and unsearchable-parent regressions to the runner tests, with red-before by mutation and per-criterion status
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Local filesystem tests; no Azure resource was created or changed and no credential was used. Source under `src/` is unchanged (test-only), so the FOCUSED tier applies and `rpi-checks.py --all` was not run.

## New angle

Earlier runs re-ran `UnusableArchivePathTests`, which mocks the stat failure. Four classifications that only a real filesystem produces were untested: an archive below a regular file (ENOTDIR), a symlink loop as archive and as ancestor (ELOOP), and a parent without search permission (real EACCES, skipped under uid 0).

## Evidence

* Probe through `runner.run` for verify, schedule and publish: each case gives `problem`, `problem` and `refused archive_unreadable`, `due` null, and no temp-root path in the output.
* New scenarios `ancestor_regular_file`, `symlink_loop`, `symlink_loop_ancestor`, `unsearchable_parent` join the existing check. From `src/core`: `PYTHONPATH=src:tests python3 -m unittest test_ranking_publication_runner test_ranking_publication -q`: 110 tests, OK.
* Red-before by mutation: `_names` changed to return `[]` on any OSError and skip `_require_creatable`; the unknown-state test fails for all seven non-regular-file scenarios, including the four new ones. Source restored; `git diff` shows no `src/zava_forward` change.
* ruff check and format pass on the test file. `python3 -m mypy` reports 3 errors in other files (for example `device_provision.py:120`), none in the touched test.

## Criteria

| Criterion | Status |
| --- | --- |
| 1 to 3 (ticked) | Proven; now also on a real filesystem for ENOTDIR, ELOOP and EACCES |
| 4 Regressions for schedule, verify, publish plus absent coverage; failing before fix | Proven (110 tests; mutation red; original pre-fix red in the failing-first note). Ticking stays with the owner |
| 5 RPI, FULL receipt, independent exact-head assessment, hosted checks | Unproven and process-gated: nothing pushed, no hosted run; no src change so no FULL receipt applies |

Live applicability: the apps are image-based and no ranking publication job exists, so Azure cannot prove or disprove this.
