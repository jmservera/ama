<!-- markdownlint-disable-file -->
# Critique: issue #81 parent alignment (2026-11-06)

Execution: `executed` once, prospectively, before any rebase or test run.
Reviewer: independent `rubber-duck` agent (read-only), run on plan, details and
research committed at starting HEAD `af891a5cc`. Verdict: **Revise** (no
unresolved significant or divergent issue after dispositions). Not repeated.

## Findings (verbatim substance) and dispositions

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Environment inherits shell; `test_resident_decisions.py` enables Azure SQL via `ZF_RESIDENT_AZURE_TEST` (line 3227) | Accepted. Run with `env -i` allowlist, explicit `ZF_RESIDENT_AZURE_TEST` and any `ZF_*`/`AZURE_*`/`MSSQL*` opt-ins unset; record skips |
| 2 | Significant | Preservation proof compared all tracking files including main's and new files | Accepted. Inventory the child evidence paths at the starting SHA, compare each path's blob and mode individually against the new HEAD |
| 3 | Significant | No failure disposition | Accepted. A failed preservation check or required regression, or an unavailable check, blocks any "aligned" claim; report as blocked or failed, never as a pass |
| 4 | Significant | Main advancing would change the premise | Accepted. If origin/main differs from the pin, inspect the delta; if it touches the children's source, tests or evidence or this scope, stop for replanning |
| 5 | Significant | SQL exclusion vs `SqlFlows` and `SqlResidentDecisions` local SQLite tests | Accepted with clarification. These use a temp-dir SQLite file (`SqlStore`, `pw.sqlite`), not SQL Server or Azure; permitted as isolated local no-service tests and recorded as `local observed (SQLite file)`, never as SQL Server parity |
| 6 | Minor | Research wording implies quality/capacity rule records cite BRD rules; code cites PRD FR-008/016/017 plus fixtures | Accepted. Amendment recorded in the plan; booking rules (funding, safety, resident, evidence) cite BRD RULE-001/002 at `gates.py:185-188`, quality and capacity cite PRD only. BRD is related traceability, not a code citation for those two |

Compatible findings were applied directly; none conflicted with a confirmed
coordinator decision; none required a user decision.
