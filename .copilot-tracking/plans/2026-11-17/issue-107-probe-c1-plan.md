---
title: Issue 107 old-image SQL probe correction plan
description: One finite correction of the eight execution-readiness findings; diagnostic, focused tests and README only
ms.date: 2026-11-17
---

## Tier and scope

FULL tier retained (security-sensitive release-admission diagnostic with an actual SQL and image planned check). Editable files: `src/api/checks/old_image_sql_probe.py`, `src/api/checks/old_image_worker.py` (partial observations only), `src/api/tests/test_old_image_sql_probe.py`, the `src/api/README.md` section, and this task's tracking files. No application, store, policy, schema, service, UI or HVE change.

## Phases

1. Reproduce: add focused regressions for findings 2 to 8 and watch them fail on the opening candidate (finding 1 as an argv assertion).
2. Judge (findings 2, 3, 4, 6): fixed protocol table and typed validation; adverse checks run on partial observations first; no SPID uniqueness; one four-column pool compared on both ceilings and both consumed columns.
3. Observation capture (finding 4): worker keeps its partial record on error; `scenario` writes into a caller-owned record and catches every error, including host operation exceptions.
4. Docker lifecycle (findings 1, 5): run-labelled internal private network; SQL on bridge (loopback publish) plus private alias; workers private only; names registered before create, reconciliation by exact name and run labels, per-resource report, bounded retries, absence verified, no exit 0 with unresolved cleanup.
5. Deadlines and output bounds (finding 7): `Deadline` with daemon-thread host calls, a total cap, capped-output process runner, readiness connection closed on failure, `os._exit` after reporting if a host call was abandoned.
6. Output path (finding 8): canonical parent, exclusive leaf creation, canonical re-check.
7. README: private-network topology, fixed protocol, limits, guarded fixed-argv continuation.
8. Checks (this runtime only): targeted tests, strict mypy on the affected files, Ruff, format, current-source SQLite self-test.

## Non-goals

Docker, SQL, the old image, the full gate and hosted CI are not run here. The self-test and fakes are lower fidelity and are never old-image evidence.
