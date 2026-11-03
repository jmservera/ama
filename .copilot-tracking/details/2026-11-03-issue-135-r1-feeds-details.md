# Details: issue 135 round 1, exception queue feeds

Date: 2026-11-03.

* P1: `raise_failure(..., ref=None)` returns the existing item for the same kind and ref; otherwise adds one with `ref` stored.
* P2: `feed_failed_ai_runs(queue, records, owner)` selects `kind == ai_task` records that are `Quarantined` or have `mode == ai`, `source != ai` and a reason. `feed_stranded_tasks(queue, overdue, owner)` selects overdue tasks whose owner is missing or `Unknown`. The named owner must hold `digital_operator`.
* P3: five tests: selection, no text leak and unreplayed, idempotence, owner role check, stranded filter.
* P4: README paragraph and updated not-delivered list.
* P5: `PYTHONPATH=src python3 -m unittest tests.test_exception_feeds tests.test_exception_queue`, ruff check and format, mypy with `--follow-imports=skip`.
