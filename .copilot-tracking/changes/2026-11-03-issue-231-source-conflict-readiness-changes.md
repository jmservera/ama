# Changes: issue #231 slice 3

* Technical queue no longer shows readiness while a source-fact conflict is unresolved; the reason names the query owner.
* Unit test fixture resolves the conflict for the ready case; one blocking test added.
* Browser stories `231` and `231q` were added to the scroll-into-view condition (`226` already had it); story `231` asserts the new reason. The story failed before scrolling because the longer blocked text moved the routing panel out of the readable region.
* README and `docs/reference/log.md` updated.

## Validation (focused tier)

* `python3 -m unittest tests.test_technical_quality_screens tests.test_role_screens_conformance tests.test_role_screens tests.test_content_standard` (from `src/api`, `PYTHONPATH=../core/src:../agents/src:src`): 40 tests, pass.
* `ruff check` and `ruff format --check` on `checks/role_screens_browser_check.py` and `tests/test_technical_quality_screens.py`: pass. The browser check file is now reformatted, which adds about 400 lines of formatting churn to its diff (279 added, 127 removed against main).
* `python3 -m mypy --cache-dir=/tmp/mypy-807b tests/test_technical_quality_screens.py`: pass.
* `python3 -m checks.role_screens_browser_check 231` and `231q`: re-run, all PASS lines shown; axe scan skipped (no `ZF_AXE_JS`), not a pass.
* No gate, benchmark or full suite run.

## Correction note (post-review)

* Confirmed in `role-screens.js` that `queries` is in scope in the Technical queue render and that all blocking reasons are listed together, so the conflict reason and its owner appear alongside others.
* `assetStatus` now treats only the terminal statuses `Reconciled` and `Withdrawn` (the only ones the core accepts) as clearing a conflict; any other status stays `Unresolved`. Test added; fixture now uses `Reconciled`.
* README scopes the unresolved-conflict claim to story `231` only; `231q` was not changed.
* `ruff format` applied to the browser check file. The original review outcome is unchanged.
