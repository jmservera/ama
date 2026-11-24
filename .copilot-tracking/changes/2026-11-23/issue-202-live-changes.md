# Issue 202 live changes, 2026-11-23

Tier: FULL by impact (workflow and gate-tool edits). `rpi-checks.py --all` was not run (forbidden here); no external receipt exists. Demo scope; no push.

## Changes

* Deleted `.github/workflows/mvp-ci.yml` and `mvp-validation.yml`; removed them from the `src-ci.yml` path filter and actionlint list.
* `tools/rpi-checks.py`: dropped both from WORKFLOWS, WORKFLOW_HASHES and coverage rows; refreshed the `src-ci.yml` hash.
* `tools/check-legacy-references.py` allowlist, `infra/tests/test_pipeline.py` (now asserts the files are absent), `tools/test_src_cutover_repoint.py`, four READMEs and the knowledge-base log updated.

## Validation

* `tools.test_src_cutover_repoint`, `tools.test_check_legacy_references`: 23 OK. `tools.test_rpi_checks`: 129 OK. `check-legacy-references.py`: 0 violations. actionlint on `src-ci.yml`: clean.
* `infra/tests/test_pipeline.py`: 33 pass, 1 error (`test_installed_local_api_denies_unauthenticated_requests`, health check failure); identical on the unmodified baseline, so pre-existing.
* Not run: hosted CI, full local gate.

## Divergences and gaps

* The hosted container-hardening probe (`image` job, non-root, read-only start) is gone from CI; `image-api` local check remains. Known gap.
* A shared `git stash` across worktrees briefly applied another worker's stash here; its two `src/core` changes were saved to `~/.local/share/ama/foreign-stash-recovered-202.patch` and reverted from this tree.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Parity matrix / prototype removed | Proven (ticked, not re-tested) | issue body 2026-11-23 |
| Tag on last mvp commit | Proven (ticked); `v0.21.0` exists on remote | `git ls-remote` record 2026-11-18 |
| Rubric registry PR merged first | Proven (ticked) | issue body |
| Old workflows removed or replaced | Proven in the working tree: files removed, references and tests updated, targeted tests pass. Hosted CI and external full receipt unproven | this commit |
| Branch protection required checks updated | Not needed: ruleset `mainprotect` has `required_status_checks: []`, no classic protection (2026-11-23); nothing changed | `gh api` output |
| No tracked file under `mvp/` | Proven (ticked) | issue body |
