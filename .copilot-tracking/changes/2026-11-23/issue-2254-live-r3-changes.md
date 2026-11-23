---
title: Issue 2254 live changes, run 3 (2026-11-23)
---

Tier: focused. Basis: one test-only line group in `src/core/tests/test_sqlreads.py`; no `src/` runtime code, workflow, dependency or deployment change. `rpi-checks.py --all` not run, per coordinator rule.

Changes:

* `src/core/tests/test_sqlreads.py`: the 2254 repair test also asserts `map_view` is in points mode and its hazard items equal the tile and list.
* New [research note](../../../docs/reference/research/issue-2254-live-r3-2026-11-23.md) with probes, results and screenshots under `docs/reference/research/issue-2254-live-r3-2026-11-23/`; index row in `docs/reference/README.md`; log entry.
* Divergence: the witness qualified implement-start as "source already dirty" because the test edit ran in the same call batch as the witness; the changes record was persisted first.

Validation: `PYTHONPATH=src:tests python3 -m unittest tests.test_sqlreads` in `src/core` (18 tests OK); `ruff check` clean on the test file; Markdown and link review. Probe scripts assert sign-in values are absent from results.

| Criterion (issue lists no checkboxes; expectation: one definition across tile, map, list) | Status | Evidence |
| --- | --- | --- |
| Overview tile matches the filtered list | Proven (demo, 2026-11-23) | tile 23, All cases "23 cases", API total 23 |
| Map markers match the list | Proven (demo) | 23 of 443 markers titled "Safety issue open"; `/api/map` 23 |
| One source / regression test covers tile, map and list | Proven locally | extended test in `test_sqlreads.py` passes |
| Live stale-row cause observed | Unproven | SQL public access disabled; not changed for the demo |
| Deployed image maps to the source commit | Unproven | digest not mapped |
