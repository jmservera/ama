# Issue 202 live research (2026-11-19)

Disposition: executed. Task: the only unticked criterion, old workflows (`mvp-ci`, `mvp-validation`) removed or replaced and required checks updated. Demo scope, desktop only; no Azure resource used.

## Observations (2026-11-19, read-only)

* `mvp/` and `prototype/` do not exist in the worktree.
* `.github/workflows/` holds `mvp-ci.yml` and `mvp-validation.yml`, both `workflow_dispatch` only and already running `src/*` packages; `src-ci.yml` is the pull request workflow.
* `gh api repos/jmservera/ama/rulesets`: `main` (disabled; deletion, non_fast_forward, copilot_code_review) and `mainprotect` (active). `mainprotect` has a `required_status_checks` rule whose `required_status_checks` list is empty, so no required check names either workflow.
* Classic branch protection on `main`: HTTP 404 (not protected).
* File-name references remain in `tools/rpi-checks.py`, `tools/check-legacy-references.py`, `tools/test_src_cutover_repoint.py`, `infra/tests/test_pipeline.py`, `infra/README.md`, `src-ci.yml` and `.github/rubric/README.md`.

## Classification

Deleting the workflows edits workflow files and a gate tool with pinned hashes: FULL tier, which needs an external full receipt. The brief forbids `rpi-checks.py --all`, and the owner reserved branch-protection changes for a deliberate post-cut-over step. Nothing needs repointing (empty required list). Planning Readiness: Ready for a stop-and-report outcome; no code change is justified.
