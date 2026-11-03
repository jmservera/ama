# Changes: issue #231 slice 3

* Technical queue no longer shows readiness while a source-fact conflict is unresolved; the reason names the query owner.
* Unit test fixture resolves the conflict for the ready case; one blocking test added.
* Browser stories read scrolled panels; story `231` asserts the new reason. The story failed before scrolling because the longer blocked text moved the routing panel out of the readable region.
* README and `docs/reference/log.md` updated.

## Validation (focused tier)

* `python3 -m unittest tests.test_technical_quality_screens tests.test_role_screens_conformance tests.test_role_screens tests.test_content_standard`: pass (with `../core/src:../agents/src:src` on PYTHONPATH because the distributions are not pip-installed in this worktree).
* `ruff check`, `ruff format --check` on the changed test file, `mypy` on the test file: pass. `ruff format --check` on the browser check reports reformatting; this file was not formatted before this change and was not reformatted here to keep the diff small.
* `python -m checks.role_screens_browser_check 231` and `231q`: pass; axe scan skipped (no `ZF_AXE_JS`), reported as a skip, not a pass.
* No gate, benchmark or full suite run.
