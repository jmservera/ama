# Issue 2195 r5 changes record

Date: 2026-11-21. Status: implemented. Tier: FULL (src/core change). `rpi-checks.py --all` not run by this worker.

## Files changed

* `src/core/src/zava_forward/core/mssqlstore.py`: statements serialised per connection.
* `src/core/tests/test_priority_order.py`: `SharedConnectionThreads` regression test.
* Research note, probes and evidence in `docs/reference/research/issue-2195-chat-routing-live-r5-2026-11-21*`; docs index and log; r5 RPI records.

## Validation

* Core 261 tests OK (87 skipped, no SQL); new test fails without the fix. API 59 OK. ruff clean; mypy 3 pre-existing errors.
* Pinned axe employee chat check PASS, 0 violations. Live Playwright probes on revision 0000043.
* Not run: `rpi-checks.py --all`, SQL-backed suites, deployment, person-run assistive-technology testing (out of scope).

## Divergences

The fix was applied from commit 193c9aaa90 after the implement-start witness, which qualified the dirty tree (untracked evidence folder). r4 critique C-1 is reversed because the 500s recurred.

## Per-criterion table

| # | Criterion | Verdict for the demo | Evidence |
| --- | --- | --- | --- |
| 1 | Routing shown with agent name and plain reason | Proven live | r5 note |
| 2 | Unroutable questions stay general and say so | Proven live | r5 note |
| 3 | Approval and consent boundaries unchanged | Proven live for refusal; no approval code changed | r5 note |
| 4 | AI-unavailable path works | Proven live | r5 note |
| 5 | Tests | Proven locally | Validation |
| 6 | Accessibility and content-standard tests | Proven (automated tests, pinned axe); AT testing out of scope | r5 note |
| - | Live chat 500s | Unproven live: fix covered by unit test, not deployed; cause is a hypothesis | r5 note |
