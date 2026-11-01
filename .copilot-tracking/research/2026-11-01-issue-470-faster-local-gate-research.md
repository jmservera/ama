# Research: issue 470 faster local gate (2026-11-01)

Research disposition: executed. Planning Readiness: Ready.

## Question

Which acceptance criteria of #470 remain unmet on `origin/main` (6785d065)?

## Evidence

* `tools/rpi-checks.py` already implements `--changed` (`changed_groups`, `selection`), `--jobs` (`worker_limit`, `ThreadPoolExecutor` scheduler, single heavy lock), `--resume`, receipt `scope` full/partial and `verify(required_scope=...)` rejecting partial receipts by default.
* `tools/test_rpi_checks.py` covers selection mapping, closure, scope rejection and resume (`test_changed_selection_mapping_and_closure`, `test_partial_scope_is_rejected_by_default_before_live_probes`, resume tests).
* `src/README.md` "Measuring full-gate scheduling" documents the serial (`--jobs 1`) versus parallel (`--jobs 3`) benchmark procedure.
* Issue comments (owner, closure audit 2026-10-31): only criterion 4, measured full-run time before and after, is unmet; the changed tier measured 60.9 s but no comparable full serial/parallel runs exist.

## Constraint

The owner's instruction for this run is the focused tier with no heavy local gate. A full serial plus parallel benchmark (about 23-26 minutes plus the parallel run) is a heavy gate and is not authorised here.

## Conclusion

No code change is justified. Criteria 1, 2, 3 and 5 are proven by merged code and tests. Criterion 4 cannot be proven in this slice, so the PR must use `Refs`, naming criterion 4.
