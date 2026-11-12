# Details: issue 128 source-completeness paired dimension

* `src/core/src/zava_forward/core/paired_equity.py`: prepend `source_completeness` to `DIMENSIONS`; add `CONTRASTS["source_completeness"] = {"source_record": ("complete", "missing")}`; update module docstring.
* `src/core/tests/test_paired_equity.py`: add source pair `r1` with its own case id `p4` (a shared base object would be mutated by other tests); counts become tested=4; add `penalise_source` ranker, seeded-defect, required-dimension and confounded-source tests.
* `src/core/README.md`, `docs/reference/research/ux/equity-journey-test-plan.md`: name source completeness.
* `docs/reference/log.md`: append entry.

Validation (venv `~/.venvs/issue-128-1112`, editable `src/core[dev]`, imported path verified under this worktree): `python -m unittest discover -s tests -p test_paired_equity.py -q`, `ruff check`, `ruff format --check`, `mypy` on the two files, `test_journey_register.py`.
