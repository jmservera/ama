# 440 C2 changes

Rebased the six branch commits onto origin/main 3a6362008 with no conflicts; `git range-diff` shows all six preserved unchanged (ids differ only by rebase). Cherry-picked 5cb6cf0242 (#202 audit) and 7c2cfd6575 (#157/#104 audit) with no conflicts. `docs/reference/log.md` and the TSV merged without conflict, so both histories survive (log diff against main: additions plus the `ms.date` bump only).

Regenerated `docs/architecture/cutover-reference-inventory.tsv` with `cutover_audit --write` after staging all tracking inputs (13 added rows); check mode PASS (130 matrix rows, 1926 reference locations).

## Critique finding applied: #157/#104 audit on the rebased tree

Upstream 3a6362008 changed `ai_consumption.py` (identity allowlist, +22 lines before the cited ranges) and `assistants.py`. The audit text is kept as historical evidence. Its `ai_consumption.py` ranges shift on this tree: 452-478 is now 474-500, 599-654 is now 621-676 and 1203-1267 is now 1225-1289. Rerun on this tree: core `test_ai_consumption_demo` 7, `test_assistants_identity` 5, `test_chat_memory` 21 OK; api `test_ai_boundary` 6, `test_ai_consumption_api` 37, `test_assistants` 136 OK (59 skipped), `test_assistant_release` 60 OK (7 skipped). Verdicts and gaps are unchanged.

## Checks (pip venv, removed before commit)

* `test_cutover_audit` 9 OK; `infra/tests/test_bicep_policy.py` 61 OK (needs `src/orchestrator` installed); `src/agents` `test_chat_eval` 45 OK.
* ruff check: core, agents, api clean. mypy: core and agents clean; api reports 66 errors, 61 of them missing `playwright` stubs (browser extra not installed) and 5 pre-existing `no-any-return` or unused-ignore in untouched files. No source files were changed here.
* Relative links: no broken link in added lines; 17 older broken links in `docs/reference/log.md` pre-exist on main.
* Secret scrub of added docs and tracking lines: 0 hits.
