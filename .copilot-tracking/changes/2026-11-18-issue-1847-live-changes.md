---
title: Issue 1847 live changes
---
# Changes (2026-11-18 live)

Files: `docs/reference/research/nomination-bootstrap-isolation-proof-1847-2026-11-18.md` plus its evidence folder, `docs/reference/README.md` index row, `docs/reference/log.md` entry. No `src/` change.

## Per-criterion status

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Layout contract documented | Proven (README section, matched by probes) |
| 2 | Both orders, fresh process, per layout; explicit rejection | Proven (source, editable, noneditable) |
| 3 | Origins and identities observed | Proven; split cause on original is inference, failure counts measured |
| 4 | Regression fails on original, passes on fix | Proven (1 failure, 20 errors original; 58 OK on main) |
| 5 | No family purge, foreign checks kept | Proven |
| 6 | Full gate and external receipt | Unproven: `rpi-checks.py --all` forbidden by owner brief; no src change |

Process note: research-open witness recorded before searching; implement-start witness follows this file.

Witness disclosure: `implement-start` reported "source was already dirty"; the docs edits (research note, index, log) were written before that call because they are the deliverable of the proof pass. Validation (FOCUSED): from `src/core/tests`, `PYTHONPATH=../src:../../agents/src:. python3 -m unittest test_nomination_bootstrap test_bulk_edits test_nomination_route`: 58 tests OK, sequential. mypy, ruff, web checks, manifest SHA: not applicable (no Python or web file edited). Original adverse output retained in the evidence folder.
Witness disclosure: implement-done was recorded after review-done (missed ordering; witness noted the missing predecessor).
