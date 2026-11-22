# Issue 2186 live changes, second run (2026-11-22)

Tier: focused (no src, workflow, dependency or gate-semantics change). No source edit: the feature landed earlier in 8c27b4940c (#2221) and cd687ef558 (#2272).

## Changes

* Dated `-r2` RPI artifacts and a state record.
* Research note `docs/reference/research/issue-2186-live-full-receipt-docs-move-2026-11-21.md`: update section for this run; index log entry.

## Validation

* `python3 -m unittest tools.test_rpi_checks -q`: 127 tests OK.
* `ruff format --isolated --line-length 100 --check tools/rpi-checks.py tools/test_rpi_checks.py`: clean.
* Hosted CI for the exact head: not observed (no push by instruction). `rpi-checks.py --all` not run.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Full receipts survive docs-only main moves | Proven | `test_full_receipt_survives_only_inert_main_moves` in the 127-test run |
| Relaxation recorded in verify output | Proven with stubbed receipt validation; end to end unproven | `test_verify_reports_docs_only_relaxation_for_full_receipt` and `test_verify_requires_stack_member_and_reports_relaxation` |
| Code, tool and image changes still invalidate | Proven | same full-receipt test rejects code, tests, src markdown, tools/rpi-checks.py, Dockerfile and mixed moves |
| Test added | Proven | tests above exist on main and pass |
| Real full receipt verified on a docs-moved main | Unproven | needs `rpi-checks.py --all`, forbidden for this task |

Azure, browser and credential surfaces do not apply to a gate tool.
