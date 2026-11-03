# Plan: issue 135 round 1, exception queue feeds

Date: 2026-11-03. Research: ../research/2026-11-03-issue-135-r1-feeds-research.md. Details: ../details/2026-11-03-issue-135-r1-feeds-details.md

## Phases

* [x] P1 Add optional idempotent `ref` to `ExceptionQueue.raise_failure`.
* [x] P2 Add `exception_feeds.py` with `feed_failed_ai_runs` and `feed_stranded_tasks`.
* [x] P3 Add `test_exception_feeds.py`.
* [x] P4 README update in `src/core/README.md`.
* [x] P5 Run focused tests, ruff and mypy.

## Critique (single pass, verdict proceed)

* Risk: feeding could leak personal text into the queue. Disposition: items keep ids, task name and stated reason only; test asserts the output text is absent.
* Risk: a deliberate workflow-only choice is flagged as a failure. Disposition: only `mode == ai` with a non-AI source, or quarantine, is raised; test covers it.
* Risk: re-reading duplicates items. Disposition: `ref` dedupes per kind.
* No user decision needed.
