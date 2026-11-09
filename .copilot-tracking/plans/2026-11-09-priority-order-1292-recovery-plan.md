<!-- markdownlint-disable-file -->
# Plan: issue 1292 recovery validation (2026-11-09)

Owner-selected demo-targeted tier (no `rpi-checks --all`; hosted CI and independent exact-head review remain mandatory). Details: [details](../details/2026-11-09-priority-order-1292-recovery-details.md).

* [x] Merge fetched origin/main locally (no source overlap).
* [x] Install worktree-local venv; run focused creation-order, resident-decision and adjacent SQL/export tests on SQLite.
* [x] Provision an owned, labelled, loopback disposable SQL Server 2022 and run the actual regression with zero skips; compare two named originally failing tests on base and head.
* [x] Run ruff and mypy.
* [x] Record no source change; commit evidence only.

Constraint: no reimplementation; source corrections only for confirmed tightly coupled defects. None confirmed.
