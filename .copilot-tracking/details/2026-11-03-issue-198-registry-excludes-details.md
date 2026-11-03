# Issue 198 details: drop dead mvp excludes (2026-11-03)

## Phase 1: registry

* Edit `.github/rubric/artifacts.json`: remove `"mvp/data/**", "mvp/web/vendor/**"` from `solution-code.exclude`.
* Success: file parses as JSON; `src/**/data/**` and `src/**/web/vendor/**` excludes remain.

## Phase 2: README

* `.github/rubric/README.md`: record the removal under the 2026-11-01 registry paragraph, state the expected no-change outcome, change "defensive exclusions" wording, and note 17 failures beside the stale 19.
* Success: README no longer says legacy exclusions remain.

## Phase 3: validation

* `test_prepare.py` (focused), ruff and mypy on the rubric scripts.
