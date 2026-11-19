# Changes: issue 203 live proof (2026-11-19)

Refs #203. Tier FOCUSED: documentation and evidence only; no `src/`, workflow, gate-tool or dependency change; `rpi-checks.py --all` not run. Not pushed.

## Files

* `docs/reference/research/issue-203-live-20261119-2026-11-19.md` and `issue-203-live-20261119-evidence/` (new)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (appended entry)
* `.copilot-tracking/` research, plans, details, critiques, changes, reviews, state

## Per-criterion table (all five issue criteria)

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Search returns only intentional historical references | Proven (demo) | research note section 1; checker exit 0; 26 tests OK |
| 2 | Relative links in changed docs resolve (ticked) | Re-checked: 0 violations in 7 changed documents | checker output |
| 3 | Index and log updated (ticked) | Applied again for this note; earlier entries untouched | diff |
| 4 | Rubric comparison (ticked) | Not re-proven | |
| 5 | Deployed app and CI green from `src/` | Unproven in part: app healthy and PR CI green; build provenance and push CI on `main` unproven | research note section 5 |

## Validation

* `python3 tools/check-legacy-references.py`: 0 violations.
* `python3 -m unittest tools.test_check_legacy_references tools.test_epic_legacy_path_retirement tools.test_epic_parity_matrix_old_paths tools.test_private_mvp_data_exclusion`: 26 OK.
* mypy, ruff and src suites not applicable (no Python or `src/` change).
* Hosted CI for the exact head: not observed (no push).
