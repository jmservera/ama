# Changes: issue 76 (Refs #76)

No source change; tier FOCUSED. Files: docs/reference/research/issue-76-live-r4-2026-11-19.md (+ folder of scripts, JSON and two masked screenshots), docs/reference/README.md, docs/reference/log.md.

Validation: `PYTHONPATH=src:tests python3 -m unittest test_hazard_safeguarding_clock_owner_76 test_taskqueues -q` in src/core: 31 tests OK. mypy, ruff and web checks not applicable (no src or web file changed). No Azure resource created; nothing to delete.

| Criterion | Status | Basis |
| --- | --- | --- |
| Default view single list, one status, one next action | ticked earlier, not reopened | issue |
| No perspective picker | ticked earlier, not reopened | issue |
| Queue buckets with visible definitions | ticked earlier, not reopened | issue; r2 screenshot |
| Blocked steps reason, owner, next action | ticked earlier, not reopened | issue |
| Hazard and safeguarding items show a clock and named owner | Safeguarding proven live; hazard partly proven (element and owner live, times Unknown) | r4 note |
| Views agree (FR-034) | ticked earlier, not reopened | issue |
| Single reset (FR-032) | ticked earlier, not reopened | issue; r2 screenshot |

Unproven for the demo: hazard time values (record carries no timestamps). Independent review and hosted CI outstanding.
