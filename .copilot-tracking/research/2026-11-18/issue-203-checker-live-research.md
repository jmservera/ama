# Research: issue-203-checker-live

Disposition: executed. Task: exempt regression-test files and dated live-evidence notes from `tools/check-legacy-references.py` (Refs #203, criterion 1).

## Opening evidence (before any edit)

* Base `2d361df88`. `python3 tools/check-legacy-references.py` exits 1 with 47 reference violations, 0 link violations.
* `python3 -m unittest tools.test_check_legacy_references`: 7 tests, 1 failure (`test_repository_has_no_violations`).
* The prior run (`issue-203-live-research.md`) found 11 violations in three `tools/test_*` regression files; new dated live-evidence notes under `docs/reference/research/` since then add more (issue-198, 200, 202, 203, src-repoint-live-audit-200).

## Planning Readiness

Ready. Two exemption classes: (a) three regression-test files that must name old paths (`test_epic_legacy_path_retirement.py`, `test_epic_parity_matrix_old_paths.py`, `test_private_mvp_data_exclusion.py`), (b) dated live-evidence records under `docs/reference/research/` whose name carries a date (`issue-N-...` or `src-repoint-...`, file or evidence folder).

## Boundaries

* Only `tools/` changes (not `src/`): FOCUSED tier. Live Azure is not needed for this checker change; criterion 5 is not provable from it.
* Issue comment of 2026-11-17 warns the literal criterion needs owner agreement; the exemption narrows scope to documented history/guards, and the criterion stays unticked.
