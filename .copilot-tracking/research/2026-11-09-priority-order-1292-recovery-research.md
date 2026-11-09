<!-- markdownlint-disable-file -->
# Research: issue 1292 recovery validation (2026-11-09)

* Seed: unpublished C4 candidate `d32b7982a` (branch fix/priority-reload-1292). Original C1-C4 research, plans, changes and reviews, including the independent C2 and C4 "Revise" outcomes, are preserved unchanged.
* Current main fetched: `b46a9ad9a9619db535368d1b2cbbddec8110e122`. Main drifted by two commits since the original base `6354b13f7`; none touches `src/core` or `src/api` (docs, tools/rpi-checks only). Local merge was clean.
* Issue #1292 hydrated 2026-11-09: no open PR; owner comments authorise corrections, record the C4 "Revise" and hold further correction pending an owner decision. Native dependencies: none; #81 waits on this fix.
* Integration edges: #81 (SQL acceptance blocked on this), #1288 (consumes core persistence; may overlap `sqlstore.py` and `store.py`; unmerged sibling not merged here), #184 (SQL sensor lane).
* Finding: no new confirmed defect in the surviving source was reproduced by this recovery. The earlier "unproven on real SQL Server" gaps now have actual evidence (see review). Original C4 residual risks (flagged legacy rows, cutover writer fence, data-owner resolution, ledger migration, SQL scale) remain open and human decisions.
* Pre-existing, unrelated defect found: `MssqlResidentControls.test_challenge_edited_in_case_outside_generation_candidates` fails identically on current main and this head (the test rewrites its JSON seed after the SQL database is already seeded, so 4 cases load instead of 44). It does not involve recommendation ordering.
* Planning readiness: Ready (validation only).
