# Changes: issue 128 source-completeness paired dimension (Refs #128)

* `src/core/src/zava_forward/core/paired_equity.py`: `source_completeness` dimension and contrast; `_position` returns `None` for an excluded case and `_check_pair` reports `excluded`.
* `src/core/tests/test_paired_equity.py`: source pair (`p4`), `penalise_source`, seeded source defect, seeded exclusion, required and confounded source dimension; counts 3 to 4.
* `src/core/README.md`, `docs/reference/research/ux/equity-journey-test-plan.md`, `docs/reference/log.md`: wording and log entry.

Amendment: the critique High finding (exclusion crash) was added to scope and fixed failing-first. No divergence from the plan otherwise.

Validation (owned venv `~/.venvs/issue-128-1112`, editable `src/core[dev]`, `zava_forward.core.paired_equity.__file__` verified under this worktree; exit codes read directly, no tail or tee):

| Check | Result |
| --- | --- |
| red run after tests, before production edit | exit 1, 6 failures |
| red run for exclusion test before fix | exit 1, StopIteration error |
| `unittest discover -s tests -p test_paired_equity.py -q` | exit 0, 26 tests OK |
| `ruff check src tests` and `ruff format --check` on the two files | exit 0 |
| `mypy` on `paired_equity.py` and its test (strict) | exit 0 |
| `unittest ... test_journey_register.py` | exit 0, 7 tests OK |

Not run: full core suite, repository gate, CI, browser. Tier: focused.
