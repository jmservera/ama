---
title: Issue 2255 changes record
date: 2026-11-22
---

# Changes

Tier: FULL (live SQL write on the demo database); no `src` change; `rpi-checks.py --all` not run (coordinator runs gates). Not published, not pushed, not deployed.

## Files

* infra/scripts/seed_demo_hazard_clock.py (new): inspect, apply [N] and revert modes; counts-only output.
* infra/tests/test_seed_demo_hazard_clock.py (new): 4 tests, pass; ruff check and format pass.
* docs/reference/research/issue-2255-backfill-2026-11-22.md and its folder (probe, outputs, screenshots); docs/reference/README.md index; docs/reference/log.md entry.

## Divergences from the plan and critique

* Reference time: first run used the wall clock; the queue reads dataset `as_of`, so five re-dated clocks showed unknown. Fixed to `as_of`, added `revert` (critique had deferred it), reverted the 23 and re-applied.
* `response_due_at`: the critique said not to write it; the live probe showed the queue prints a target window only from that field, so the tool now seeds the reference-window due time when absent, marked synthetic and revertible. No `responded_at` or resident update time is written.

## Live actions

Four exec sessions into `ca-cutover-test-demo-api` (inspect, applies, reverts); temp files removed; no Azure resource created.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Safety cases show elapsed time (22 of 22) | Proven |
| Response target window shown (22 of 22) | Proven |
| Some clocks running (6 re-dated, "response open") | Proven |
| Named owner still shown (22) | Proven |
| Hazard service stays timing authority | Partly: seeded due times are synthetic reference values, marked and revertible |
| Repo seeding path, synthetic demo data only, tested | Proven |
| Re-runnable and reversible | Proven |
| Stays valid if the dataset is re-seeded | Not proven; a re-seed drops the fields |
| Independent exact-head review, hosted CI, full local gate | Unproven here |

## Rebase record (2026-11-22, refs #2255)

* Candidate 03f1e95994 (base 15fd62a8e8) rebased onto origin/main 6fd6e3f838. Seven `.copilot-tracking` files and the research note collided with the earlier evidence-only `issue-2255-live-*` artifacts now on main (merged in #2258); those stay unchanged. The candidate artifacts are renamed `issue-2255-backfill-*`, its note and evidence folder `issue-2255-backfill-2026-11-22`, and the index and log entries point at the new names.
* Not rerun: the live SQL write and Playwright proofs (recorded in the candidate on 2026-11-22; table above is carried over unchanged). Rerun here: `cd infra && python3 -m unittest tests.test_seed_demo_hazard_clock -q` (4 tests OK), ruff check and ruff format check on the two Python files (pass). No `src` change; Tier FULL stays as the candidate stated; `rpi-checks.py --all` not run.
