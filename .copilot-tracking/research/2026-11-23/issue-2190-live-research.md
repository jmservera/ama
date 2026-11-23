---
title: "Issue 2190 live research: regression tests for flakes 2 and 3, tighter _region_passed"
description: Gaps in the issue 2190 gate-flake fixes found by the gate-speed review, with baseline evidence and the per-criterion proof status for the synthetic demo.
ms.date: 2026-11-23
---

Scope: review finding `/tmp/gate-review-findings.md` items D6, D7 and D9 against issue #2190 ("each reproduced or explained, fixed with a regression test, no check relaxed"). Synthetic DEMO, desktop only. Disposition: Research `executed`; the earlier note [issue-2190-live-20261121](../../../docs/reference/research/issue-2190-live-20261121-2026-11-21.md) is reused for the reproductions. Planning Readiness: Ready.

## Baseline (HEAD 342fad401d)

* `python3 -m unittest tools.test_rpi_checks`: 129 tests, OK (35.7 s).
* `tests.test_rai_release_readiness_api_218` from `src/api`: 5 tests, OK (13.6 s).
* Azure is not involved: all three flakes are local gate behaviour. No resource read or changed.

## Findings

* D9, `_region_passed` (`tools/rpi-checks.py`): it accepts any region line that ends in `ok` after a non-letter. A thread log such as `http-response status ok` therefore counts as the result of a test whose own result line is missing. The rejecting test has no case for it. Verbose unittest prints the result on its own line (or directly after the header when nothing interleaves), so the real result is a line that is exactly `ok`. Tightening to that shape keeps every accepted case in the existing tests and rejects the log-line-ends-in-ok shape. A log line shaped like a header (`name (a.b) ... `) still starts a region and cannot be told apart from a real header; the failing-pattern scan and the `Ran N` plus final `OK` checks stay the backstop.
* D7, flake 3: `test_request_budget_survives_a_slow_report_under_load` asserts the constant that was passed to a patched `urlopen`; it never exercises a slow server. A deterministic behavioural test is possible with a local HTTP server that delays its reply: with the module budget the helper returns the reply; with a budget below the delay it raises `TimeoutError`, which is the failure the issue reports.
* D6, flake 2: `networkidle` only waits for 500 ms without requests. The route list read is two sequential fetches (`/api/facets`, then the cases list), and `app.js:1004` writes the long `Perspective:` status when the second ends, so a CPU stall longer than 500 ms between them lets the snapshot run early. A request-level reproduction cannot be made deterministic because requests in flight are already awaited by `networkidle`; the gap is client-side. The deterministic fix is to wait for the destination's own end state (`#workspace-status` starting with `Perspective:` for `#/`) before the snapshot. The ordering is testable with a recording page double.

## Per-criterion status (issue 2190, before this change)

| Criterion | Status | Basis |
| --- | --- | --- |
| Each flake reproduced or explained | Proven | Earlier note with evidence files; unchanged |
| Fixed with a regression test | Flake 1 proven; flake 2 and 3 open | D6 and D7 above |
| No check relaxed | Open for D9 | `_region_passed` accepts log lines ending in `ok` |
