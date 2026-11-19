# Research: issue 1258 live rerun (2026-11-19)

Research disposition: executed. Planning Readiness: Ready (no source change).

Issue state read with `gh issue view 1258` on 2026-11-19: acceptance criteria 1 to 4 are ticked (closure audits 2026-11-13 and 2026-11-18). Criterion 5 (original RPI, current FULL receipt, independent exact-head review, hosted checks) is the only unticked one.

Evidence at HEAD 910adb0a1: `ranking_publication.py` `_confirmed` fsyncs the archive directory and ancestors and raises `DurabilityUnconfirmedError` when a sync fails. `python3 -m unittest test_ranking_publication -q` from `src/core` with `PYTHONPATH=src:tests` ran 57 tests, OK.

Criterion 5 cannot be proven for the demo. A FULL receipt needs `rpi-checks.py --all`, which is forbidden here and not required because no src code changes. Hosted CI and an independent exact-head review need a pushed head, and pushing is not allowed. Mocks do not prove real crash durability. No Azure resource is relevant to a local filesystem fix, so none was touched.
