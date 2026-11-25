---
title: Issue 107 live r12 changes
ms.date: 2026-11-25
---

Status: implemented and validated locally (FULL tier for test code; `rpi-checks.py --all` not run). The stash/restore of the edit around `implement-start` was done so the changes record existed before the source edit landed in the tree.

## Files

* `src/api/tests/assistant_process_worker.py`: `provider`, `endpoint`, `deployment` variations (`ROUTE`).
* `src/api/tests/test_assistant_release.py`: three separate-process tests.
* `docs/reference/research/issue-107-live-r12-endpoint-deployment-2026-11-25.md`: research note with live evidence.
* `docs/reference/log.md` and the research index entry.
* Evidence: `.copilot-tracking/evidence/107-live/` (probe scripts, redacted JSON).

## Validation

* SQLite: 115 tests OK (32 skipped, SQL Server classes). SQL Server 2022 container: 49 tests OK, 0 skipped; container removed.
* Mutation check fails the endpoint test when the route is not applied. `ruff check`, `ruff format --check`, `python3 -m mypy` clean.
* No hosted CI observed (nothing pushed). No Azure write; no resource created.

## Per-criterion table

| Unticked criterion | Status | Basis | Why not fully proven |
| --- | --- | --- | --- |
| Independent SQL connection/worker and race tests; material mismatches, revocation, restart; no restore or replenishment | Proven for the demo (11 of 13 bound fields in separate processes; racing, restart, non-replenishment on SQLite and SQL Server 2022 container) | tests above | Constructed fixtures, local disposable SQL, no real older image; task contract and evaluation version in-process only |
| Matching approved exercise record permits bounded proposals only; delivered-build acceptance | Partly proven; delivered-build acceptance unproven | Fixture approved path; live deployed build default-off, five assistants denied, delivery gate blocked on OQ-017/018/019 | No named approver (OQ-017) so no approved actual release can legitimately exist; real-AI version-linked evidence needs one |
