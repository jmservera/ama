---
title: Issue 202 changes
date: 2026-11-17
---

## Changes

* README.md: archive paragraph now says `v0.21.0` is published on origin and the owner-decided GitHub release is still absent; removed the stale push command.
* tools/test_epic_legacy_path_retirement.py: added `ArchiveTagDocTests` (fails on the pre-fix README, passes now; verified by stashing the README change).
* docs/reference/log.md: appended dated entry.

## Validation (FOCUSED)

* `python3 -m unittest tools.test_epic_legacy_path_retirement`: 6 tests OK.
* `python3 -m unittest tools.test_check_legacy_references`: 1 failure, `test_repository_has_no_violations`. Pre-existing at base: 11 violations in `tools/test_epic_*`/`test_private_mvp_data_exclusion.py` (same count with and without my change); not fixed, out of scope.
* `ruff format --isolated --line-length 100 --check` on the tools test file: reports reformat needed both at base and now (pre-existing; `tools/` is not in the src-ci scope). Not applicable: mypy (no `src/` change), `rpi-checks.py --all` (heavy lock; FOCUSED tier).
* Link check: `check-legacy-references.py` reports 0 link violations.
