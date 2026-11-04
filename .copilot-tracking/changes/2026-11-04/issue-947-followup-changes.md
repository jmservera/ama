<!-- markdownlint-disable-file -->
# Changes: issue 947

* `src/core/src/zava_forward/core/ledger.py`, `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`: fix.
* `src/core/tests/test_recovery.py`, `src/orchestrator/tests/test_digest_blob.py`: regression tests (confirmed failing before the fix with TypeError and list mismatches).
* `docs/reference/log.md`: entry.

## Validation

* Run: `test_recovery` (15 OK), `test_digest_blob` (27 OK), ruff check on both projects, mypy on touched files.
* Not run: gate, benchmarks, full suites, CI. Tests used `PYTHONPATH` to this worktree because installed editable packages pointed at another worktree. No `pyproject.toml` edited.
