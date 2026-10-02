<!-- markdownlint-disable-file -->

# Changes: rubric-gate-change-detection

* Task ID: 2026-10-02-rubric-gate-change-detection (child of 2026-10-02-rubric-score-gate)
* Plan: .copilot-tracking/plans/2026-10-02/rubric-gate-change-detection-plan.md

## Modified

* .github/rubric/scripts/prepare.py: regex `glob_match` over `git ls-files`; `parse_name_status` (`-z`); `diff_args` (PR merge base, otherwise last commit that wrote latest.json); `classify_changes` (deletes, rename sources, oversize in diff); `removed_files`; fail closed when the diff cannot be resolved outside bootstrap or force; `--force`; `differs_from_base` compares git object ids (fixes CRLF false positives on Windows checkouts); context adds `removed_files`, `diff_range`, `calibration`, withholds baseline scores in force mode; diff uses `-M -D` (P01-T01)
* .github/rubric/scripts/gate.py: `removed_files` justify decreases only; calibration mode scores from scratch, never writes latest.json, decision carries `calibration`; `--force` (P01-T02)
* .github/rubric/scripts/test_gate.py: removed-path drop, removed-path increase, calibration tests (P01-T03)
* .github/workflows/rubric-score.md and lock: `force` dispatch input read through env at all three call sites; concurrency group includes event name and a per-run discriminator; issues only for non-forced `refs/heads/main` runs; prompt guidance on removed files and calibration (P02-T01)
* .github/rubric/README.md: removal semantics, live criteria, setup PR bootstrap, fixes apply after merge, force calibration, instrument-change behaviour, model pinned twice, separate detection credit cap (P02-T02)

## Added

* .github/rubric/scripts/test_prepare.py: glob, name-status, rename classification, and temporary-repo tests for unchanged main, PR deletion through the gate, direct push deletion and force (P01-T03)

## Divergences

* `differs_from_base` rewritten to compare object ids: discovered when the unchanged-main test failed under `core.autocrlf=true`.
* Concurrency `job-discriminator` added to clear a gh-aw compiler warning.

## Validation

* 28 test cases pass (minimal pytest stub; pytest download blocked on this host).
* `gh aw compile rubric-score`: 1 succeeded, 0 warnings; lock contains the `force` input and three FORCE env bindings.
* `get_errors`: no errors.
