# Changes: issue-76 live r2

Tier: FOCUSED (docs and evidence only; no src, workflow, infra, SQL or deployment change). Azure: read-only (revision lookup); nothing created, nothing to delete. Divergence from plan: none.

## Files

* docs/reference/research/issue-76-live-r2-2026-11-18.md (+ evidence dir with scripts, raw output, 2 masked screenshots)
* docs/reference/README.md (index line), docs/reference/log.md (entry)

## Per-criterion proven/unproven (Refs #76)

| Criterion | Status | Basis |
| --- | --- | --- |
| Default view single list, one status and next action | Ticked, not reopened | |
| No perspective picker or role simulator | Ticked, not reopened | |
| Queue with visible definitions | Ticked; definitions seen live again (screenshot 02) | |
| Blocked steps reason, owner, next action | Ticked, not reopened | |
| Hazard and safeguarding items show a clock and named owner | UNPROVEN in full: hazard clock and named owner display but value Unknown (no timestamp in synthetic record); safeguarding has no demo item (0 of 16) | probe-clocks.out.json, screenshot 01 |
| Views agree on ownership (FR-034) | Ticked, not reopened | |
| Single reset to versioned default (FR-032) | Ticked; "Reset my queue" with default work-queues-1 text seen live (screenshot 02) | |

## Validation

* src/api 3 test modules, 9 tests OK; src/core test_taskqueues 29 tests OK (outputs retained in evidence dir).
* mypy, ruff and rpi-checks not applicable: no Python source under src/ or infra/ changed. rpi-checks --all not run.
* Hosted CI, independent exact-head review and owner decision on "Unknown" clock outstanding.
