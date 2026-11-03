# Changes: issue 135 round 1, exception queue feeds

Date: 2026-11-03.

* `src/core/src/zava_forward/core/exception_queue.py`: `raise_failure` gains optional `ref` for idempotent re-reads.
* `src/core/src/zava_forward/core/exception_feeds.py`: new read-only feeds for failed AI runs and ownerless overdue tasks.
* `src/core/tests/test_exception_feeds.py`: five new tests.
* `src/core/README.md`: feeds paragraph; not-delivered list updated.

Validation run: 19 unit tests (exception queue and feeds) pass; ruff check and format pass; mypy (cache /tmp/mypy-135, `--follow-imports=skip`) passes on touched files.
Not run: gate, benchmarks, full suites, project-wide mypy, dependency-rule test. Tier: focused; no security, infrastructure, SQL or deployment change.
Divergences: none.
