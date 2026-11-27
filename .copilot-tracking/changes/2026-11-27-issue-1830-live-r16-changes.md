---
title: Issue 1830 live r16 changes (2026-11-27)
ms.date: 2026-11-27
---

Tier: classified FULL by doubt (gate tool `tools/rpi-checks.py` edited; semantics of receipts unchanged). `rpi-checks.py --all` not run; the coordinator runs gates.

Planned changes: `tools/rpi-checks.py` rejects gate-only options with `--preflight`; focused test in `tools/test_rpi_checks.py`; one README sentence; research note and log entry.

Final changes: `tools/rpi-checks.py` (gate-only options refused under `--preflight`), `tools/test_rpi_checks.py` (one test, 5 subtests), `src/README.md` (one sentence), research note [issue-1830-live-r16-2026-11-27.md](../../docs/reference/research/issue-1830-live-r16-2026-11-27.md), README row, log entry. Evidence: reproduction before (exit 0 with bogus `--extra-test`), after (exit 1 BLOCKED), 135 tool tests OK.

Not run: `rpi-checks.py --all`, hosted CI, independent exact-head review. No live Azure, no push or PR. Dependency: the issue says edits to `rpi-checks.py` and `src/README.md` wait for #1297's correction to merge; not verified here, flagged for the owner.

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Wall, queue wait, timing, critical path, high-cost and redundant checks | Partly proven | Receipts analysed in r6 and r9, not redone. Unproven: retained queue-wait logs, same-head receipt pair, redundant-coverage candidates; the cited `/tmp` receipt is gone |
| 2 | Preflight, rejections, non-receipt label, #1297 caught, #1828 rerun | Proven for the demo | Zero-test, invalid path, invalid selector, bad class all BLOCKED; new: ignored gate options now BLOCKED (defect fixed here). #1297 320px replay is from r7; #1828 direct check from r15 |
| 3 | Tests, docs, benchmark method, before and after | Partly proven | Test and README sentence added for the new behaviour; no gate optimization implemented, so no gate before and after |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Owner-gated | Artifacts and tier classification done; independent review and hosted CI need a PR, forbidden here |
