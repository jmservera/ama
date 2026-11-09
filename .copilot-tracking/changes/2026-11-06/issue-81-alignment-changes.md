<!-- markdownlint-disable-file -->
# Changes: issue #81 parent alignment (2026-11-06)

Plan: [plan](../../plans/2026-11-06/issue-81-alignment-plan.md).

| Change | Evidence |
| --- | --- |
| Pre-alignment commit of research, plan, details, critique and state | commit `5b92be4a4` on `af891a5cc` (original SHA, now rebased as `ac163c23a`) |
| Local rebase of the parent branch onto `origin/main` `56eec736906774ef56d8c9a66ed7f3f9c1e520c6`, no conflict | child commits now `9055abce3`, `e6434dd1d`, `81c106998`; `git range-diff` all `=` |
| Preservation proof of 48 child paths (8 source/test, 40 evidence) | 48 same, 0 different; `src` diff against `refs/ama/issue81-start` empty; inventory kept in scratch `child-inventory-start.txt`, `preservation.txt` |
| Bounded checkpoint appended to [cutover evidence pack](../../../docs/architecture/cutover-evidence-pack.md) (`ms.date` 2026-11-06) | section "Issue 81 parent alignment checkpoint (2026-11-06)" |

## Divergences and amendments

* No divergence from the plan. Plan Amendment 1 (critique dispositions) was applied before alignment.
* Extra selected authority-refusal tests (`test_bulk_edits`, `test_aftercare`, `test_consultation_controls`, `test_change_provenance`) were chosen by grep for refusal behavior, within the plan's "selected by name" rule.
* `mypy` was absent in the isolated environment (real `ModuleNotFoundError`); installed into a scratch venv with pip only. No other install, no uv.
* The pre-alignment commit's SHA changed from `5b92be4a4` to `ac163c23a` by the rebase; the starting parent identity `af891a5cc` is retained in `refs/ama/issue81-start` (local only) and in the records.

## Not done

FULL gate, API/agents suites, SQL Server, Azure, browser, Docker, scanner, push, PR, issue writes, child86 changes. Issue #81 criteria and #440 acceptance unticked.
