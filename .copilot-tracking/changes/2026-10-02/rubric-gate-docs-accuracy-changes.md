<!-- markdownlint-disable-file -->

# Changes: rubric-gate-docs-accuracy

* .github/rubric/scripts/prepare.py: force mode withholds the full baseline from context; new `diff_base` field (RG-003, RG-007)
* .github/workflows/rubric-score.md and lock: dispatch runs get a per-run concurrency group; prompt reads deleted files via `diff_base` and forbids reading the scores file in calibration (RG-003, RG-004, RG-007)
* .github/rubric/README.md: live-criteria instrument exception; issues only for regressions or invalid scorecards on `main`; calibration blindness and non-cancelling forced runs (RG-003 to RG-006)
* .github/rubric/scripts/test_prepare.py: symlink case uses `pytest.skip` (RS-001)
* .copilot-tracking/changes/2026-10-02/rubric-gate-symlink-tests-changes.md: appended correction (RS-001)

## Validation

* 35 passed, 1 skipped (symlink, WinError 1314 on this host), minimal pytest stub with skip support.
* `gh aw compile rubric-score`: 0 warnings.
* Force-mode context smoke test: `calibration` true, `diff_base` set, baseline fields null, 20 open criteria.
