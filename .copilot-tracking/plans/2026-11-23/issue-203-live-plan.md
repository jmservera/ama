# Plan: issue 203 sixth run (2026-11-23)

Refs #203.

* [ ] Add `.github/rubric/scripts/test_prepare.py` to `GUARD_FILES` in `tools/check-legacy-references.py`.
* [ ] Re-run the checker (expect exit 0) and `tools.test_check_legacy_references`, `test_epic_legacy_path_retirement`, `test_epic_parity_matrix_old_paths`, `test_private_mvp_data_exclusion`.
* [ ] Run `ruff check` and `ruff format --check` on the edited file; mypy not applicable (no `src/` project).
* [ ] Write the research note `docs/reference/research/issue-203-live-20261123-2026-11-23.md`, index row and log entry.
* [ ] Changes record with the per-criterion table; review; one local commit.
