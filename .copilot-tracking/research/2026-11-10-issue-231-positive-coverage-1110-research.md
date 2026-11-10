<!-- markdownlint-disable-file -->
# Issue 231 positive browser coverage research (2026-11-10)

Task `issue-231-positive-coverage-1110`; parent #149; Refs #231 only. Research disposition: executed (prospective). Opened as a minimal record before substantive research; findings are appended below after the witness research-open event.

## Pinned facts

* Branch `test/demo-positive-quality-coverage-231-1110`, worktree HEAD `736561ba0cccb9beb69eea3ae0d3a997bd0dd9bd` (initial main), target `feat/demo-ux-coverage-parent-149-1110`.
* Scope: initial, previously undelivered two-state positive browser coverage in `src/api/checks/role_screens_browser_check.py`. Not a repair of any failed candidate. Correction balance UNKNOWN; no post-review repair granted.

## Findings (after the research-open witness event)

* Admission read: `demo-source-admissions-225-228-231-1110.md` (#231 section) and `admission-231-issue-1110.json`. Gap: `SCENARIOS` `231` and `231q` in `src/api/checks/role_screens_browser_check.py` only exercise blocked or returned states; `check_readonly_accessibility` rejects the positive phrases for those stories. Node-render tests `tests/test_technical_quality_screens.py` already cover the positive states.
* Environment: system `python3` has no `zava_forward` import from this worktree (namespace imports resolve to `None`), and the other venvs are editable installs of other worktrees. Missing-dependency failure therefore preceded a new owned external venv `/tmp/zf231-venv` (`pip install -e src/core[sql,blob] -e src/agents -e src/api[dev]`): ruff 0.17.1, mypy 2.4.0, playwright 1.64.0. Imports verified: `zava_forward.core.quality`, `zava_forward.api.server` and `checks.role_screens_browser_check` all resolve under this worktree.
* Unchanged baseline (external logs `evidence231/`): `test_technical_quality_screens` 16 OK, `test_role_screens` 8 OK, `test_accessibility_baseline` 12 OK (an earlier `-m unittest <modules>` invocation failed with `ModuleNotFoundError: test_role_screens` because `tests/` was not on `sys.path`; kept as `baseline-unit.log`, rerun with `discover -s tests -p`). Browser `231` and `231q` under the nonqueued `flock -n /tmp/ama-rpi-heavy.lock` (free: `fuser` rc 1): both exit 0, 36 PASS each, pinned axe 4.10.3 (sha256 verified) ran with no violations, incomplete `[]`, Chromium 156.0.8078.4. Baseline passes, so no stop.
* Real projection prerequisites (server `Store.detail`): `technical_missing` is empty only when no unresolved stock query, all four sign-offs `Signed off` and every evidence kind present and scanned clean; `quality_handover_blockers` is empty only when every Accepted record has all checklist labels with evidence, no unreleased hazard and a current resident decision matching `resident_binding`. Existing helpers suffice: `synthetic_data()` plus `supplied_resident_fixture` (re-run through `runpy`, as `role_screens_fixtures.py` does) restore documents and the Accepted resident decision. A probe over `Store.detail("ZF-1")` with the constructed home returned `[] []`; this is the server's own computation, not a stubbed response.
* Real-projection fixture choices: no hazard records (rather than a released one, so no safety release is asserted), one measure (Loft insulation), the existing SQ-1 query given a terminal `Reconciled` event, sign-offs with synthetic `SYN` names and design version, one Accepted quality record whose `accepted_by` differs from `submitted_by`. These are test inputs, not professional approval.
* Single process per scenario: `main(run_browser, data_factory)` takes one factory chosen by `argv[1]`, so two positive selectors (`231p` technical complete, `231qp` quality accepted) share one private factory.
* Recipe: `role_screens_browser_check` is not a registered scenario or needs-inventory entry (`git grep` finds only README/docs/log mentions), so no SHA or Core manifest update is applicable. To be re-verified at implementation.
* Excluded files untouched by plan: `atlas_tensions_browser_check.py`, `test_atlas_tensions_checker.py`, `role_screens_fixtures.py` (#233); #130 and #111 hooks.

## Planning Readiness

Ready. Remaining unknown: exact rendered text of the positive states, confirmed by the first browser run.
