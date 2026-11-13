# Issue 202 close audit: rubric registry and workflow criteria (research)

Date: 2026-11-13. Base: `origin/main` 31c31b2e1 (worktree HEAD 03f5f830a, one docs-only commit behind). Tier: Focused (documentation only). Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue 202 body: 4 of 6 ticked; unticked are the rubric-registry PR criterion and the workflows/branch-protection criterion.
* Rubric registry: `.github/rubric/artifacts.json` has no `mvp/` or `prototype/` string. Include globs dropped in #300 (M5) and #302 (M6) on 2026-10-15; dead excludes dropped in #851 (a81329ef9, 2026-11-03). `mvp/` deleted by #499 (4a02baf6f, 2026-10-27). Archive tag `v0.21.0` exists (contains `mvp/`).
* Score record: `.github/rubric/README.md` (Zava Forward MVP section) records the 47 baseline, the current 77 and that recovery came from re-evidencing, not registry change.
* Workflows: `mvp-ci.yml` (name `Source CI`) and `mvp-validation.yml` (name `Source validation`) remain, `workflow_dispatch` only. `src-ci.yml` runs on pull requests. The legacy files are pinned by SHA-256 in `tools/rpi-checks.py` (WORKFLOWS, WORKFLOW_HASHES, check mapping) and referenced by `infra/tests/test_pipeline.py` and `src-ci.yml` path filters.
* Branch protection (read-only): `GET branches/main/protection` returns 404 (not protected). Ruleset `mainprotect` (24504150) is active with `required_status_checks: []`; ruleset `main` (24682333) is disabled. No required check names any legacy workflow.
* PR #714 body: main has no branch protection, so no required check is dropped.

## Assessment

* Critique corrections (rubber-duck, 2026-11-13): only the include globs left before #499; the two dead excludes left in #851 after it. Current protection state (empty required list) is not historical proof of an update. The current score snapshot is 79 (`latest.json`, 2026-11-13); 77 is historical.
* Registry criterion: the include-glob sequencing is met in fact (all mvp include globs left before #499), but no single dedicated registry-only PR preceded deletion; #302 was a README split that removed the last include glob. Dip acceptance and recovery are recorded. Literal "dedicated PR" is an owner interpretation.
* Workflow criterion: not met literally. The workflows were renamed and neutralised, not removed. The required-check part is vacuously true today (empty list). Removing the files is a gate-tool change (hash pins) and needs the full tier plus owner direction; out of scope here.

## Open for owner

* Accept #302/#851 as the registry step, or require nothing further.
* Accept dispatch-only retention as "replaced", or authorise a full-tier PR removing the two files and their pins.
