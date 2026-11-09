<!-- markdownlint-disable-file -->
# Changes: issue #81 parent re-alignment (2026-11-07)

Plan: [plan](../../plans/2026-11-07/issue-81-realign-r2-plan.md).

| Change | Evidence |
| --- | --- |
| Prospective records committed on old base | commit `29ddbc4cb` (now rebased) |
| Local rebase onto pinned `origin/main` `0f420dc9514db22081cb48fa733267d9d33a0d24`, no conflict | child commits `cf9bf329e`, `eca6e1bbf`, `5f1bf0a42`; backup ref `refs/ama/issue81-r2-pre-realign` = `c5edb320a`; `refs/ama/issue81-start` = `af891a5cc` |
| `quality.py` proof | diff against backup is exactly main's `typing.Any` import and `checklist_rows()` |
| 48-path inventory | 47 same, 1 different (`quality.py`, explained) |
| Addendum in [evidence pack](../../../docs/architecture/cutover-evidence-pack.md) (`ms.date` 2026-11-07) | new subsection; earlier text unchanged |

## Commands and results

See the addendum table: core 193/4/383 tests OK (skips 1/0/109 with reasons), ruff, format and mypy clean, API 123 tests OK (1 skip, local Chromium opt-in). Scratch `/mnt/ama-gates/r2-81-realign-1107`.

## Divergences and amendments

* Plan Amendment 1 applied. The first API run failed with `FileNotFoundError: node` because `env -i` dropped it from `PATH`; adverse run preserved here, corrected by adding the Node directory to `PATH`; second run passed. No retry hid a product failure.
* `pip install` of core and agents created ignored `build/` and `egg-info` directories in the worktree; removed (run-generated only) before freeze.
* Rubric run 42361331168 completed with success; the final fetch added score-only `0f420dc95`.

## Not done

FULL gate, browsers, SQL Server, Azure, Docker, scanner, push, PR, issue writes, child #86 and other worktrees. Receipt r15 not reused. Issue #81 criteria unticked.
